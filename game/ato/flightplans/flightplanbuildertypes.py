from __future__ import annotations

from typing import Any, TYPE_CHECKING, Type

from game.ato import FlightType
from game.theater.controlpoint import NavalControlPoint
from game.theater.frontline import FrontLine
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
from .ibuilder import IBuilder
from .ocaaircraft import OcaAircraftFlightPlan
from .ocarunway import OcaRunwayFlightPlan
from .packagerefueling import PackageRefuelingFlightPlan
from .planningerror import PlanningError
from .sead import SeadFlightPlan
from .shiprecoverytanker import RecoveryTankerFlightPlan
from .strike import StrikeFlightPlan
from .sweep import SweepFlightPlan
from .tarcap import TarCapFlightPlan
from .theaterrefueling import TheaterRefuelingFlightPlan

if TYPE_CHECKING:
    from game.ato import Flight


class FlightPlanBuilderTypes:
    @staticmethod
    def for_flight(flight: Flight) -> Type[IBuilder[Any, Any]]:
        if flight.flight_type is FlightType.REFUELING:
            target = flight.package.target
            if target.is_friendly(flight.squadron.player) and isinstance(
                target, NavalControlPoint
            ):
                return RecoveryTankerFlightPlan.builder_type()
            if target.is_friendly(flight.squadron.player) or isinstance(
                target, FrontLine
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
