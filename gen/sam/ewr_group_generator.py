import random
from typing import Dict, Iterable, List, Optional, Sequence, Set, Type

from game import Game
from game.factions.faction import Faction
from game.theater import TheaterGroundObject
from game.theater.theatergroundobject import EwrGroundObject

from gen.sam.airdefensegroupgenerator import AirDefenseGroupGenerator

from dcs.unitgroup import VehicleGroup

from gen.sam.ewrs import (
    BigBirdGenerator,
    BoxSpringGenerator,
    DogEarGenerator,
    FlatFaceGenerator,
    HawkEwrGenerator,
    PatriotEwrGenerator,
    RolandEwrGenerator,
    SnowDriftGenerator,
    StraightFlushGenerator,
    TallRackGenerator,
)

EWR_MAP = {
    "BoxSpringGenerator": BoxSpringGenerator,
    "TallRackGenerator": TallRackGenerator,
    "DogEarGenerator": DogEarGenerator,
    "RolandEwrGenerator": RolandEwrGenerator,
    "FlatFaceGenerator": FlatFaceGenerator,
    "PatriotEwrGenerator": PatriotEwrGenerator,
    "BigBirdGenerator": BigBirdGenerator,
    "SnowDriftGenerator": SnowDriftGenerator,
    "StraightFlushGenerator": StraightFlushGenerator,
    "HawkEwrGenerator": HawkEwrGenerator,
}


def get_faction_possible_ewrs_generator(
    faction: Faction,
) -> List[Type[AirDefenseGroupGenerator]]:
    """
    Return the list of possible EWR generators for the given faction
    :param faction: Faction name to search units for
    """
    return [EWR_MAP[s] for s in faction.ewrs]


def generate_ewr_group(
    game: Game, ground_object: EwrGroundObject, faction: Faction
) -> List[VehicleGroup]:
    """Generates an early warning radar group.

    :param game: The Game.
    :param ground_object: The ground object which will own the EWR group.
    :param faction: Owner faction.
    :return: The generated group, or None if one could not be generated.
    """
    generators = get_faction_possible_ewrs_generator(faction)
    if len(generators) > 0:
        generator_class = random.choice(generators)
        generator = generator_class(game, ground_object)
        generator.generate()
        return list(generator.get_generated_group())
    return []
