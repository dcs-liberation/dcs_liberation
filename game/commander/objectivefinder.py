from __future__ import annotations

import math
import operator
from collections import Iterator, Iterable
from typing import TypeVar, TYPE_CHECKING, Tuple

from game.theater import (
    ControlPoint,
    OffMapSpawn,
    MissionTarget,
    Fob,
    FrontLine,
    Airfield,
)
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    IadsGroundObject,
    NavalGroundObject,
)
from game.utils import meters, nautical_miles
from gen.flights.closestairfields import ObjectiveDistanceCache, ClosestAirfields
from gen.flights.flight import FlightType

if TYPE_CHECKING:
    from game import Game
    from game.transfers import CargoShip, Convoy

MissionTargetType = TypeVar("MissionTargetType", bound=MissionTarget)


class ObjectiveFinder:
    """Identifies potential objectives for the mission planner."""

    # TODO: Merge into doctrine.
    AIRFIELD_THREAT_RANGE = nautical_miles(150)
    SAM_THREAT_RANGE = nautical_miles(100)

    def __init__(self, game: Game, is_player: bool) -> None:
        self.game = game
        self.is_player = is_player

    def enemy_air_defenses(self) -> Iterator[IadsGroundObject]:
        """Iterates over all enemy SAM sites."""
        for cp in self.enemy_control_points():
            for ground_object in cp.ground_objects:
                if ground_object.is_dead:
                    continue

                if isinstance(ground_object, IadsGroundObject):
                    # Check if already SEAD, SEAD_ESCORT or DEAD was planned
                    if not (
                        self.rounds_to_plan_for(ground_object, FlightType.SEAD) > 0
                        and self.rounds_to_plan_for(
                            ground_object, FlightType.SEAD_ESCORT
                        )
                        > 0
                        and self.rounds_to_plan_for(ground_object, FlightType.DEAD) > 0
                    ):
                        continue
                    yield ground_object

    def enemy_ships(self) -> Iterator[NavalGroundObject]:
        for cp in self.enemy_control_points():
            for ground_object in cp.ground_objects:
                if not isinstance(ground_object, NavalGroundObject):
                    continue

                if ground_object.is_dead:
                    continue
                if self.rounds_to_plan_for(ground_object, FlightType.ANTISHIP) > 0:
                    yield ground_object

    def threatening_ships(self) -> Iterator[NavalGroundObject]:
        """Iterates over enemy ships near friendly control points.

        Groups are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        return self._targets_by_range(self.enemy_ships())

    def _targets_by_range(
        self, targets: Iterable[MissionTargetType]
    ) -> Iterator[MissionTargetType]:
        target_ranges: list[tuple[MissionTargetType, float]] = []
        for target in targets:
            ranges: list[float] = []
            for cp in self.friendly_control_points():
                ranges.append(target.distance_to(cp))
            target_ranges.append((target, min(ranges)))

        target_ranges = sorted(target_ranges, key=operator.itemgetter(1))
        for target, _range in target_ranges:
            yield target

    def strike_targets(self) -> Iterator[BuildingGroundObject]:
        """Iterates over enemy strike targets.

        Targets are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        targets: list[tuple[BuildingGroundObject, float]] = []
        # Building objectives are made of several individual TGOs (one per
        # building).
        found_targets: set[str] = set()
        for enemy_cp in self.enemy_control_points():
            for ground_object in enemy_cp.ground_objects:
                # TODO: Reuse ground_object.mission_types.
                # The mission types for ground objects are currently not
                # accurate because we include things like strike and BAI for all
                # targets since they have different planning behavior (waypoint
                # generation is better for players with strike when the targets
                # are stationary, AI behavior against weaker air defenses is
                # better with BAI), so that's not a useful filter. Once we have
                # better control over planning profiles and target dependent
                # loadouts we can clean this up.
                if not isinstance(ground_object, BuildingGroundObject):
                    # Other group types (like ships, SAMs, garrisons, etc) have better
                    # suited mission types like anti-ship, DEAD, and BAI.
                    continue

                if isinstance(enemy_cp, Fob) and ground_object.is_control_point:
                    # This is the FOB structure itself. Can't be repaired or
                    # targeted by the player, so shouldn't be targetable by the
                    # AI.
                    continue

                if ground_object.is_dead:
                    continue
                if ground_object.name in found_targets:
                    continue
                ranges: list[float] = []
                for friendly_cp in self.friendly_control_points():
                    ranges.append(ground_object.distance_to(friendly_cp))
                targets.append((ground_object, min(ranges)))
                found_targets.add(ground_object.name)
        targets = sorted(targets, key=operator.itemgetter(1))
        for target, _range in targets:
            yield target

    def front_lines(self) -> Iterator[FrontLine]:
        """Iterates over all active front lines in the theater."""
        yield from self.game.theater.conflicts()

    def vulnerable_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over friendly CPs that are vulnerable to enemy CPs.

        Vulnerability is defined as any enemy CP within threat range of of the
        CP.
        """
        for cp in self.friendly_control_points():
            if isinstance(cp, OffMapSpawn):
                # Off-map spawn locations don't need protection.
                continue
            airfields_in_proximity = self.closest_airfields_to(cp)
            airfields_in_threat_range = (
                airfields_in_proximity.operational_airfields_within(
                    self.AIRFIELD_THREAT_RANGE
                )
            )
            for airfield in airfields_in_threat_range:
                if not airfield.is_friendly(self.is_player):
                    yield cp
                    break

    def oca_targets(self, min_aircraft: int) -> Iterator[ControlPoint]:
        airfields = []
        for control_point in self.enemy_control_points():
            if not isinstance(control_point, Airfield):
                continue
            if control_point.base.total_aircraft >= min_aircraft:
                airfields.append(control_point)
        return self._targets_by_range(airfields)

    def convoys(self) -> Iterator[Convoy]:
        for front_line in self.front_lines():
            for convoy in self.game.coalition_for(
                self.is_player
            ).transfers.convoys.travelling_to(
                front_line.control_point_hostile_to(self.is_player)
            ):
                if self.rounds_to_plan_for(convoy, FlightType.BAI) > 0:
                    yield convoy

    def cargo_ships(self) -> Iterator[CargoShip]:
        for front_line in self.front_lines():
            for cargo_ship in self.game.coalition_for(
                self.is_player
            ).transfers.cargo_ships.travelling_to(
                front_line.control_point_hostile_to(self.is_player)
            ):
                if self.rounds_to_plan_for(cargo_ship, FlightType.ANTISHIP) > 0:
                    yield cargo_ship

    def friendly_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over all friendly control points."""
        return (
            c for c in self.game.theater.controlpoints if c.is_friendly(self.is_player)
        )

    def farthest_friendly_control_point(self) -> ControlPoint:
        """Finds the friendly control point that is farthest from any threats."""
        threat_zones = self.game.threat_zone_for(not self.is_player)

        farthest = None
        max_distance = meters(0)
        for cp in self.friendly_control_points():
            if isinstance(cp, OffMapSpawn):
                continue
            distance = threat_zones.distance_to_threat(cp.position)
            if distance > max_distance:
                farthest = cp
                max_distance = distance

        if farthest is None:
            raise RuntimeError("Found no friendly control points. You probably lost.")
        return farthest

    def closest_friendly_control_point(self) -> ControlPoint:
        """Finds the friendly control point that is closest to any threats."""
        threat_zones = self.game.threat_zone_for(not self.is_player)

        closest = None
        min_distance = meters(math.inf)
        for cp in self.friendly_control_points():
            if isinstance(cp, OffMapSpawn):
                continue
            distance = threat_zones.distance_to_threat(cp.position)
            if distance < min_distance:
                closest = cp
                min_distance = distance

        if closest is None:
            raise RuntimeError("Found no friendly control points. You probably lost.")
        return closest

    def enemy_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over all enemy control points."""
        return (
            c
            for c in self.game.theater.controlpoints
            if not c.is_friendly(self.is_player)
        )

    def prioritized_unisolated_points(self) -> list[ControlPoint]:
        prioritized = []
        capturable_later = []
        for cp in self.game.theater.control_points_for(not self.is_player):
            if cp.is_isolated:
                continue
            if cp.has_active_frontline:
                prioritized.append(cp)
            else:
                capturable_later.append(cp)
        prioritized.extend(self._targets_by_range(capturable_later))
        return prioritized

    @staticmethod
    def closest_airfields_to(location: MissionTarget) -> ClosestAirfields:
        """Returns the closest airfields to the given location."""
        return ObjectiveDistanceCache.get_closest_airfields(location)

    def for_flight_type(
        self, flight_type: FlightType, rounds_requested: int = 1
    ) -> Iterator[Tuple[MissionTarget, int]]:
        mission_target: list[MissionTarget] = []
        if FlightType.AEWC == flight_type:
            # Return only the first found cp
            mission_target = [self.farthest_friendly_control_point()]
        elif FlightType.REFUELING == flight_type:
            # Return only the first found cp
            mission_target = [self.closest_friendly_control_point()]
        elif FlightType.BARCAP == flight_type:
            mission_target = list(self.vulnerable_control_points())
        elif FlightType.CAS == flight_type:
            mission_target = list(self.front_lines())

        for target in mission_target:
            yield target, self.rounds_to_plan_for(target, flight_type, rounds_requested)

        return None

    def targets_for_flight_type(
        self, flight_type: FlightType, rounds_requested: int = 1
    ) -> list[MissionTarget]:
        return list(
            target
            for target, rounds in self.for_flight_type(flight_type, rounds_requested)
            if rounds > 0
        )

    def rounds_to_plan_for(
        self, objective: MissionTarget, task: FlightType, rounds_requested: int = 1
    ) -> int:
        """Checks if the objective is already addressed and more should be planned"""
        # Refueling and AEWC should only be planned once, independent of the target cp
        already_assigned = sum(
            (
                task in (FlightType.AEWC, FlightType.REFUELING)
                or package.target == objective
            )
            and package.primary_task == task
            for package in self.game.coalition_for(self.is_player).ato.packages
        )
        return rounds_requested - already_assigned
