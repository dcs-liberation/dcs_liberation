from collections.abc import Iterator

from game.commander.tasks.primitive.barcap import PlanBarcap
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class ProtectAirSpace(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for cp, needed in state.barcaps_needed.items():
            if needed > 0:
                yield [PlanBarcap(cp, needed)]
