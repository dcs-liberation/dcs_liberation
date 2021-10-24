import logging
import random
from typing import Any, Union

from dcs import Mission, Point
from dcs.country import Country
from dcs.mission import StartType as DcsStartType
from dcs.planes import Su_33
from dcs.point import PointAction
from dcs.ships import KUZNECOW
from dcs.terrain import Airport, NoParkingSlotError
from dcs.unitgroup import FlyingGroup, ShipGroup, StaticGroup

from game.ato import Flight
from game.ato.starttype import StartType
from game.theater import Airfield, ControlPoint, NavalControlPoint, OffMapSpawn
from game.utils import meters
from gen.flights.traveltime import GroundSpeed
from gen.naming import namegen

WARM_START_HELI_ALT = meters(500)
WARM_START_ALTITUDE = meters(3000)

RTB_ALTITUDE = meters(800)
RTB_DISTANCE = 5000
HELI_ALT = 500


class FlightGroupSpawner:
    def __init__(
        self,
        flight: Flight,
        country: Country,
        mission: Mission,
        helipads: dict[ControlPoint, list[StaticGroup]],
    ) -> None:
        self.flight = flight
        self.country = country
        self.mission = mission
        self.helipads = helipads

    def create_flight_group(self) -> FlyingGroup[Any]:
        return self.generate_flight_at_departure()

    def create_idle_aircraft(self) -> FlyingGroup[Any]:
        assert isinstance(self.flight.squadron.location, Airfield)
        group = self._generate_at_airport(
            name=namegen.next_aircraft_name(
                self.country, self.flight.departure.id, self.flight
            ),
            airport=self.flight.squadron.location.airport,
        )

        group.uncontrolled = True
        return group

    def generate_flight_at_departure(self) -> FlyingGroup[Any]:
        name = namegen.next_aircraft_name(
            self.country, self.flight.departure.id, self.flight
        )
        cp = self.flight.departure
        try:
            if self.flight.get_start_type is StartType.IN_FLIGHT:
                group = self._generate_over_departure(name, cp)
                return group
            elif isinstance(cp, NavalControlPoint):
                group_name = cp.get_carrier_group_name()
                carrier_group = self.mission.find_group(group_name)
                if not isinstance(carrier_group, ShipGroup):
                    raise RuntimeError(
                        f"Carrier group {carrier_group} is a "
                        "{carrier_group.__class__.__name__}, expected a ShipGroup"
                    )
                return self._generate_at_group(name, carrier_group)
            else:
                # If the flight is an helicopter flight, then prioritize dedicated
                # helipads
                if self.flight.unit_type.helicopter:
                    return self._generate_at_cp_helipad(name, cp)

                if not isinstance(cp, Airfield):
                    raise RuntimeError(
                        f"Attempted to spawn at airfield for non-airfield {cp}"
                    )
                return self._generate_at_airport(name, cp.airport)
        except NoParkingSlotError:
            # Generated when there is no place on Runway or on Parking Slots
            logging.exception(
                "No room on runway or parking slots. Starting from the air."
            )
            self.flight.custom_start_type = StartType.IN_FLIGHT
            group = self._generate_over_departure(name, cp)
            group.points[0].alt = 1500
            return group

    def _generate_at_airport(self, name: str, airport: Airport) -> FlyingGroup[Any]:
        # TODO: Delayed runway starts should be converted to air starts for multiplayer.
        # Runway starts do not work with late activated aircraft in multiplayer. Instead
        # of spawning on the runway the aircraft will spawn on the taxiway, potentially
        # somewhere that they don't fit anyway. We should either upgrade these to air
        # starts or (less likely) downgrade to warm starts to avoid the issue when the
        # player is generating the mission for multiplayer (which would need a new
        # option).
        return self.mission.flight_group_from_airport(
            country=self.country,
            name=name,
            aircraft_type=self.flight.unit_type.dcs_unit_type,
            airport=airport,
            maintask=None,
            start_type=self.dcs_start_type(),
            group_size=self.flight.count,
            parking_slots=None,
        )

    def _generate_over_departure(
        self, name: str, origin: ControlPoint
    ) -> FlyingGroup[Any]:
        at = origin.position

        alt_type = "RADIO"
        if isinstance(origin, OffMapSpawn):
            alt = self.flight.flight_plan.waypoints[0].alt
            alt_type = self.flight.flight_plan.waypoints[0].alt_type
        elif self.flight.unit_type.helicopter:
            alt = WARM_START_HELI_ALT
        else:
            alt = WARM_START_ALTITUDE

        speed = GroundSpeed.for_flight(self.flight, alt)
        pos = Point(at.x + random.randint(100, 1000), at.y + random.randint(100, 1000))

        group = self.mission.flight_group(
            country=self.country,
            name=name,
            aircraft_type=self.flight.unit_type.dcs_unit_type,
            airport=None,
            position=pos,
            altitude=alt.meters,
            speed=speed.kph,
            maintask=None,
            group_size=self.flight.count,
        )

        group.points[0].alt_type = alt_type
        return group

    def _generate_at_group(
        self, name: str, at: Union[ShipGroup, StaticGroup]
    ) -> FlyingGroup[Any]:
        return self.mission.flight_group_from_unit(
            country=self.country,
            name=name,
            aircraft_type=self.flight.unit_type.dcs_unit_type,
            pad_group=at,
            maintask=None,
            start_type=self._start_type_at_group(at),
            group_size=self.flight.count,
        )

    def _generate_at_cp_helipad(self, name: str, cp: ControlPoint) -> FlyingGroup[Any]:
        try:
            helipad = self.helipads[cp].pop()
        except IndexError as ex:
            raise RuntimeError(f"Not enough helipads available at {cp}") from ex

        group = self._generate_at_group(name, helipad)

        # Note : A bit dirty, need better support in pydcs
        group.points[0].action = PointAction.FromGroundArea
        group.points[0].type = "TakeOffGround"
        group.units[0].heading = helipad.units[0].heading
        if self.flight.get_start_type != "Cold":
            group.points[0].action = PointAction.FromGroundAreaHot
            group.points[0].type = "TakeOffGroundHot"

        for i in range(self.flight.count - 1):
            try:
                helipad = self.helipads[cp].pop()
                group.units[1 + i].position = Point(helipad.x, helipad.y)
                group.units[1 + i].heading = helipad.units[0].heading
            except IndexError as ex:
                raise RuntimeError(f"Not enough helipads available at {cp}") from ex
        return group

    def dcs_start_type(self) -> DcsStartType:
        if self.flight.get_start_type is StartType.RUNWAY:
            return DcsStartType.Runway
        elif self.flight.get_start_type is StartType.COLD:
            return DcsStartType.Cold
        elif self.flight.get_start_type is StartType.WARM:
            return DcsStartType.Warm
        raise ValueError(
            f"There is no pydcs StartType matching {self.flight.get_start_type}"
        )

    def _start_type_at_group(
        self,
        at: Union[ShipGroup, StaticGroup],
    ) -> DcsStartType:
        group_units = at.units
        # Setting Su-33s starting from the non-supercarrier Kuznetsov to take off from
        # runway to work around a DCS AI issue preventing Su-33s from taking off when
        # set to "Takeoff from ramp" (#1352)
        if (
            self.flight.unit_type.dcs_unit_type == Su_33
            and group_units[0] is not None
            and group_units[0].type == KUZNECOW.id
        ):
            return DcsStartType.Runway
        else:
            return self.dcs_start_type()
