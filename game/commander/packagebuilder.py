from typing import Optional

from game.commander.missionproposals import ProposedFlight
from game.dcs.aircrafttype import AircraftType
from game.inventory import GlobalAircraftInventory
from game.squadrons.airwing import AirWing
from game.theater import MissionTarget, OffMapSpawn, ControlPoint
from game.utils import nautical_miles
from gen.ato import Package
from game.commander.aircraftallocator import AircraftAllocator
from gen.flights.closestairfields import ClosestAirfields
from gen.flights.flight import Flight


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
        assignment = self.allocator.find_squadron_for_flight(self.package.target, plan)
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
