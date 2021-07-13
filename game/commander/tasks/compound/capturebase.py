from collections import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.destroyenemygroundunits import (
    DestroyEnemyGroundUnits,
)
from game.commander.tasks.primitive.breakthroughattack import BreakthroughAttack
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method
from game.theater import FrontLine


@dataclass(frozen=True)
class CaptureBase(CompoundTask[TheaterState]):
    front_line: FrontLine

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [BreakthroughAttack(self.front_line, state.player)]
        yield [DestroyEnemyGroundUnits(self.front_line)]
