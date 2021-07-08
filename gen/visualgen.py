from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from dcs.mission import Mission
from dcs.unit import Static
from dcs.unittype import StaticType

if TYPE_CHECKING:
    from game import Game

from .conflictgen import Conflict


class MarkerSmoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 5
    rate = 0.1


class Smoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 2
    rate = 1


class BigSmoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 3
    rate = 1


class MassiveSmoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 4
    rate = 1


def __monkey_static_dict(self: Static) -> dict[str, Any]:
    global __original_static_dict

    d = __original_static_dict(self)
    if self.type == "big_smoke":
        d["effectPreset"] = self.shape_name
        d["effectTransparency"] = self.rate
    return d


__original_static_dict = Static.dict
Static.dict = __monkey_static_dict

FRONT_SMOKE_RANDOM_SPREAD = 4000
FRONT_SMOKE_TYPE_CHANCES = {
    2: MassiveSmoke,
    15: BigSmoke,
    30: Smoke,
    100: Smoke,
}


class VisualGenerator:
    def __init__(self, mission: Mission, game: Game) -> None:
        self.mission = mission
        self.game = game

    def _generate_frontline_smokes(self) -> None:
        for front_line in self.game.theater.conflicts():
            from_cp = front_line.blue_cp
            to_cp = front_line.red_cp
            if from_cp.is_global or to_cp.is_global:
                continue

            plane_start, heading, distance = Conflict.frontline_vector(
                front_line, self.game.theater
            )
            if not plane_start:
                continue

            for offset in range(0, distance, self.game.settings.perf_smoke_spacing):
                position = plane_start.point_from_heading(heading, offset)

                for k, v in FRONT_SMOKE_TYPE_CHANCES.items():
                    if random.randint(0, 100) <= k:
                        pos = position.random_point_within(
                            FRONT_SMOKE_RANDOM_SPREAD, FRONT_SMOKE_RANDOM_SPREAD
                        )
                        if not self.game.theater.is_on_land(pos):
                            break

                        self.mission.static_group(
                            self.mission.country(self.game.enemy_country),
                            "",
                            _type=v,
                            position=pos,
                        )
                        break

    def generate(self) -> None:
        self._generate_frontline_smokes()
