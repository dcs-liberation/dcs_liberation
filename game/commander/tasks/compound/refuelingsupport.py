from collections.abc import Iterator

from game.commander.tasks.primitive.refueling import PlanRefueling
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class PlanRefuelingSupport(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for target in state.refueling_targets:
            yield [PlanRefueling(target)]
