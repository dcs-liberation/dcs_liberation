from abc import ABC, abstractmethod
from enum import Enum

from game import Game
from gen.sam.group_generator import GroupGenerator
from game.theater.theatergroundobject import SamGroundObject


class AirDefenseRange(Enum):
    Short = "short"
    Medium = "medium"
    Long = "long"


class AirDefenseGroupGenerator(GroupGenerator, ABC):
    """
    This is the base for all SAM group generators
    """

    def __init__(self, game: Game, ground_object: SamGroundObject) -> None:
        ground_object.skynet_capable = True
        super().__init__(game, ground_object)

    @classmethod
    @abstractmethod
    def range(cls) -> AirDefenseRange:
        ...
