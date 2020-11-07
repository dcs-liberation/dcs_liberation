from abc import ABC

from game import Game
from gen.sam.group_generator import GroupGenerator
from theater.theatergroundobject import SamGroundObject


class GenericSamGroupGenerator(GroupGenerator, ABC):
    """
    This is the base for all SAM group generators
    """

    def __init__(self, game: Game, ground_object: SamGroundObject) -> None:
        ground_object.skynet_capable = True
        super().__init__(game, ground_object)
