from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.server.combat.models import FrozenCombatJs
from game.server.leaflet import LeafletLatLon

if TYPE_CHECKING:
    from game import Game
    from game.sim import GameUpdateEvents


class GameUpdateEventsJs(BaseModel):
    updated_flights: dict[UUID, LeafletLatLon]
    new_combats: list[FrozenCombatJs] = []
    updated_combats: list[FrozenCombatJs] = []
    navmesh_updates: set[bool] = set()

    @classmethod
    def from_events(cls, events: GameUpdateEvents, game: Game) -> GameUpdateEventsJs:
        return GameUpdateEventsJs(
            updated_flights={
                f[0].id: f[1].latlng().as_list() for f in events.updated_flights
            },
            new_combats=[
                FrozenCombatJs.for_combat(c, game.theater) for c in events.new_combats
            ],
            updated_combats=[
                FrozenCombatJs.for_combat(c, game.theater)
                for c in events.updated_combats
            ],
            navmesh_updates=events.navmesh_updates,
        )
