from __future__ import annotations

import logging
import math
import random
from typing import List, TYPE_CHECKING, Type

from dcs.task import CAP, CAS
from dcs.unittype import FlyingType, UnitType

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

    def reinforce_front_line(self, budget: int) -> int:
        if not self.faction.frontline_units:
            return budget

        armor_limit = int(30 * self.game.settings.multiplier)
        candidates = self.front_line_candidates(armor_limit)
        if not candidates:
            return budget

        # TODO: No need to limit?
        for _ in range(50):
            if budget <= 0:
                break

            cp = random.choice(candidates)
            unit = random.choice(self.faction.frontline_units)
            price = db.PRICES[unit] * 2
            # TODO: Don't allow negative budget.
            # Build a list of only affordable units and choose from those.
            budget -= price * 2
            cp.base.armor[unit] = cp.base.armor.get(unit, 0) + 2
            self.reinforcement_message(unit, cp)

            if cp.base.total_armor >= armor_limit:
                candidates.remove(cp)
                if not candidates:
                    break

        return budget

    def purchase_aircraft(self, budget: int) -> int:
        aircraft_limit = int(25 * self.game.settings.multiplier)
        candidates = self.airbase_candidates(aircraft_limit)
        if not candidates:
            return budget

        unit_pool = [u for u in self.faction.aircrafts
                     if u in db.UNIT_BY_TASK[CAS] or u in db.UNIT_BY_TASK[CAP]]
        if not unit_pool:
            return budget

        # TODO: No need to limit?
        for _ in range(50):
            if budget <= 0:
                break

            cp = random.choice(candidates)
            unit = random.choice(unit_pool)
            price = db.PRICES[unit] * 2
            # TODO: Don't allow negative budget.
            # Build a list of only affordable units and choose from those.
            budget -= price * 2
            cp.base.aircraft[unit] = cp.base.aircraft.get(unit, 0) + 2
            self.reinforcement_message(unit, cp)

            if cp.base.total_aircraft >= aircraft_limit:
                candidates.remove(cp)
                if not candidates:
                    break

        return budget

    def reinforcement_message(self, unit_type: Type[UnitType],
                              control_point: ControlPoint) -> None:
        description = f"{unit_type.id} x 2 at {control_point.name}"
        if self.is_player:
            self.game.message(f"Our reinforcements: {description}")
        else:
            self.game.message(f"OPFOR reinforcements: {description}")

    @property
    def owned_points(self) -> List[ControlPoint]:
        if self.is_player:
            return self.game.theater.player_points()
        else:
            return self.game.theater.enemy_points()

    def airbase_candidates(self, unit_limit: int) -> List[ControlPoint]:
        candidates = []

        # Prefer to buy front line units at active front lines that are not
        # already overloaded.
        # TODO: Buy aircraft where they are needed, not at front lines.
        for cp in self.owned_points:
            if cp.base.total_aircraft >= unit_limit:
                continue
            for connected in cp.connected_points:
                if not connected.is_friendly(to_player=self.is_player):
                    candidates.append(cp)

        if not candidates:
            # Otherwise buy them anywhere valid.
            candidates = [p for p in self.owned_points
                          if p.can_deploy_ground_units]

        return candidates

    def front_line_candidates(self, unit_limit: int) -> List[ControlPoint]:
        candidates = []

        # Prefer to buy front line units at active front lines that are not
        # already overloaded.
        for cp in self.owned_points:
            if cp.base.total_armor >= unit_limit:
                continue
            for connected in cp.connected_points:
                if not connected.is_friendly(to_player=self.is_player):
                    candidates.append(cp)

        if not candidates:
            # Otherwise buy them anywhere valid.
            candidates = [p for p in self.owned_points
                          if p.can_deploy_ground_units]

        return candidates
