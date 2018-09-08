import logging

from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.statics import *


CATEGORY_MAPPING = {
    "power": [Fortification.Workshop_A],
    "warehouse": [Warehouse.Warehouse],
    "fuel": [Warehouse.Tank],
    "ammo": [Warehouse.Ammunition_depot],
}


class GroundObjectsGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.m = mission
        self.conflict = conflict
        self.game = game

    def generate(self):
        side = self.m.country(self.game.enemy)

        cp = None  # type: ControlPoint
        if self.conflict.attackers_side.name == self.game.player:
            cp = self.conflict.to_cp
        else:
            cp = self.conflict.from_cp

        for ground_object in cp.ground_objects:
            if ground_object.category == "defense":
                unit_type = random.choice(self.game.commision_unit_types(cp, AirDefence))
                assert unit_type is not None, "Cannot find unit type for GroundObject defense ({})!".format(cp)

                group = self.m.vehicle_group(
                    country=side,
                    name=ground_object.string_identifier,
                    _type=unit_type,
                    position=Point(*ground_object.location),
                    heading=ground_object.heading
                )

                logging.info("generated defense object identifier {} with mission id {}".format(group.name, group.id))
            else:
                group = self.m.static_group(
                    country=side,
                    name=ground_object.string_identifier,
                    _type=random.choice(CATEGORY_MAPPING[ground_object.category]),
                    position=Point(*ground_object.location),
                    heading=ground_object.heading
                )

                logging.info("generated object identifier {} with mission id {}".format(group.name, group.id))
