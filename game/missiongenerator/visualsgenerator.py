from __future__ import annotations

import random
from typing import Any, TYPE_CHECKING

from dcs.mission import Mission
from dcs.unit import Static
from dcs.unittype import StaticType

if TYPE_CHECKING:
    from game import Game

from .frontlineconflictdescription import FrontLineConflictDescription


class MarkerSmoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 5  # type: ignore
    rate = 0.1  # type: ignore


class Smoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 2  # type: ignore
    rate = 1


class BigSmoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 3  # type: ignore
    rate = 1


class MassiveSmoke(StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 4  # type: ignore
    rate = 1


def __monkey_static_dict(self: Static) -> dict[str, Any]:
    global __original_static_dict

    d = __original_static_dict(self)
    if self.type == "big_smoke":
        d["effectPreset"] = self.shape_name
        d["effectTransparency"] = self.rate
    return d


__original_static_dict = Static.dict
Static.dict = __monkey_static_dict  # type: ignore

FRONT_SMOKE_RANDOM_SPREAD = 4000
FRONT_SMOKE_TYPE_CHANCES = {
    2: MassiveSmoke,
    15: BigSmoke,
    30: Smoke,
    100: Smoke,
}


class VisualsGenerator:
    def __init__(self, mission: Mission, game: Game) -> None:
        self.mission = mission
        self.game = game

    def _generate_frontline_smokes(self) -> None:
        for front_line in self.game.theater.conflicts():
            from_cp = front_line.blue_cp
            to_cp = front_line.red_cp
            if from_cp.is_global or to_cp.is_global:
                continue

            bounds = FrontLineConflictDescription.frontline_bounds(
                front_line, self.game.theater
            )

            for offset in range(
                0, bounds.length, self.game.settings.perf_smoke_spacing
            ):
                position = bounds.left_position.point_from_heading(
                    bounds.heading_from_left_to_right.degrees, offset
                )

                for k, v in FRONT_SMOKE_TYPE_CHANCES.items():
                    if random.randint(0, 100) <= k:
                        pos = position.random_point_within(
                            FRONT_SMOKE_RANDOM_SPREAD, FRONT_SMOKE_RANDOM_SPREAD
                        )
                        if not self.game.theater.is_on_land(pos):
                            break

                        self.mission.static_group(
                            self.mission.country(self.game.red.country_name),
                            "",
                            _type=v,
                            position=pos,
                        )
                        break

    def generate(self) -> None:
        if self.game.settings.perf_smoke_gen:
            self._generate_frontline_smokes()
