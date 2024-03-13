from __future__ import annotations
from abc import ABC
import itertools
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    TYPE_CHECKING,
    TypeVar,
    Union,
)
from uuid import UUID

from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.theater import Airfield, ControlPoint

if TYPE_CHECKING:
    from game import Game
    from game.ato.flight import Flight
    from game.dcs.unittype import UnitType
    from game.sim.simulationresults import SimulationResults
    from game.transfers import CargoShip
    from game.theater import TheaterUnit
    from game.unitmap import (
        AirliftUnits,
        ConvoyUnit,
        FlyingUnit,
        FrontLineUnit,
        TheaterUnitMapping,
        UnitMap,
        SceneryObjectMapping,
    )

DEBRIEFING_LOG_EXTENSION = "log"


@dataclass(frozen=True)
class AirLosses:
    player: list[FlyingUnit]
    enemy: list[FlyingUnit]

    @property
    def losses(self) -> Iterator[FlyingUnit]:
        return itertools.chain(self.player, self.enemy)

    def by_type(self, player: bool) -> Dict[AircraftType, int]:
        losses_by_type: Dict[AircraftType, int] = defaultdict(int)
        losses = self.player if player else self.enemy
        for loss in losses:
            losses_by_type[loss.flight.unit_type] += 1
        return losses_by_type

    def surviving_flight_members(self, flight: Flight) -> int:
        losses = 0
        for loss in self.losses:
            if loss.flight == flight:
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

    player_airlifts: List[AirliftUnits] = field(default_factory=list)
    enemy_airlifts: List[AirliftUnits] = field(default_factory=list)

    player_ground_objects: List[TheaterUnitMapping] = field(default_factory=list)
    enemy_ground_objects: List[TheaterUnitMapping] = field(default_factory=list)

    player_scenery: List[SceneryObjectMapping] = field(default_factory=list)
    enemy_scenery: List[SceneryObjectMapping] = field(default_factory=list)

    player_airfields: List[Airfield] = field(default_factory=list)
    enemy_airfields: List[Airfield] = field(default_factory=list)


@dataclass(frozen=True)
class BaseCaptureEvent:
    control_point: ControlPoint
    captured_by_player: bool


@dataclass
class UnitHitpointUpdate(ABC):
    unit: Any
    hit_points: int

    @classmethod
    def from_json(
        cls, data: dict[str, Any], unit_map: UnitMap
    ) -> Optional[UnitHitpointUpdate]:
        raise NotImplementedError()

    def is_dead(self) -> bool:
        # Use hit_points > 1 to indicate unit is alive, rather than >=1 (DCS logic) to account for uncontrolled units which often have a
        # health floor of 1
        if self.hit_points > 1:
            return False
        return True

    def is_friendly(self, to_player: bool) -> bool:
        raise NotImplementedError()


@dataclass
class FlyingUnitHitPointUpdate(UnitHitpointUpdate):
    unit: FlyingUnit

    @classmethod
    def from_json(
        cls, data: dict[str, Any], unit_map: UnitMap
    ) -> Optional[FlyingUnitHitPointUpdate]:
        unit = unit_map.flight(data["name"])
        if unit is None:
            return None
        return cls(unit, int(float(data["hit_points"])))

    def is_friendly(self, to_player: bool) -> bool:
        if to_player:
            return self.unit.flight.departure.captured
        return not self.unit.flight.departure.captured


@dataclass
class TheaterUnitHitPointUpdate(UnitHitpointUpdate):
    unit: TheaterUnitMapping

    @classmethod
    def from_json(
        cls, data: dict[str, Any], unit_map: UnitMap
    ) -> Optional[TheaterUnitHitPointUpdate]:
        unit = unit_map.theater_units(data["name"])
        if unit is None:
            return None

        if unit.theater_unit.unit_type is None:
            logging.debug(
                f"Ground unit {data['name']} does not have a valid unit type."
            )
            return None

        if unit.theater_unit.hit_points is None:
            logging.debug(f"Ground unit {data['name']} does not have hit_points set.")
            return None

        sim_hit_points = int(
            float(data["hit_points"])
        )  # Hit points out of the sim i.e. new unit hit points - damage in this turn
        previous_turn_hit_points = (
            unit.theater_unit.hit_points
        )  # Hit points at the end of the previous turn
        full_health_hit_points = (
            unit.theater_unit.unit_type.hit_points
        )  # Hit points of a new unit

        # Hit points left after damage this turn is subtracted from hit points at the end of the previous turn
        new_hit_points = previous_turn_hit_points - (
            full_health_hit_points - sim_hit_points
        )

        return cls(unit, new_hit_points)

    def is_dead(self) -> bool:
        # Some TheaterUnits can start with low health of around 1, make sure we don't always kill them off.
        if (
            self.unit.theater_unit.unit_type is not None
            and self.unit.theater_unit.unit_type.hit_points is not None
            and self.unit.theater_unit.unit_type.hit_points <= 1
        ):
            return False
        return super().is_dead()

    def is_friendly(self, to_player: bool) -> bool:
        return self.unit.theater_unit.ground_object.is_friendly(to_player)

    def commit(self) -> None:
        self.unit.theater_unit.hit_points = self.hit_points


@dataclass(frozen=True)
class StateData:
    #: True if the mission ended. If False, the mission exited abnormally.
    mission_ended: bool

    #: Names of aircraft units that were killed during the mission.
    killed_aircraft: List[str]

    #: Names of vehicles, ships or buildings that were killed during the mission.
    killed_ground_units: List[str]

    #: List of descriptions of destroyed statics. Format of each element is a mapping of
    #: the coordinate type ("x", "y", "z", "type", "orientation") to the value.
    destroyed_statics: List[dict[str, Union[float, str]]]

    #: Mangled names of bases that were captured during the mission.
    base_capture_events: List[str]

    # List of descriptions of damage done to units. Each list element is a dict like the following
    # {"name": "<damaged unit name>", "hit_points": <hit points as float>}
    unit_hit_point_updates: List[dict[str, Any]]

    @classmethod
    def from_json(cls, data: Dict[str, Any], unit_map: UnitMap) -> StateData:
        def clean_unit_list(unit_list: List[Any]) -> List[str]:
            # Cleans list of units in state.json by
            # - Removing duplicates. Airfields emit a new "dead" event every time a bomb
            #   is dropped on them when they've already dead.
            # - Normalise dead map objects (which are ints) to strings. The unit map
            #   only stores strings
            units = set()
            for unit in unit_list:
                units.add(str(unit))
            return list(units)

        killed_aircraft = []
        killed_ground_units = []

        # Process killed units from S_EVENT_UNIT_LOST, S_EVENT_CRASH, S_EVENT_DEAD & S_EVENT_KILL
        # Try to process every event that could indicate a unit was killed, even if it is
        # inefficient and results in duplication as the logic DCS uses to trigger the various
        # event types is not clear and may change over time.
        killed_units = clean_unit_list(
            data["unit_lost_events"]
            + data["kill_events"]
            + data["crash_events"]
            + data["dead_events"]
            + data["killed_ground_units"]
        )
        for unit in killed_units:  # organize killed units into aircraft vs ground
            if unit_map.flight(unit) is not None:
                killed_aircraft.append(unit)
            else:
                killed_ground_units.append(unit)

        return cls(
            mission_ended=data["mission_ended"],
            killed_aircraft=killed_aircraft,
            killed_ground_units=killed_ground_units,
            destroyed_statics=data["destroyed_objects_positions"],
            base_capture_events=data["base_capture_events"],
            unit_hit_point_updates=data["unit_hit_point_updates"],
        )


class Debriefing:
    def __init__(
        self, state_data: Dict[str, Any], game: Game, unit_map: UnitMap
    ) -> None:
        self.state_data = StateData.from_json(state_data, unit_map)
        self.game = game
        self.unit_map = unit_map

        self.player_country = game.blue.country_name
        self.enemy_country = game.red.country_name

        self.air_losses = self.dead_aircraft()
        self.ground_losses = self.dead_ground_units()
        self.base_captures = self.base_capture_events()

    def merge_simulation_results(self, results: SimulationResults) -> None:
        for air_loss in results.air_losses:
            if air_loss.flight.squadron.player:
                self.air_losses.player.append(air_loss)
            else:
                self.air_losses.enemy.append(air_loss)

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
    def airlift_losses(self) -> Iterator[AirliftUnits]:
        yield from self.ground_losses.player_airlifts
        yield from self.ground_losses.enemy_airlifts

    @property
    def ground_object_losses(self) -> Iterator[TheaterUnitMapping]:
        yield from self.ground_losses.player_ground_objects
        yield from self.ground_losses.enemy_ground_objects

    @property
    def scenery_object_losses(self) -> Iterator[SceneryObjectMapping]:
        yield from self.ground_losses.player_scenery
        yield from self.ground_losses.enemy_scenery

    @property
    def damaged_runways(self) -> Iterator[Airfield]:
        yield from self.ground_losses.player_airfields
        yield from self.ground_losses.enemy_airfields

    def casualty_count(self, control_point: ControlPoint) -> int:
        return len([x for x in self.front_line_losses if x.origin == control_point])

    def front_line_losses_by_type(self, player: bool) -> dict[GroundUnitType, int]:
        losses_by_type: dict[GroundUnitType, int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_front_line
        else:
            losses = self.ground_losses.enemy_front_line
        for loss in losses:
            losses_by_type[loss.unit_type] += 1
        return losses_by_type

    def convoy_losses_by_type(self, player: bool) -> dict[GroundUnitType, int]:
        losses_by_type: dict[GroundUnitType, int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_convoy
        else:
            losses = self.ground_losses.enemy_convoy
        for loss in losses:
            losses_by_type[loss.unit_type] += 1
        return losses_by_type

    def cargo_ship_losses_by_type(self, player: bool) -> dict[GroundUnitType, int]:
        losses_by_type: dict[GroundUnitType, int] = defaultdict(int)
        if player:
            ships = self.ground_losses.player_cargo_ships
        else:
            ships = self.ground_losses.enemy_cargo_ships
        for ship in ships:
            for unit_type, count in ship.units.items():
                losses_by_type[unit_type] += count
        return losses_by_type

    def airlift_losses_by_type(self, player: bool) -> dict[GroundUnitType, int]:
        losses_by_type: dict[GroundUnitType, int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_airlifts
        else:
            losses = self.ground_losses.enemy_airlifts
        for loss in losses:
            for unit_type in loss.cargo:
                losses_by_type[unit_type] += 1
        return losses_by_type

    def ground_object_losses_by_type(self, player: bool) -> Dict[str, int]:
        losses_by_type: Dict[str, int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_ground_objects
        else:
            losses = self.ground_losses.enemy_ground_objects
        for loss in losses:
            losses_by_type[loss.theater_unit.type.id] += 1
        return losses_by_type

    def scenery_losses_by_type(self, player: bool) -> Dict[str, int]:
        losses_by_type: Dict[str, int] = defaultdict(int)
        if player:
            losses = self.ground_losses.player_scenery
        else:
            losses = self.ground_losses.enemy_scenery
        for loss in losses:
            losses_by_type[loss.trigger_zone.name] += 1
        return losses_by_type

    def dead_aircraft(self) -> AirLosses:
        player_losses = []
        enemy_losses = []
        for unit_name in self.state_data.killed_aircraft:
            aircraft = self.unit_map.flight(unit_name)
            if aircraft is None:
                logging.error(f"Could not find Flight matching {unit_name}")
                continue
            if aircraft.flight.departure.captured:
                player_losses.append(aircraft)
            else:
                enemy_losses.append(aircraft)

        for unit_data in self.state_data.unit_hit_point_updates:
            damaged_unit = FlyingUnitHitPointUpdate.from_json(unit_data, self.unit_map)
            if damaged_unit is None:
                continue
            if damaged_unit.is_dead():
                # If unit already killed, nothing to do.
                if unit_data["name"] in self.state_data.killed_aircraft:
                    continue
                if damaged_unit.is_friendly(to_player=True):
                    player_losses.append(damaged_unit.unit)
                else:
                    enemy_losses.append(damaged_unit.unit)
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

            ground_object = self.unit_map.theater_units(unit_name)
            if ground_object is not None:
                if ground_object.theater_unit.ground_object.is_friendly(to_player=True):
                    losses.player_ground_objects.append(ground_object)
                else:
                    losses.enemy_ground_objects.append(ground_object)
                continue

            scenery_object = self.unit_map.scenery_object(unit_name)
            # Try appending object to the name, because we do this for building statics.
            if scenery_object is not None:
                if scenery_object.ground_unit.ground_object.is_friendly(to_player=True):
                    losses.player_scenery.append(scenery_object)
                else:
                    losses.enemy_scenery.append(scenery_object)
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

        for unit_data in self.state_data.unit_hit_point_updates:
            damaged_unit = TheaterUnitHitPointUpdate.from_json(unit_data, self.unit_map)
            if damaged_unit is None:
                continue
            if damaged_unit.is_dead():
                if unit_data["name"] in self.state_data.killed_ground_units:
                    continue
                if damaged_unit.is_friendly(to_player=True):
                    losses.player_ground_objects.append(damaged_unit.unit)
                else:
                    losses.enemy_ground_objects.append(damaged_unit.unit)

        return losses

    def unit_hit_point_update_events(self) -> List[TheaterUnitHitPointUpdate]:
        damaged_units = []
        for unit_data in self.state_data.unit_hit_point_updates:
            unit = TheaterUnitHitPointUpdate.from_json(unit_data, self.unit_map)
            if unit is None:
                continue
            damaged_units.append(unit)
        return damaged_units

    def base_capture_events(self) -> List[BaseCaptureEvent]:
        """Keeps only the last instance of a base capture event for each base ID."""
        blue_coalition_id = 2
        seen = set()
        captures = []
        for capture in reversed(self.state_data.base_capture_events):
            # The ID string in the JSON file will be the UUID generated from liberation
            cp_id, new_owner_id_str, _name = capture.split("||")

            # Only the most recent capture event matters.
            if cp_id in seen:
                continue
            seen.add(cp_id)

            try:
                control_point = self.game.theater.find_control_point_by_id(UUID(cp_id))
            except (KeyError, ValueError):
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
