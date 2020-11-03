import logging
import random

from game import db
from gen.fleet.carrier_group import CarrierGroupGenerator
from gen.fleet.cn_dd_group import ChineseNavyGroupGenerator, Type54GroupGenerator
from gen.fleet.dd_group import ArleighBurkeGroupGenerator, OliverHazardPerryGroupGenerator
from gen.fleet.lha_group import LHAGroupGenerator
from gen.fleet.ru_dd_group import RussianNavyGroupGenerator, GrishaGroupGenerator, MolniyaGroupGenerator, \
    KiloSubGroupGenerator, TangoSubGroupGenerator
from gen.fleet.schnellboot import SchnellbootGroupGenerator
from gen.fleet.uboat import UBoatGroupGenerator
from gen.fleet.ww2lst import WW2LSTGroupGenerator
# from dcs import unitgroup
# from dcs.unit import Ship


SHIP_MAP = {
    "SchnellbootGroupGenerator": SchnellbootGroupGenerator,
    "WW2LSTGroupGenerator": WW2LSTGroupGenerator,
    "UBoatGroupGenerator": UBoatGroupGenerator,
    "OliverHazardPerryGroupGenerator": OliverHazardPerryGroupGenerator,
    "ArleighBurkeGroupGenerator": ArleighBurkeGroupGenerator,
    "RussianNavyGroupGenerator": RussianNavyGroupGenerator,
    "ChineseNavyGroupGenerator": ChineseNavyGroupGenerator,
    "GrishaGroupGenerator": GrishaGroupGenerator,
    "MolniyaGroupGenerator": MolniyaGroupGenerator,
    "KiloSubGroupGenerator": KiloSubGroupGenerator,
    "TangoSubGroupGenerator": TangoSubGroupGenerator,
    "Type54GroupGenerator": Type54GroupGenerator
}


def generate_ship_group(game, ground_object, faction_name: str):
    """
    This generate a ship group
    :return: Nothing, but put the group reference inside the ground object
    """
    faction = db.FACTIONS[faction_name]
    if len(faction.navy_generators) > 0:
        gen = random.choice(faction.navy_generators)
        if gen in SHIP_MAP.keys():
            generator = SHIP_MAP[gen](game, ground_object, faction)
            generator.generate()
            return generator.get_generated_group()
        else:
            logging.info("Unable to generate ship group, generator : " + str(gen) + "does not exists")
    return None


def generate_carrier_group(faction:str, game, ground_object):
    """
    This generate a carrier group
    :param parentCp: The parent control point
    :param ground_object: The ground object which will own the ship group
    :param country: Owner country
    :return: Nothing, but put the group reference inside the ground object
    """
    generator = CarrierGroupGenerator(game, ground_object, db.FACTIONS[faction])
    generator.generate()
    return generator.get_generated_group()


def generate_lha_group(faction:str, game, ground_object):
    """
    This generate a lha carrier group
    :param parentCp: The parent control point
    :param ground_object: The ground object which will own the ship group
    :param country: Owner country
    :return: Nothing, but put the group reference inside the ground object
    """
    generator = LHAGroupGenerator(game, ground_object, db.FACTIONS[faction])
    generator.generate()
    return generator.get_generated_group()

# class ShipGroupGenerator(GroupGenerator):
#     """Abstract class for other ship generator classes"""
#     def __init__(self, game, ground_object, faction):
#         self.game = game
#         self.go = ground_object
#         self.position = ground_object.position
#         self.heading = random.randint(0, 359)
#         self.faction = faction
#         self.vg = unitgroup.ShipGroup(self.game.next_group_id(), self.groupNamePrefix + self.go.group_identifier)
#         wp = self.vg.add_waypoint(self.position, 0)
#         wp.ETA_locked = True
    
#     def add_unit(self, unit_type, name, pos_x, pos_y, heading):
#         nn = "cgroup|" + str(self.go.cp_id) + '|' + str(self.go.group_id) + '|' + str(self.go.group_identifier) + "|" + name

#         unit = Ship(self.game.next_unit_id(),
#                        nn, unit_type)
#         unit.position.x = pos_x
#         unit.position.y = pos_y
#         unit.heading = heading
#         self.vg.add_unit(unit)
#         return unit
