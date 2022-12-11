from dataclasses import dataclass
from typing import Iterator, Type
from game.ato.flightplans.standard import StandardFlightPlan, StandardLayout
from game.ato.flightplans.ibuilder import IBuilder
from game.ato.flightplans.standard import StandardLayout
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.ato.flightwaypoint import FlightWaypoint
from game.utils import feet


@dataclass(frozen=True)
class RecoveryTankerLayout(StandardLayout):
    nav_to: list[FlightWaypoint]
    recovery_ship: FlightWaypoint
    nav_from: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.recovery_ship
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class RecoveryTankerFlightPlan(StandardFlightPlan[RecoveryTankerLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(IBuilder[RecoveryTankerFlightPlan, RecoveryTankerLayout]):
    def layout(self) -> RecoveryTankerLayout:

        # TODO: Propagate the ship position.
        ship = self.package.target.position

        builder = WaypointBuilder(self.flight, self.coalition)

        recovery = builder.recovery_tanker(ship)

        tanker_type = self.flight.unit_type
        if tanker_type.ingress_altitude is not None:
            altitude = self.doctrine.ingress_altitude
        else:
            altitude = feet(21000)

        return RecoveryTankerLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(self.flight.departure.position, ship, altitude),
            nav_from=builder.nav_path(ship, self.flight.arrival.position, altitude),
            recovery_ship=recovery,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> RecoveryTankerFlightPlan:
        return RecoveryTankerFlightPlan(self.flight, self.layout())
