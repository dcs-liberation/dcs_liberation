from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.primitive.strike import PlanStrike
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method
from game.theater import ControlPoint


@dataclass(frozen=True)
class ReduceEnemyFrontLineCapacity(CompoundTask[TheaterState]):
    control_point: ControlPoint

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for ammo_dump in state.ammo_dumps_at(self.control_point):
            yield [PlanStrike(ammo_dump)]
