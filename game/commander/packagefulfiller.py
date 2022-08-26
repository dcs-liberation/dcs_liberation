from __future__ import annotations

import logging
from collections import defaultdict
from typing import Dict, Iterable, Optional, Set, TYPE_CHECKING

from game.ato.airtaaskingorder import AirTaskingOrder
from game.ato.closestairfields import ObjectiveDistanceCache
from game.ato.flighttype import FlightType
from game.ato.package import Package
from game.commander.missionproposals import EscortType, ProposedFlight, ProposedMission
from game.commander.packagebuilder import PackageBuilder
from game.data.doctrine import Doctrine
from game.db import Database
from game.procurement import AircraftProcurementRequest
from game.profiling import MultiEventTracer
from game.settings import Settings
from game.squadrons import AirWing
from game.theater import ConflictTheater
from game.threatzones import ThreatZones

if TYPE_CHECKING:
    from game.ato import Flight
    from game.coalition import Coalition


class PackageFulfiller:
    """Responsible for package aircraft allocation and flight plan layout."""

    def __init__(
        self,
        coalition: Coalition,
        theater: ConflictTheater,
        flight_db: Database[Flight],
        settings: Settings,
    ) -> None:
        self.coalition = coalition
        self.theater = theater
        self.flight_db = flight_db
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

    def add_procurement_request(self, request: AircraftProcurementRequest) -> None:
        self.coalition.add_procurement_request(request)

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
        purchase_multiplier: int,
    ) -> None:
        if not builder.plan_flight(flight):
            missing_types.add(flight.task)
            purchase_order = AircraftProcurementRequest(
                near=mission.location,
                task_capability=flight.task,
                number=flight.num_aircraft * purchase_multiplier,
            )
            # Reserves are planned for critical missions, so prioritize those orders
            # over aircraft needed for non-critical missions.
            self.add_procurement_request(purchase_order)

    def scrub_mission_missing_aircraft(
        self,
        mission: ProposedMission,
        builder: PackageBuilder,
        missing_types: Set[FlightType],
        not_attempted: Iterable[ProposedFlight],
        purchase_multiplier: int,
    ) -> None:
        # Try to plan the rest of the mission just so we can count the missing
        # types to buy.
        for flight in not_attempted:
            self.plan_flight(
                mission, flight, builder, missing_types, purchase_multiplier
            )

        missing_types_str = ", ".join(sorted([t.name for t in missing_types]))
        builder.release_planned_aircraft()
        color = "Blue" if self.is_player else "Red"
        logging.debug(
            f"{color}: not enough aircraft in range for {mission.location.name} "
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
        self,
        mission: ProposedMission,
        purchase_multiplier: int,
        tracer: MultiEventTracer,
    ) -> Optional[Package]:
        """Allocates aircraft for a proposed mission and adds it to the ATO."""
        builder = PackageBuilder(
            mission.location,
            ObjectiveDistanceCache.get_closest_airfields(mission.location),
            self.air_wing,
            self.flight_db,
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
                    mission,
                    proposed_flight,
                    builder,
                    missing_types,
                    purchase_multiplier,
                )

        if missing_types:
            self.scrub_mission_missing_aircraft(
                mission, builder, missing_types, escorts, purchase_multiplier
            )
            return None

        if not builder.package.flights:
            # The non-escort part of this mission is unplannable by this faction. Scrub
            # the mission and do not attempt planning escorts because there's no reason
            # to buy them because this mission will never be planned.
            return None

        # Create flight plans for the main flights of the package so we can
        # determine threats. This is done *after* creating all of the flights
        # rather than as each flight is added because the flight plan for
        # flights that will rendezvous with their package will be affected by
        # the other flights in the package. Escorts will not be able to
        # contribute to this.
        for flight in builder.package.flights:
            with tracer.trace("Flight plan population"):
                flight.recreate_flight_plan()

        needed_escorts = self.check_needed_escorts(builder)
        for escort in escorts:
            # This list was generated from the not None set, so this should be
            # impossible.
            assert escort.escort_type is not None
            if needed_escorts[escort.escort_type]:
                with tracer.trace("Flight planning"):
                    self.plan_flight(
                        mission, escort, builder, missing_types, purchase_multiplier
                    )

        # Check again for unavailable aircraft. If the escort was required and
        # none were found, scrub the mission.
        if missing_types:
            self.scrub_mission_missing_aircraft(
                mission, builder, missing_types, escorts, purchase_multiplier
            )
            return None

        package = builder.build()
        # Add flight plans for escorts.
        for flight in package.flights:
            if not flight.flight_plan.waypoints:
                with tracer.trace("Flight plan population"):
                    flight.recreate_flight_plan()

        if package.has_players and self.player_missions_asap:
            package.auto_asap = True
            package.set_tot_asap()

        return package
