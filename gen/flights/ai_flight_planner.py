from __future__ import annotations

import logging
import random
from collections import defaultdict
from datetime import timedelta
from typing import (
    Dict,
    Iterable,
    Iterator,
    Optional,
    Set,
    TYPE_CHECKING,
    Tuple,
)

from game.commander.missionproposals import ProposedFlight, ProposedMission, EscortType
from game.data.doctrine import Doctrine
from game.dcs.aircrafttype import AircraftType
from game.procurement import AircraftProcurementRequest
from game.profiling import MultiEventTracer
from game.settings import Settings
from game.squadrons import AirWing, Squadron
from game.theater import (
    ControlPoint,
    MissionTarget,
    OffMapSpawn,
    ConflictTheater,
)
from game.threatzones import ThreatZones
from game.utils import nautical_miles
from gen.ato import Package, AirTaskingOrder
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
    from game.coalition import Coalition
    from game.inventory import GlobalAircraftInventory


class AircraftAllocator:
    """Finds suitable aircraft for proposed missions."""

    def __init__(
        self,
        air_wing: AirWing,
        closest_airfields: ClosestAirfields,
        global_inventory: GlobalAircraftInventory,
        is_player: bool,
    ) -> None:
        self.air_wing = air_wing
        self.closest_airfields = closest_airfields
        self.global_inventory = global_inventory
        self.is_player = is_player

    def find_squadron_for_flight(
        self, flight: ProposedFlight
    ) -> Optional[Tuple[ControlPoint, Squadron]]:
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
        return self.find_aircraft_for_task(flight, flight.task)

    def find_aircraft_for_task(
        self, flight: ProposedFlight, task: FlightType
    ) -> Optional[Tuple[ControlPoint, Squadron]]:
        types = aircraft_for_task(task)
        airfields_in_range = self.closest_airfields.operational_airfields_within(
            flight.max_distance
        )

        for airfield in airfields_in_range:
            if not airfield.is_friendly(self.is_player):
                continue
            inventory = self.global_inventory.for_control_point(airfield)
            for aircraft in types:
                if not airfield.can_operate(aircraft):
                    continue
                if inventory.available(aircraft) < flight.num_aircraft:
                    continue
                # Valid location with enough aircraft available. Find a squadron to fit
                # the role.
                squadrons = self.air_wing.auto_assignable_for_task_with_type(
                    aircraft, task
                )
                for squadron in squadrons:
                    if squadron.can_provide_pilots(flight.num_aircraft):
                        inventory.remove_aircraft(aircraft, flight.num_aircraft)
                        return airfield, squadron
        return None


class PackageBuilder:
    """Builds a Package for the flights it receives."""

    def __init__(
        self,
        location: MissionTarget,
        closest_airfields: ClosestAirfields,
        global_inventory: GlobalAircraftInventory,
        air_wing: AirWing,
        is_player: bool,
        package_country: str,
        start_type: str,
        asap: bool,
    ) -> None:
        self.closest_airfields = closest_airfields
        self.is_player = is_player
        self.package_country = package_country
        self.package = Package(location, auto_asap=asap)
        self.allocator = AircraftAllocator(
            air_wing, closest_airfields, global_inventory, is_player
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
        assignment = self.allocator.find_squadron_for_flight(plan)
        if assignment is None:
            return False
        airfield, squadron = assignment
        if isinstance(airfield, OffMapSpawn):
            start_type = "In Flight"
        else:
            start_type = self.start_type

        flight = Flight(
            self.package,
            self.package_country,
            squadron,
            plan.num_aircraft,
            plan.task,
            start_type,
            departure=airfield,
            arrival=airfield,
            divert=self.find_divert_field(squadron.aircraft, airfield),
        )
        self.package.add_flight(flight)
        return True

    def find_divert_field(
        self, aircraft: AircraftType, arrival: ControlPoint
    ) -> Optional[ControlPoint]:
        divert_limit = nautical_miles(150)
        for airfield in self.closest_airfields.operational_airfields_within(
            divert_limit
        ):
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
            flight.clear_roster()
            self.package.remove_flight(flight)


class MissionScheduler:
    def __init__(self, coalition: Coalition, desired_mission_length: timedelta) -> None:
        self.coalition = coalition
        self.desired_mission_length = desired_mission_length

    def schedule_missions(self) -> None:
        """Identifies and plans mission for the turn."""

        def start_time_generator(
            count: int, earliest: int, latest: int, margin: int
        ) -> Iterator[timedelta]:
            interval = (latest - earliest) // count
            for time in range(earliest, latest, interval):
                error = random.randint(-margin, margin)
                yield timedelta(seconds=max(0, time + error))

        dca_types = {
            FlightType.BARCAP,
            FlightType.TARCAP,
        }

        previous_cap_end_time: Dict[MissionTarget, timedelta] = defaultdict(timedelta)
        non_dca_packages = [
            p for p in self.coalition.ato.packages if p.primary_task not in dca_types
        ]

        start_time = start_time_generator(
            count=len(non_dca_packages),
            earliest=5 * 60,
            latest=int(self.desired_mission_length.total_seconds()),
            margin=5 * 60,
        )
        for package in self.coalition.ato.packages:
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
            elif package.auto_asap:
                package.set_tot_asap()
            else:
                # But other packages should be spread out a bit. Note that take
                # times are delayed, but all aircraft will become active at
                # mission start. This makes it more worthwhile to attack enemy
                # airfields to hit grounded aircraft, since they're more likely
                # to be present. Runway and air started aircraft will be
                # delayed until their takeoff time by AirConflictGenerator.
                package.time_over_target = next(start_time) + tot


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

    def __init__(
        self,
        coalition: Coalition,
        theater: ConflictTheater,
        aircraft_inventory: GlobalAircraftInventory,
        settings: Settings,
    ) -> None:
        self.coalition = coalition
        self.theater = theater
        self.aircraft_inventory = aircraft_inventory
        self.player_missions_asap = settings.auto_ato_player_missions_asap
        self.default_start_type = settings.default_start_type

    @property
    def is_player(self) -> bool:
        return self.coalition.player

    @property
    def ato(self) -> AirTaskingOrder:
        return self.coalition.ato

    @property
    def air_wing(self) -> AirWing:
        return self.coalition.air_wing

    @property
    def doctrine(self) -> Doctrine:
        return self.coalition.doctrine

    @property
    def threat_zones(self) -> ThreatZones:
        return self.coalition.opponent.threat_zone

    def add_procurement_request(
        self, request: AircraftProcurementRequest, priority: bool
    ) -> None:
        if priority:
            self.coalition.procurement_requests.insert(0, request)
        else:
            self.coalition.procurement_requests.append(request)

    def air_wing_can_plan(self, mission_type: FlightType) -> bool:
        """Returns True if it is possible for the air wing to plan this mission type.

        Not all mission types can be fulfilled by all air wings. Many factions do not
        have AEW&C aircraft, so they will never be able to plan those missions. It's
        also possible for the player to exclude mission types from their squadron
        designs.
        """
        return self.air_wing.can_auto_plan(mission_type)

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
            # Reserves are planned for critical missions, so prioritize those orders
            # over aircraft needed for non-critical missions.
            self.add_procurement_request(purchase_order, priority=for_reserves)

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
        logging.debug(
            f"Not enough {desc} in range for {mission.location.name} "
            f"capable of: {missing_types_str}"
        )

    def check_needed_escorts(self, builder: PackageBuilder) -> Dict[EscortType, bool]:
        threats = defaultdict(bool)
        for flight in builder.package.flights:
            if self.threat_zones.waypoints_threatened_by_aircraft(
                flight.flight_plan.escorted_waypoints()
            ):
                threats[EscortType.AirToAir] = True
            if self.threat_zones.waypoints_threatened_by_radar_sam(
                list(flight.flight_plan.escorted_waypoints())
            ):
                threats[EscortType.Sead] = True
        return threats

    def plan_mission(
        self, mission: ProposedMission, tracer: MultiEventTracer, reserves: bool = False
    ) -> None:
        """Allocates aircraft for a proposed mission and adds it to the ATO."""
        builder = PackageBuilder(
            mission.location,
            ObjectiveDistanceCache.get_closest_airfields(mission.location),
            self.aircraft_inventory,
            self.air_wing,
            self.is_player,
            self.coalition.country_name,
            self.default_start_type,
            mission.asap,
        )

        # Attempt to plan all the main elements of the mission first. Escorts
        # will be planned separately so we can prune escorts for packages that
        # are not expected to encounter that type of threat.
        missing_types: Set[FlightType] = set()
        escorts = []
        for proposed_flight in mission.flights:
            if not self.air_wing_can_plan(proposed_flight.task):
                # This air wing can never plan this mission type because they do not
                # have compatible aircraft or squadrons. Skip fulfillment so that we
                # don't place the purchase request.
                continue
            if proposed_flight.escort_type is not None:
                # Escorts are planned after the primary elements of the package.
                # If the package does not need escorts they may be pruned.
                escorts.append(proposed_flight)
                continue
            with tracer.trace("Flight planning"):
                self.plan_flight(
                    mission, proposed_flight, builder, missing_types, reserves
                )

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
            builder.package, self.coalition, self.theater
        )
        for flight in builder.package.flights:
            with tracer.trace("Flight plan population"):
                flight_plan_builder.populate_flight_plan(flight)

        needed_escorts = self.check_needed_escorts(builder)
        for escort in escorts:
            # This list was generated from the not None set, so this should be
            # impossible.
            assert escort.escort_type is not None
            if needed_escorts[escort.escort_type]:
                with tracer.trace("Flight planning"):
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
                with tracer.trace("Flight plan population"):
                    flight_plan_builder.populate_flight_plan(flight)

        if package.has_players and self.player_missions_asap:
            package.auto_asap = True
            package.set_tot_asap()

        self.ato.add_package(package)
