from collections import Iterator

from game.commander.tasks.primitive.barcap import PlanBarcap
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method
from game.theater import ControlPoint


class ProtectAirSpace(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for cp, needed in state.barcaps_needed.items():
            assert isinstance(cp, ControlPoint)
            if needed > 0:
                yield [PlanBarcap(cp)]
