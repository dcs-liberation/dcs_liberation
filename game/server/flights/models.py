from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from game.ato import Flight
from game.ato.flightstate import InFlight
from game.server.leaflet import LeafletPoint


class FlightJs(BaseModel):
    id: UUID
    blue: bool
    position: LeafletPoint | None
    sidc: str

    @staticmethod
    def for_flight(flight: Flight) -> FlightJs:
        # Don't provide a location for aircraft that aren't in the air. Later we can
        # expand the model to include the state data for the UI so that it can make its
        # own decisions about whether or not to draw the aircraft, but for now we'll
        # filter here.
        position = None
        if isinstance(flight.state, InFlight):
            position = flight.position().latlng()
        return FlightJs(
            id=flight.id, blue=flight.blue, position=position, sidc=str(flight.sidc())
        )
