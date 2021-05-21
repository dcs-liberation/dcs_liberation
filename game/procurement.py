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
from gen.ground_forces.ai_ground_planner_db import TYPE_SHORAD, TYPE_TANKS

from game import dic_filter

if TYPE_CHECKING:
    from game import Game


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
        self.faction = faction
        self.manage_runways = manage_runways
        self.manage_front_line = manage_front_line
        self.manage_aircraft = manage_aircraft
        self.front_line_budget_share = front_line_budget_share
        self.threat_zones = self.game.threat_zone_for(not self.is_player)

    def spend_budget(
        self, budget: float, aircraft_requests: List[AircraftProcurementRequest]
    ) -> float:
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

    def random_affordable_ground_unit(
        self, budget: float, cp: ControlPoint
    ) -> Optional[Type[VehicleType]]:
        affordable_units = [
            u
            for u in self.faction.frontline_units + self.faction.artillery_units
            if db.PRICES[u] <= budget
        ]

        total_number_aa = (
            cp.base.total_shorad_cost + cp.pending_frontline_aa_deliveries_count
        )
        total_non_aa = (
            cp.base.total_armor + cp.pending_deliveries_count - total_number_aa
        )
        max_aa = math.ceil(total_non_aa / 8)

        # Limit the number of AA units the AI will buy
        if not total_number_aa < max_aa:
            for unit in [u for u in affordable_units if u in TYPE_SHORAD]:
                affordable_units.remove(unit)

        if not affordable_units:
            return None
        return random.choice(affordable_units)

    def reinforce_front_line(self, ground_unit_budget: float) -> float:
        if not self.faction.frontline_units and not self.faction.artillery_units:
            return ground_unit_budget

        # TODO: Attempt to transfer from reserves.

        frontline_controlpoints = self.front_line_candidates()
        if not frontline_controlpoints:
            return ground_unit_budget

        budget_for_each_controlpoint = int(
            ground_unit_budget / len(frontline_controlpoints)
        )

        for cp in frontline_controlpoints:
            budget = self.buy_groundUnits_for_controlpoint(
                int (ground_unit_budget), budget_for_each_controlpoint, cp
            )

        return budget

    def buy_groundUnits_for_controlpoint(
        self,
        ground_unit_budget: int,
        budget_for_each_controlpoint: int,
        cp: ControlPoint,
    ):
        cp_budget = budget_for_each_controlpoint
        while cp_budget > 0:
            tanks_in_base = dic_filter.dic_analyser.get_all_vehicletype_from_dic(
                cp.base.armor, TYPE_TANKS
            )
            tanks_orderd = dic_filter.dic_analyser.get_all_vehicletype_from_dic(
                cp.pending_unit_deliveries.units, TYPE_TANKS
            )
            all_tanks_list = tanks_in_base + tanks_orderd
            all_tanks_dic = (
                dic_filter.dic_analyser.get_dic_with_numbers_of_vehicles_from_list(
                    all_tanks_list
                )
            )
            tank_costs = dic_filter.dic_analyser.get_costs_for_provided_vehicles(
                all_tanks_dic
            )

            unit = self.random_affordable_ground_unit(cp_budget, cp)

            if unit is None:
                # Can't afford any more units.
                break

            unit_price = db.PRICES[unit]
            ground_unit_budget -= unit_price
            cp_budget -= unit_price
            cp.pending_unit_deliveries.order({unit: 1})
        return ground_unit_budget

    def _affordable_aircraft_of_types(
        self,
        types: List[Type[FlyingType]],
        airbase: ControlPoint,
        number: int,
        max_price: float,
    ) -> Optional[Type[FlyingType]]:
        best_choice: Optional[Type[FlyingType]] = None
        for unit in [u for u in types if u in self.faction.aircrafts]:
            if db.PRICES[unit] * number > max_price:
                continue
            if not airbase.can_operate(unit):
                continue

            # Affordable and compatible. To keep some variety, skip with a 50/50
            # chance. Might be a good idea to have the chance to skip based on
            # the price compared to the rest of the choices.
            best_choice = unit
            if random.choice([True, False]):
                break
        return best_choice

    def affordable_aircraft_for(
        self, request: AircraftProcurementRequest, airbase: ControlPoint, budget: float
    ) -> Optional[Type[FlyingType]]:
        return self._affordable_aircraft_of_types(
            aircraft_for_task(request.task_capability), airbase, request.number, budget
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

    def front_line_candidates(self) -> List[ControlPoint]:
        candidates = []

        # Prefer to buy front line units at active front lines that are not
        # already overloaded.
        for cp in self.owned_points:
            if not cp.has_ground_unit_source(self.game):
                continue

            if self.total_ground_units_allocated_to(cp) >= 50:
                # Control point is already sufficiently defended.
                continue
            for connected in cp.connected_points:
                if not connected.is_friendly(to_player=self.is_player):
                    candidates.append(cp)

        if not candidates:
            # Otherwise buy reserves, but don't exceed 10 reserve units per CP.
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
                if not cp.can_recruit_ground_units(self.game):
                    continue
                if self.total_ground_units_allocated_to(cp) >= 10:
                    continue
                if cp.is_global:
                    continue
                candidates.append(cp)

        return candidates

    def total_ground_units_allocated_to(self, control_point: ControlPoint) -> int:
        total = control_point.expected_ground_units_next_turn.total
        for transfer in self.game.transfers:
            if transfer.destination == control_point:
                total += sum(transfer.units.values())
        return total
