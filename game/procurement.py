from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterator, List, Optional, TYPE_CHECKING, Type

from dcs.task import CAP, CAS
from dcs.unittype import FlyingType, VehicleType

from game import db
from game.factions.faction import Faction
from game.theater import ControlPoint, MissionTarget
from game.utils import Distance
from gen.flights.ai_flight_planner_db import aircraft_for_task
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.flights.flight import FlightType
from gen.ground_forces.ai_ground_planner_db import TYPE_SHORAD

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
    def __init__(self, game: Game, for_player: bool, faction: Faction,
                 manage_runways: bool, manage_front_line: bool,
                 manage_aircraft: bool) -> None:
        self.game = game
        self.is_player = for_player
        self.faction = faction
        self.manage_runways = manage_runways
        self.manage_front_line = manage_front_line
        self.manage_aircraft = manage_aircraft
        self.threat_zones = self.game.threat_zone_for(not self.is_player)

    def spend_budget(
            self, budget: int,
            aircraft_requests: List[AircraftProcurementRequest]) -> int:
        if self.manage_runways:
            budget = self.repair_runways(budget)
        if self.manage_front_line:
            armor_budget = math.ceil(budget / 2)
            budget -= armor_budget
            budget += self.reinforce_front_line(armor_budget)
        if self.manage_aircraft:
            budget = self.purchase_aircraft(budget, aircraft_requests)
        return budget

    def repair_runways(self, budget: int) -> int:
        for control_point in self.owned_points:
            if budget < db.RUNWAY_REPAIR_COST:
                break
            if control_point.runway_can_be_repaired:
                control_point.begin_runway_repair()
                budget -= db.RUNWAY_REPAIR_COST
                if self.is_player:
                    self.game.message(
                        "OPFOR has begun repairing the runway at "
                        f"{control_point}"
                    )
                else:
                    self.game.message(
                        "We have begun repairing the runway at "
                        f"{control_point}"
                    )
        return budget

    def random_affordable_ground_unit(
            self, budget: int, cp: ControlPoint) -> Optional[Type[VehicleType]]:
        affordable_units = [u for u in self.faction.frontline_units + self.faction.artillery_units if
                            db.PRICES[u] <= budget]

        total_number_aa = cp.base.total_frontline_aa + cp.pending_frontline_aa_deliveries_count
        total_non_aa = cp.base.total_armor + cp.pending_deliveries_count - total_number_aa
        max_aa = math.ceil(total_non_aa/8)

        # Limit the number of AA units the AI will buy
        if not total_number_aa < max_aa:
            for unit in [u for u in affordable_units if u in TYPE_SHORAD]:
                affordable_units.remove(unit)

        if not affordable_units:
            return None
        return random.choice(affordable_units)

    def reinforce_front_line(self, budget: int) -> int:
        if not self.faction.frontline_units and not self.faction.artillery_units:
            return budget

        while budget > 0:
            candidates = self.front_line_candidates()
            if not candidates:
                break

            cp = random.choice(candidates)
            unit = self.random_affordable_ground_unit(budget, cp)
            if unit is None:
                # Can't afford any more units.
                break

            budget -= db.PRICES[unit]
            assert cp.pending_unit_deliveries is not None
            cp.pending_unit_deliveries.deliver({unit: 1})

        return budget

    def _affordable_aircraft_of_types(
            self, types: List[Type[FlyingType]], airbase: ControlPoint,
            number: int, max_price: int) -> Optional[Type[FlyingType]]:
        best_choice: Optional[Type[FlyingType]] = None
        for unit in [u for u in self.faction.aircrafts if u in types]:
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
            self, request: AircraftProcurementRequest,
            airbase: ControlPoint, budget: int) -> Optional[Type[FlyingType]]:
        return self._affordable_aircraft_of_types(
            aircraft_for_task(request.task_capability),
            airbase, request.number, budget)

    def purchase_aircraft(
            self, budget: int,
            aircraft_requests: List[AircraftProcurementRequest]) -> int:
        unit_pool = [u for u in self.faction.aircrafts
                     if u in db.UNIT_BY_TASK[CAS] or u in db.UNIT_BY_TASK[CAP]]
        if not unit_pool:
            return budget

        for request in aircraft_requests:
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
                assert airbase.pending_unit_deliveries is not None
                airbase.pending_unit_deliveries.deliver({unit: request.number})

        return budget

    @property
    def owned_points(self) -> List[ControlPoint]:
        if self.is_player:
            return self.game.theater.player_points()
        else:
            return self.game.theater.enemy_points()

    def best_airbases_for(
            self,
            request: AircraftProcurementRequest) -> Iterator[ControlPoint]:
        distance_cache = ObjectiveDistanceCache.get_closest_airfields(
            request.near
        )
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
            if cp.base.total_armor >= 30:
                # Control point is already sufficiently defended.
                continue
            for connected in cp.connected_points:
                if not connected.is_friendly(to_player=self.is_player):
                    candidates.append(cp)

        if not candidates:
            # Otherwise buy them anywhere valid.
            candidates = [p for p in self.owned_points
                          if p.can_deploy_ground_units]

        return candidates
