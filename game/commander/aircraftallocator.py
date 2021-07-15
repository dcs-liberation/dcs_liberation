from typing import Optional, Tuple

from game.commander.missionproposals import ProposedFlight
from game.inventory import GlobalAircraftInventory
from game.squadrons import AirWing, Squadron
from game.theater import ControlPoint
from gen.flights.ai_flight_planner_db import aircraft_for_task
from gen.flights.closestairfields import ClosestAirfields
from gen.flights.flight import FlightType


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
