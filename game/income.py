from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.config import REWARDS

if TYPE_CHECKING:
    from game import Game


@dataclass(frozen=True)
class BuildingIncome:
    name: str
    category: str
    number: int
    income_per_building: float

    @property
    def income(self) -> float:
        return self.number * self.income_per_building


class Income:
    def __init__(self, game: Game, player: bool) -> None:
        if player:
            self.multiplier = game.settings.player_income_multiplier
        else:
            self.multiplier = game.settings.enemy_income_multiplier
        self.control_points = []
        self.buildings = []

        for cp in game.theater.control_points_for(player):
            if cp.income_per_turn:
                self.control_points.append(cp)

            for tgo in cp.ground_objects:
                if tgo.category not in REWARDS:
                    continue
                self.buildings.append(
                    BuildingIncome(
                        tgo.obj_name,
                        tgo.category,
                        sum(1 for b in tgo.statics if b.alive),
                        REWARDS[tgo.category],
                    )
                )

        self.from_bases = sum(cp.income_per_turn for cp in self.control_points)
        self.total_buildings = sum(b.income for b in self.buildings)
        self.total = (self.total_buildings + self.from_bases) * self.multiplier
