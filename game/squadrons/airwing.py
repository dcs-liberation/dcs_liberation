from __future__ import annotations

import itertools
from collections import defaultdict
from typing import Sequence, Iterator, TYPE_CHECKING

from game.dcs.aircrafttype import AircraftType
from gen.flights.flight import FlightType
from .squadron import Squadron
from ..theater import ControlPoint

if TYPE_CHECKING:
    from game import Game


class AirWing:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.squadrons: dict[AircraftType, list[Squadron]] = defaultdict(list)

    def add_squadron(self, squadron: Squadron) -> None:
        squadron.location.squadrons.append(squadron)
        self.squadrons[squadron.aircraft].append(squadron)

    def squadrons_for(self, aircraft: AircraftType) -> Sequence[Squadron]:
        return self.squadrons[aircraft]

    def can_auto_plan(self, task: FlightType) -> bool:
        try:
            next(self.auto_assignable_for_task(task))
            return True
        except StopIteration:
            return False

    def auto_assignable_for_task(self, task: FlightType) -> Iterator[Squadron]:
        for squadron in self.iter_squadrons():
            if squadron.can_auto_assign(task):
                yield squadron

    def auto_assignable_for_task_with_type(
        self, aircraft: AircraftType, task: FlightType, base: ControlPoint
    ) -> Iterator[Squadron]:
        for squadron in self.squadrons_for(aircraft):
            if (
                squadron.location == base
                and squadron.can_auto_assign(task)
                and squadron.has_available_pilots
            ):
                yield squadron

    def squadron_for(self, aircraft: AircraftType) -> Squadron:
        return self.squadrons_for(aircraft)[0]

    def iter_squadrons(self) -> Iterator[Squadron]:
        return itertools.chain.from_iterable(self.squadrons.values())

    def squadron_at_index(self, index: int) -> Squadron:
        return list(self.iter_squadrons())[index]

    def populate_for_turn_0(self) -> None:
        for squadron in self.iter_squadrons():
            squadron.populate_for_turn_0()

    def replenish(self) -> None:
        for squadron in self.iter_squadrons():
            squadron.replenish_lost_pilots()

    def reset(self) -> None:
        for squadron in self.iter_squadrons():
            squadron.return_all_pilots()

    @property
    def size(self) -> int:
        return sum(len(s) for s in self.squadrons.values())
