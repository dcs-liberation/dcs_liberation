from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterator, List, Optional, TYPE_CHECKING, Tuple, Type

from dcs.unittype import FlyingType, VehicleType

from game import db
from game.factions.faction import Faction
from game.theater import ControlPoint, MissionTarget
from game.utils import Distance
from gen.flights.ai_flight_planner_db import aircraft_for_task
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.flights.flight import FlightType
from game.data.groundunitclass import GroundUnitClass


if TYPE_CHECKING:
    from game import Game

FRONTLINE_RESERVES_FACTOR = 1.3


@dataclass(frozen=True)
class AircraftProcurementRequest:
    near: MissionTarget
    range: Distance
    task_capability: FlightType
    number: int

    def __str__(self) -> str:
        task = self.task_capability.value
        distance = self.range.nautical_miles
        target = self.near.name
        return f"{self.number} ship {task} within {distance} nm of {target}"


class ProcurementAi:
    def __init__(
        self,
        game: Game,
        for_player: bool,
        faction: Faction,
        manage_runways: bool,
        manage_front_line: bool,
        manage_aircraft: bool,
        front_line_budget_share: float,
    ) -> None:
        if front_line_budget_share > 1.0:
            raise ValueError

        self.game = game
        self.is_player = for_player
        self.air_wing = game.air_wing_for(for_player)
        self.faction = faction
        self.manage_runways = manage_runways
        self.manage_front_line = manage_front_line
        self.manage_aircraft = manage_aircraft
        self.front_line_budget_share = front_line_budget_share
        self.threat_zones = self.game.threat_zone_for(not self.is_player)

    def spend_budget(self, budget: float) -> float:
        if self.manage_runways:
            budget = self.repair_runways(budget)
        if self.manage_front_line:
            armor_budget = math.ceil(budget * self.front_line_budget_share)
            budget -= armor_budget
            budget += self.reinforce_front_line(armor_budget)

        # Don't sell overstock aircraft until after we've bought runways and
        # front lines. Any budget we free up should be earmarked for aircraft.
        if not self.is_player:
            budget += self.sell_incomplete_squadrons()
        if self.manage_aircraft:
            budget = self.purchase_aircraft(budget)
        return budget

    def sell_incomplete_squadrons(self) -> float:
        # Selling incomplete squadrons gives us more money to spend on the next
        # turn. This serves as a short term fix for
        # https://github.com/dcs-liberation/dcs_liberation/issues/41.
        #
        # Only incomplete squadrons which are unlikely to get used will be sold
        # rather than all unused aircraft because the unused aircraft are what
        # make OCA strikes worthwhile.
        #
        # This option is only used by the AI since players cannot cancel sales
        # (https://github.com/dcs-liberation/dcs_liberation/issues/365).
        total = 0.0
        for cp in self.game.theater.control_points_for(self.is_player):
            inventory = self.game.aircraft_inventory.for_control_point(cp)
            for aircraft, available in inventory.all_aircraft:
                # We only ever plan even groups, so the odd aircraft is unlikely
                # to get used.
                if available % 2 == 0:
                    continue
                inventory.remove_aircraft(aircraft, 1)
                total += db.PRICES[aircraft]
        return total

    def repair_runways(self, budget: float) -> float:
        for control_point in self.owned_points:
            if budget < db.RUNWAY_REPAIR_COST:
                break
            if control_point.runway_can_be_repaired:
                control_point.begin_runway_repair()
                budget -= db.RUNWAY_REPAIR_COST
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
        self, budget: float, unit_class: GroundUnitClass
    ) -> Optional[Type[VehicleType]]:
        faction_units = set(self.faction.frontline_units) | set(
            self.faction.artillery_units
        )
        of_class = set(unit_class.unit_list) & faction_units
        affordable_units = [u for u in of_class if db.PRICES[u] <= budget]
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

            budget -= db.PRICES[unit]
            cp.pending_unit_deliveries.order({unit: 1})

        return budget

    def most_needed_unit_class(self, cp: ControlPoint) -> GroundUnitClass:
        worst_balanced: Optional[GroundUnitClass] = None
        worst_fulfillment = math.inf
        for unit_class in GroundUnitClass:
            if not self.faction.has_access_to_unittype(unit_class):
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
            return GroundUnitClass.Tank
        return worst_balanced

    def _affordable_aircraft_for_task(
        self,
        task: FlightType,
        airbase: ControlPoint,
        number: int,
        max_price: float,
    ) -> Optional[Type[FlyingType]]:
        best_choice: Optional[Type[FlyingType]] = None
        for unit in aircraft_for_task(task):
            if unit not in self.faction.aircrafts:
                continue
            if db.PRICES[unit] * number > max_price:
                continue
            if not airbase.can_operate(unit):
                continue

            for squadron in self.air_wing.squadrons_for(unit):
                if task in squadron.mission_types:
                    break
            else:
                continue

            # Affordable, compatible, and we have a squadron capable of the task. To
            # keep some variety, skip with a 50/50 chance. Might be a good idea to have
            # the chance to skip based on the price compared to the rest of the choices.
            best_choice = unit
            if random.choice([True, False]):
                break
        return best_choice

    def affordable_aircraft_for(
        self, request: AircraftProcurementRequest, airbase: ControlPoint, budget: float
    ) -> Optional[Type[FlyingType]]:
        return self._affordable_aircraft_for_task(
            request.task_capability, airbase, request.number, budget
        )

    def fulfill_aircraft_request(
        self, request: AircraftProcurementRequest, budget: float
    ) -> Tuple[float, bool]:
        for airbase in self.best_airbases_for(request):
            unit = self.affordable_aircraft_for(request, airbase, budget)
            if unit is None:
                # Can't afford any aircraft capable of performing the
                # required mission that can operate from this airbase. We
                # might be able to afford aircraft at other airbases though,
                # in the case where the airbase we attempted to use is only
                # able to operate expensive aircraft.
                continue

            budget -= db.PRICES[unit] * request.number
            airbase.pending_unit_deliveries.order({unit: request.number})
            return budget, True
        return budget, False

    def purchase_aircraft(self, budget: float) -> float:
        for request in self.game.procurement_requests_for(self.is_player):
            if not list(self.best_airbases_for(request)):
                # No airbases in range of this request. Skip it.
                continue
            budget, fulfilled = self.fulfill_aircraft_request(request, budget)
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

    def best_airbases_for(
        self, request: AircraftProcurementRequest
    ) -> Iterator[ControlPoint]:
        distance_cache = ObjectiveDistanceCache.get_closest_airfields(request.near)
        threatened = []
        for cp in distance_cache.airfields_within(request.range):
            if not cp.is_friendly(self.is_player):
                continue
            if not cp.runway_is_operational():
                continue
            if cp.unclaimed_parking(self.game) < request.number:
                continue
            if self.threat_zones.threatened(cp.position):
                threatened.append(cp)
            yield cp
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
            allocated = cp.allocated_ground_units(self.game.transfers)
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

            allocated = cp.allocated_ground_units(self.game.transfers)
            if allocated.total >= self.game.settings.reserves_procurement_target:
                continue

            if allocated.total < worst_supply:
                worst_supply = allocated.total
                understaffed = cp

        return understaffed

    def cost_ratio_of_ground_unit(
        self, control_point: ControlPoint, unit_class: GroundUnitClass
    ) -> float:
        allocations = control_point.allocated_ground_units(self.game.transfers)
        class_cost = 0
        total_cost = 0
        for unit_type, count in allocations.all.items():
            cost = db.PRICES[unit_type] * count
            total_cost += cost
            if unit_type in unit_class:
                class_cost += cost
        if not total_cost:
            return 0
        return class_cost / total_cost
