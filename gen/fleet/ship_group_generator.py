import random

from game import db
from gen.fleet.carrier_group import CarrierGroupGenerator
from gen.fleet.lha_group import LHAGroupGenerator
from dcs.ships import *

from gen.fleet.schnellboot import SchnellbootGroupGenerator
from gen.fleet.uboat import UBoatGroupGenerator
from gen.fleet.ww2lst import WW2LSTGroupGenerator

SHIP_MAP = {
    Schnellboot_type_S130: SchnellbootGroupGenerator,
    LS_Samuel_Chase: WW2LSTGroupGenerator,
    Uboat_VIIC_U_flak: UBoatGroupGenerator
}


def generate_ship_group(game, ground_object, faction:str):
    """
    This generate a ship group
    :return: Nothing, but put the group reference inside the ground object
    """
    faction = db.FACTIONS[faction]
    if "boat" in faction.keys():
        ships = faction["boat"]
        if len(ships) > 0:
            sam = random.choice(ships)
            generator = SHIP_MAP[sam](game, ground_object, faction)
            generator.generate()
            return generator.get_generated_group()
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