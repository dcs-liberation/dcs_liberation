from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.server.combat.models import FrozenCombatJs
from game.server.controlpoints.models import ControlPointJs
from game.server.flights.models import FlightJs
from game.server.frontlines.models import FrontLineJs
from game.server.iadsnetwork.models import IadsConnectionJs
from game.server.leaflet import LeafletPoint
from game.server.mapzones.models import ThreatZonesJs
from game.server.navmesh.models import NavMeshJs
from game.server.tgos.models import TgoJs
from game.server.mapzones.models import UnculledZoneJs

if TYPE_CHECKING:
    from game import Game
    from game.sim import GameUpdateEvents


class GameUpdateEventsJs(BaseModel):
    updated_flight_positions: dict[UUID, LeafletPoint]
    new_combats: list[FrozenCombatJs]
    updated_combats: list[FrozenCombatJs]
    ended_combats: list[UUID]
    navmesh_updates: dict[bool, NavMeshJs]
    updated_unculled_zones: list[UnculledZoneJs]
    threat_zones_updated: dict[bool, ThreatZonesJs]
    new_flights: list[FlightJs]
    updated_flights: list[FlightJs]
    deleted_flights: set[UUID]
    selected_flight: UUID | None
    deselected_flight: bool
    updated_front_lines: list[FrontLineJs]
    deleted_front_lines: set[UUID]
    updated_tgos: list[TgoJs]
    updated_control_points: list[ControlPointJs]
    updated_iads: list[IadsConnectionJs]
    deleted_iads: set[UUID]
    reset_on_map_center: LeafletPoint | None
    game_unloaded: bool
    new_turn: bool

    @classmethod
    def from_events(
        cls, events: GameUpdateEvents, game: Game | None
    ) -> GameUpdateEventsJs:

        # We still need to be able to send update events when there is no game loaded
        # because we need to send the unload event.
        new_combats = []
        updated_combats = []
        updated_navmeshes = {}
        updated_threat_zones = {}
        updated_unculled_zones = []
        updated_iads = []
        if game is not None:
            new_combats = [
                FrozenCombatJs.for_combat(c, game.theater) for c in events.new_combats
            ]
            updated_combats = [
                FrozenCombatJs.for_combat(c, game.theater)
                for c in events.updated_combats
            ]
            updated_navmeshes = {
                player: NavMeshJs.from_navmesh(mesh, game)
                for player, mesh in events.navmesh_updates.items()
            }
            updated_threat_zones = {
                player: ThreatZonesJs.from_zones(zones, game.theater)
                for player, zones in events.threat_zones_updated.items()
            }
            updated_unculled_zones = UnculledZoneJs.from_game(game)
            for node in events.updated_iads:
                updated_iads.extend(IadsConnectionJs.connections_for_node(node))

        return GameUpdateEventsJs(
            updated_flight_positions={
                f[0].id: f[1].latlng() for f in events.updated_flight_positions
            },
            new_combats=new_combats,
            updated_combats=updated_combats,
            ended_combats=[c.id for c in events.ended_combats],
            navmesh_updates=updated_navmeshes,
            updated_unculled_zones=updated_unculled_zones,
            threat_zones_updated=updated_threat_zones,
            new_flights=[
                FlightJs.for_flight(f, with_waypoints=True) for f in events.new_flights
            ],
            updated_flights=[
                FlightJs.for_flight(f, with_waypoints=True)
                for f in events.updated_flights
            ],
            deleted_flights=events.deleted_flights,
            selected_flight=events.selected_flight,
            deselected_flight=events.deselected_flight,
            updated_front_lines=[
                FrontLineJs.for_front_line(f) for f in events.updated_front_lines
            ],
            deleted_front_lines=events.deleted_front_lines,
            updated_tgos=[TgoJs.for_tgo(tgo) for tgo in events.updated_tgos],
            updated_control_points=[
                ControlPointJs.for_control_point(cp)
                for cp in events.updated_control_points
            ],
            updated_iads=updated_iads,
            deleted_iads=events.deleted_iads_connections,
            reset_on_map_center=events.reset_on_map_center,
            game_unloaded=events.game_unloaded,
            new_turn=events.new_turn,
        )
