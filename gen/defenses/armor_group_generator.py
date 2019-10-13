import random

from dcs.vehicles import Armor

from game import db
from gen.defenses.armored_group_generator import ArmoredGroupGenerator


def generate_armor_group(faction:str, game, ground_object):
    """
    This generate a SAM group
    :param parentCp: The parent control point
    :param ground_object: The ground object which will own the sam group
    :param country: Owner country
    :return: Nothing, but put the group reference inside the ground object
    """

    possible_unit = [u for u in db.FACTIONS[faction]["units"] if u in Armor.__dict__.values()]
    if len(possible_unit) > 0:
        unit_type = random.choice(possible_unit)
        generator = ArmoredGroupGenerator(game, ground_object, unit_type)
        generator.generate()
        return generator.get_generated_group()
    return None
