import logging
import random
from game import db
from gen.missiles.scud_site import ScudGenerator
from gen.missiles.v1_group import V1GroupGenerator

MISSILES_MAP = {
    "V1GroupGenerator": V1GroupGenerator,
    "ScudGenerator": ScudGenerator
}


def generate_missile_group(game, ground_object, faction_name: str):
    """
    This generate a ship group
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
                logging.info("Unable to generate missile group, generator : " + str(gen) + "does not exists")
    return None