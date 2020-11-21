from __future__ import annotations

import random
from typing import TYPE_CHECKING

from dcs.mapping import Point
from dcs.mission import Mission
from dcs.unit import Static
from dcs.unittype import StaticType

if TYPE_CHECKING:
    from game import Game

from .conflictgen import Conflict, FRONTLINE_LENGTH


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


class Outpost(StaticType):
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
    def __init__(self, mission: Mission, game: Game):
        self.mission = mission
        self.game = game

    def _generate_frontline_smokes(self):
        for front_line in self.game.theater.conflicts():
            from_cp = front_line.control_point_a
            to_cp = front_line.control_point_b
            if from_cp.is_global or to_cp.is_global:
                continue

            frontline = Conflict.frontline_position(from_cp, to_cp, self.game.theater)
            if not frontline:
                continue

            point, heading = frontline
            plane_start = point.point_from_heading(turn_heading(heading, 90), FRONTLINE_LENGTH / 2)

            for offset in range(0, FRONTLINE_LENGTH, FRONT_SMOKE_SPACING):
                position = plane_start.point_from_heading(turn_heading(heading, - 90), offset)

                for k, v in FRONT_SMOKE_TYPE_CHANCES.items():
                    if random.randint(0, 100) <= k:
                        pos = position.random_point_within(FRONT_SMOKE_RANDOM_SPREAD, FRONT_SMOKE_RANDOM_SPREAD)
                        if not self.game.theater.is_on_land(pos):
                            break

                        self.mission.static_group(
                            self.mission.country(self.game.enemy_country),
                            "",
                            _type=v,
                            position=pos)
                        break

    def _generate_stub_planes(self):
        pass
        """
        mission_units = set()
        for coalition_name, coalition in self.mission.coalition.items():
            for country in coalition.countries.values():
                for group in country.plane_group + country.helicopter_group + country.vehicle_group:
                    for unit in group.units:
                        mission_units.add(db.unit_type_of(unit))

        for unit_type in mission_units:
            self.mission.static_group(self.mission.country(self.game.player_country), "a", unit_type, Point(0, 300000), hidden=True)"""

    def generate_target_smokes(self, target):
        spread = target.size * DESTINATION_SMOKE_DISTANCE_FACTOR
        for _ in range(0, int(target.size * DESTINATION_SMOKE_AMOUNT_FACTOR * (1.1 - target.base.strength))):
            for k, v in DESTINATION_SMOKE_TYPE_CHANCES.items():
                if random.randint(0, 100) <= k:
                    position = target.position.random_point_within(0, spread)
                    if not self.game.theater.is_on_land(position):
                        break

                    self.mission.static_group(
                        self.mission.country(self.game.enemy_country),
                        "",
                        _type=v,
                        position=position)
                    break

    def generate_transportation_marker(self, at: Point):
        self.mission.static_group(
            self.mission.country(self.game.player_country),
            "",
            _type=MarkerSmoke,
            position=at
        )

    def generate_transportation_destination(self, at: Point):
        self.generate_transportation_marker(at.point_from_heading(0, 20))
        self.mission.static_group(
            self.mission.country(self.game.player_country),
            "",
            _type=Outpost,
            position=at
        )

    def generate(self):
        self._generate_frontline_smokes()
        self._generate_stub_planes()
