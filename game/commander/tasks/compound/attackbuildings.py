from collections import Iterator

from game.commander.tasks.primitive.strike import PlanStrike
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class AttackBuildings(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for garrison in state.strike_targets:
            yield [PlanStrike(garrison)]
