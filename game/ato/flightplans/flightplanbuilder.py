from __future__ import annotations

from typing import Any, TYPE_CHECKING, Type

from game.ato import FlightType
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
from .ibuilder import IBuilder
from .ocaaircraft import OcaAircraftFlightPlan
from .ocarunway import OcaRunwayFlightPlan
from .packagerefueling import PackageRefuelingFlightPlan
from .planningerror import PlanningError
from .sead import SeadFlightPlan
from .strike import StrikeFlightPlan
from .sweep import SweepFlightPlan
from .tarcap import TarCapFlightPlan
from .theaterrefueling import TheaterRefuelingFlightPlan
from ..packagewaypoints import PackageWaypoints

if TYPE_CHECKING:
    from game.ato import Flight, Package
    from game.coalition import Coalition
    from game.theater import ConflictTheater, FrontLine


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

    def populate_flight_plan(self, flight: Flight) -> None:
        """Creates a default flight plan for the given mission."""
        if flight not in self.package.flights:
            raise RuntimeError("Flight must be a part of the package")

        from game.navmesh import NavMeshError

        try:
            if self.package.waypoints is None:
                self.package.waypoints = PackageWaypoints.create(
                    self.package, self.coalition
                )
            flight.flight_plan = self.generate_flight_plan(flight)
        except NavMeshError as ex:
            color = "blue" if self.is_player else "red"
            raise PlanningError(
                f"Could not plan {color} {flight.flight_type.value} from "
                f"{flight.departure} to {flight.package.target}"
            ) from ex

    def builder_type(self, flight: Flight) -> Type[IBuilder[Any, Any]]:
        if flight.flight_type is FlightType.REFUELING:
            if self.package.target.is_friendly(self.is_player) or isinstance(
                self.package.target, FrontLine
            ):
                return TheaterRefuelingFlightPlan.builder_type()
            return PackageRefuelingFlightPlan.builder_type()

        builder_dict: dict[FlightType, Type[IBuilder[Any, Any]]] = {
            FlightType.ANTISHIP: AntiShipFlightPlan.builder_type(),
            FlightType.BAI: BaiFlightPlan.builder_type(),
            FlightType.BARCAP: BarCapFlightPlan.builder_type(),
            FlightType.CAS: CasFlightPlan.builder_type(),
            FlightType.DEAD: DeadFlightPlan.builder_type(),
            FlightType.ESCORT: EscortFlightPlan.builder_type(),
            FlightType.OCA_AIRCRAFT: OcaAircraftFlightPlan.builder_type(),
            FlightType.OCA_RUNWAY: OcaRunwayFlightPlan.builder_type(),
            FlightType.SEAD: SeadFlightPlan.builder_type(),
            FlightType.SEAD_ESCORT: EscortFlightPlan.builder_type(),
            FlightType.STRIKE: StrikeFlightPlan.builder_type(),
            FlightType.SWEEP: SweepFlightPlan.builder_type(),
            FlightType.TARCAP: TarCapFlightPlan.builder_type(),
            FlightType.AEWC: AewcFlightPlan.builder_type(),
            FlightType.TRANSPORT: AirliftFlightPlan.builder_type(),
            FlightType.FERRY: FerryFlightPlan.builder_type(),
            FlightType.AIR_ASSAULT: AirAssaultFlightPlan.builder_type(),
        }
        try:
            return builder_dict[flight.flight_type]
        except KeyError as ex:
            raise PlanningError(
                f"{flight.flight_type} flight plan generation not implemented"
            ) from ex

    def generate_flight_plan(self, flight: Flight) -> FlightPlan[Any]:
        return self.builder_type(flight)(flight).build()
