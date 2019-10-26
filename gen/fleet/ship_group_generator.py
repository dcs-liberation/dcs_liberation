import random

from dcs.vehicles import Armor

from game import db
from gen.defenses.armored_group_generator import ArmoredGroupGenerator
from gen.fleet.carrier_group import CarrierGroupGenerator


def generate_carrier_group(faction:str, game, ground_object):
    """
    This generate a ship group
    :param parentCp: The parent control point
    :param ground_object: The ground object which will own the ship group
    :param country: Owner country
    :return: Nothing, but put the group reference inside the ground object
    """
    generator = CarrierGroupGenerator(game, ground_object, db.FACTIONS[faction])
    generator.generate()
    return generator.get_generated_group()
