from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.capturebase import CaptureBase
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


@dataclass(frozen=True)
class CaptureBases(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for front in state.active_front_lines:
            yield [CaptureBase(front)]
