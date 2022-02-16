from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletLatLon

if TYPE_CHECKING:
    from game import Game
    from game.sim.gameupdateevents import GameUpdateEvents


class GameUpdateEventsJs(BaseModel):
    updated_flights: dict[UUID, LeafletLatLon]

    @classmethod
    def from_events(cls, events: GameUpdateEvents, game: Game) -> GameUpdateEventsJs:
        return GameUpdateEventsJs(
            updated_flights={
                f[0].id: game.theater.point_to_ll(f[1]).as_list()
                for f in events.updated_flights
            }
        )
