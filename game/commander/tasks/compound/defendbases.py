from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.defendbase import DefendBase
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


@dataclass(frozen=True)
class DefendBases(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for front in state.active_front_lines:
            yield [DefendBase(front)]
