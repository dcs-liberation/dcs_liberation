from collections.abc import Iterator

from game.commander.tasks.primitive.aewc import PlanAewc
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class PlanAewcSupport(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for target in state.aewc_targets:
            yield [PlanAewc(target)]
