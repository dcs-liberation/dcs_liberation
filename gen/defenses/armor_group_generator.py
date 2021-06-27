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


def generate_armor_group(
    faction: str, game, ground_object, shorad_included_probability: int
):
    """
    This generate a group of ground units
    :return: Generated group
    """
    armor_types = (
        GroundUnitClass.Atgm,
        GroundUnitClass.Tank,
    )
    possible_unit = [
        u for u in db.FACTIONS[faction].frontline_units if u.unit_class in armor_types
    ]
    if len(possible_unit) > 0:
        unit_type = random.choice(possible_unit)
        return generate_armor_group_of_type(
            game, ground_object, unit_type, faction, shorad_included_probability
        )
    return None


def generate_light_armor_group(
    faction: str, game, ground_object, shorad_included_probability: int
):
    """
    This generate a group of ground units
    :return: Generated group
    """
    armor_types = (GroundUnitClass.Apc, GroundUnitClass.Ifv)
    possible_unit = [
        u for u in db.FACTIONS[faction].frontline_units if u.unit_class in armor_types
    ]
    if len(possible_unit) > 0:
        unit_type = random.choice(possible_unit)
        return generate_armor_group_of_type(
            game, ground_object, unit_type, faction, shorad_included_probability
        )
    return None


def generate_armor_group_of_type(
    game: Game,
    ground_object: VehicleGroupGroundObject,
    unit_type: GroundUnitType,
    faction: str,
    shorad_included_probability: int,
) -> VehicleGroup:
    """
    This generate a group of ground units of given type
    :return: Generated group
    """
    generator = ArmoredGroupGenerator(game, ground_object, unit_type)
    generator.generate()

    vehicle_group = generator.get_generated_group()

    # add shorad to group if probability
    random_percentage = random.randint(1, 100)

    if random_percentage <= shorad_included_probability:
        shorads = [
            u
            for u in db.FACTIONS[faction].frontline_units
            if u.unit_class == GroundUnitClass.Shorads
        ]
        if len(shorads) > 0:
            shorad = random.choice(shorads)
            s_posx, s_posy = caluclate_shorad_position(
                vehicle_group.units[0].position.x,
                vehicle_group.units[0].position.y,
                vehicle_group.units[3].position.x,
                vehicle_group.units[3].position.y,
            )
            generator.add_unit(
                shorad.dcs_unit_type,
                "group-shorad",
                s_posx,
                s_posy,
                vehicle_group.units[0].heading,
            )
    return vehicle_group


def caluclate_shorad_position(pos1_x: int, pos1_y: int, pos2_x: int, pos2_y: int):
    middle_x = (pos1_x + pos2_x) / 2
    middle_y = (pos1_y + pos2_y) / 2
    spacing_x = random.randint(90, 100)
    spacing_y = random.randint(90, 100)

    return (middle_x + spacing_x, middle_y + spacing_y)


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
