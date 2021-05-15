from __future__ import annotations

import itertools
import json
import logging
import os
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Type,
    TYPE_CHECKING,
)

from dcs.unittype import FlyingType, UnitType

from game import db
from game.theater import Airfield, ControlPoint
from game.transfers import CargoShip
from game.unitmap import (
    AirliftUnit,
    Building,
    ConvoyUnit,
    FrontLineUnit,
    GroundObjectUnit,
    UnitMap,
)
from gen.flights.flight import Flight

if TYPE_CHECKING:
    from game import Game

DEBRIEFING_LOG_EXTENSION = "log"


@dataclass(frozen=True)
class AirLosses:
    player: List[Flight]
    enemy: List[Flight]

    @property
    def losses(self) -> Iterator[Flight]:
        return itertools.chain(self.player, self.enemy)

    def by_type(self, player: bool) -> Dict[Type[FlyingType], int]:
        losses_by_type: Dict[Type[FlyingType], int] = defaultdict(int)
        losses = self.player if player else self.enemy
        for loss in losses:
            losses_by_type[loss.unit_type] += 1
        return losses_by_type

    def surviving_flight_members(self, flight: Flight) -> int:
        losses = 0
        for loss in self.losses:
            if loss == flight:
                losses += 1
        return flight.count - losses


@dataclass
class GroundLosses:
    player_front_line: List[FrontLineUnit] = field(default_factory=list)
    enemy_front_line: List[FrontLineUnit] = field(default_factory=list)

    player_convoy: List[ConvoyUnit] = field(default_factory=list)
    enemy_convoy: List[ConvoyUnit] = field(default_factory=list)

    player_cargo_ships: List[CargoShip] = field(default_factory=list)
    enemy_cargo_ships: List[CargoShip] = field(default_factory=list)

    player_airlifts: List[AirliftUnit] = field(default_factory=list)
    enemy_airlifts: List[AirliftUnit] = field(default_factory=list)

    player_ground_objects: List[GroundObjectUnit] = field(default_factory=list)
    enemy_ground_objects: List[GroundObjectUnit] = field(default_factory=list)

    player_buildings: List[Building] = field(default_factory=list)
    enemy_buildings: List[Building] = field(default_factory=list)

    player_airfields: List[Airfield] = field(default_factory=list)
    enemy_airfields: List[Airfield] = field(default_factory=list)


@dataclass(frozen=True)
class BaseCaptureEvent:
    control_point: ControlPoint
    captured_by_player: bool


@dataclass(frozen=True)
class StateData:
    #: True if the mission ended. If False, the mission exited abnormally.
    mission_ended: bool

    #: Names of aircraft units that were killed during the mission.
    killed_aircraft: List[str]

    #: Names of vehicle (and ship) units that were killed during the mission.
    killed_ground_units: List[str]

    #: Names of static units that were destroyed during the mission.
    destroyed_statics: List[str]

    #: Mangled names of bases that were captured during the mission.
    base_capture_events: List[str]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> StateData:
        return cls(
            mission_ended=data["mission_ended"],
            killed_aircraft=data["killed_aircrafts"],
            # Airfields emit a new "dead" event every time a bomb is dropped on
            # them when they've already dead. Dedup.
            #
            # Also normalize dead map objects (which are ints) to strings. The unit map
            # only stores strings.
            killed_ground_units=list({str(u) for u in data["killed_ground_units"]}),
            destroyed_statics=data["destroyed_objects_positions"],
            base_capture_events=data["base_capture_events"],
        )


class Debriefing:
    def __init__(
        self, state_data: Dict[str, Any], game: Game, unit_map: UnitMap
    ) -> None:
        self.state_data = StateData.from_json(state_data)
        self.game = game
        self.unit_map = unit_map

        self.player_country = game.player_country
        self.enemy_country = game.enemy_country
        self.player_country_id = db.country_id_from_name(game.player_country)
        self.enemy_country_id = db.country_id_from_name(game.enemy_country)

        self.air_losses = self.dead_aircraft()
        self.ground_losses = self.dead_ground_units()
        self.base_captures = self.base_capture_events()

    @property
    def front_line_losses(self) -> Iterator[FrontLineUnit]:
        yield from self.ground_losses.player_front_line
        yield from self.ground_losses.enemy_front_line

    @property
    def convoy_losses(self) -> Iterator[ConvoyUnit]:
        yield from self.ground_losses.player_convoy
        yield from self.ground_losses.enemy_convoy

    @property
    def cargo_ship_losses(self) -> Iterator[CargoShip]:
        yield from self.ground_losses.player_cargo_ships
        yield from self.ground_losses.enemy_cargo_ships

    @property
    def airlift_losses(self) -> Iterator[AirliftUnit]:
        yield from self.ground_losses.player_airlifts
        yield from self.ground_losses.enemy_airlifts

    @property
    def ground_object_losses(self) -> Iterator[GroundObjectUnit]:
        yield from self.ground_losses.player_ground_objects
        yield from self.ground_losses.enemy_ground_objects

    @property
    def building_losses(self) -> Iterator[Building]:
        yield from self.ground_losses.player_buildings
        yield from self.ground_losses.enemy_buildings

    @property
    def damaged_runways(self) -> Iterator[Airfield]:
        yield from self.ground_losses.player_airfields
        yield from self.ground_losses.enemy_airfields

    def casualty_count(self, control_point: ControlPoint) -> int:
        return len([x for x in self.front_line_losses if x.origin == control_point])

    def front_line_losses_by_type(self, player: bool) -> Dict[Type[UnitType], int]:
        losses_by_type: Dict[Type[UnitType], int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_front_line
        else:
            losses = self.ground_losses.enemy_front_line
        for loss in losses:
            losses_by_type[loss.unit_type] += 1
        return losses_by_type

    def convoy_losses_by_type(self, player: bool) -> Dict[Type[UnitType], int]:
        losses_by_type: Dict[Type[UnitType], int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_convoy
        else:
            losses = self.ground_losses.enemy_convoy
        for loss in losses:
            losses_by_type[loss.unit_type] += 1
        return losses_by_type

    def cargo_ship_losses_by_type(self, player: bool) -> Dict[Type[UnitType], int]:
        losses_by_type: Dict[Type[UnitType], int] = defaultdict(int)
        if player:
            ships = self.ground_losses.player_cargo_ships
        else:
            ships = self.ground_losses.enemy_cargo_ships
        for ship in ships:
            for unit_type, count in ship.units.items():
                losses_by_type[unit_type] += count
        return losses_by_type

    def airlift_losses_by_type(self, player: bool) -> Dict[Type[UnitType], int]:
        losses_by_type: Dict[Type[UnitType], int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_airlifts
        else:
            losses = self.ground_losses.enemy_airlifts
        for loss in losses:
            losses_by_type[loss.unit_type] += 1
        return losses_by_type

    def building_losses_by_type(self, player: bool) -> Dict[str, int]:
        losses_by_type: Dict[str, int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_buildings
        else:
            losses = self.ground_losses.enemy_buildings
        for loss in losses:
            if loss.ground_object.control_point.captured != player:
                continue

            losses_by_type[loss.ground_object.dcs_identifier] += 1
        return losses_by_type

    def dead_aircraft(self) -> AirLosses:
        player_losses = []
        enemy_losses = []
        for unit_name in self.state_data.killed_aircraft:
            flight = self.unit_map.flight(unit_name)
            if flight is None:
                logging.error(f"Could not find Flight matching {unit_name}")
                continue
            if flight.departure.captured:
                player_losses.append(flight)
            else:
                enemy_losses.append(flight)
        return AirLosses(player_losses, enemy_losses)

    def dead_ground_units(self) -> GroundLosses:
        losses = GroundLosses()
        for unit_name in self.state_data.killed_ground_units:
            front_line_unit = self.unit_map.front_line_unit(unit_name)
            if front_line_unit is not None:
                if front_line_unit.origin.captured:
                    losses.player_front_line.append(front_line_unit)
                else:
                    losses.enemy_front_line.append(front_line_unit)
                continue

            convoy_unit = self.unit_map.convoy_unit(unit_name)
            if convoy_unit is not None:
                if convoy_unit.convoy.player_owned:
                    losses.player_convoy.append(convoy_unit)
                else:
                    losses.enemy_convoy.append(convoy_unit)
                continue

            cargo_ship = self.unit_map.cargo_ship(unit_name)
            if cargo_ship is not None:
                if cargo_ship.player_owned:
                    losses.player_cargo_ships.append(cargo_ship)
                else:
                    losses.enemy_cargo_ships.append(cargo_ship)
                continue

            ground_object_unit = self.unit_map.ground_object_unit(unit_name)
            if ground_object_unit is not None:
                if ground_object_unit.ground_object.control_point.captured:
                    losses.player_ground_objects.append(ground_object_unit)
                else:
                    losses.enemy_ground_objects.append(ground_object_unit)
                continue

            building = self.unit_map.building_or_fortification(unit_name)
            # Try appending object to the name, because we do this for building statics.
            if building is None:
                building = self.unit_map.building_or_fortification(
                    f"{unit_name} object"
                )
            if building is not None:
                if building.ground_object.control_point.captured:
                    losses.player_buildings.append(building)
                else:
                    losses.enemy_buildings.append(building)
                continue

            airfield = self.unit_map.airfield(unit_name)
            if airfield is not None:
                if airfield.captured:
                    losses.player_airfields.append(airfield)
                else:
                    losses.enemy_airfields.append(airfield)
                continue

            # Only logging as debug because we don't currently track infantry
            # deaths, so we expect to see quite a few unclaimed dead ground
            # units. We should start tracking those and covert this to a
            # warning.
            logging.debug(
                f"Death of untracked ground unit {unit_name} will "
                "have no effect. This may be normal behavior."
            )

        for unit_name in self.state_data.killed_aircraft:
            airlift_unit = self.unit_map.airlift_unit(unit_name)
            if airlift_unit is not None:
                if airlift_unit.transfer.player:
                    losses.player_airlifts.append(airlift_unit)
                else:
                    losses.enemy_airlifts.append(airlift_unit)
                continue

        return losses

    def base_capture_events(self) -> List[BaseCaptureEvent]:
        """Keeps only the last instance of a base capture event for each base ID."""
        blue_coalition_id = 2
        seen = set()
        captures = []
        for capture in reversed(self.state_data.base_capture_events):
            cp_id_str, new_owner_id_str, _name = capture.split("||")
            cp_id = int(cp_id_str)

            # Only the most recent capture event matters.
            if cp_id in seen:
                continue
            seen.add(cp_id)

            try:
                control_point = self.game.theater.find_control_point_by_id(cp_id)
            except KeyError:
                # Captured base is not a part of the campaign. This happens when neutral
                # bases are near the conflict. Nothing to do.
                continue

            captured_by_player = int(new_owner_id_str) == blue_coalition_id
            if control_point.is_friendly(to_player=captured_by_player):
                # Base is currently friendly to the new owner. Was captured and
                # recaptured in the same mission. Nothing to do.
                continue

            captures.append(BaseCaptureEvent(control_point, captured_by_player))
        return captures


class PollDebriefingFileThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(
        self, callback: Callable[[Debriefing], None], game: Game, unit_map: UnitMap
    ) -> None:
        super().__init__()
        self._stop_event = threading.Event()
        self.callback = callback
        self.game = game
        self.unit_map = unit_map

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        if os.path.isfile("state.json"):
            last_modified = os.path.getmtime("state.json")
        else:
            last_modified = 0
        while not self.stopped():
            if (
                os.path.isfile("state.json")
                and os.path.getmtime("state.json") > last_modified
            ):
                with open("state.json", "r") as json_file:
                    json_data = json.load(json_file)
                    debriefing = Debriefing(json_data, self.game, self.unit_map)
                    self.callback(debriefing)
                break
            time.sleep(5)


def wait_for_debriefing(
    callback: Callable[[Debriefing], None], game: Game, unit_map
) -> PollDebriefingFileThread:
    thread = PollDebriefingFileThread(callback, game, unit_map)
    thread.start()
    return thread
