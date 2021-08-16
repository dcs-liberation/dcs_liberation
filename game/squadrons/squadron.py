from __future__ import annotations

import logging
from collections import Iterable
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Optional,
    Sequence,
)

from faker import Faker

from game.dcs.aircrafttype import AircraftType
from game.settings import AutoAtoBehavior, Settings
from game.squadrons.operatingbases import OperatingBases
from game.squadrons.pilot import Pilot, PilotStatus
from game.squadrons.squadrondef import SquadronDef

if TYPE_CHECKING:
    from game import Game
    from game.coalition import Coalition
    from gen.flights.flight import FlightType
    from game.theater import ControlPoint


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
    settings: Settings = field(hash=False, compare=False)

    location: ControlPoint

    def __post_init__(self) -> None:
        self.auto_assignable_mission_types = set(self.mission_types)

    def __str__(self) -> str:
        if self.nickname is None:
            return self.name
        return f'{self.name} "{self.nickname}"'

    @property
    def player(self) -> bool:
        return self.coalition.player

    def assign_to_base(self, base: ControlPoint) -> None:
        self.location.squadrons.remove(self)
        self.location = base
        self.location.squadrons.append(self)
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
        new_pilots.extend([Pilot(self.faker.name()) for _ in range(count)])
        self.current_roster.extend(new_pilots)
        self.available_pilots.extend(new_pilots)

    def populate_for_turn_0(self) -> None:
        if any(p.status is not PilotStatus.Active for p in self.pilot_pool):
            raise ValueError("Squadrons can only be created with active pilots.")
        self._recruit_pilots(self.settings.squadron_pilot_limit)

    def replenish_lost_pilots(self) -> None:
        if not self.pilot_limits_enabled:
            return

        replenish_count = min(
            self.settings.squadron_replenishment_rate,
            self._number_of_unfilled_pilot_slots,
        )
        if replenish_count > 0:
            self._recruit_pilots(replenish_count)

    def return_all_pilots(self) -> None:
        self.available_pilots = list(self.active_pilots)

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

    def operates_from(self, control_point: ControlPoint) -> bool:
        if control_point.is_carrier:
            return self.operating_bases.carrier
        elif control_point.is_lha:
            return self.operating_bases.lha
        else:
            return self.operating_bases.shore

    def pilot_at_index(self, index: int) -> Pilot:
        return self.current_roster[index]

    @classmethod
    def create_from(
        cls,
        squadron_def: SquadronDef,
        base: ControlPoint,
        coalition: Coalition,
        game: Game,
    ) -> Squadron:
        return Squadron(
            squadron_def.name,
            squadron_def.nickname,
            squadron_def.country,
            squadron_def.role,
            squadron_def.aircraft,
            squadron_def.livery,
            squadron_def.mission_types,
            squadron_def.operating_bases,
            squadron_def.pilot_pool,
            coalition,
            game.settings,
            base,
        )
