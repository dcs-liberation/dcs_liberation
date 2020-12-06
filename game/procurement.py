from __future__ import annotations

import math
import random
from typing import List, Optional, TYPE_CHECKING, Type

from dcs.task import CAP, CAS
from dcs.unittype import FlyingType, UnitType, VehicleType

from game import db
from game.factions.faction import Faction
from game.theater import ControlPoint

if TYPE_CHECKING:
    from game import Game


class AircraftProcurer:
    def __init__(self, faction: Faction) -> None:
        self.faction = faction


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

    def spend_budget(self, budget: int) -> int:
        if self.manage_runways:
            budget = self.repair_runways(budget)
        if self.manage_front_line:
            armor_budget = math.ceil(budget / 2)
            budget -= armor_budget
            budget += self.reinforce_front_line(armor_budget)
        if self.manage_aircraft:
            budget = self.purchase_aircraft(budget)
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
            self, budget: int) -> Optional[Type[VehicleType]]:
        affordable_units = [u for u in self.faction.frontline_units if
                            db.PRICES[u] <= budget]
        if not affordable_units:
            return None
        return random.choice(affordable_units)

    def reinforce_front_line(self, budget: int) -> int:
        if not self.faction.frontline_units:
            return budget

        while budget > 0:
            candidates = self.front_line_candidates()
            if not candidates:
                break

            cp = random.choice(candidates)
            unit = self.random_affordable_ground_unit(budget)
            if unit is None:
                # Can't afford any more units.
                break

            budget -= db.PRICES[unit]
            assert cp.pending_unit_deliveries is not None
            cp.pending_unit_deliveries.deliver({unit: 1})

        return budget

    def random_affordable_aircraft_group(
            self, budget: int, size: int) -> Optional[Type[FlyingType]]:
        unit_pool = [u for u in self.faction.aircrafts
                     if u in db.UNIT_BY_TASK[CAS] or u in db.UNIT_BY_TASK[CAP]]

        affordable_units = [u for u in unit_pool
                            if db.PRICES[u] * size <= budget]
        if not affordable_units:
            return None
        return random.choice(affordable_units)

    def purchase_aircraft(self, budget: int) -> int:
        unit_pool = [u for u in self.faction.aircrafts
                     if u in db.UNIT_BY_TASK[CAS] or u in db.UNIT_BY_TASK[CAP]]
        if not unit_pool:
            return budget

        while budget > 0:
            group_size = 2
            candidates = self.airbase_candidates(group_size)
            if not candidates:
                break

            cp = random.choice(candidates)
            unit = self.random_affordable_aircraft_group(budget, group_size)
            if unit is None:
                # Can't afford any more aircraft.
                break

            budget -= db.PRICES[unit] * group_size
            assert cp.pending_unit_deliveries is not None
            cp.pending_unit_deliveries.deliver({unit: group_size})

        return budget

    @property
    def owned_points(self) -> List[ControlPoint]:
        if self.is_player:
            return self.game.theater.player_points()
        else:
            return self.game.theater.enemy_points()

    def airbase_candidates(self, group_size: int) -> List[ControlPoint]:
        all_usable = []
        preferred = []
        for cp in self.owned_points:
            if not cp.runway_is_operational():
                continue
            if cp.unclaimed_parking(self.game) < group_size:
                continue

            all_usable.append(cp)
            for connected in cp.connected_points:
                # Prefer to buy aircraft at active front lines.
                # TODO: Buy aircraft where they are needed, not at front lines.
                if not connected.is_friendly(to_player=self.is_player):
                    preferred.append(cp)

        if preferred:
            return preferred

        # Otherwise buy them anywhere valid.
        return all_usable

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
