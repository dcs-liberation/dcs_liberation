from __future__ import annotations

import itertools
import operator
from abc import abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum, auto, unique
from typing import Generic, Iterator, Optional, TYPE_CHECKING, TypeVar, Union

from game.ato.flighttype import FlightType
from game.ato.package import Package
from game.commander.missionproposals import EscortType, ProposedFlight, ProposedMission
from game.commander.packagefulfiller import PackageFulfiller
from game.commander.tasks.theatercommandertask import TheaterCommanderTask
from game.commander.theaterstate import TheaterState
from game.settings import AutoAtoBehavior
from game.theater import MissionTarget
from game.theater.theatergroundobject import IadsGroundObject, NavalGroundObject
from game.utils import Distance, meters

if TYPE_CHECKING:
    from game.coalition import Coalition

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
    package: Optional[Package] = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.flights = []

    def preconditions_met(self, state: TheaterState) -> bool:
        if (
            state.context.coalition.player
            and state.context.settings.auto_ato_behavior is AutoAtoBehavior.Disabled
        ):
            return False
        return self.fulfill_mission(state)

    def execute(self, coalition: Coalition) -> None:
        if self.package is None:
            raise RuntimeError("Attempted to execute failed package planning task")
        coalition.ato.add_package(self.package)

    @abstractmethod
    def propose_flights(self) -> None:
        ...

    def propose_flight(
        self,
        task: FlightType,
        num_aircraft: int,
        escort_type: Optional[EscortType] = None,
    ) -> None:
        self.flights.append(ProposedFlight(task, num_aircraft, escort_type))

    @property
    def asap(self) -> bool:
        return False

    @property
    def purchase_multiplier(self) -> int:
        """The multiplier for aircraft quantity when missions could not be fulfilled.

        For missions that do not schedule in rounds like BARCAPs do, this should be one
        to ensure that the we only purchase enough aircraft to plan the mission once.

        For missions that repeat within the same turn, however, we may need to buy for
        the same mission more than once. If three rounds of BARCAP still need to be
        fulfilled, this would return 3, and we'd triplicate the purchase order.

        There is a small misbehavior here that's not symptomatic for our current mission
        planning: multi-round, multi-flight packages will only purchase multiple sets of
        aircraft for whatever is unavailable for the *first* failed package. For
        example, if we extend this to CAS and have no CAS aircraft but enough TARCAP
        aircraft for one round, we'll order CAS for every round but will not order any
        TARCAP aircraft, since we can't know that TARCAP aircraft are needed until we
        attempt to plan the second mission *without returning the first round aircraft*.
        """
        return 1

    def fulfill_mission(self, state: TheaterState) -> bool:
        color = "blue" if state.context.coalition.player else "red"
        self.propose_flights()
        fulfiller = PackageFulfiller(
            state.context.coalition,
            state.context.theater,
            state.context.game_db.flights,
            state.context.settings,
        )
        with state.context.tracer.trace(f"{color} {self.flights[0].task} planning"):
            self.package = fulfiller.plan_mission(
                ProposedMission(self.target, self.flights),
                self.purchase_multiplier,
                state.context.tracer,
            )
        return self.package is not None

    def propose_common_escorts(self) -> None:
        self.propose_flight(FlightType.SEAD_ESCORT, 2, EscortType.Sead)
        self.propose_flight(FlightType.ESCORT, 2, EscortType.AirToAir)

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
