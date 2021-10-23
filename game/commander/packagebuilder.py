from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from game.utils import nautical_miles
from ..ato.package import Package
from game.theater import MissionTarget, OffMapSpawn, ControlPoint
from ..ato.flight import Flight
from ..ato.starttype import StartType
from ..settings import Settings

if TYPE_CHECKING:
    from game.dcs.aircrafttype import AircraftType
    from game.squadrons.airwing import AirWing
    from gen.flights.closestairfields import ClosestAirfields
    from .missionproposals import ProposedFlight


class PackageBuilder:
    """Builds a Package for the flights it receives."""

    def __init__(
        self,
        location: MissionTarget,
        closest_airfields: ClosestAirfields,
        air_wing: AirWing,
        is_player: bool,
        package_country: str,
        start_type: StartType,
        asap: bool,
        settings: Settings,
    ) -> None:
        self.closest_airfields = closest_airfields
        self.is_player = is_player
        self.package_country = package_country
        self.package = Package(location, auto_asap=asap)
        self.air_wing = air_wing
        self.start_type = start_type
        self.settings = settings

    def plan_flight(self, plan: ProposedFlight) -> bool:
        """Allocates aircraft for the given flight and adds them to the package.

        If no suitable aircraft are available, False is returned. If the failed
        flight was critical and the rest of the mission will be scrubbed, the
        caller should return any previously planned flights to the inventory
        using release_planned_aircraft.
        """
        squadron = self.air_wing.best_squadron_for(
            self.package.target, plan.task, plan.num_aircraft, this_turn=True
        )
        if squadron is None:
            return False
        start_type = squadron.location.required_aircraft_start_type
        if start_type is None:
            start_type = self.start_type

        flight = Flight(
            self.settings,
            self.package,
            self.package_country,
            squadron,
            plan.num_aircraft,
            plan.task,
            start_type,
            divert=self.find_divert_field(squadron.aircraft, squadron.location),
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
            flight.return_pilots_and_aircraft()
            self.package.remove_flight(flight)
