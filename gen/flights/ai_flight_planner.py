from __future__ import annotations

import logging
import operator
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Set, TYPE_CHECKING, Tuple

from dcs.unittype import UnitType

from game import db
from game.data.radar_db import UNITS_WITH_RADAR
from game.infos.information import Information
from game.utils import nm_to_meter
from gen import Conflict
from gen.ato import Package
from gen.flights.ai_flight_planner_db import (
    CAP_CAPABLE,
    CAS_CAPABLE,
    SEAD_CAPABLE,
    STRIKE_CAPABLE,
)
from gen.flights.flight import (
    Flight,
    FlightType,
)
from gen.flights.flightplan import FlightPlanBuilder
from theater import (
    ControlPoint,
    FrontLine,
    MissionTarget,
    TheaterGroundObject,
)

# Avoid importing some types that cause circular imports unless type checking.
if TYPE_CHECKING:
    from game import Game
    from game.inventory import GlobalAircraftInventory


class ClosestAirfields:
    """Precalculates which control points are closes to the given target."""

    def __init__(self, target: MissionTarget,
                 all_control_points: List[ControlPoint]) -> None:
        self.target = target
        self.closest_airfields: List[ControlPoint] = sorted(
            all_control_points, key=lambda c: self.target.distance_to(c)
        )

    def airfields_within(self, meters: int) -> Iterator[ControlPoint]:
        """Iterates over all airfields within the given range of the target.

        Note that this iterates over *all* airfields, not just friendly
        airfields.
        """
        for cp in self.closest_airfields:
            if cp.distance_to(self.target) < meters:
                yield cp
            else:
                break


@dataclass(frozen=True)
class ProposedFlight:
    """A flight outline proposed by the mission planner.

    Proposed flights haven't been assigned specific aircraft yet. They have only
    a task, a required number of aircraft, and a maximum distance allowed
    between the objective and the departure airfield.
    """

    #: The flight's role.
    task: FlightType

    #: The number of aircraft required.
    num_aircraft: int

    #: The maximum distance between the objective and the departure airfield.
    max_distance: int

    def __str__(self) -> str:
        return f"{self.task.name} {self.num_aircraft} ship"


@dataclass(frozen=True)
class ProposedMission:
    """A mission outline proposed by the mission planner.

    Proposed missions haven't been assigned aircraft yet. They have only an
    objective location and a list of proposed flights that are required for the
    mission.
    """

    #: The mission objective.
    location: MissionTarget

    #: The proposed flights that are required for the mission.
    flights: List[ProposedFlight]

    def __str__(self) -> str:
        flights = ', '.join([str(f) for f in self.flights])
        return f"{self.location.name}: {flights}"


class AircraftAllocator:
    """Finds suitable aircraft for proposed missions."""

    def __init__(self, closest_airfields: ClosestAirfields,
                 global_inventory: GlobalAircraftInventory,
                 is_player: bool) -> None:
        self.closest_airfields = closest_airfields
        self.global_inventory = global_inventory
        self.is_player = is_player

    def find_aircraft_for_flight(
            self, flight: ProposedFlight
    ) -> Optional[Tuple[ControlPoint, UnitType]]:
        """Finds aircraft suitable for the given mission.

        Searches for aircraft capable of performing the given mission within the
        maximum allowed range. If insufficient aircraft are available for the
        mission, None is returned.

        Note that aircraft *will* be removed from the global inventory on
        success. This is to ensure that the same aircraft are not matched twice
        on subsequent calls. If the found aircraft are not used, the caller is
        responsible for returning them to the inventory.
        """
        cap_missions = (FlightType.BARCAP, FlightType.CAP, FlightType.TARCAP)
        if flight.task in cap_missions:
            types = CAP_CAPABLE
        elif flight.task == FlightType.CAS:
            types = CAS_CAPABLE
        elif flight.task in (FlightType.DEAD, FlightType.SEAD):
            types = SEAD_CAPABLE
        elif flight.task == FlightType.STRIKE:
            types = STRIKE_CAPABLE
        else:
            logging.error(f"Unplannable flight type: {flight.task}")
            return None

        # TODO: Implement mission type weighting for aircraft.
        # We should avoid assigning F/A-18s to CAP missions when there are F-15s
        # available, since the F/A-18 is capable of performing other tasks that
        # the F-15 is not capable of.
        airfields_in_range = self.closest_airfields.airfields_within(
            flight.max_distance
        )
        for airfield in airfields_in_range:
            if not airfield.is_friendly(self.is_player):
                continue
            inventory = self.global_inventory.for_control_point(airfield)
            for aircraft, available in inventory.all_aircraft:
                if aircraft in types and available >= flight.num_aircraft:
                    inventory.remove_aircraft(aircraft, flight.num_aircraft)
                    return airfield, aircraft

        return None


class PackageBuilder:
    """Builds a Package for the flights it receives."""

    def __init__(self, location: MissionTarget,
                 closest_airfields: ClosestAirfields,
                 global_inventory: GlobalAircraftInventory,
                 is_player: bool) -> None:
        self.package = Package(location)
        self.allocator = AircraftAllocator(closest_airfields, global_inventory,
                                           is_player)
        self.global_inventory = global_inventory

    def plan_flight(self, plan: ProposedFlight) -> bool:
        """Allocates aircraft for the given flight and adds them to the package.

        If no suitable aircraft are available, False is returned. If the failed
        flight was critical and the rest of the mission will be scrubbed, the
        caller should return any previously planned flights to the inventory
        using release_planned_aircraft.
        """
        assignment = self.allocator.find_aircraft_for_flight(plan)
        if assignment is None:
            return False
        airfield, aircraft = assignment
        flight = Flight(aircraft, plan.num_aircraft, airfield, plan.task)
        self.package.add_flight(flight)
        return True

    def build(self) -> Package:
        """Returns the built package."""
        return self.package

    def release_planned_aircraft(self) -> None:
        """Returns any planned flights to the inventory."""
        flights = list(self.package.flights)
        for flight in flights:
            self.global_inventory.return_from_flight(flight)
            self.package.remove_flight(flight)


class ObjectiveFinder:
    """Identifies potential objectives for the mission planner."""

    # TODO: Merge into doctrine.
    AIRFIELD_THREAT_RANGE = nm_to_meter(150)
    SAM_THREAT_RANGE = nm_to_meter(100)

    def __init__(self, game: Game, is_player: bool) -> None:
        self.game = game
        self.is_player = is_player
        # TODO: Cache globally at startup to avoid generating twice per turn?
        self.closest_airfields: Dict[str, ClosestAirfields] = {
            t.name: ClosestAirfields(t, self.game.theater.controlpoints)
            for t in self.all_possible_targets()
        }

    def enemy_sams(self) -> Iterator[TheaterGroundObject]:
        """Iterates over all enemy SAM sites."""
        # Control points might have the same ground object several times, for
        # some reason.
        found_targets: Set[str] = set()
        for cp in self.enemy_control_points():
            for ground_object in cp.ground_objects:
                if ground_object.name in found_targets:
                    continue

                if ground_object.dcs_identifier != "AA":
                    continue

                if not self.object_has_radar(ground_object):
                    continue

                # TODO: Yield in order of most threatening.
                # Need to sort in order of how close their defensive range comes
                # to friendly assets. To do that we need to add effective range
                # information to the database.
                yield ground_object
                found_targets.add(ground_object.name)

    def threatening_sams(self) -> Iterator[TheaterGroundObject]:
        """Iterates over enemy SAMs in threat range of friendly control points.

        SAM sites are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        sams: List[Tuple[TheaterGroundObject, int]] = []
        for sam in self.enemy_sams():
            ranges: List[int] = []
            for cp in self.friendly_control_points():
                ranges.append(sam.distance_to(cp))
            sams.append((sam, min(ranges)))

        sams = sorted(sams, key=operator.itemgetter(1))
        for sam, _range in sams:
            yield sam

    def strike_targets(self) -> Iterator[TheaterGroundObject]:
        """Iterates over enemy strike targets.

        Targets are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        targets: List[Tuple[TheaterGroundObject, int]] = []
        # Control points might have the same ground object several times, for
        # some reason.
        found_targets: Set[str] = set()
        for enemy_cp in self.enemy_control_points():
            for ground_object in enemy_cp.ground_objects:
                if ground_object.name in found_targets:
                    continue
                ranges: List[int] = []
                for friendly_cp in self.friendly_control_points():
                    ranges.append(ground_object.distance_to(friendly_cp))
                targets.append((ground_object, min(ranges)))
                found_targets.add(ground_object.name)
        targets = sorted(targets, key=operator.itemgetter(1))
        for target, _range in targets:
            yield target

    @staticmethod
    def object_has_radar(ground_object: TheaterGroundObject) -> bool:
        """Returns True if the ground object contains a unit with radar."""
        for group in ground_object.groups:
            for unit in group.units:
                if db.unit_type_from_name(unit.type) in UNITS_WITH_RADAR:
                    return True
        return False

    def front_lines(self) -> Iterator[FrontLine]:
        """Iterates over all active front lines in the theater."""
        for cp in self.friendly_control_points():
            for connected in cp.connected_points:
                if connected.is_friendly(self.is_player):
                    continue

                if Conflict.has_frontline_between(cp, connected):
                    yield FrontLine(cp, connected)

    def vulnerable_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over friendly CPs that are vulnerable to enemy CPs.

        Vulnerability is defined as any enemy CP within threat range of of the
        CP.
        """
        for cp in self.friendly_control_points():
            airfields_in_proximity = self.closest_airfields[cp.name]
            airfields_in_threat_range = airfields_in_proximity.airfields_within(
                self.AIRFIELD_THREAT_RANGE
            )
            for airfield in airfields_in_threat_range:
                if not airfield.is_friendly(self.is_player):
                    yield cp
                    break

    def friendly_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over all friendly control points."""
        return (c for c in self.game.theater.controlpoints if
                c.is_friendly(self.is_player))

    def enemy_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over all enemy control points."""
        return (c for c in self.game.theater.controlpoints if
                not c.is_friendly(self.is_player))

    def all_possible_targets(self) -> Iterator[MissionTarget]:
        """Iterates over all possible mission targets in the theater.

        Valid mission targets are control points (airfields and carriers), front
        lines, and ground objects (SAM sites, factories, resource extraction
        sites, etc).
        """
        for cp in self.game.theater.controlpoints:
            yield cp
            yield from cp.ground_objects
        yield from self.front_lines()

    def closest_airfields_to(self, location: MissionTarget) -> ClosestAirfields:
        """Returns the closest airfields to the given location."""
        return self.closest_airfields[location.name]


class CoalitionMissionPlanner:
    """Coalition flight planning AI.

    This class is responsible for automatically planning missions for the
    coalition at the start of the turn.

    The primary goal of the mission planner is to protect existing friendly
    assets. Missions will be planned with the following priorities:

    1. CAP for airfields/fleets in close proximity to the enemy to prevent heavy
       losses of friendly aircraft.
    2. CAP for front line areas to protect ground and CAS units.
    3. DEAD to reduce necessity of SEAD for future missions.
    4. CAS to protect friendly ground units.
    5. Strike missions to reduce the enemy's resources.

    TODO: Anti-ship and airfield strikes to reduce enemy sortie rates.
    TODO: BAI to prevent enemy forces from reaching the front line.
    TODO: Should fleets always have a CAP?

    TODO: Stance and doctrine-specific planning behavior.
    """

    # TODO: Merge into doctrine, also limit by aircraft.
    MAX_CAP_RANGE = nm_to_meter(100)
    MAX_CAS_RANGE = nm_to_meter(50)
    MAX_SEAD_RANGE = nm_to_meter(150)
    MAX_STRIKE_RANGE = nm_to_meter(150)

    def __init__(self, game: Game, is_player: bool) -> None:
        self.game = game
        self.is_player = is_player
        self.objective_finder = ObjectiveFinder(self.game, self.is_player)
        self.ato = self.game.blue_ato if is_player else self.game.red_ato

    def propose_missions(self) -> Iterator[ProposedMission]:
        """Identifies and iterates over potential mission in priority order."""
        # Find friendly CPs within 100 nmi from an enemy airfield, plan CAP.
        for cp in self.objective_finder.vulnerable_control_points():
            yield ProposedMission(cp, [
                ProposedFlight(FlightType.CAP, 2, self.MAX_CAP_RANGE),
            ])

        # Find front lines, plan CAP.
        for front_line in self.objective_finder.front_lines():
            yield ProposedMission(front_line, [
                ProposedFlight(FlightType.TARCAP, 2, self.MAX_CAP_RANGE),
                ProposedFlight(FlightType.CAS, 2, self.MAX_CAS_RANGE),
            ])

        # Find enemy SAM sites with ranges that cover friendly CPs, front lines,
        # or objects, plan DEAD.
        # Find enemy SAM sites with ranges that extend to within 50 nmi of
        # friendly CPs, front, lines, or objects, plan DEAD.
        for sam in self.objective_finder.threatening_sams():
            yield ProposedMission(sam, [
                ProposedFlight(FlightType.DEAD, 2, self.MAX_SEAD_RANGE),
                # TODO: Max escort range.
                ProposedFlight(FlightType.CAP, 2, self.MAX_SEAD_RANGE),
            ])

        # Plan strike missions.
        for target in self.objective_finder.strike_targets():
            yield ProposedMission(target, [
                ProposedFlight(FlightType.STRIKE, 2, self.MAX_STRIKE_RANGE),
                # TODO: Max escort range.
                ProposedFlight(FlightType.SEAD, 2, self.MAX_STRIKE_RANGE),
                ProposedFlight(FlightType.CAP, 2, self.MAX_STRIKE_RANGE),
            ])

    def plan_missions(self) -> None:
        """Identifies and plans mission for the turn."""
        for proposed_mission in self.propose_missions():
            self.plan_mission(proposed_mission)

        for cp in self.objective_finder.friendly_control_points():
            inventory = self.game.aircraft_inventory.for_control_point(cp)
            for aircraft, available in inventory.all_aircraft:
                self.message("Unused aircraft",
                             f"{available} {aircraft.id} from {cp}")

    def plan_mission(self, mission: ProposedMission) -> None:
        """Allocates aircraft for a proposed mission and adds it to the ATO."""
        builder = PackageBuilder(
            mission.location,
            self.objective_finder.closest_airfields_to(mission.location),
            self.game.aircraft_inventory,
            self.is_player
        )
        for flight in mission.flights:
            if not builder.plan_flight(flight):
                builder.release_planned_aircraft()
                self.message("Insufficient aircraft",
                             f"Not enough aircraft in range for {mission}")
                return

        package = builder.build()
        for flight in package.flights:
            builder = FlightPlanBuilder(self.game, self.is_player)
            builder.populate_flight_plan(flight, package.target)
        self.ato.add_package(package)

    def message(self, title, text) -> None:
        """Emits a planning message to the player.

        If the mission planner belongs to the players coalition, this emits a
        message to the info panel.
        """
        if self.is_player:
            self.game.informations.append(
                Information(title, text, self.game.turn)
            )
        else:
            logging.info(f"{title}: {text}")
