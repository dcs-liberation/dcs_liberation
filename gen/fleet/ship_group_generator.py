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


def generate_carrier_group(faction: str, game, ground_object):
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


def generate_lha_group(faction: str, game, ground_object):
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
