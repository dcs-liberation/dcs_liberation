import random

from dcs.unitgroup import VehicleGroup

from game import db, Game, settings
from game.data.groundunitclass import GroundUnitClass
from game.dcs.groundunittype import GroundUnitType
from game.theater.theatergroundobject import VehicleGroupGroundObject
from gen.defenses.armored_group_generator import (
    ArmoredGroupGenerator,
    FixedSizeArmorGroupGenerator,
)


def generate_armor_group(faction: str, game, ground_object):
    """
    This generate a group of ground units
    :return: Generated group
    """
    armor_types = (
        GroundUnitClass.Apc,
        GroundUnitClass.Atgm,
        GroundUnitClass.Ifv,
        GroundUnitClass.Tank,
    )
    possible_unit = [
        u for u in db.FACTIONS[faction].frontline_units if u.unit_class in armor_types
    ]
    if len(possible_unit) > 0:
        unit_type = random.choice(possible_unit)
        return generate_armor_group_of_type(game, ground_object, unit_type, faction)
    return None


def generate_armor_group_of_type(
    game: Game,
    ground_object: VehicleGroupGroundObject,
    unit_type: GroundUnitType,
    faction: str,
) -> VehicleGroup:
    """
    This generate a group of ground units of given type
    :return: Generated group
    """
    generator = ArmoredGroupGenerator(game, ground_object, unit_type)
    generator.generate()

    vehicle_group = generator.get_generated_group()

    if (settings.Settings.shorad_added_to_armor_groups):
        shorads = [
            u
            for u in db.FACTIONS[faction].frontline_units
            if u.unit_class == GroundUnitClass.Shorads
        ]
        if len(shorads) > 0:
            shorad = random.choice(shorads)
            spacing = (
                vehicle_group.units[0].position.x - vehicle_group.units[1].position.x
            )
            generator.add_unit(
                shorad.dcs_unit_type,
                "group-shorad",
                vehicle_group.units[0].position.x - spacing,
                vehicle_group.units[0].position.y - spacing,
                vehicle_group.units[0].heading,
            )

    return vehicle_group


def generate_armor_group_of_type_and_size(
    game: Game,
    ground_object: VehicleGroupGroundObject,
    unit_type: GroundUnitType,
    size: int,
) -> VehicleGroup:
    """
    This generate a group of ground units of given type and size
    :return: Generated group
    """
    generator = FixedSizeArmorGroupGenerator(game, ground_object, unit_type, size)
    generator.generate()
    return generator.get_generated_group()
