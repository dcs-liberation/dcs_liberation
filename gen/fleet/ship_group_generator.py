from __future__ import annotations

import logging
import random
from typing import Optional, TYPE_CHECKING

from dcs.unitgroup import ShipGroup

from game.factions import FACTIONS
from game.theater.theatergroundobject import (
    CarrierGroundObject,
    LhaGroundObject,
    ShipGroundObject,
)
from gen.fleet.carrier_group import CarrierGroupGenerator
from gen.fleet.cn_dd_group import ChineseNavyGroupGenerator, Type54GroupGenerator
from gen.fleet.dd_group import (
    ArleighBurkeGroupGenerator,
    OliverHazardPerryGroupGenerator,
)
from gen.fleet.lacombattanteII import LaCombattanteIIGroupGenerator
from gen.fleet.lha_group import LHAGroupGenerator
from gen.fleet.ru_dd_group import (
    GrishaGroupGenerator,
    KiloSubGroupGenerator,
    MolniyaGroupGenerator,
    RussianNavyGroupGenerator,
    TangoSubGroupGenerator,
)
from gen.fleet.schnellboot import SchnellbootGroupGenerator
from gen.fleet.uboat import UBoatGroupGenerator
from gen.fleet.ww2lst import WW2LSTGroupGenerator

if TYPE_CHECKING:
    from game import Game


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
    "Type54GroupGenerator": Type54GroupGenerator,
    "LaCombattanteIIGroupGenerator": LaCombattanteIIGroupGenerator,
}


def generate_ship_group(
    game: Game, ground_object: ShipGroundObject, faction_name: str
) -> Optional[ShipGroup]:
    """
    This generate a ship group
    :return: The generated group, or None if this faction does not support ships.
    """
    faction = FACTIONS[faction_name]
    if len(faction.navy_generators) > 0:
        gen = random.choice(faction.navy_generators)
        if gen in SHIP_MAP.keys():
            generator = SHIP_MAP[gen](game, ground_object, faction)
            print(generator.position)
            generator.generate()
            return generator.get_generated_group()
        else:
            logging.info(
                "Unable to generate ship group, generator : "
                + str(gen)
                + "does not exists"
            )
    return None


def generate_carrier_group(
    faction: str, game: Game, ground_object: CarrierGroundObject
) -> ShipGroup:
    """Generates a carrier group.

    :param faction: The faction the TGO belongs to.
    :param game: The Game the group is being generated for.
    :param ground_object: The ground object which will own the ship group
    :return: The generated group.
    """
    generator = CarrierGroupGenerator(game, ground_object, FACTIONS[faction])
    generator.generate()
    return generator.get_generated_group()


def generate_lha_group(
    faction: str, game: Game, ground_object: LhaGroundObject
) -> ShipGroup:
    """Generate an LHA group.

    :param faction: The faction the TGO belongs to.
    :param game: The Game the group is being generated for.
    :param ground_object: The ground object which will own the ship group
    :return: The generated group.
    """
    generator = LHAGroupGenerator(game, ground_object, FACTIONS[faction])
    generator.generate()
    return generator.get_generated_group()
