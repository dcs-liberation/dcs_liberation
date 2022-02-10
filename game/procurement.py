from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterator, List, Optional, TYPE_CHECKING, Tuple

from game.config import RUNWAY_REPAIR_COST
from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.theater import ControlPoint, MissionTarget

if TYPE_CHECKING:
    from game import Game
    from game.ato import FlightType
    from game.factions.faction import Faction
    from game.squadrons import Squadron

FRONTLINE_RESERVES_FACTOR = 1.3


@dataclass(frozen=True)
class AircraftProcurementRequest:
    near: MissionTarget
    task_capability: FlightType
    number: int

    def __str__(self) -> str:
        task = self.task_capability.value
        target = self.near.name
        return f"{self.number} ship {task} near {target}"


class ProcurementAi:
    def __init__(
        self,
        game: Game,
        for_player: bool,
        faction: Faction,
        manage_runways: bool,
        manage_front_line: bool,
        manage_aircraft: bool,
    ) -> None:

        self.game = game
        self.is_player = for_player
        self.air_wing = game.air_wing_for(for_player)
        self.faction = faction
        self.manage_runways = manage_runways
        self.manage_front_line = manage_front_line
        self.manage_aircraft = manage_aircraft
        self.threat_zones = self.game.threat_zone_for(not self.is_player)

    def calculate_ground_unit_budget_share(self) -> float:
        armor_investment = 0
        aircraft_investment = 0

        # faction has no ground units
        if (
            len(self.faction.artillery_units) == 0
            and len(self.faction.frontline_units) == 0
        ):
            return 0

        # faction has no planes
        if len(self.faction.aircrafts) == 0:
            return 1

        for cp in self.owned_points:
            cp_ground_units = cp.allocated_ground_units(
                self.game.coalition_for(self.is_player).transfers
            )
            armor_investment += cp_ground_units.total_value
            cp_aircraft = cp.allocated_aircraft()
            aircraft_investment += cp_aircraft.total_value

        total_investment = aircraft_investment + armor_investment
        if total_investment == 0:
            # Turn 0 or all units were destroyed. Either way, split 30/70.
            return 0.3

        # the more planes we have, the more ground units we want and vice versa
        ground_unit_share = aircraft_investment / total_investment
        if ground_unit_share > 1.0:
            raise ValueError

        return ground_unit_share

    def spend_budget(self, budget: float) -> float:
        if self.manage_runways:
            budget = self.repair_runways(budget)
        if self.manage_front_line:
            armor_budget = budget * self.calculate_ground_unit_budget_share()
            budget -= armor_budget
            budget += self.reinforce_front_line(armor_budget)

        if self.manage_aircraft:
            budget = self.purchase_aircraft(budget)
        return budget

    def repair_runways(self, budget: float) -> float:
        for control_point in self.owned_points:
            if budget < RUNWAY_REPAIR_COST:
                break
            if control_point.runway_can_be_repaired:
                control_point.begin_runway_repair()
                budget -= RUNWAY_REPAIR_COST
                if self.is_player:
                    self.game.message(
                        "OPFOR has begun repairing the runway at " f"{control_point}"
                    )
                else:
                    self.game.message(
                        "We have begun repairing the runway at " f"{control_point}"
                    )
        return budget

    def affordable_ground_unit_of_class(
        self, budget: float, unit_class: UnitClass
    ) -> Optional[GroundUnitType]:
        faction_units = set(self.faction.frontline_units) | set(
            self.faction.artillery_units
        )
        of_class = {u for u in faction_units if u.unit_class is unit_class}

        # faction has no access to needed unit type, take a random unit
        if not of_class:
            of_class = faction_units

        affordable_units = [u for u in of_class if u.price <= budget]
        if not affordable_units:
            return None
        return random.choice(affordable_units)

    def reinforce_front_line(self, budget: float) -> float:
        if not self.faction.frontline_units and not self.faction.artillery_units:
            return budget

        # TODO: Attempt to transfer from reserves.

        while budget > 0:
            cp = self.ground_reinforcement_candidate()
            if cp is None:
                break

            most_needed_type = self.most_needed_unit_class(cp)
            unit = self.affordable_ground_unit_of_class(budget, most_needed_type)
            if unit is None:
                # Can't afford any more units.
                break

            budget -= unit.price
            cp.ground_unit_orders.order({unit: 1})

        return budget

    def most_needed_unit_class(self, cp: ControlPoint) -> UnitClass:
        worst_balanced: Optional[UnitClass] = None
        worst_fulfillment = math.inf
        for unit_class in UnitClass:
            if not self.faction.has_access_to_unit_class(unit_class):
                continue

            current_ratio = self.cost_ratio_of_ground_unit(cp, unit_class)
            desired_ratio = (
                self.faction.doctrine.ground_unit_procurement_ratios.for_unit_class(
                    unit_class
                )
            )
            if not desired_ratio:
                continue
            if current_ratio >= desired_ratio:
                continue
            fulfillment = current_ratio / desired_ratio
            if fulfillment < worst_fulfillment:
                worst_fulfillment = fulfillment
                worst_balanced = unit_class
        if worst_balanced is None:
            return UnitClass.TANK
        return worst_balanced

    @staticmethod
    def fulfill_aircraft_request(
        squadrons: list[Squadron], quantity: int, budget: float
    ) -> Tuple[float, bool]:
        for squadron in squadrons:
            price = squadron.aircraft.price * quantity
            # Final check to make sure the number of aircraft won't exceed the number of available pilots
            # after fulfilling this aircraft request.
            if (
                squadron.pilot_limits_enabled
                and squadron.expected_size_next_turn + quantity
                > squadron.expected_pilots_next_turn
            ):
                continue
            if price > budget:
                continue

            squadron.pending_deliveries += quantity
            budget -= price
            return budget, True
        return budget, False

    def purchase_aircraft(self, budget: float) -> float:
        for request in self.game.coalition_for(self.is_player).procurement_requests:
            squadrons = list(self.best_squadrons_for(request))
            if not squadrons:
                # No airbases in range of this request. Skip it.
                continue
            budget, fulfilled = self.fulfill_aircraft_request(
                squadrons, request.number, budget
            )
            if not fulfilled:
                # The request was not fulfilled because we could not afford any suitable
                # aircraft. Rather than continuing, which could proceed to buy tons of
                # cheap escorts that will never allow us to plan a strike package, stop
                # buying so we can save the budget until a turn where we *can* afford to
                # fill the package.
                break
        return budget

    @property
    def owned_points(self) -> List[ControlPoint]:
        if self.is_player:
            return self.game.theater.player_points()
        else:
            return self.game.theater.enemy_points()

    def best_squadrons_for(
        self, request: AircraftProcurementRequest
    ) -> Iterator[Squadron]:
        threatened = []
        for squadron in self.air_wing.best_squadrons_for(
            request.near, request.task_capability, request.number, this_turn=False
        ):
            if not squadron.can_provide_pilots(request.number):
                continue
            if squadron.location.unclaimed_parking() < request.number:
                continue
            if self.threat_zones.threatened(squadron.location.position):
                threatened.append(squadron)
                continue
            yield squadron
        yield from threatened

    def ground_reinforcement_candidate(self) -> Optional[ControlPoint]:
        worst_supply = math.inf
        understaffed: Optional[ControlPoint] = None

        # Prefer to buy front line units at active front lines that are not
        # already overloaded.
        for cp in self.owned_points:
            if not cp.has_active_frontline:
                continue

            if not cp.has_ground_unit_source(self.game):
                # No source of ground units, so can't buy anything.
                continue

            purchase_target = cp.frontline_unit_count_limit * FRONTLINE_RESERVES_FACTOR
            allocated = cp.allocated_ground_units(
                self.game.coalition_for(self.is_player).transfers
            )
            if allocated.total >= purchase_target:
                # Control point is already sufficiently defended.
                continue
            if allocated.total < worst_supply:
                worst_supply = allocated.total
                understaffed = cp

        if understaffed is not None:
            return understaffed

        # Otherwise buy reserves, but don't exceed the amount defined in the settings.
        # These units do not exist in the world until the CP becomes
        # connected to an active front line, at which point all these units
        # will suddenly appear at the gates of the newly captured CP.
        #
        # To avoid sudden overwhelming numbers of units we avoid buying
        # many.
        #
        # Also, do not bother buying units at bases that will never connect
        # to a front line.
        for cp in self.owned_points:
            if cp.is_global:
                continue
            if not cp.can_recruit_ground_units(self.game):
                continue

            allocated = cp.allocated_ground_units(
                self.game.coalition_for(self.is_player).transfers
            )
            if allocated.total >= self.game.settings.reserves_procurement_target:
                continue

            if allocated.total < worst_supply:
                worst_supply = allocated.total
                understaffed = cp

        return understaffed

    def cost_ratio_of_ground_unit(
        self, control_point: ControlPoint, unit_class: UnitClass
    ) -> float:
        allocations = control_point.allocated_ground_units(
            self.game.coalition_for(self.is_player).transfers
        )
        class_cost = 0
        total_cost = 0
        for unit_type, count in allocations.all.items():
            cost = unit_type.price * count
            total_cost += cost
            if unit_type.unit_class is unit_class:
                class_cost += cost
        if not total_cost:
            return 0
        return class_cost / total_cost
