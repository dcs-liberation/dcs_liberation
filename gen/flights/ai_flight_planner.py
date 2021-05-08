from __future__ import annotations

import logging
import operator
import random
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum, auto
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    TYPE_CHECKING,
    Tuple,
    Type,
)

from dcs.unittype import FlyingType

from game.infos.information import Information
from game.procurement import AircraftProcurementRequest
from game.theater import (
    Airfield,
    ControlPoint,
    Fob,
    FrontLine,
    MissionTarget,
    OffMapSpawn,
    SamGroundObject,
    TheaterGroundObject,
)
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    EwrGroundObject,
    NavalGroundObject,
    VehicleGroupGroundObject,
)
from game.transfers import CargoShip, Convoy
from game.utils import Distance, nautical_miles
from gen import Conflict
from gen.ato import Package
from gen.flights.ai_flight_planner_db import aircraft_for_task
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

# Avoid importing some types that cause circular imports unless type checking.
if TYPE_CHECKING:
    from game import Game
    from game.inventory import GlobalAircraftInventory


class EscortType(Enum):
    AirToAir = auto()
    Sead = auto()


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
    max_distance: Distance

    #: The type of threat this flight defends against if it is an escort. Escort
    #: flights will be pruned if the rest of the package is not threatened by
    #: the threat they defend against. If this flight is not an escort, this
    #: field is None.
    escort_type: Optional[EscortType] = field(default=None)

    def __str__(self) -> str:
        return f"{self.task} {self.num_aircraft} ship"


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
        flights = ", ".join([str(f) for f in self.flights])
        return f"{self.location.name}: {flights}"


class AircraftAllocator:
    """Finds suitable aircraft for proposed missions."""

    def __init__(
        self,
        closest_airfields: ClosestAirfields,
        global_inventory: GlobalAircraftInventory,
        is_player: bool,
    ) -> None:
        self.closest_airfields = closest_airfields
        self.global_inventory = global_inventory
        self.is_player = is_player

    def find_aircraft_for_flight(
        self, flight: ProposedFlight
    ) -> Optional[Tuple[ControlPoint, Type[FlyingType]]]:
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
        return self.find_aircraft_of_type(flight, aircraft_for_task(flight.task))

    def find_aircraft_of_type(
        self,
        flight: ProposedFlight,
        types: List[Type[FlyingType]],
    ) -> Optional[Tuple[ControlPoint, Type[FlyingType]]]:
        airfields_in_range = self.closest_airfields.airfields_within(
            flight.max_distance
        )
        for airfield in airfields_in_range:
            if not airfield.is_friendly(self.is_player):
                continue
            inventory = self.global_inventory.for_control_point(airfield)
            for aircraft, available in inventory.all_aircraft:
                if not airfield.can_operate(aircraft):
                    continue
                if aircraft in types and available >= flight.num_aircraft:
                    inventory.remove_aircraft(aircraft, flight.num_aircraft)
                    return airfield, aircraft

        return None


class PackageBuilder:
    """Builds a Package for the flights it receives."""

    def __init__(
        self,
        location: MissionTarget,
        closest_airfields: ClosestAirfields,
        global_inventory: GlobalAircraftInventory,
        is_player: bool,
        package_country: str,
        start_type: str,
    ) -> None:
        self.closest_airfields = closest_airfields
        self.is_player = is_player
        self.package_country = package_country
        self.package = Package(location)
        self.allocator = AircraftAllocator(
            closest_airfields, global_inventory, is_player
        )
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
        if isinstance(airfield, OffMapSpawn):
            start_type = "In Flight"
        else:
            start_type = self.start_type

        flight = Flight(
            self.package,
            self.package_country,
            aircraft,
            plan.num_aircraft,
            plan.task,
            start_type,
            departure=airfield,
            arrival=airfield,
            divert=self.find_divert_field(aircraft, airfield),
        )
        self.package.add_flight(flight)
        return True

    def find_divert_field(
        self, aircraft: Type[FlyingType], arrival: ControlPoint
    ) -> Optional[ControlPoint]:
        divert_limit = nautical_miles(150)
        for airfield in self.closest_airfields.airfields_within(divert_limit):
            if airfield.captured != self.is_player:
                continue
            if airfield == arrival:
                continue
            if not airfield.can_operate(aircraft):
                continue
            if isinstance(airfield, OffMapSpawn):
                continue
            return airfield
        return None

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
    AIRFIELD_THREAT_RANGE = nautical_miles(150)
    SAM_THREAT_RANGE = nautical_miles(100)

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

                if not ground_object.has_radar:
                    continue

                # TODO: Yield in order of most threatening.
                # Need to sort in order of how close their defensive range comes
                # to friendly assets. To do that we need to add effective range
                # information to the database.
                yield ground_object
                found_targets.add(ground_object.name)

    def threatening_sams(self) -> Iterator[MissionTarget]:
        """Iterates over enemy SAMs in threat range of friendly control points.

        SAM sites are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        return self._targets_by_range(self.enemy_sams())

    def enemy_vehicle_groups(self) -> Iterator[VehicleGroupGroundObject]:
        """Iterates over all enemy vehicle groups."""
        for cp in self.enemy_control_points():
            for ground_object in cp.ground_objects:
                if not isinstance(ground_object, VehicleGroupGroundObject):
                    continue

                if ground_object.is_dead:
                    continue

                yield ground_object

    def threatening_vehicle_groups(self) -> Iterator[MissionTarget]:
        """Iterates over enemy vehicle groups near friendly control points.

        Groups are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        return self._targets_by_range(self.enemy_vehicle_groups())

    def enemy_ships(self) -> Iterator[NavalGroundObject]:
        for cp in self.enemy_control_points():
            for ground_object in cp.ground_objects:
                if not isinstance(ground_object, NavalGroundObject):
                    continue

                if ground_object.is_dead:
                    continue

                yield ground_object

    def threatening_ships(self) -> Iterator[MissionTarget]:
        """Iterates over enemy ships near friendly control points.

        Groups are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        return self._targets_by_range(self.enemy_ships())

    def _targets_by_range(
        self, targets: Iterable[MissionTarget]
    ) -> Iterator[MissionTarget]:
        target_ranges: List[Tuple[MissionTarget, int]] = []
        for target in targets:
            ranges: List[int] = []
            for cp in self.friendly_control_points():
                ranges.append(target.distance_to(cp))
            target_ranges.append((target, min(ranges)))

        target_ranges = sorted(target_ranges, key=operator.itemgetter(1))
        for target, _range in target_ranges:
            yield target

    def strike_targets(self) -> Iterator[TheaterGroundObject]:
        """Iterates over enemy strike targets.

        Targets are sorted by their closest proximity to any friendly control
        point (airfield or fleet).
        """
        targets: List[Tuple[TheaterGroundObject, int]] = []
        # Building objectives are made of several individual TGOs (one per
        # building).
        found_targets: Set[str] = set()
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
                if isinstance(ground_object, VehicleGroupGroundObject):
                    # BAI target, not strike target.
                    continue

                if isinstance(ground_object, NavalGroundObject):
                    # Anti-ship target, not strike target.
                    continue

                if isinstance(ground_object, SamGroundObject):
                    # SAMs are targeted by DEAD. No need to double plan.
                    continue

                is_building = isinstance(ground_object, BuildingGroundObject)
                is_fob = isinstance(enemy_cp, Fob)
                if is_building and is_fob and ground_object.airbase_group:
                    # This is the FOB structure itself. Can't be repaired or
                    # targeted by the player, so shouldn't be targetable by the
                    # AI.
                    continue

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
            if isinstance(cp, OffMapSpawn):
                # Off-map spawn locations don't need protection.
                continue
            airfields_in_proximity = self.closest_airfields_to(cp)
            airfields_in_threat_range = airfields_in_proximity.airfields_within(
                self.AIRFIELD_THREAT_RANGE
            )
            for airfield in airfields_in_threat_range:
                if not airfield.is_friendly(self.is_player):
                    yield cp
                    break

    def oca_targets(self, min_aircraft: int) -> Iterator[MissionTarget]:
        airfields = []
        for control_point in self.enemy_control_points():
            if not isinstance(control_point, Airfield):
                continue
            if control_point.base.total_aircraft >= min_aircraft:
                airfields.append(control_point)
        return self._targets_by_range(airfields)

    def convoys(self) -> Iterator[Convoy]:
        for front_line in self.front_lines():
            if front_line.control_point_a.is_friendly(self.is_player):
                enemy_cp = front_line.control_point_a
            else:
                enemy_cp = front_line.control_point_b

            yield from self.game.transfers.convoys.travelling_to(enemy_cp)

    def cargo_ships(self) -> Iterator[CargoShip]:
        for front_line in self.front_lines():
            if front_line.control_point_a.is_friendly(self.is_player):
                enemy_cp = front_line.control_point_a
            else:
                enemy_cp = front_line.control_point_b

            yield from self.game.transfers.cargo_ships.travelling_to(enemy_cp)

    def friendly_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over all friendly control points."""
        return (
            c for c in self.game.theater.controlpoints if c.is_friendly(self.is_player)
        )

    def farthest_friendly_control_point(self) -> Optional[ControlPoint]:
        """
        Iterates over all friendly control points and find the one farthest away from the frontline
        BUT! prefer Cvs. Everybody likes CVs!
        """
        from_frontline = 0
        cp = None
        first_friendly_cp = None

        for c in self.game.theater.controlpoints:
            if c.is_friendly(self.is_player):
                if first_friendly_cp is None:
                    first_friendly_cp = c
                if c.is_carrier:
                    return c
                if c.has_active_frontline:
                    if c.distance_to(self.front_lines().__next__()) > from_frontline:
                        from_frontline = c.distance_to(self.front_lines().__next__())
                        cp = c

        # If no frontlines on the map, return the first friendly cp
        if cp is None:
            return first_friendly_cp
        else:
            return cp

    def enemy_control_points(self) -> Iterator[ControlPoint]:
        """Iterates over all enemy control points."""
        return (
            c
            for c in self.game.theater.controlpoints
            if not c.is_friendly(self.is_player)
        )

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
    MAX_CAP_RANGE = nautical_miles(100)
    MAX_CAS_RANGE = nautical_miles(50)
    MAX_ANTISHIP_RANGE = nautical_miles(150)
    MAX_BAI_RANGE = nautical_miles(150)
    MAX_OCA_RANGE = nautical_miles(150)
    MAX_SEAD_RANGE = nautical_miles(150)
    MAX_STRIKE_RANGE = nautical_miles(150)
    MAX_AWEC_RANGE = nautical_miles(200)

    def __init__(self, game: Game, is_player: bool) -> None:
        self.game = game
        self.is_player = is_player
        self.objective_finder = ObjectiveFinder(self.game, self.is_player)
        self.ato = self.game.blue_ato if is_player else self.game.red_ato
        self.threat_zones = self.game.threat_zone_for(not self.is_player)
        self.procurement_requests = self.game.procurement_requests_for(self.is_player)
        self.faction = self.game.faction_for(self.is_player)

    def faction_can_plan(self, mission_type: FlightType) -> bool:
        """Returns True if it is possible for the faction to plan this mission type.

        Not all mission types can be fulfilled by all factions. Many factions do not
        have AEW&C aircraft, so they will never be able to plan those missions.
        """
        all_compatible = aircraft_for_task(mission_type)
        for aircraft in self.faction.aircrafts:
            if aircraft in all_compatible:
                return True
        return False

    def critical_missions(self) -> Iterator[ProposedMission]:
        """Identifies the most important missions to plan this turn.

        Non-critical missions that cannot be fulfilled will create purchase
        orders for the next turn. Critical missions will create a purchase order
        unless the mission can be doubly fulfilled. In other words, the AI will
        attempt to have *double* the aircraft it needs for these missions to
        ensure that they can be planned again next turn even if all aircraft are
        eliminated this turn.
        """

        # Find farthest, friendly CP for AEWC
        cp = self.objective_finder.farthest_friendly_control_point()
        if cp is not None:
            yield ProposedMission(
                cp, [ProposedFlight(FlightType.AEWC, 1, self.MAX_AWEC_RANGE)]
            )

        # Find friendly CPs within 100 nmi from an enemy airfield, plan CAP.
        for cp in self.objective_finder.vulnerable_control_points():
            # Plan three rounds of CAP to give ~90 minutes coverage. Spacing
            # these out appropriately is done in stagger_missions.
            yield ProposedMission(
                cp,
                [
                    ProposedFlight(FlightType.BARCAP, 2, self.MAX_CAP_RANGE),
                ],
            )
            yield ProposedMission(
                cp,
                [
                    ProposedFlight(FlightType.BARCAP, 2, self.MAX_CAP_RANGE),
                ],
            )
            yield ProposedMission(
                cp,
                [
                    ProposedFlight(FlightType.BARCAP, 2, self.MAX_CAP_RANGE),
                ],
            )

        # Find front lines, plan CAS.
        for front_line in self.objective_finder.front_lines():
            yield ProposedMission(
                front_line,
                [
                    ProposedFlight(FlightType.CAS, 2, self.MAX_CAS_RANGE),
                    # This is *not* an escort because front lines don't create a threat
                    # zone. Generating threat zones from front lines causes the front
                    # line to push back BARCAPs as it gets closer to the base. While
                    # front lines do have the same problem of potentially pulling
                    # BARCAPs off bases to engage a front line TARCAP, that's probably
                    # the one time where we do want that.
                    #
                    # TODO: Use intercepts and extra TARCAPs to cover bases near fronts.
                    # We don't have intercept missions yet so this isn't something we
                    # can do today, but we should probably return to having the front
                    # line project a threat zone (so that strike missions will route
                    # around it) and instead *not plan* a BARCAP at bases near the
                    # front, since there isn't a place to put a barrier. Instead, the
                    # aircraft that would have been a BARCAP could be used as additional
                    # interceptors and TARCAPs which will defend the base but won't be
                    # trying to avoid front line contacts.
                    ProposedFlight(FlightType.TARCAP, 2, self.MAX_CAP_RANGE),
                ],
            )

    def propose_missions(self) -> Iterator[ProposedMission]:
        """Identifies and iterates over potential mission in priority order."""
        yield from self.critical_missions()

        # Find enemy SAM sites with ranges that cover friendly CPs, front lines,
        # or objects, plan DEAD.
        # Find enemy SAM sites with ranges that extend to within 50 nmi of
        # friendly CPs, front, lines, or objects, plan DEAD.
        for sam in self.objective_finder.threatening_sams():
            yield ProposedMission(
                sam,
                [
                    ProposedFlight(FlightType.DEAD, 2, self.MAX_SEAD_RANGE),
                    # TODO: Max escort range.
                    ProposedFlight(
                        FlightType.ESCORT, 2, self.MAX_SEAD_RANGE, EscortType.AirToAir
                    ),
                ],
            )

        # These will only rarely get planned. When a convoy is travelling multiple legs,
        # they're targetable after the first leg. The reason for this is that
        # procurement happens *after* mission planning so that the missions that could
        # not be filled will guide the procurement process. Procurement is the stage
        # that convoys are created (because they're created to move ground units that
        # were just purchased), so we haven't created any yet. Any incomplete transfers
        # from the previous turn (multi-leg journeys) will still be present though so
        # they can be targeted.
        #
        # Even after this is fixed, the player's convoys that were created through the
        # UI will never be targeted on the first turn of their journey because the AI
        # stops planning after the start of the turn. We could potentially fix this by
        # moving opfor mission planning until the takeoff button is pushed.
        for convoy in self.objective_finder.convoys():
            yield ProposedMission(
                convoy,
                [
                    ProposedFlight(FlightType.BAI, 2, self.MAX_BAI_RANGE),
                    # TODO: Max escort range.
                    ProposedFlight(
                        FlightType.ESCORT, 2, self.MAX_BAI_RANGE, EscortType.AirToAir
                    ),
                    ProposedFlight(
                        FlightType.SEAD, 2, self.MAX_BAI_RANGE, EscortType.Sead
                    ),
                ],
            )

        for ship in self.objective_finder.cargo_ships():
            yield ProposedMission(
                ship,
                [
                    ProposedFlight(FlightType.ANTISHIP, 2, self.MAX_ANTISHIP_RANGE),
                    # TODO: Max escort range.
                    ProposedFlight(
                        FlightType.ESCORT, 2, self.MAX_BAI_RANGE, EscortType.AirToAir
                    ),
                    ProposedFlight(
                        FlightType.SEAD, 2, self.MAX_BAI_RANGE, EscortType.Sead
                    ),
                ],
            )

        for group in self.objective_finder.threatening_ships():
            yield ProposedMission(
                group,
                [
                    ProposedFlight(FlightType.ANTISHIP, 2, self.MAX_ANTISHIP_RANGE),
                    # TODO: Max escort range.
                    ProposedFlight(
                        FlightType.ESCORT,
                        2,
                        self.MAX_ANTISHIP_RANGE,
                        EscortType.AirToAir,
                    ),
                ],
            )

        for group in self.objective_finder.threatening_vehicle_groups():
            yield ProposedMission(
                group,
                [
                    ProposedFlight(FlightType.BAI, 2, self.MAX_BAI_RANGE),
                    # TODO: Max escort range.
                    ProposedFlight(
                        FlightType.ESCORT, 2, self.MAX_BAI_RANGE, EscortType.AirToAir
                    ),
                    ProposedFlight(
                        FlightType.SEAD, 2, self.MAX_OCA_RANGE, EscortType.Sead
                    ),
                ],
            )

        for target in self.objective_finder.oca_targets(min_aircraft=20):
            flights = [
                ProposedFlight(FlightType.OCA_RUNWAY, 2, self.MAX_OCA_RANGE),
            ]
            if self.game.settings.default_start_type == "Cold":
                # Only schedule if the default start type is Cold. If the player
                # has set anything else there are no targets to hit.
                flights.append(
                    ProposedFlight(FlightType.OCA_AIRCRAFT, 2, self.MAX_OCA_RANGE)
                )
            flights.extend(
                [
                    # TODO: Max escort range.
                    ProposedFlight(
                        FlightType.ESCORT, 2, self.MAX_OCA_RANGE, EscortType.AirToAir
                    ),
                    ProposedFlight(
                        FlightType.SEAD, 2, self.MAX_OCA_RANGE, EscortType.Sead
                    ),
                ]
            )
            yield ProposedMission(target, flights)

        # Plan strike missions.
        for target in self.objective_finder.strike_targets():
            yield ProposedMission(
                target,
                [
                    ProposedFlight(FlightType.STRIKE, 2, self.MAX_STRIKE_RANGE),
                    # TODO: Max escort range.
                    ProposedFlight(
                        FlightType.ESCORT, 2, self.MAX_STRIKE_RANGE, EscortType.AirToAir
                    ),
                    ProposedFlight(
                        FlightType.SEAD, 2, self.MAX_STRIKE_RANGE, EscortType.Sead
                    ),
                ],
            )

    def plan_missions(self) -> None:
        """Identifies and plans mission for the turn."""
        for proposed_mission in self.propose_missions():
            self.plan_mission(proposed_mission)

        for critical_mission in self.critical_missions():
            self.plan_mission(critical_mission, reserves=True)

        self.stagger_missions()

        for cp in self.objective_finder.friendly_control_points():
            inventory = self.game.aircraft_inventory.for_control_point(cp)
            for aircraft, available in inventory.all_aircraft:
                self.message("Unused aircraft", f"{available} {aircraft.id} from {cp}")

    def plan_flight(
        self,
        mission: ProposedMission,
        flight: ProposedFlight,
        builder: PackageBuilder,
        missing_types: Set[FlightType],
        for_reserves: bool,
    ) -> None:
        if not builder.plan_flight(flight):
            missing_types.add(flight.task)
            purchase_order = AircraftProcurementRequest(
                near=mission.location,
                range=flight.max_distance,
                task_capability=flight.task,
                number=flight.num_aircraft,
            )
            if for_reserves:
                # Reserves are planned for critical missions, so prioritize
                # those orders over aircraft needed for non-critical missions.
                self.procurement_requests.insert(0, purchase_order)
            else:
                self.procurement_requests.append(purchase_order)

    def scrub_mission_missing_aircraft(
        self,
        mission: ProposedMission,
        builder: PackageBuilder,
        missing_types: Set[FlightType],
        not_attempted: Iterable[ProposedFlight],
        reserves: bool,
    ) -> None:
        # Try to plan the rest of the mission just so we can count the missing
        # types to buy.
        for flight in not_attempted:
            self.plan_flight(mission, flight, builder, missing_types, reserves)

        missing_types_str = ", ".join(sorted([t.name for t in missing_types]))
        builder.release_planned_aircraft()
        desc = "reserve aircraft" if reserves else "aircraft"
        self.message(
            "Insufficient aircraft",
            f"Not enough {desc} in range for {mission.location.name} "
            f"capable of: {missing_types_str}",
        )

    def check_needed_escorts(self, builder: PackageBuilder) -> Dict[EscortType, bool]:
        threats = defaultdict(bool)
        for flight in builder.package.flights:
            if self.threat_zones.threatened_by_aircraft(flight):
                threats[EscortType.AirToAir] = True
            if self.threat_zones.threatened_by_air_defense(flight):
                threats[EscortType.Sead] = True
        return threats

    def plan_mission(self, mission: ProposedMission, reserves: bool = False) -> None:
        """Allocates aircraft for a proposed mission and adds it to the ATO."""

        if self.is_player:
            package_country = self.game.player_country
        else:
            package_country = self.game.enemy_country

        builder = PackageBuilder(
            mission.location,
            self.objective_finder.closest_airfields_to(mission.location),
            self.game.aircraft_inventory,
            self.is_player,
            package_country,
            self.game.settings.default_start_type,
        )

        # Attempt to plan all the main elements of the mission first. Escorts
        # will be planned separately so we can prune escorts for packages that
        # are not expected to encounter that type of threat.
        missing_types: Set[FlightType] = set()
        escorts = []
        for proposed_flight in mission.flights:
            if not self.faction_can_plan(proposed_flight.task):
                # This faction can never plan this mission type because they do not have
                # compatible aircraft. Skip fulfillment so that we don't place the
                # purchase request.
                continue
            if proposed_flight.escort_type is not None:
                # Escorts are planned after the primary elements of the package.
                # If the package does not need escorts they may be pruned.
                escorts.append(proposed_flight)
                continue
            self.plan_flight(mission, proposed_flight, builder, missing_types, reserves)

        if missing_types:
            self.scrub_mission_missing_aircraft(
                mission, builder, missing_types, escorts, reserves
            )
            return

        if not builder.package.flights:
            # The non-escort part of this mission is unplannable by this faction. Scrub
            # the mission and do not attempt planning escorts because there's no reason
            # to buy them because this mission will never be planned.
            return

        # Create flight plans for the main flights of the package so we can
        # determine threats. This is done *after* creating all of the flights
        # rather than as each flight is added because the flight plan for
        # flights that will rendezvous with their package will be affected by
        # the other flights in the package. Escorts will not be able to
        # contribute to this.
        flight_plan_builder = FlightPlanBuilder(
            self.game, builder.package, self.is_player
        )
        for flight in builder.package.flights:
            flight_plan_builder.populate_flight_plan(flight)

        needed_escorts = self.check_needed_escorts(builder)
        for escort in escorts:
            # This list was generated from the not None set, so this should be
            # impossible.
            assert escort.escort_type is not None
            if needed_escorts[escort.escort_type]:
                self.plan_flight(mission, escort, builder, missing_types, reserves)

        # Check again for unavailable aircraft. If the escort was required and
        # none were found, scrub the mission.
        if missing_types:
            self.scrub_mission_missing_aircraft(
                mission, builder, missing_types, escorts, reserves
            )
            return

        if reserves:
            # Mission is planned reserves which will not be used this turn.
            # Return reserves to the inventory.
            builder.release_planned_aircraft()
            return

        package = builder.build()
        # Add flight plans for escorts.
        for flight in package.flights:
            if not flight.flight_plan.waypoints:
                flight_plan_builder.populate_flight_plan(flight)
        self.ato.add_package(package)

    def stagger_missions(self) -> None:
        def start_time_generator(
            count: int, earliest: int, latest: int, margin: int
        ) -> Iterator[timedelta]:
            interval = (latest - earliest) // count
            for time in range(earliest, latest, interval):
                error = random.randint(-margin, margin)
                yield timedelta(minutes=max(0, time + error))

        dca_types = {
            FlightType.BARCAP,
            FlightType.TARCAP,
        }

        previous_cap_end_time: Dict[MissionTarget, timedelta] = defaultdict(timedelta)
        non_dca_packages = [
            p for p in self.ato.packages if p.primary_task not in dca_types
        ]

        start_time = start_time_generator(
            count=len(non_dca_packages), earliest=5, latest=90, margin=5
        )
        for package in self.ato.packages:
            tot = TotEstimator(package).earliest_tot()
            if package.primary_task in dca_types:
                previous_end_time = previous_cap_end_time[package.target]
                if tot > previous_end_time:
                    # Can't get there exactly on time, so get there ASAP. This
                    # will typically only happen for the first CAP at each
                    # target.
                    package.time_over_target = tot
                else:
                    package.time_over_target = previous_end_time

                departure_time = package.mission_departure_time
                # Should be impossible for CAPs
                if departure_time is None:
                    logging.error(f"Could not determine mission end time for {package}")
                    continue
                previous_cap_end_time[package.target] = departure_time
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
            self.game.informations.append(Information(title, text, self.game.turn))
        else:
            logging.info(f"{title}: {text}")
