from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.aewcsupport import PlanAewcSupport
from game.commander.tasks.compound.refuelingsupport import PlanRefuelingSupport
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


@dataclass(frozen=True)
class TheaterSupport(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [PlanAewcSupport()]
        yield [PlanRefuelingSupport()]
