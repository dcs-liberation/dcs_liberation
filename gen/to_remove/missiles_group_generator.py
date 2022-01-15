import logging
import random
from typing import Optional

from dcs.unitgroup import VehicleGroup

from game import db, Game
from game.theater.theatergroundobject import MissileSiteGroundObject
from gen.to_remove.scud_site import ScudGenerator
from gen.to_remove.v1_group import V1GroupGenerator

MISSILES_MAP = {"V1GroupGenerator": V1GroupGenerator, "ScudGenerator": ScudGenerator}


def generate_missile_group(
    game: Game, ground_object: MissileSiteGroundObject, faction_name: str
) -> Optional[VehicleGroup]:
    """
    This generate a missiles group
    :return: Nothing, but put the group reference inside the ground object
    """
    faction = db.FACTIONS[faction_name]
    if len(faction.missiles) > 0:
        generators = faction.missiles
        if len(generators) > 0:
            gen = random.choice(generators)
            if gen in MISSILES_MAP.keys():
                generator = MISSILES_MAP[gen](game, ground_object, faction)
                generator.generate()
                return generator.get_generated_group()
            else:
                logging.info(
                    "Unable to generate missile group, generator : "
                    + str(gen)
                    + "does not exists"
                )
    return None
