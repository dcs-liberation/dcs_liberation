from __future__ import annotations

import logging
import random
from functools import cached_property
from typing import Any, Dict, List, TYPE_CHECKING, Type, Union

from dcs import helicopters
from dcs.country import Country
from dcs.mapping import Point
from dcs.mission import Mission, StartType as DcsStartType
from dcs.planes import (
    Su_33,
)
from dcs.point import PointAction
from dcs.ships import KUZNECOW
from dcs.terrain.terrain import Airport, NoParkingSlotError
from dcs.unitgroup import FlyingGroup, ShipGroup, StaticGroup
from dcs.unittype import FlyingType

from game.ato.airtaaskingorder import AirTaskingOrder
from game.ato.flight import Flight
from game.ato.flighttype import FlightType
from game.ato.package import Package
from game.ato.starttype import StartType
from game.factions.faction import Faction
from game.missiongenerator.airsupport import AirSupport
from game.missiongenerator.lasercoderegistry import LaserCodeRegistry
from game.radio.radios import RadioRegistry
from game.radio.tacan import TacanRegistry
from game.settings import Settings
from game.theater.controlpoint import (
    Airfield,
    ControlPoint,
    NavalControlPoint,
    OffMapSpawn,
)
from game.unitmap import UnitMap
from game.utils import meters
from gen.flights.traveltime import GroundSpeed
from gen.naming import namegen
from gen.runways import RunwayData
from .aircraftpainter import AircraftPainter
from .flightdata import FlightData
from .flightgroupconfigurator import FlightGroupConfigurator

if TYPE_CHECKING:
    from game import Game
    from game.squadrons import Squadron

WARM_START_HELI_ALT = meters(500)
WARM_START_ALTITUDE = meters(3000)

RTB_ALTITUDE = meters(800)
RTB_DISTANCE = 5000
HELI_ALT = 500


class AircraftGenerator:
    def __init__(
        self,
        mission: Mission,
        settings: Settings,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        laser_code_registry: LaserCodeRegistry,
        unit_map: UnitMap,
        air_support: AirSupport,
        helipads: dict[ControlPoint, list[StaticGroup]],
    ) -> None:
        self.m = mission
        self.game = game
        self.settings = settings
        self.radio_registry = radio_registry
        self.tacan_registy = tacan_registry
        self.laser_code_registry = laser_code_registry
        self.unit_map = unit_map
        self.flights: List[FlightData] = []
        self.air_support = air_support
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

    @staticmethod
    def _start_type(start_type: str) -> DcsStartType:
        if start_type == "Runway":
            return DcsStartType.Runway
        elif start_type == "Cold":
            return DcsStartType.Cold
        return DcsStartType.Warm

    @staticmethod
    def _start_type_at_group(
        start_type: str,
        unit_type: Type[FlyingType],
        at: Union[ShipGroup, StaticGroup],
    ) -> DcsStartType:
        group_units = at.units
        # Setting Su-33s starting from the non-supercarrier Kuznetsov to take off from runway
        # to work around a DCS AI issue preventing Su-33s from taking off when set to "Takeoff from ramp" (#1352)
        if (
            unit_type.id == Su_33.id
            and group_units[0] is not None
            and group_units[0].type == KUZNECOW.id
        ):
            return DcsStartType.Runway
        else:
            return AircraftGenerator._start_type(start_type)

    def _generate_at_airport(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        airport: Airport,
    ) -> FlyingGroup[Any]:
        assert count > 0

        # TODO: Delayed runway starts should be converted to air starts for multiplayer.
        # Runway starts do not work with late activated aircraft in multiplayer. Instead
        # of spawning on the runway the aircraft will spawn on the taxiway, potentially
        # somewhere that they don't fit anyway. We should either upgrade these to air
        # starts or (less likely) downgrade to warm starts to avoid the issue when the
        # player is generating the mission for multiplayer (which would need a new
        # option).
        logging.info("airgen: {} for {} at {}".format(unit_type, side.id, airport))
        return self.m.flight_group_from_airport(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=airport,
            maintask=None,
            start_type=self._start_type(start_type),
            group_size=count,
            parking_slots=None,
        )

    def _generate_over_departure(
        self, name: str, side: Country, flight: Flight, origin: ControlPoint
    ) -> FlyingGroup[Any]:
        assert flight.count > 0
        at = origin.position

        alt_type = "RADIO"
        if isinstance(origin, OffMapSpawn):
            alt = flight.flight_plan.waypoints[0].alt
            alt_type = flight.flight_plan.waypoints[0].alt_type
        elif flight.unit_type in helicopters.helicopter_map.values():
            alt = WARM_START_HELI_ALT
        else:
            alt = WARM_START_ALTITUDE

        speed = GroundSpeed.for_flight(flight, alt)

        pos = Point(at.x + random.randint(100, 1000), at.y + random.randint(100, 1000))

        logging.info(
            "airgen: {} for {} at {} at {}".format(
                flight.unit_type, side.id, alt, int(speed.kph)
            )
        )
        group = self.m.flight_group(
            country=side,
            name=name,
            aircraft_type=flight.unit_type.dcs_unit_type,
            airport=None,
            position=pos,
            altitude=alt.meters,
            speed=speed.kph,
            maintask=None,
            group_size=flight.count,
        )

        group.points[0].alt_type = alt_type
        return group

    def _generate_at_group(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        at: Union[ShipGroup, StaticGroup],
    ) -> FlyingGroup[Any]:
        assert count > 0

        logging.info("airgen: {} for {} at unit {}".format(unit_type, side.id, at))
        return self.m.flight_group_from_unit(
            country=side,
            name=name,
            aircraft_type=unit_type,
            pad_group=at,
            maintask=None,
            start_type=self._start_type_at_group(start_type, unit_type, at),
            group_size=count,
        )

    def _generate_at_cp_helipad(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        cp: ControlPoint,
    ) -> FlyingGroup[Any]:
        assert count > 0

        logging.info(
            "airgen at cp's helipads : {} for {} at {}".format(
                unit_type, side.id, cp.name
            )
        )

        try:
            helipad = self.helipads[cp].pop()
        except IndexError as ex:
            raise RuntimeError(f"Not enough helipads available at {cp}") from ex

        group = self._generate_at_group(
            name=name,
            side=side,
            unit_type=unit_type,
            count=count,
            start_type=start_type,
            at=helipad,
        )

        # Note : A bit dirty, need better support in pydcs
        group.points[0].action = PointAction.FromGroundArea
        group.points[0].type = "TakeOffGround"
        group.units[0].heading = helipad.units[0].heading
        if start_type != "Cold":
            group.points[0].action = PointAction.FromGroundAreaHot
            group.points[0].type = "TakeOffGroundHot"

        for i in range(count - 1):
            try:
                helipad = self.helipads[cp].pop()
                group.units[1 + i].position = Point(helipad.x, helipad.y)
                group.units[1 + i].heading = helipad.units[0].heading
            except IndexError as ex:
                raise RuntimeError(f"Not enough helipads available at {cp}") from ex
        return group

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
                Package(squadron.location),
                faction.country,
                squadron,
                1,
                FlightType.BARCAP,
                StartType.COLD,
                divert=None,
            )

            group = self._generate_at_airport(
                name=namegen.next_aircraft_name(country, flight.departure.id, flight),
                side=country,
                unit_type=squadron.aircraft.dcs_unit_type,
                count=1,
                start_type="Cold",
                airport=squadron.location.airport,
            )

            group.uncontrolled = True
            AircraftPainter(flight, group).apply_livery()
            self.unit_map.add_aircraft(group, flight)

    def create_and_configure_flight(
        self, flight: Flight, country: Country, dynamic_runways: Dict[str, RunwayData]
    ) -> FlyingGroup[Any]:
        group = self.generate_planned_flight(country, flight)
        self.flights.append(
            FlightGroupConfigurator(
                flight,
                group,
                self.game,
                self.m,
                self.radio_registry,
                self.tacan_registy,
                self.laser_code_registry,
                self.air_support,
                dynamic_runways,
                self.use_client,
            ).configure()
        )
        return group

    def generate_flight_at_departure(
        self, country: Country, flight: Flight, start_type: StartType
    ) -> FlyingGroup[Any]:
        name = namegen.next_aircraft_name(country, flight.departure.id, flight)
        cp = flight.departure
        try:
            if start_type is StartType.IN_FLIGHT:
                group = self._generate_over_departure(
                    name=name, side=country, flight=flight, origin=cp
                )
                return group
            elif isinstance(cp, NavalControlPoint):
                group_name = cp.get_carrier_group_name()
                carrier_group = self.m.find_group(group_name)
                if not isinstance(carrier_group, ShipGroup):
                    raise RuntimeError(
                        f"Carrier group {carrier_group} is a "
                        "{carrier_group.__class__.__name__}, expected a ShipGroup"
                    )
                return self._generate_at_group(
                    name=name,
                    side=country,
                    unit_type=flight.unit_type.dcs_unit_type,
                    count=flight.count,
                    start_type=start_type.value,
                    at=carrier_group,
                )
            else:
                # If the flight is an helicopter flight, then prioritize dedicated helipads
                if flight.unit_type.helicopter:
                    return self._generate_at_cp_helipad(
                        name=name,
                        side=country,
                        unit_type=flight.unit_type.dcs_unit_type,
                        count=flight.count,
                        start_type=start_type.value,
                        cp=cp,
                    )

                if not isinstance(cp, Airfield):
                    raise RuntimeError(
                        f"Attempted to spawn at airfield for non-airfield {cp}"
                    )
                return self._generate_at_airport(
                    name=name,
                    side=country,
                    unit_type=flight.unit_type.dcs_unit_type,
                    count=flight.count,
                    start_type=start_type.value,
                    airport=cp.airport,
                )
        except NoParkingSlotError:
            # Generated when there is no place on Runway or on Parking Slots
            logging.exception(
                "No room on runway or parking slots. Starting from the air."
            )
            flight.start_type = StartType.IN_FLIGHT
            group = self._generate_over_departure(
                name=name, side=country, flight=flight, origin=cp
            )
            group.points[0].alt = 1500
            return group

    def generate_planned_flight(
        self, country: Country, flight: Flight
    ) -> FlyingGroup[Any]:
        return self.generate_flight_at_departure(country, flight, flight.start_type)
