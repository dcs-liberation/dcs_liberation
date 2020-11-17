from __future__ import annotations

import logging
import operator
import random
from dataclasses import dataclass
from datetime import timedelta
from typing import Iterator, List, Optional, Set, TYPE_CHECKING, Tuple, Type

from dcs.unittype import FlyingType, UnitType

from game import db
from game.data.radar_db import UNITS_WITH_RADAR
from game.infos.information import Information
from game.utils import nm_to_meter
from gen import Conflict
from gen.ato import Package
from gen.flights.ai_flight_planner_db import (
    CAP_CAPABLE,
    CAP_PREFERRED,
    CAS_CAPABLE,
    CAS_PREFERRED,
    SEAD_CAPABLE,
    SEAD_PREFERRED,
    STRIKE_CAPABLE,
    STRIKE_PREFERRED,
)
from gen.flights.closestairfields import (
    ClosestAirfields,
    ObjectiveDistanceCache,
)
from gen.flights.flight import (
    Flight,
    FlightType,
)
from gen.flights.flightplan import FlightPlanBuilder
from gen.flights.traveltime import TotEstimator
from theater import (
    ControlPoint,
    FrontLine,
    MissionTarget,
    TheaterGroundObject,
    SamGroundObject,
)

# Avoid importing some types that cause circular imports unless type checking.
from theater.theatergroundobject import (
    EwrGroundObject,
    VehicleGroupGroundObject,
)

if TYPE_CHECKING:
    from game import Game
    from game.inventory import GlobalAircraftInventory


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

        Airfields are searched ordered nearest to farthest from the target and
        searched twice. The first search looks for aircraft which prefer the
        mission type, and the second search looks for any aircraft which are
        capable of the mission type. For example, an F-14 from a nearby carrier
        will be preferred for the CAP of an airfield that has only F-16s, but if
        the carrier has only F/A-18s the F-16s will be used for CAP instead.

        Note that aircraft *will* be removed from the global inventory on
        success. This is to ensure that the same aircraft are not matched twice
        on subsequent calls. If the found aircraft are not used, the caller is
        responsible for returning them to the inventory.
        """
        result = self.find_aircraft_of_type(
            flight, self.preferred_aircraft_for_task(flight.task)
        )
        if result is not None:
            return result
        return self.find_aircraft_of_type(
            flight, self.capable_aircraft_for_task(flight.task)
        )

    @staticmethod
    def preferred_aircraft_for_task(task: FlightType) -> List[Type[FlyingType]]:
        cap_missions = (FlightType.BARCAP, FlightType.TARCAP)
        if task in cap_missions:
            return CAP_PREFERRED
        elif task == FlightType.BAI:
            return CAS_CAPABLE
        elif task == FlightType.CAS:
            return CAS_PREFERRED
        elif task in (FlightType.DEAD, FlightType.SEAD):
            return SEAD_PREFERRED
        elif task == FlightType.STRIKE:
            return STRIKE_PREFERRED
        elif task == FlightType.ESCORT:
            return CAP_PREFERRED
        else:
            return []

    @staticmethod
    def capable_aircraft_for_task(task: FlightType) -> List[Type[FlyingType]]:
        cap_missions = (FlightType.BARCAP, FlightType.TARCAP)
        if task in cap_missions:
            return CAP_CAPABLE
        elif task == FlightType.BAI:
            return CAS_CAPABLE
        elif task == FlightType.CAS:
            return CAS_CAPABLE
        elif task in (FlightType.DEAD, FlightType.SEAD):
            return SEAD_CAPABLE
        elif task == FlightType.STRIKE:
            return STRIKE_CAPABLE
        elif task == FlightType.ESCORT:
            return CAP_CAPABLE
        else:
            logging.error(f"Unplannable flight type: {task}")
            return []

    def find_aircraft_of_type(
            self, flight: ProposedFlight, types: List[Type[FlyingType]],
    ) -> Optional[Tuple[ControlPoint, UnitType]]:
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
                 is_player: bool,
                 start_type: str) -> None:
        self.package = Package(location)
        self.allocator = AircraftAllocator(closest_airfields, global_inventory,
                                           is_player)
        self.global_inventory = global_inventory
        self.start_type = start_type

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
        flight = Flight(self.package, aircraft, plan.num_aircraft, airfield,
                        plan.task, self.start_type)
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

    def enemy_sams(self) -> Iterator[TheaterGroundObject]:
        """Iterates over all enemy SAM sites."""
        # Control points might have the same ground object several times, for
        # some reason.
        found_targets: Set[str] = set()
        for cp in self.enemy_control_points():
            for ground_object in cp.ground_objects:
                is_ewr = isinstance(ground_object, EwrGroundObject)
                is_sam = isinstance(ground_object, SamGroundObject)
                if not is_ewr and not is_sam:
                    continue

                if ground_object.is_dead:
                    continue

                if ground_object.name in found_targets:
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

    def enemy_vehicle_groups(self) -> Iterator[VehicleGroupGroundObject]:
        """Iterates over all enemy vehicle groups."""
        # Control points might have the same ground object several times, for
        # some reason.
        found_targets: Set[str] = set()
        for cp in self.enemy_control_points():
            for ground_object in cp.ground_objects:
                if not isinstance(ground_object, VehicleGroupGroundObject):
                    continue

                if ground_object.is_dead:
                    continue

                if ground_object.name in found_targets:
                    continue

                yield ground_object
                found_targets.add(ground_object.name)

    def threatening_vehicle_groups(self) -> Iterator[TheaterGroundObject]:
        """Iterates over enemy vehicle groups near friendly control points.

        Groups are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        groups: List[Tuple[VehicleGroupGroundObject, int]] = []
        for group in self.enemy_vehicle_groups():
            ranges: List[int] = []
            for cp in self.friendly_control_points():
                ranges.append(group.distance_to(cp))
            groups.append((group, min(ranges)))

        groups = sorted(groups, key=operator.itemgetter(1))
        for group, _range in groups:
            yield group

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
                if ground_object.is_dead:
                    continue
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
                    yield FrontLine(cp, connected, self.game.theater)

    def vulnerable_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over friendly CPs that are vulnerable to enemy CPs.

        Vulnerability is defined as any enemy CP within threat range of of the
        CP.
        """
        for cp in self.friendly_control_points():
            airfields_in_proximity = self.closest_airfields_to(cp)
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

    @staticmethod
    def closest_airfields_to(location: MissionTarget) -> ClosestAirfields:
        """Returns the closest airfields to the given location."""
        return ObjectiveDistanceCache.get_closest_airfields(location)


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
    MAX_BAI_RANGE = nm_to_meter(150)
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
                ProposedFlight(FlightType.BARCAP, 2, self.MAX_CAP_RANGE),
            ])

        # Find front lines, plan CAS.
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
                ProposedFlight(FlightType.ESCORT, 2, self.MAX_SEAD_RANGE),
            ])

        for group in self.objective_finder.threatening_vehicle_groups():
            yield ProposedMission(group, [
                ProposedFlight(FlightType.BAI, 2, self.MAX_BAI_RANGE),
                # TODO: Max escort range.
                ProposedFlight(FlightType.ESCORT, 2, self.MAX_BAI_RANGE),
            ])

        # Plan strike missions.
        for target in self.objective_finder.strike_targets():
            yield ProposedMission(target, [
                ProposedFlight(FlightType.STRIKE, 2, self.MAX_STRIKE_RANGE),
                # TODO: Max escort range.
                ProposedFlight(FlightType.SEAD, 2, self.MAX_STRIKE_RANGE),
                ProposedFlight(FlightType.ESCORT, 2, self.MAX_STRIKE_RANGE),
            ])

    def plan_missions(self) -> None:
        """Identifies and plans mission for the turn."""
        for proposed_mission in self.propose_missions():
            self.plan_mission(proposed_mission)

        self.stagger_missions()

        for cp in self.objective_finder.friendly_control_points():
            inventory = self.game.aircraft_inventory.for_control_point(cp)
            for aircraft, available in inventory.all_aircraft:
                self.message("Unused aircraft",
                             f"{available} {aircraft.id} from {cp}")

    def plan_mission(self, mission: ProposedMission) -> None:
        """Allocates aircraft for a proposed mission and adds it to the ATO."""

        if self.game.settings.perf_ai_parking_start:
            start_type = "Cold"
        else:
            start_type = "Warm"

        builder = PackageBuilder(
            mission.location,
            self.objective_finder.closest_airfields_to(mission.location),
            self.game.aircraft_inventory,
            self.is_player,
            start_type
        )

        missing_types: Set[FlightType] = set()
        for proposed_flight in mission.flights:
            if not builder.plan_flight(proposed_flight):
                missing_types.add(proposed_flight.task)

        if missing_types:
            missing_types_str = ", ".join(
                sorted([t.name for t in missing_types]))
            builder.release_planned_aircraft()
            self.message(
                "Insufficient aircraft",
                f"Not enough aircraft in range for {mission.location.name} "
                f"capable of: {missing_types_str}")
            return

        package = builder.build()
        flight_plan_builder = FlightPlanBuilder(self.game, package,
                                                self.is_player)
        for flight in package.flights:
            flight_plan_builder.populate_flight_plan(flight)
        self.ato.add_package(package)

    def stagger_missions(self) -> None:
        def start_time_generator(count: int, earliest: int, latest: int,
                                 margin: int) -> Iterator[timedelta]:
            interval = (latest - earliest) // count
            for time in range(earliest, latest, interval):
                error = random.randint(-margin, margin)
                yield timedelta(minutes=max(0, time + error))

        dca_types = {
            FlightType.BARCAP,
            FlightType.INTERCEPTION,
            FlightType.TARCAP,
        }

        non_dca_packages = [p for p in self.ato.packages if
                            p.primary_task not in dca_types]

        start_time = start_time_generator(
            count=len(non_dca_packages),
            earliest=5,
            latest=90,
            margin=5
        )
        for package in self.ato.packages:
            tot = TotEstimator(package).earliest_tot()
            if package.primary_task in dca_types:
                # All CAP missions should be on station ASAP.
                package.time_over_target = tot
            else:
                # But other packages should be spread out a bit. Note that take
                # times are delayed, but all aircraft will become active at
                # mission start. This makes it more worthwhile to attack enemy
                # airfields to hit grounded aircraft, since they're more likely
                # to be present. Runway and air started aircraft will be
                # delayed until their takeoff time by AirConflictGenerator.
                package.time_over_target = next(start_time) + tot

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
