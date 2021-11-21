from collections.abc import Iterator

from game.commander.tasks.primitive.cas import PlanCas
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class FrontLineDefense(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for front_line in state.vulnerable_front_lines:
            yield [PlanCas(front_line)]
