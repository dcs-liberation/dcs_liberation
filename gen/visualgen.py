import typing
import random
from datetime import datetime, timedelta

from dcs.mission import Mission
from dcs.statics import *
from dcs.unit import Static

from theater import *
from .conflictgen import *
#from game.game import Game


class MarkerSmoke(unittype.StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 5
    rate = 0.1


class Smoke(unittype.StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 2
    rate = 1


class BigSmoke(unittype.StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 3
    rate = 1


class MassiveSmoke(unittype.StaticType):
    id = "big_smoke"
    category = "Effects"
    name = "big_smoke"
    shape_name = 4
    rate = 1


class Outpost(unittype.StaticType):
    id = "outpost"
    name = "outpost"
    category = "Fortifications"


def __monkey_static_dict(self: Static):
    global __original_static_dict

    d = __original_static_dict(self)
    if self.type == "big_smoke":
        d["effectPreset"] = self.shape_name
        d["effectTransparency"] = self.rate
    return d


__original_static_dict = Static.dict
Static.dict = __monkey_static_dict

FRONT_SMOKE_SPACING = 800
FRONT_SMOKE_RANDOM_SPREAD = 4000
FRONT_SMOKE_TYPE_CHANCES = {
    2: MassiveSmoke,
    15: BigSmoke,
    30: Smoke,
    100: Smoke,
}

DESTINATION_SMOKE_AMOUNT_FACTOR = 0.03
DESTINATION_SMOKE_DISTANCE_FACTOR = 1
DESTINATION_SMOKE_TYPE_CHANCES = {
    5: BigSmoke,
    100: Smoke,
}


def turn_heading(heading, fac):
    heading += fac
    if heading > 359:
        heading = heading - 359
    if heading < 0:
        heading = 359 + heading
    return heading


class VisualGenerator:
    game = None  # type: Game

    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def _generate_frontline_smokes(self):
        for from_cp, to_cp in self.game.theater.conflicts():
            point, heading = Conflict.frontline_position(from_cp, to_cp)
            plane_start = point.point_from_heading(turn_heading(heading, 90), FRONTLINE_LENGTH / 2)

            for offset in range(0, FRONTLINE_LENGTH, FRONT_SMOKE_SPACING):
                position = plane_start.point_from_heading(turn_heading(heading, - 90), offset)

                for k, v in FRONT_SMOKE_TYPE_CHANCES.items():
                    if random.randint(0, 100) <= k:
                        pos = position.random_point_within(FRONT_SMOKE_RANDOM_SPREAD, FRONT_SMOKE_RANDOM_SPREAD)
                        if not self.game.theater.is_on_land(pos):
                            break

                        self.mission.static_group(
                            self.mission.country(self.game.enemy),
                            "",
                            _type=v,
                            position=pos)
                        break

    def generate_target_smokes(self, target):
        spread = target.size * DESTINATION_SMOKE_DISTANCE_FACTOR
        for _ in range(0, int(target.size * DESTINATION_SMOKE_AMOUNT_FACTOR * (1.1 - target.base.strength))):
            for k, v in DESTINATION_SMOKE_TYPE_CHANCES.items():
                if random.randint(0, 100) <= k:
                    position = target.position.random_point_within(0, spread)
                    if not self.game.theater.is_on_land(position):
                        break

                    self.mission.static_group(
                        self.mission.country(self.game.enemy),
                        "",
                        _type=v,
                        position=position)
                    break

    def generate_transportation_marker(self, at: Point):
        self.mission.static_group(
            self.mission.country(self.game.player),
            "",
            _type=MarkerSmoke,
            position=at
        )

    def generate_transportation_destination(self, at: Point):
        self.generate_transportation_marker(at.point_from_heading(0, 20))
        self.mission.static_group(
            self.mission.country(self.game.player),
            "",
            _type=Outpost,
            position=at
        )

    def generate(self):
        self._generate_frontline_smokes()
