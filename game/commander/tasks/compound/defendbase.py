from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.primitive.cas import PlanCas
from game.commander.tasks.primitive.defensivestance import DefensiveStance
from game.commander.tasks.primitive.retreatstance import RetreatStance
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method
from game.theater import FrontLine


@dataclass(frozen=True)
class DefendBase(CompoundTask[TheaterState]):
    front_line: FrontLine

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [DefensiveStance(self.front_line, state.context.coalition.player)]
        yield [RetreatStance(self.front_line, state.context.coalition.player)]
        yield [PlanCas(self.front_line)]
