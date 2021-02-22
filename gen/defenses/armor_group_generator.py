import random

from dcs.vehicles import Armor

from game import db
from gen.defenses.armored_group_generator import (
    ArmoredGroupGenerator,
    FixedSizeArmorGroupGenerator,
)


def generate_armor_group(faction: str, game, ground_object):
    """
    This generate a group of ground units
    :return: Generated group
    """
    possible_unit = [
        u for u in db.FACTIONS[faction].frontline_units if u in Armor.__dict__.values()
    ]
    if len(possible_unit) > 0:
        unit_type = random.choice(possible_unit)
        return generate_armor_group_of_type(game, ground_object, unit_type)
    return None


def generate_armor_group_of_type(game, ground_object, unit_type):
    """
    This generate a group of ground units of given type
    :return: Generated group
    """
    generator = ArmoredGroupGenerator(game, ground_object, unit_type)
    generator.generate()
    return generator.get_generated_group()


def generate_armor_group_of_type_and_size(game, ground_object, unit_type, size: int):
    """
    This generate a group of ground units of given type and size
    :return: Generated group
    """
    generator = FixedSizeArmorGroupGenerator(game, ground_object, unit_type, size)
    generator.generate()
    return generator.get_generated_group()
