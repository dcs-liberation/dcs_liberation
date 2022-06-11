from __future__ import annotations

from typing import Any, TYPE_CHECKING, Type

from game.ato import FlightType
from game.ato.closestairfields import ObjectiveDistanceCache
from game.data.doctrine import Doctrine
from game.flightplan import IpZoneGeometry, JoinZoneGeometry
from game.flightplan.refuelzonegeometry import RefuelZoneGeometry
from .aewc import AewcFlightPlan
from .airassault import AirAssaultFlightPlan
from .airlift import AirliftFlightPlan
from .antiship import AntiShipFlightPlan
from .bai import BaiFlightPlan
from .barcap import BarCapFlightPlan
from .cas import CasFlightPlan
from .dead import DeadFlightPlan
from .escort import EscortFlightPlan
from .ferry import FerryFlightPlan
from .flightplan import FlightPlan
from .ocaaircraft import OcaAircraftFlightPlan
from .ocarunway import OcaRunwayFlightPlan
from .packagerefueling import PackageRefuelingFlightPlan
from .planningerror import PlanningError
from .sead import SeadFlightPlan
from .strike import StrikeFlightPlan
from .sweep import SweepFlightPlan
from .tarcap import TarCapFlightPlan
from .theaterrefueling import TheaterRefuelingFlightPlan
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from game.ato import Flight, FlightWaypoint, Package
    from game.coalition import Coalition
    from game.theater import ConflictTheater, ControlPoint, FrontLine
    from game.threatzones import ThreatZones


class FlightPlanBuilder:
    """Generates flight plans for flights."""

    def __init__(
        self, package: Package, coalition: Coalition, theater: ConflictTheater
    ) -> None:
        # TODO: Plan similar altitudes for the in-country leg of the mission.
        # Waypoint altitudes for a given flight *shouldn't* differ too much
        # between the join and split points, so we don't need speeds for each
        # leg individually since they should all be fairly similar. This doesn't
        # hold too well right now since nothing is stopping each waypoint from
        # jumping 20k feet each time, but that's a huge waste of energy we
        # should be avoiding anyway.
        self.package = package
        self.coalition = coalition
        self.theater = theater

    @property
    def is_player(self) -> bool:
        return self.coalition.player

    @property
    def doctrine(self) -> Doctrine:
        return self.coalition.doctrine

    @property
    def threat_zones(self) -> ThreatZones:
        return self.coalition.opponent.threat_zone

    def populate_flight_plan(self, flight: Flight) -> None:
        """Creates a default flight plan for the given mission."""
        if flight not in self.package.flights:
            raise RuntimeError("Flight must be a part of the package")

        from game.navmesh import NavMeshError

        try:
            if self.package.waypoints is None:
                self.regenerate_package_waypoints()
            flight.flight_plan = self.generate_flight_plan(flight)
        except NavMeshError as ex:
            color = "blue" if self.is_player else "red"
            raise PlanningError(
                f"Could not plan {color} {flight.flight_type.value} from "
                f"{flight.departure} to {flight.package.target}"
            ) from ex

    def plan_type(self, task: FlightType) -> Type[FlightPlan[Any]] | None:
        plan_type: Type[FlightPlan[Any]]
        if task == FlightType.REFUELING:
            if self.package.target.is_friendly(self.is_player) or isinstance(
                self.package.target, FrontLine
            ):
                return TheaterRefuelingFlightPlan
            return PackageRefuelingFlightPlan

        plan_dict: dict[FlightType, Type[FlightPlan[Any]]] = {
            FlightType.ANTISHIP: AntiShipFlightPlan,
            FlightType.BAI: BaiFlightPlan,
            FlightType.BARCAP: BarCapFlightPlan,
            FlightType.CAS: CasFlightPlan,
            FlightType.DEAD: DeadFlightPlan,
            FlightType.ESCORT: EscortFlightPlan,
            FlightType.OCA_AIRCRAFT: OcaAircraftFlightPlan,
            FlightType.OCA_RUNWAY: OcaRunwayFlightPlan,
            FlightType.SEAD: SeadFlightPlan,
            FlightType.SEAD_ESCORT: EscortFlightPlan,
            FlightType.STRIKE: StrikeFlightPlan,
            FlightType.SWEEP: SweepFlightPlan,
            FlightType.TARCAP: TarCapFlightPlan,
            FlightType.AEWC: AewcFlightPlan,
            FlightType.TRANSPORT: AirliftFlightPlan,
            FlightType.FERRY: FerryFlightPlan,
            FlightType.AIR_ASSAULT: AirAssaultFlightPlan,
        }
        return plan_dict.get(task)

    def generate_flight_plan(self, flight: Flight) -> FlightPlan[Any]:
        plan_type = self.plan_type(flight.flight_type)
        if plan_type is None:
            raise PlanningError(
                f"{flight.flight_type} flight plan generation not implemented"
            )
        layout = plan_type.builder_type()(flight, self.theater).build()
        return plan_type(flight, layout)

    def regenerate_flight_plans(self) -> None:
        new_flights: list[Flight] = []
        for old_flight in self.package.flights:
            old_flight.flight_plan = self.generate_flight_plan(old_flight)
            new_flights.append(old_flight)
        self.package.flights = new_flights

    def regenerate_package_waypoints(self) -> None:
        from game.ato.packagewaypoints import PackageWaypoints

        package_airfield = self.package_airfield()

        # Start by picking the best IP for the attack.
        ingress_point = IpZoneGeometry(
            self.package.target.position,
            package_airfield.position,
            self.coalition,
        ).find_best_ip()

        join_point = JoinZoneGeometry(
            self.package.target.position,
            package_airfield.position,
            ingress_point,
            self.coalition,
        ).find_best_join_point()

        refuel_point = RefuelZoneGeometry(
            package_airfield.position,
            join_point,
            self.coalition,
        ).find_best_refuel_point()

        # And the split point based on the best route from the IP. Since that's no
        # different than the best route *to* the IP, this is the same as the join point.
        # TODO: Estimate attack completion point based on the IP and split from there?
        self.package.waypoints = PackageWaypoints(
            WaypointBuilder.perturb(join_point),
            ingress_point,
            WaypointBuilder.perturb(join_point),
            refuel_point,
        )

    # TODO: Make a model for the waypoint builder and use that in the UI.
    def generate_rtb_waypoint(
        self, flight: Flight, arrival: ControlPoint
    ) -> FlightWaypoint:
        """Generate RTB landing point.

        Args:
            flight: The flight to generate the landing waypoint for.
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(flight, self.coalition)
        return builder.land(arrival)

    def package_airfield(self) -> ControlPoint:
        # We'll always have a package, but if this is being planned via the UI
        # it could be the first flight in the package.
        if not self.package.flights:
            raise PlanningError(
                "Cannot determine source airfield for package with no flights"
            )

        # The package airfield is either the flight's airfield (when there is no
        # package) or the closest airfield to the objective that is the
        # departure airfield for some flight in the package.
        cache = ObjectiveDistanceCache.get_closest_airfields(self.package.target)
        for airfield in cache.operational_airfields:
            for flight in self.package.flights:
                if flight.departure == airfield:
                    return airfield
        raise PlanningError("Could not find any airfield assigned to this package")
