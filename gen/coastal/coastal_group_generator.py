import logging
import random
from typing import Optional

from dcs.unitgroup import VehicleGroup

from game import db, Game
from game.theater.theatergroundobject import CoastalSiteGroundObject
from gen.coastal.silkworm import SilkwormGenerator

COASTAL_MAP = {
    "SilkwormGenerator": SilkwormGenerator,
}


def generate_coastal_group(
    game: Game, ground_object: CoastalSiteGroundObject, faction_name: str
) -> Optional[VehicleGroup]:
    """
    This generate a coastal defenses group
    :return: The generated group, or None if this faction does not support coastal
    defenses.
    """
    faction = db.FACTIONS[faction_name]
    if len(faction.coastal_defenses) > 0:
        generators = faction.coastal_defenses
        if len(generators) > 0:
            gen = random.choice(generators)
            if gen in COASTAL_MAP.keys():
                generator = COASTAL_MAP[gen](game, ground_object, faction)
                generator.generate()
                return generator.get_generated_group()
            else:
                logging.info(
                    "Unable to generate missile group, generator : "
                    + str(gen)
                    + "does not exists"
                )
    return None
