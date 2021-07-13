from __future__ import annotations

import itertools
import operator
from abc import abstractmethod
from dataclasses import dataclass, field
from enum import unique, IntEnum, auto
from typing import TYPE_CHECKING, Optional, Generic, TypeVar, Iterator, Union

from game.commander.missionproposals import ProposedFlight, EscortType, ProposedMission
from game.commander.tasks.theatercommandertask import TheaterCommanderTask
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.profiling import MultiEventTracer
from game.theater import MissionTarget
from game.theater.theatergroundobject import IadsGroundObject, NavalGroundObject
from game.utils import Distance, meters
from gen.flights.flight import FlightType

if TYPE_CHECKING:
    from gen.flights.ai_flight_planner import CoalitionMissionPlanner


MissionTargetT = TypeVar("MissionTargetT", bound=MissionTarget)


@unique
class RangeType(IntEnum):
    Detection = auto()
    Threat = auto()


# TODO: Refactor so that we don't need to call up to the mission planner.
# Bypass type checker due to https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class PackagePlanningTask(TheaterCommanderTask, Generic[MissionTargetT]):
    target: MissionTargetT
    flights: list[ProposedFlight] = field(init=False)

    def __post_init__(self) -> None:
        self.flights = []

    def execute(
        self, mission_planner: CoalitionMissionPlanner, tracer: MultiEventTracer
    ) -> None:
        self.propose_flights(mission_planner.doctrine)
        mission_planner.plan_mission(ProposedMission(self.target, self.flights), tracer)

    @abstractmethod
    def propose_flights(self, doctrine: Doctrine) -> None:
        ...

    def propose_flight(
        self,
        task: FlightType,
        num_aircraft: int,
        max_distance: Optional[Distance],
        escort_type: Optional[EscortType] = None,
    ) -> None:
        if max_distance is None:
            max_distance = Distance.inf()
        self.flights.append(
            ProposedFlight(task, num_aircraft, max_distance, escort_type)
        )

    @property
    def asap(self) -> bool:
        return False

    def propose_common_escorts(self, doctrine: Doctrine) -> None:
        self.propose_flight(
            FlightType.SEAD_ESCORT,
            2,
            doctrine.mission_ranges.offensive,
            EscortType.Sead,
        )

        self.propose_flight(
            FlightType.ESCORT,
            2,
            doctrine.mission_ranges.offensive,
            EscortType.AirToAir,
        )

    def iter_iads_ranges(
        self, state: TheaterState, range_type: RangeType
    ) -> Iterator[Union[IadsGroundObject, NavalGroundObject]]:
        target_ranges: list[
            tuple[Union[IadsGroundObject, NavalGroundObject], Distance]
        ] = []
        all_iads: Iterator[
            Union[IadsGroundObject, NavalGroundObject]
        ] = itertools.chain(state.enemy_air_defenses, state.enemy_ships)
        for target in all_iads:
            distance = meters(target.distance_to(self.target))
            if range_type is RangeType.Detection:
                target_range = target.max_detection_range()
            elif range_type is RangeType.Threat:
                target_range = target.max_threat_range()
            else:
                raise ValueError(f"Unknown RangeType: {range_type}")
            if not target_range:
                continue

            # IADS out of range of our target area will have a positive
            # distance_to_threat and should be pruned. The rest have a decreasing
            # distance_to_threat as overlap increases. The most negative distance has
            # the greatest coverage of the target and should be treated as the highest
            # priority threat.
            distance_to_threat = distance - target_range
            if distance_to_threat > meters(0):
                continue
            target_ranges.append((target, distance_to_threat))

        # TODO: Prioritize IADS by vulnerability?
        target_ranges = sorted(target_ranges, key=operator.itemgetter(1))
        for target, _range in target_ranges:
            yield target

    def iter_detecting_iads(
        self, state: TheaterState
    ) -> Iterator[Union[IadsGroundObject, NavalGroundObject]]:
        return self.iter_iads_ranges(state, RangeType.Detection)

    def iter_iads_threats(
        self, state: TheaterState
    ) -> Iterator[Union[IadsGroundObject, NavalGroundObject]]:
        return self.iter_iads_ranges(state, RangeType.Threat)

    def target_area_preconditions_met(
        self, state: TheaterState, ignore_iads: bool = False
    ) -> bool:
        """Checks if the target area has been cleared of threats."""
        threatened = False

        # Non-blocking, but analyzed so we can pick detectors worth eliminating.
        for detector in self.iter_detecting_iads(state):
            if detector not in state.detecting_air_defenses:
                state.detecting_air_defenses.append(detector)

        if not ignore_iads:
            for iads_threat in self.iter_iads_threats(state):
                threatened = True
                if iads_threat not in state.threatening_air_defenses:
                    state.threatening_air_defenses.append(iads_threat)
        return not threatened
