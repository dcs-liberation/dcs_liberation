from abc import ABC

from dcs import Point

from game.ato.flightstate import FlightState


class AtDeparture(FlightState, ABC):
    def estimate_position(self) -> Point:
        return self.flight.departure.position
