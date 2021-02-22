from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.db import REWARDS

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


class Income:
    def __init__(self, game: Game, player: bool) -> None:
        if player:
            self.multiplier = game.settings.player_income_multiplier
        else:
            self.multiplier = game.settings.enemy_income_multiplier
        self.control_points = []
        self.buildings = []

        names = set()
        for cp in game.theater.control_points_for(player):
            if cp.income_per_turn:
                self.control_points.append(cp)
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
            self.buildings.append(
                BuildingIncome(name, category, count, REWARDS[category])
            )

        self.from_bases = sum(cp.income_per_turn for cp in self.control_points)
        self.total_buildings = sum(b.income for b in self.buildings)
        self.total = (self.total_buildings + self.from_bases) * self.multiplier
