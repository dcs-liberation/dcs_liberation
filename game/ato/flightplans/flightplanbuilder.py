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
