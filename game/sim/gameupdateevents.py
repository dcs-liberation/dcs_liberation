from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from dcs import Point
from dcs.mapping import LatLng

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight, Package
    from game.navmesh import NavMesh
    from game.sim.combat import FrozenCombat
    from game.theater import ControlPoint, FrontLine, TheaterGroundObject
    from game.threatzones import ThreatZones
    from game.theater.iadsnetwork.iadsnetwork import IadsNetworkNode


@dataclass
class GameUpdateEvents:
    simulation_complete = False
    new_combats: list[FrozenCombat] = field(default_factory=list)
    updated_combats: list[FrozenCombat] = field(default_factory=list)
    ended_combats: list[FrozenCombat] = field(default_factory=list)
    updated_flight_positions: list[tuple[Flight, Point]] = field(default_factory=list)
    navmesh_updates: dict[bool, NavMesh] = field(default_factory=dict)
    unculled_zones_updated: list[Point] = field(default_factory=list)
    threat_zones_updated: dict[bool, ThreatZones] = field(default_factory=dict)
    new_flights: set[Flight] = field(default_factory=set)
    updated_flights: set[Flight] = field(default_factory=set)
    deleted_flights: set[UUID] = field(default_factory=set)
    selected_flight: UUID | None = None
    deselected_flight: bool = False
    updated_front_lines: set[FrontLine] = field(default_factory=set)
    deleted_front_lines: set[UUID] = field(default_factory=set)
    updated_tgos: set[TheaterGroundObject] = field(default_factory=set)
    updated_control_points: set[ControlPoint] = field(default_factory=set)
    updated_iads: set[IadsNetworkNode] = field(default_factory=set)
    deleted_iads_connections: set[UUID] = field(default_factory=set)
    reset_on_map_center: LatLng | None = None
    game_unloaded: bool = False
    new_turn: bool = False
    shutting_down: bool = False

    @property
    def empty(self) -> bool:
        return self == GameUpdateEvents()

    def complete_simulation(self) -> GameUpdateEvents:
        self.simulation_complete = True
        return self

    def new_combat(self, combat: FrozenCombat) -> GameUpdateEvents:
        self.new_combats.append(combat)
        return self

    def update_combat(self, combat: FrozenCombat) -> GameUpdateEvents:
        self.updated_combats.append(combat)
        return self

    def end_combat(self, combat: FrozenCombat) -> GameUpdateEvents:
        self.ended_combats.append(combat)
        return self

    def update_flight_position(
        self, flight: Flight, new_position: Point
    ) -> GameUpdateEvents:
        self.updated_flight_positions.append((flight, new_position))
        return self

    def update_navmesh(self, player: bool, navmesh: NavMesh) -> GameUpdateEvents:
        self.navmesh_updates[player] = navmesh
        return self

    def update_unculled_zones(self, zones: list[Point]) -> GameUpdateEvents:
        self.unculled_zones_updated = zones
        return self

    def update_threat_zones(self, player: bool, zones: ThreatZones) -> GameUpdateEvents:
        self.threat_zones_updated[player] = zones
        return self

    def new_flight(self, flight: Flight) -> GameUpdateEvents:
        self.new_flights.add(flight)
        return self

    def update_flight(self, flight: Flight) -> GameUpdateEvents:
        self.updated_flights.add(flight)
        return self

    def update_flights_in_package(self, package: Package) -> GameUpdateEvents:
        self.updated_flights.update({f for f in package.flights})
        return self

    def delete_flight(self, flight: Flight) -> GameUpdateEvents:
        self.deleted_flights.add(flight.id)
        return self

    def delete_flights_in_package(self, package: Package) -> GameUpdateEvents:
        self.deleted_flights.update({f.id for f in package.flights})
        return self

    def select_flight(self, flight: Flight) -> GameUpdateEvents:
        self.selected_flight = flight.id
        self.deselected_flight = False
        return self

    def deselect_flight(self) -> GameUpdateEvents:
        self.deselected_flight = True
        self.selected_flight = None
        return self

    def update_front_line(self, front_line: FrontLine) -> GameUpdateEvents:
        self.updated_front_lines.add(front_line)
        return self

    def delete_front_line(self, front_line: FrontLine) -> GameUpdateEvents:
        self.deleted_front_lines.add(front_line.id)
        return self

    def update_tgo(self, tgo: TheaterGroundObject) -> GameUpdateEvents:
        self.updated_tgos.add(tgo)
        return self

    def update_control_point(self, control_point: ControlPoint) -> GameUpdateEvents:
        self.updated_control_points.add(control_point)
        return self

    def update_iads_node(self, iads_node: IadsNetworkNode) -> GameUpdateEvents:
        self.updated_iads.add(iads_node)
        return self

    def delete_iads_connection(self, connection_id: UUID) -> GameUpdateEvents:
        self.deleted_iads_connections.add(connection_id)
        return self

    def game_loaded(self, game: Game | None) -> GameUpdateEvents:
        if game is None:
            self.game_unloaded = True
            self.reset_on_map_center = None
        else:
            self.reset_on_map_center = (
                game.theater.terrain.map_view_default.position.latlng()
            )
            self.game_unloaded = False
        return self

    def begin_new_turn(self) -> GameUpdateEvents:
        self.new_turn = True
        return self

    def shut_down(self) -> GameUpdateEvents:
        self.shutting_down = True
        return self
