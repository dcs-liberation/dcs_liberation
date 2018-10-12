import logging

from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.statics import *

FARP_FRONTLINE_DISTANCE = 10000
AA_CP_MIN_DISTANCE = 40000


class GroundObjectsGenerator:
    FARP_CAPACITY = 4

    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.m = mission
        self.conflict = conflict
        self.game = game

    def generate_farps(self, number_of_units=1) -> typing.Collection[StaticGroup]:
        if self.conflict.is_vector:
            center = self.conflict.center
            heading = self.conflict.heading - 90
        else:
            center, heading = self.conflict.frontline_position(self.conflict.from_cp, self.conflict.to_cp)
            heading -= 90

        position = self.conflict.find_ground_position(center.point_from_heading(heading, FARP_FRONTLINE_DISTANCE), heading)
        for i, _ in enumerate(range(0, number_of_units, self.FARP_CAPACITY)):
            position = position.point_from_heading(0, i * 275)

            yield self.m.farp(
                country=self.m.country(self.game.player),
                name="FARP",
                position=position,
            )

    def generate(self):
        side = self.m.country(self.game.enemy)

        cp = None  # type: ControlPoint
        if self.conflict.attackers_side.name == self.game.player:
            cp = self.conflict.to_cp
        else:
            cp = self.conflict.from_cp

        for ground_object in cp.ground_objects:
            if ground_object.dcs_identifier == "AA":
                if ground_object.position.distance_to_point(self.conflict.from_cp.position) < AA_CP_MIN_DISTANCE:
                    continue

                if ground_object.is_dead:
                    continue

                unit_type = random.choice(self.game.commision_unit_types(cp, AirDefence))
                assert unit_type is not None, "Cannot find unit type for GroundObject defense ({})!".format(cp)

                group = self.m.vehicle_group(
                    country=side,
                    name=ground_object.string_identifier,
                    _type=unit_type,
                    position=ground_object.position,
                    heading=ground_object.heading,
                )

                logging.info("generated defense object identifier {} with mission id {}".format(group.name, group.id))
            else:
                if ground_object.dcs_identifier in warehouse_map:
                    static_type = warehouse_map[ground_object.dcs_identifier]
                else:
                    static_type = fortification_map[ground_object.dcs_identifier]

                if not static_type:
                    print("Didn't find {} in static _map(s)!".format(ground_object.dcs_identifier))
                    continue

                group = self.m.static_group(
                    country=side,
                    name=ground_object.string_identifier,
                    _type=static_type,
                    position=ground_object.position,
                    heading=ground_object.heading,
                    dead=ground_object.is_dead,
                )

                logging.info("generated {}object identifier {} with mission id {}".format("dead " if ground_object.is_dead else "", group.name, group.id))
