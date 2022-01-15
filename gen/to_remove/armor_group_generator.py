import random
from typing import Optional

from dcs.unitgroup import VehicleGroup

from game import db, Game
from game.data.groundunitclass import GroundUnitClass
from game.dcs.groundunittype import GroundUnitType
from game.theater.theatergroundobject import VehicleGroupGroundObject
from gen.to_remove.armored_group_generator import (
    ArmoredGroupGenerator,
    FixedSizeArmorGroupGenerator,
)


def generate_armor_group(
    faction: str, game: Game, ground_object: VehicleGroupGroundObject
) -> Optional[VehicleGroup]:
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
        return generate_armor_group_of_type(game, ground_object, unit_type)
    return None


def generate_armor_group_of_type(
    game: Game, ground_object: VehicleGroupGroundObject, unit_type: GroundUnitType
) -> VehicleGroup:
    """
    This generate a group of ground units of given type
    :return: Generated group
    """
    generator = ArmoredGroupGenerator(game, ground_object, unit_type)
    generator.generate()
    return generator.get_generated_group()


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
