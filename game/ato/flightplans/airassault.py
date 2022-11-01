from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterator, TYPE_CHECKING, Type

from game.ato.flightplans.standard import StandardFlightPlan, StandardLayout
from game.theater.controlpoint import ControlPointType
from game.theater.missiontarget import MissionTarget
from game.utils import Distance, feet, meters
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class AirAssaultLayout(StandardLayout):
    # The pickup point is optional because we don't always need to load the cargo. When
    # departing from a carrier, LHA, or off-map spawn, the cargo is pre-loaded.
    pickup: FlightWaypoint | None
    nav_to_drop_off: list[FlightWaypoint]
    drop_off: FlightWaypoint
    # This is an implementation detail used by CTLD. The aircraft will not go to this
    # waypoint. It is used by CTLD as the destination for unloaded troops.
    target: FlightWaypoint
    nav_to_home: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        if self.pickup is not None:
            yield self.pickup
        yield from self.nav_to_drop_off
        yield self.drop_off
        yield self.target
        yield from self.nav_to_home
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class AirAssaultFlightPlan(StandardFlightPlan[AirAssaultLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.drop_off

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.tot_waypoint:
            return self.tot
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def engagement_distance(self) -> Distance:
        # The radius of the WaypointZone created at the target location
        return meters(2500)

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target


class Builder(IBuilder[AirAssaultFlightPlan, AirAssaultLayout]):
    def layout(self) -> AirAssaultLayout:
        if not self.flight.is_helo:
            raise PlanningError("Air assault is only usable by helicopters")

        altitude = feet(1500) if self.flight.is_helo else self.doctrine.ingress_altitude
        altitude_is_agl = self.flight.is_helo

        builder = WaypointBuilder(self.flight, self.coalition)

        if not self.flight.is_helo or self.flight.departure.cptype in [
            ControlPointType.AIRCRAFT_CARRIER_GROUP,
            ControlPointType.LHA_GROUP,
            ControlPointType.OFF_MAP,
        ]:
            # Non-Helo flights or Off_Map will be preloaded
            # Carrier operations load the logistics directly from the carrier
            pickup = None
            pickup_position = self.flight.departure.position
        else:
            # Create a special pickup zone for Helos from Airbase / FOB
            pickup = builder.cargo_pickup(
                MissionTarget(
                    "Pickup Zone",
                    self.flight.departure.position.random_point_within(1200, 600),
                ),
                self.flight.is_helo,
            )
            pickup_position = pickup.position
        assault_area = builder.assault_area(self.package.target)
        heading = self.package.target.position.heading_between_point(pickup_position)

        # Once there is a plane which is capable of AirDrop Paratrooper
        # we can make use of the AIRDROP Wayppoint type.
        # This would also need a special Waypointbuilder.
        # Currently AirAssault can only be used by Helos so we just create
        # the drop_off Landing Zone
        drop_off_zone = MissionTarget(
            "Dropoff zone",
            self.package.target.position.point_from_heading(heading, 1200),
        )

        return AirAssaultLayout(
            departure=builder.takeoff(self.flight.departure),
            pickup=pickup,
            nav_to_drop_off=builder.nav_path(
                pickup_position,
                drop_off_zone.position,
                altitude,
                altitude_is_agl,
            ),
            drop_off=builder.air_assault_dropoff(drop_off_zone),
            target=assault_area,
            nav_to_home=builder.nav_path(
                drop_off_zone.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> AirAssaultFlightPlan:
        return AirAssaultFlightPlan(self.flight, self.layout())
