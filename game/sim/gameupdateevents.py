from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from dcs import Point

if TYPE_CHECKING:
    from game.ato import Flight, Package
    from game.sim.combat import FrozenCombat
    from game.theater import ControlPoint, FrontLine, TheaterGroundObject


@dataclass
class GameUpdateEvents:
    simulation_complete = False
    new_combats: list[FrozenCombat] = field(default_factory=list)
    updated_combats: list[FrozenCombat] = field(default_factory=list)
    ended_combats: list[FrozenCombat] = field(default_factory=list)
    updated_flight_positions: list[tuple[Flight, Point]] = field(default_factory=list)
    navmesh_updates: set[bool] = field(default_factory=set)
    unculled_zones_updated: bool = False
    threat_zones_updated: bool = False
    new_flights: set[Flight] = field(default_factory=set)
    updated_flights: set[UUID] = field(default_factory=set)
    deleted_flights: set[UUID] = field(default_factory=set)
    selected_flight: UUID | None = None
    deselected_flight: bool = False
    new_front_lines: set[FrontLine] = field(default_factory=set)
    updated_front_lines: set[UUID] = field(default_factory=set)
    deleted_front_lines: set[UUID] = field(default_factory=set)
    updated_tgos: set[UUID] = field(default_factory=set)
    updated_control_points: set[int] = field(default_factory=set)
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

    def end_combat(self, combat: FrozenCombat) -> None:
        self.ended_combats.append(combat)

    def update_flight_position(
        self, flight: Flight, new_position: Point
    ) -> GameUpdateEvents:
        self.updated_flight_positions.append((flight, new_position))
        return self

    def update_navmesh(self, player: bool) -> GameUpdateEvents:
        self.navmesh_updates.add(player)
        return self

    def update_unculled_zones(self) -> GameUpdateEvents:
        self.unculled_zones_updated = True
        return self

    def update_threat_zones(self) -> GameUpdateEvents:
        self.threat_zones_updated = True
        return self

    def new_flight(self, flight: Flight) -> GameUpdateEvents:
        self.new_flights.add(flight)
        return self

    def update_flight(self, flight: Flight) -> GameUpdateEvents:
        self.updated_flights.add(flight.id)
        return self

    def update_flights_in_package(self, package: Package) -> GameUpdateEvents:
        self.updated_flights.update({f.id for f in package.flights})
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

    def new_front_line(self, front_line: FrontLine) -> GameUpdateEvents:
        self.new_front_lines.add(front_line)
        return self

    def update_front_line(self, front_line: FrontLine) -> GameUpdateEvents:
        self.updated_front_lines.add(front_line.id)
        return self

    def delete_front_line(self, front_line: FrontLine) -> GameUpdateEvents:
        self.deleted_front_lines.add(front_line.id)
        return self

    def update_tgo(self, tgo: TheaterGroundObject) -> GameUpdateEvents:
        self.updated_tgos.add(tgo.id)
        return self

    def update_control_point(self, control_point: ControlPoint) -> GameUpdateEvents:
        self.updated_control_points.add(control_point.id)
        return self

    def shut_down(self) -> GameUpdateEvents:
        self.shutting_down = True
        return self
