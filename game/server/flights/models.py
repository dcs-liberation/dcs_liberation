from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.ato.flightstate import InFlight
from game.ato.flightstate.killed import Killed
from game.server.leaflet import LeafletPoint
from game.server.waypoints.models import FlightWaypointJs
from game.server.waypoints.routes import waypoints_for_flight

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight


class FlightJs(BaseModel):
    id: UUID
    blue: bool
    position: LeafletPoint | None
    sidc: str
    waypoints: list[FlightWaypointJs] | None

    class Config:
        title = "Flight"

    @staticmethod
    def for_flight(flight: Flight, with_waypoints: bool) -> FlightJs:
        # Don't provide a location for aircraft that aren't in the air. Later we can
        # expand the model to include the state data for the UI so that it can make its
        # own decisions about whether to draw the aircraft, but for now we'll filter
        # here.
        #
        # We also draw dead aircraft so the player has some feedback about what's being
        # lost.
        position = None
        if isinstance(flight.state, InFlight) or isinstance(flight.state, Killed):
            position = flight.position().latlng()
        waypoints = None
        if with_waypoints:
            waypoints = waypoints_for_flight(flight)
        return FlightJs(
            id=flight.id,
            blue=flight.blue,
            position=position,
            sidc=str(flight.sidc()),
            waypoints=waypoints,
        )

    @staticmethod
    def all_in_game(game: Game, with_waypoints: bool) -> list[FlightJs]:
        flights = []
        for coalition in game.coalitions:
            for package in coalition.ato.packages:
                for flight in package.flights:
                    flights.append(FlightJs.for_flight(flight, with_waypoints))
        return flights
