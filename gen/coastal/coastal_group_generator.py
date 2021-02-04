import logging
import random
from game import db
from gen.coastal.silkworm import SilkwormGenerator

COASTAL_MAP = {
    "SilkwormGenerator": SilkwormGenerator,
}


def generate_coastal_group(game, ground_object, faction_name: str):
    """
    This generate a coastal defenses group
    :return: Nothing, but put the group reference inside the ground object
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
                logging.info("Unable to generate missile group, generator : " + str(gen) + "does not exists")
    return None