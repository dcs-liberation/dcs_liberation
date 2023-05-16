from __future__ import annotations

import logging
from datetime import datetime
from functools import cached_property
from typing import Any, Dict, List, TYPE_CHECKING

from dcs.country import Country
from dcs.mission import Mission
from dcs.terrain.terrain import NoParkingSlotError
from dcs.unitgroup import FlyingGroup, StaticGroup

from game.ato.airtaaskingorder import AirTaskingOrder
from game.ato.flight import Flight
from game.ato.flightstate import Completed
from game.ato.flighttype import FlightType
from game.ato.package import Package
from game.ato.starttype import StartType
from game.factions.faction import Faction
from game.missiongenerator.missiondata import MissionData
from game.missiongenerator.lasercoderegistry import LaserCodeRegistry
from game.radio.radios import RadioRegistry
from game.radio.tacan import TacanRegistry
from game.runways import RunwayData
from game.settings import Settings
from game.theater.controlpoint import (
    Airfield,
    ControlPoint,
    Fob,
)
from game.unitmap import UnitMap
from .aircraftpainter import AircraftPainter
from .flightdata import FlightData
from .flightgroupconfigurator import FlightGroupConfigurator
from .flightgroupspawner import FlightGroupSpawner

if TYPE_CHECKING:
    from game import Game
    from game.squadrons import Squadron


class AircraftGenerator:
    def __init__(
        self,
        mission: Mission,
        settings: Settings,
        game: Game,
        time: datetime,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        laser_code_registry: LaserCodeRegistry,
        unit_map: UnitMap,
        mission_data: MissionData,
        helipads: dict[ControlPoint, StaticGroup],
    ) -> None:
        self.mission = mission
        self.settings = settings
        self.game = game
        self.time = time
        self.radio_registry = radio_registry
        self.tacan_registy = tacan_registry
        self.laser_code_registry = laser_code_registry
        self.unit_map = unit_map
        self.flights: List[FlightData] = []
        self.mission_data = mission_data
        self.helipads = helipads

    @cached_property
    def use_client(self) -> bool:
        """True if Client should be used instead of Player."""
        blue_clients = self.client_slots_in_ato(self.game.blue.ato)
        red_clients = self.client_slots_in_ato(self.game.red.ato)
        return blue_clients + red_clients > 1

    @staticmethod
    def client_slots_in_ato(ato: AirTaskingOrder) -> int:
        total = 0
        for package in ato.packages:
            for flight in package.flights:
                total += flight.client_count
        return total

    def clear_parking_slots(self) -> None:
        for cp in self.game.theater.controlpoints:
            for parking_slot in cp.parking_slots:
                parking_slot.unit_id = None

    def generate_flights(
        self,
        country: Country,
        ato: AirTaskingOrder,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        """Adds aircraft to the mission for every flight in the ATO.

        Aircraft generation is done by walking the ATO and spawning each flight in turn.
        After the flight is generated the group is added to the UnitMap so aircraft
        deaths can be tracked.

        Args:
            country: The country from the mission to use for this ATO.
            ato: The ATO to spawn aircraft for.
            dynamic_runways: Runway data for carriers and FARPs.
        """
        for package in ato.packages:
            if not package.flights:
                continue
            for flight in package.flights:
                if flight.alive:
                    logging.info(f"Generating flight: {flight.unit_type}")
                    group = self.create_and_configure_flight(
                        flight, country, dynamic_runways
                    )
                    self.unit_map.add_aircraft(group, flight)

    def spawn_unused_aircraft(
        self, player_country: Country, enemy_country: Country
    ) -> None:
        for control_point in self.game.theater.controlpoints:
            if not isinstance(control_point, Airfield):
                continue

            faction = self.game.coalition_for(control_point.captured).faction
            if control_point.captured:
                country = player_country
            else:
                country = enemy_country

            for squadron in control_point.squadrons:
                try:
                    self._spawn_unused_for(squadron, country, faction)
                except NoParkingSlotError:
                    # If we run out of parking, stop spawning aircraft at this base.
                    break

    def _spawn_unused_for(
        self, squadron: Squadron, country: Country, faction: Faction
    ) -> None:
        assert isinstance(squadron.location, Airfield)
        for _ in range(squadron.untasked_aircraft):
            # Creating a flight even those this isn't a fragged mission lets us
            # reuse the existing debriefing code.
            # TODO: Special flight type?
            flight = Flight(
                Package(squadron.location, self.game.db.flights),
                faction.country,
                squadron,
                1,
                FlightType.BARCAP,
                StartType.COLD,
                divert=None,
            )
            flight.state = Completed(flight, self.game.settings)

            group = FlightGroupSpawner(
                flight, country, self.mission, self.helipads
            ).create_idle_aircraft()
            AircraftPainter(flight, group).apply_livery()
            self.unit_map.add_aircraft(group, flight)

    def create_and_configure_flight(
        self, flight: Flight, country: Country, dynamic_runways: Dict[str, RunwayData]
    ) -> FlyingGroup[Any]:
        """Creates and configures the flight group in the mission."""
        group = FlightGroupSpawner(
            flight, country, self.mission, self.helipads
        ).create_flight_group()
        self.flights.append(
            FlightGroupConfigurator(
                flight,
                group,
                self.game,
                self.mission,
                self.time,
                self.radio_registry,
                self.tacan_registy,
                self.laser_code_registry,
                self.mission_data,
                dynamic_runways,
                self.use_client,
                self.unit_map,
            ).configure()
        )

        wpt = group.waypoint("LANDING")
        if flight.is_helo and isinstance(flight.arrival, Fob) and wpt:
            hpad = self.helipads[flight.arrival].units.pop(0)
            wpt.helipad_id = hpad.id
            wpt.link_unit = hpad.id
            self.helipads[flight.arrival].units.append(hpad)

        return group
