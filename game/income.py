from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.db import PLAYER_BUDGET_BASE, REWARDS
from game.theater import ControlPoint

if TYPE_CHECKING:
    from game import Game


@dataclass(frozen=True)
class BuildingIncome:
    name: str
    category: str
    number: int
    income_per_building: int

    @property
    def income(self) -> int:
        return self.number * self.income_per_building


@dataclass(frozen=True)
class ControlPointIncome:
    control_point: ControlPoint
    income: int


class Income:
    def __init__(self, game: Game, player: bool) -> None:
        if player:
            self.multiplier = game.settings.player_income_multiplier
        else:
            self.multiplier = game.settings.enemy_income_multiplier
        self.control_points = []
        self.buildings = []

        self.income_per_base = PLAYER_BUDGET_BASE if player else 0

        names = set()
        for cp in game.theater.control_points_for(player):
            self.control_points.append(
                ControlPointIncome(cp, self.income_per_base))
            for tgo in cp.ground_objects:
                names.add(tgo.obj_name)

        for name in names:
            count = 0
            tgos = game.theater.find_ground_objects_by_obj_name(name)
            category = tgos[0].category
            if category not in REWARDS:
                continue
            for tgo in tgos:
                if not tgo.is_dead:
                    count += 1
            self.buildings.append(BuildingIncome(name, category, count,
                                                 REWARDS[category]))

        self.from_bases = sum(cp.income for cp in self.control_points)
        self.total_buildings = sum(b.income for b in self.buildings)
        self.total = ((self.total_buildings + self.from_bases) *
                      self.multiplier)
