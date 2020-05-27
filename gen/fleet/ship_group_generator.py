from game import db
from gen.fleet.carrier_group import CarrierGroupGenerator
from gen.fleet.lha_group import LHAGroupGenerator


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