from __future__ import annotations

import logging
import random
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Optional, Sequence, TYPE_CHECKING

from faker import Faker

from game.ato import Flight, FlightType, Package
from game.settings import AutoAtoBehavior, Settings
from .pilot import Pilot, PilotStatus
from ..db.database import Database
from ..utils import meters

if TYPE_CHECKING:
    from game import Game
    from game.coalition import Coalition
    from game.dcs.aircrafttype import AircraftType
    from game.theater import ControlPoint, MissionTarget
    from .operatingbases import OperatingBases
    from .squadrondef import SquadronDef


@dataclass
class Squadron:
    name: str
    nickname: Optional[str]
    country: str
    role: str
    aircraft: AircraftType
    livery: Optional[str]
    mission_types: tuple[FlightType, ...]
    operating_bases: OperatingBases
    female_pilot_percentage: int

    #: The pool of pilots that have not yet been assigned to the squadron. This only
    #: happens when a preset squadron defines more preset pilots than the squadron limit
    #: allows. This pool will be consumed before random pilots are generated.
    pilot_pool: list[Pilot]

    current_roster: list[Pilot] = field(default_factory=list, init=False, hash=False)
    available_pilots: list[Pilot] = field(
        default_factory=list, init=False, hash=False, compare=False
    )

    auto_assignable_mission_types: set[FlightType] = field(
        init=False, hash=False, compare=False
    )

    coalition: Coalition = field(hash=False, compare=False)
    flight_db: Database[Flight] = field(hash=False, compare=False)
    settings: Settings = field(hash=False, compare=False)

    location: ControlPoint
    destination: Optional[ControlPoint] = field(
        init=False, hash=False, compare=False, default=None
    )

    owned_aircraft: int = field(init=False, hash=False, compare=False, default=0)
    untasked_aircraft: int = field(init=False, hash=False, compare=False, default=0)
    pending_deliveries: int = field(init=False, hash=False, compare=False, default=0)

    def __post_init__(self) -> None:
        self.auto_assignable_mission_types = set(self.mission_types)

    def __str__(self) -> str:
        if self.nickname is None:
            return self.name
        return f'{self.name} "{self.nickname}"'

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.nickname,
                self.country,
                self.role,
                self.aircraft,
            )
        )

    @property
    def player(self) -> bool:
        return self.coalition.player

    def assign_to_base(self, base: ControlPoint) -> None:
        self.location = base
        logging.debug(f"Assigned {self} to {base}")

    @property
    def pilot_limits_enabled(self) -> bool:
        return self.settings.enable_squadron_pilot_limits

    def set_allowed_mission_types(self, mission_types: Iterable[FlightType]) -> None:
        self.mission_types = tuple(mission_types)
        self.auto_assignable_mission_types.intersection_update(self.mission_types)

    def set_auto_assignable_mission_types(
        self, mission_types: Iterable[FlightType]
    ) -> None:
        self.auto_assignable_mission_types = set(self.mission_types).intersection(
            mission_types
        )

    def claim_new_pilot_if_allowed(self) -> Optional[Pilot]:
        if self.pilot_limits_enabled:
            return None
        self._recruit_pilots(1)
        return self.available_pilots.pop()

    def claim_available_pilot(self) -> Optional[Pilot]:
        if not self.available_pilots:
            return self.claim_new_pilot_if_allowed()

        # For opfor, so player/AI option is irrelevant.
        if not self.player:
            return self.available_pilots.pop()

        preference = self.settings.auto_ato_behavior

        # No preference, so the first pilot is fine.
        if preference is AutoAtoBehavior.Default:
            return self.available_pilots.pop()

        prefer_players = preference is AutoAtoBehavior.Prefer
        for pilot in self.available_pilots:
            if pilot.player == prefer_players:
                self.available_pilots.remove(pilot)
                return pilot

        # No pilot was found that matched the user's preference.
        #
        # If they chose to *never* assign players and only players remain in the pool,
        # we cannot fill the slot with the available pilots.
        #
        # If they only *prefer* players and we're out of players, just return an AI
        # pilot.
        if not prefer_players:
            return self.claim_new_pilot_if_allowed()
        return self.available_pilots.pop()

    def claim_pilot(self, pilot: Pilot) -> None:
        if pilot not in self.available_pilots:
            raise ValueError(
                f"Cannot assign {pilot} to {self} because they are not available"
            )
        self.available_pilots.remove(pilot)

    def return_pilot(self, pilot: Pilot) -> None:
        self.available_pilots.append(pilot)

    def return_pilots(self, pilots: Sequence[Pilot]) -> None:
        # Return in reverse so that returning two pilots and then getting two more
        # results in the same ordering. This happens commonly when resetting rosters in
        # the UI, when we clear the roster because the UI is updating, then end up
        # repopulating the same size flight from the same squadron.
        self.available_pilots.extend(reversed(pilots))

    def _recruit_pilots(self, count: int) -> None:
        new_pilots = self.pilot_pool[:count]
        self.pilot_pool = self.pilot_pool[count:]
        count -= len(new_pilots)
        for _ in range(count):
            if random.randint(1, 100) > self.female_pilot_percentage:
                new_pilots.append(Pilot(self.faker.name_male()))
            else:
                new_pilots.append(Pilot(self.faker.name_female()))
        self.current_roster.extend(new_pilots)
        self.available_pilots.extend(new_pilots)

    def populate_for_turn_0(self) -> None:
        if any(p.status is not PilotStatus.Active for p in self.pilot_pool):
            raise ValueError("Squadrons can only be created with active pilots.")
        self._recruit_pilots(self.settings.squadron_pilot_limit)

    def end_turn(self) -> None:
        if self.destination is not None:
            self.relocate_to(self.destination)
        self.replenish_lost_pilots()
        self.deliver_orders()

    def replenish_lost_pilots(self) -> None:
        if self.pilot_limits_enabled and self.replenish_count > 0:
            self._recruit_pilots(self.replenish_count)

    def return_all_pilots_and_aircraft(self) -> None:
        self.available_pilots = list(self.active_pilots)
        self.untasked_aircraft = self.owned_aircraft

    @staticmethod
    def send_on_leave(pilot: Pilot) -> None:
        pilot.send_on_leave()

    def return_from_leave(self, pilot: Pilot) -> None:
        if not self.has_unfilled_pilot_slots:
            raise RuntimeError(
                f"Cannot return {pilot} from leave because {self} is full"
            )
        pilot.return_from_leave()

    @property
    def faker(self) -> Faker:
        return self.coalition.faker

    def _pilots_with_status(self, status: PilotStatus) -> list[Pilot]:
        return [p for p in self.current_roster if p.status == status]

    def _pilots_without_status(self, status: PilotStatus) -> list[Pilot]:
        return [p for p in self.current_roster if p.status != status]

    @property
    def max_size(self) -> int:
        return self.settings.squadron_pilot_limit

    @property
    def expected_pilots_next_turn(self) -> int:
        return len(self.active_pilots) + self.replenish_count

    @property
    def replenish_count(self) -> int:
        return min(
            self.settings.squadron_replenishment_rate,
            self._number_of_unfilled_pilot_slots,
        )

    @property
    def active_pilots(self) -> list[Pilot]:
        return self._pilots_with_status(PilotStatus.Active)

    @property
    def pilots_on_leave(self) -> list[Pilot]:
        return self._pilots_with_status(PilotStatus.OnLeave)

    @property
    def number_of_pilots_including_inactive(self) -> int:
        return len(self.current_roster)

    @property
    def _number_of_unfilled_pilot_slots(self) -> int:
        return self.max_size - len(self.active_pilots)

    @property
    def number_of_available_pilots(self) -> int:
        return len(self.available_pilots)

    def can_provide_pilots(self, count: int) -> bool:
        return not self.pilot_limits_enabled or self.number_of_available_pilots >= count

    @property
    def has_available_pilots(self) -> bool:
        return not self.pilot_limits_enabled or bool(self.available_pilots)

    @property
    def has_unfilled_pilot_slots(self) -> bool:
        return not self.pilot_limits_enabled or self._number_of_unfilled_pilot_slots > 0

    def can_auto_assign(self, task: FlightType) -> bool:
        return task in self.auto_assignable_mission_types

    def can_auto_assign_mission(
        self, location: MissionTarget, task: FlightType, size: int, this_turn: bool
    ) -> bool:
        if not self.can_auto_assign(task):
            return False
        if this_turn and not self.can_fulfill_flight(size):
            return False

        distance_to_target = meters(location.distance_to(self.location))
        return distance_to_target <= self.aircraft.max_mission_range

    def operates_from(self, control_point: ControlPoint) -> bool:
        if not control_point.can_operate(self.aircraft):
            return False
        if control_point.is_carrier:
            return self.operating_bases.carrier
        elif control_point.is_lha:
            return self.operating_bases.lha
        else:
            return self.operating_bases.shore

    def pilot_at_index(self, index: int) -> Pilot:
        return self.current_roster[index]

    def claim_inventory(self, count: int) -> None:
        if self.untasked_aircraft < count:
            raise ValueError(
                f"Cannot remove {count} from {self.name}. Only have "
                f"{self.untasked_aircraft}."
            )
        self.untasked_aircraft -= count

    def can_fulfill_flight(self, count: int) -> bool:
        return self.can_provide_pilots(count) and self.untasked_aircraft >= count

    def refund_orders(self, count: Optional[int] = None) -> None:
        if count is None:
            count = self.pending_deliveries
        self.coalition.adjust_budget(self.aircraft.price * count)
        self.pending_deliveries -= count

    def deliver_orders(self) -> None:
        self.cancel_overflow_orders()
        self.owned_aircraft += self.pending_deliveries
        self.pending_deliveries = 0

    def relocate_to(self, destination: ControlPoint) -> None:
        self.location = destination
        if self.location == self.destination:
            self.destination = None

    def cancel_overflow_orders(self) -> None:
        if self.pending_deliveries <= 0:
            return
        overflow = -self.location.unclaimed_parking()
        if overflow > 0:
            sell_count = min(overflow, self.pending_deliveries)
            logging.debug(
                f"{self.location} is overfull by {overflow} aircraft. Cancelling "
                f"orders for {sell_count} aircraft to make room."
            )
            self.refund_orders(sell_count)

    @property
    def max_fulfillable_aircraft(self) -> int:
        return max(self.number_of_available_pilots, self.untasked_aircraft)

    @property
    def expected_size_next_turn(self) -> int:
        return self.owned_aircraft + self.pending_deliveries

    @property
    def arrival(self) -> ControlPoint:
        return self.location if self.destination is None else self.destination

    def plan_relocation(self, destination: ControlPoint) -> None:
        if destination == self.location:
            logging.warning(
                f"Attempted to plan relocation of {self} to current location "
                f"{destination}. Ignoring."
            )
            return
        if destination == self.destination:
            logging.warning(
                f"Attempted to plan relocation of {self} to current destination "
                f"{destination}. Ignoring."
            )
            return

        if self.expected_size_next_turn > destination.unclaimed_parking():
            raise RuntimeError(f"Not enough parking for {self} at {destination}.")
        if not destination.can_operate(self.aircraft):
            raise RuntimeError(f"{self} cannot operate at {destination}.")
        self.destination = destination
        self.replan_ferry_flights()

    def cancel_relocation(self) -> None:
        if self.destination is None:
            logging.warning(
                f"Attempted to cancel relocation of squadron with no transfer order. "
                "Ignoring."
            )
            return

        if self.expected_size_next_turn >= self.location.unclaimed_parking():
            raise RuntimeError(f"Not enough parking for {self} at {self.location}.")
        self.destination = None
        self.cancel_ferry_flights()

    def replan_ferry_flights(self) -> None:
        self.cancel_ferry_flights()
        self.plan_ferry_flights()

    def cancel_ferry_flights(self) -> None:
        for package in self.coalition.ato.packages:
            # Copy the list so our iterator remains consistent throughout the removal.
            for flight in list(package.flights):
                if flight.squadron == self and flight.flight_type is FlightType.FERRY:
                    package.remove_flight(flight)
            if not package.flights:
                self.coalition.ato.remove_package(package)

    def plan_ferry_flights(self) -> None:
        if self.destination is None:
            raise RuntimeError(
                f"Cannot plan ferry flights for {self} because there is no destination."
            )
        remaining = self.untasked_aircraft
        if not remaining:
            return

        package = Package(self.destination, self.flight_db)
        while remaining:
            size = min(remaining, self.aircraft.max_group_size)
            self.plan_ferry_flight(package, size)
            remaining -= size
        package.set_tot_asap()
        self.coalition.ato.add_package(package)

    def plan_ferry_flight(self, package: Package, size: int) -> None:
        start_type = self.location.required_aircraft_start_type
        if start_type is None:
            start_type = self.settings.default_start_type

        flight = Flight(
            package,
            self.coalition.country_name,
            self,
            size,
            FlightType.FERRY,
            start_type,
            divert=None,
        )
        package.add_flight(flight)
        flight.recreate_flight_plan()

    @classmethod
    def create_from(
        cls,
        squadron_def: SquadronDef,
        base: ControlPoint,
        coalition: Coalition,
        game: Game,
    ) -> Squadron:
        squadron_def.claimed = True
        return Squadron(
            squadron_def.name,
            squadron_def.nickname,
            squadron_def.country,
            squadron_def.role,
            squadron_def.aircraft,
            squadron_def.livery,
            squadron_def.mission_types,
            squadron_def.operating_bases,
            squadron_def.female_pilot_percentage,
            squadron_def.pilot_pool,
            coalition,
            game.db.flights,
            game.settings,
            base,
        )
