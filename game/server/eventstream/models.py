from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.server.combat.models import FrozenCombatJs
from game.server.flights.models import FlightJs
from game.server.frontlines.models import FrontLineJs
from game.server.leaflet import LeafletLatLon

if TYPE_CHECKING:
    from game import Game
    from game.sim import GameUpdateEvents


class GameUpdateEventsJs(BaseModel):
    updated_flight_positions: dict[UUID, LeafletLatLon]
    new_combats: list[FrozenCombatJs]
    updated_combats: list[FrozenCombatJs]
    ended_combats: list[UUID]
    navmesh_updates: set[bool]
    unculled_zones_updated: bool
    threat_zones_updated: bool
    new_flights: list[FlightJs]
    updated_flights: set[UUID]
    deleted_flights: set[UUID]
    selected_flight: UUID | None
    deselected_flight: bool
    new_front_lines: list[FrontLineJs]
    updated_front_lines: set[UUID]
    deleted_front_lines: set[UUID]

    @classmethod
    def from_events(cls, events: GameUpdateEvents, game: Game) -> GameUpdateEventsJs:
        return GameUpdateEventsJs(
            updated_flight_positions={
                f[0].id: f[1].latlng().as_list()
                for f in events.updated_flight_positions
            },
            new_combats=[
                FrozenCombatJs.for_combat(c, game.theater) for c in events.new_combats
            ],
            updated_combats=[
                FrozenCombatJs.for_combat(c, game.theater)
                for c in events.updated_combats
            ],
            ended_combats=[c.id for c in events.ended_combats],
            navmesh_updates=events.navmesh_updates,
            unculled_zones_updated=events.unculled_zones_updated,
            threat_zones_updated=events.threat_zones_updated,
            new_flights=[
                FlightJs.for_flight(f, with_waypoints=True) for f in events.new_flights
            ],
            updated_flights=events.updated_flights,
            deleted_flights=events.deleted_flights,
            selected_flight=events.selected_flight,
            deselected_flight=events.deselected_flight,
            new_front_lines=[
                FrontLineJs.for_front_line(f) for f in events.new_front_lines
            ],
            updated_front_lines=events.updated_front_lines,
            deleted_front_lines=events.deleted_front_lines,
        )
