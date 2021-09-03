from __future__ import annotations

import itertools
from collections import defaultdict
from typing import Sequence, Iterator, TYPE_CHECKING, Optional

from game.dcs.aircrafttype import AircraftType
from gen.flights.ai_flight_planner_db import aircraft_for_task
from gen.flights.closestairfields import ObjectiveDistanceCache
from .squadron import Squadron
from ..theater import ControlPoint, MissionTarget

if TYPE_CHECKING:
    from gen.flights.flight import FlightType


class AirWing:
    def __init__(self, player: bool) -> None:
        self.player = player
        self.squadrons: dict[AircraftType, list[Squadron]] = defaultdict(list)

    def add_squadron(self, squadron: Squadron) -> None:
        self.squadrons[squadron.aircraft].append(squadron)

    def squadrons_for(self, aircraft: AircraftType) -> Sequence[Squadron]:
        return self.squadrons[aircraft]

    def can_auto_plan(self, task: FlightType) -> bool:
        try:
            next(self.auto_assignable_for_task(task))
            return True
        except StopIteration:
            return False

    def best_squadrons_for(
        self, location: MissionTarget, task: FlightType, size: int, this_turn: bool
    ) -> list[Squadron]:
        airfield_cache = ObjectiveDistanceCache.get_closest_airfields(location)
        best_aircraft = aircraft_for_task(task)
        ordered: list[Squadron] = []
        for control_point in airfield_cache.operational_airfields:
            if control_point.captured != self.player:
                continue
            capable_at_base = []
            for squadron in control_point.squadrons:
                if squadron.can_auto_assign_mission(location, task, size, this_turn):
                    capable_at_base.append(squadron)

            ordered.extend(
                sorted(
                    capable_at_base,
                    key=lambda s: best_aircraft.index(s.aircraft),
                )
            )
        return ordered

    def best_squadron_for(
        self, location: MissionTarget, task: FlightType, size: int, this_turn: bool
    ) -> Optional[Squadron]:
        for squadron in self.best_squadrons_for(location, task, size, this_turn):
            return squadron
        return None

    @property
    def available_aircraft_types(self) -> Iterator[AircraftType]:
        for aircraft, squadrons in self.squadrons.items():
            for squadron in squadrons:
                if squadron.untasked_aircraft:
                    yield aircraft
                    break

    def auto_assignable_for_task(self, task: FlightType) -> Iterator[Squadron]:
        for squadron in self.iter_squadrons():
            if squadron.can_auto_assign(task):
                yield squadron

    def auto_assignable_for_task_at(
        self, task: FlightType, base: ControlPoint
    ) -> Iterator[Squadron]:
        for squadron in self.iter_squadrons():
            if squadron.can_auto_assign(task) and squadron.location == base:
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

    def end_turn(self) -> None:
        for squadron in self.iter_squadrons():
            squadron.end_turn()

    def reset(self) -> None:
        for squadron in self.iter_squadrons():
            squadron.return_all_pilots_and_aircraft()

    @property
    def size(self) -> int:
        return sum(len(s) for s in self.squadrons.values())
