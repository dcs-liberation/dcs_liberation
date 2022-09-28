from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast

import dcs.lua
from dcs import Mission, Point
from dcs.coalition import Coalition
from dcs.countries import country_dict

from game.atcdata import AtcData
from game.dcs.beacons import Beacons
from game.dcs.helpers import unit_type_from_name
from game.missiongenerator.aircraft.aircraftgenerator import (
    AircraftGenerator,
)
from game.naming import namegen
from game.radio.radios import RadioFrequency, RadioRegistry
from game.radio.tacan import TacanRegistry
from game.theater import Airfield
from game.theater.bullseye import Bullseye
from game.unitmap import UnitMap
from .airconflictdescription import AirConflictDescription
from .airsupportgenerator import AirSupportGenerator
from .briefinggenerator import BriefingGenerator, MissionInfoGenerator
from .cargoshipgenerator import CargoShipGenerator
from .convoygenerator import ConvoyGenerator
from .drawingsgenerator import DrawingsGenerator
from .environmentgenerator import EnvironmentGenerator
from .flotgenerator import FlotGenerator
from .forcedoptionsgenerator import ForcedOptionsGenerator
from .frontlineconflictdescription import FrontLineConflictDescription
from .kneeboard import KneeboardGenerator
from .lasercoderegistry import LaserCodeRegistry
from .luagenerator import LuaGenerator
from .missiondata import MissionData
from .tgogenerator import TgoGenerator
from .triggergenerator import TriggerGenerator
from .visualsgenerator import VisualsGenerator

if TYPE_CHECKING:
    from game import Game


COMBINED_ARMS_SLOTS = 1


def country_id_from_name(name: str) -> int:
    for k, v in country_dict.items():
        if v.name == name:
            return k
    return -1


class MissionGenerator:
    def __init__(self, game: Game, time: datetime) -> None:
        self.game = game
        self.time = time
        self.mission = Mission(game.theater.terrain)
        self.unit_map = UnitMap()

        self.mission_data = MissionData()

        self.laser_code_registry = LaserCodeRegistry()
        self.radio_registry = RadioRegistry()
        self.tacan_registry = TacanRegistry()

        self.generation_started = False

        with open("resources/default_options.lua", "r", encoding="utf-8") as f:
            self.mission.options.load_from_dict(dcs.lua.loads(f.read())["options"])

    def generate_miz(self, output: Path) -> UnitMap:
        if self.generation_started:
            raise RuntimeError(
                "Mission has already begun generating. To reset, create a new "
                "MissionSimulation."
            )
        self.generation_started = True

        self.setup_mission_coalitions()
        self.add_airfields_to_unit_map()
        self.initialize_registries()

        EnvironmentGenerator(self.mission, self.game.conditions, self.time).generate()

        tgo_generator = TgoGenerator(
            self.mission,
            self.game,
            self.radio_registry,
            self.tacan_registry,
            self.unit_map,
            self.mission_data,
        )
        tgo_generator.generate()

        ConvoyGenerator(self.mission, self.game, self.unit_map).generate()
        CargoShipGenerator(self.mission, self.game, self.unit_map).generate()

        self.generate_destroyed_units()

        # Generate ground conflicts first so the JTACs get the first laser code (1688)
        # rather than the first player flight with a TGP.
        self.generate_ground_conflicts()
        self.generate_air_units(tgo_generator)

        TriggerGenerator(self.mission, self.game).generate()
        ForcedOptionsGenerator(self.mission, self.game).generate()
        VisualsGenerator(self.mission, self.game).generate()
        LuaGenerator(self.game, self.mission, self.mission_data).generate()
        DrawingsGenerator(self.mission, self.game).generate()

        self.setup_combined_arms()

        self.notify_info_generators()

        # TODO: Shouldn't this be first?
        namegen.reset_numbers()
        self.mission.save(output)

        return self.unit_map

    def setup_mission_coalitions(self) -> None:
        self.mission.coalition["blue"] = Coalition(
            "blue", bullseye=self.game.blue.bullseye.to_pydcs()
        )
        self.mission.coalition["red"] = Coalition(
            "red", bullseye=self.game.red.bullseye.to_pydcs()
        )
        self.mission.coalition["neutrals"] = Coalition(
            "neutrals", bullseye=Bullseye(Point(0, 0, self.mission.terrain)).to_pydcs()
        )

        p_country = self.game.blue.country_name
        e_country = self.game.red.country_name
        self.mission.coalition["blue"].add_country(
            country_dict[country_id_from_name(p_country)]()
        )
        self.mission.coalition["red"].add_country(
            country_dict[country_id_from_name(e_country)]()
        )

        belligerents = [
            country_id_from_name(p_country),
            country_id_from_name(e_country),
        ]
        for country in country_dict.keys():
            if country not in belligerents:
                self.mission.coalition["neutrals"].add_country(country_dict[country]())

    def add_airfields_to_unit_map(self) -> None:
        for control_point in self.game.theater.controlpoints:
            if isinstance(control_point, Airfield):
                self.unit_map.add_airfield(control_point)

    def initialize_registries(self) -> None:
        unique_map_frequencies: set[RadioFrequency] = set()
        self.initialize_tacan_registry(unique_map_frequencies)
        self.initialize_radio_registry(unique_map_frequencies)
        for frequency in unique_map_frequencies:
            self.radio_registry.reserve(frequency)

    def initialize_tacan_registry(
        self, unique_map_frequencies: set[RadioFrequency]
    ) -> None:
        """
        Dedup beacon/radio frequencies, since some maps have some frequencies
        used multiple times.
        """
        for beacon in Beacons.iter_theater(self.game.theater):
            unique_map_frequencies.add(beacon.frequency)
            if beacon.is_tacan:
                if beacon.channel is None:
                    logging.warning(f"TACAN beacon has no channel: {beacon.callsign}")
                else:
                    self.tacan_registry.mark_unavailable(beacon.tacan_channel)

    def initialize_radio_registry(
        self, unique_map_frequencies: set[RadioFrequency]
    ) -> None:
        for airport in self.game.theater.terrain.airport_list():
            if (atc := AtcData.from_pydcs(airport)) is not None:
                unique_map_frequencies.add(atc.hf)
                unique_map_frequencies.add(atc.vhf_fm)
                unique_map_frequencies.add(atc.vhf_am)
                unique_map_frequencies.add(atc.uhf)
                # No need to reserve ILS or TACAN because those are in the
                # beacon list.

    def generate_ground_conflicts(self) -> None:
        """Generate FLOTs and JTACs for each active front line."""
        for front_line in self.game.theater.conflicts():
            player_cp = front_line.blue_cp
            enemy_cp = front_line.red_cp
            conflict = FrontLineConflictDescription.frontline_cas_conflict(
                front_line, self.game.theater
            )
            # Generate frontline ops
            player_gp = self.game.ground_planners[player_cp.id].units_per_cp[
                enemy_cp.id
            ]
            enemy_gp = self.game.ground_planners[enemy_cp.id].units_per_cp[player_cp.id]
            ground_conflict_gen = FlotGenerator(
                self.mission,
                conflict,
                self.game,
                player_gp,
                enemy_gp,
                player_cp.stances[enemy_cp.id],
                enemy_cp.stances[player_cp.id],
                self.unit_map,
                self.radio_registry,
                self.mission_data,
                self.laser_code_registry,
            )
            ground_conflict_gen.generate()

    def generate_air_units(self, tgo_generator: TgoGenerator) -> None:
        """Generate the air units for the Operation"""

        # Air Support (Tanker & Awacs)
        air_support_generator = AirSupportGenerator(
            self.mission,
            AirConflictDescription.for_theater(self.game.theater),
            self.game,
            self.radio_registry,
            self.tacan_registry,
            self.mission_data,
        )
        air_support_generator.generate()

        # Generate Aircraft Activity on the map
        aircraft_generator = AircraftGenerator(
            self.mission,
            self.game.settings,
            self.game,
            self.time,
            self.radio_registry,
            self.tacan_registry,
            self.laser_code_registry,
            self.unit_map,
            mission_data=air_support_generator.mission_data,
            helipads=tgo_generator.helipads,
        )

        aircraft_generator.clear_parking_slots()

        aircraft_generator.generate_flights(
            self.mission.country(self.game.blue.country_name),
            self.game.blue.ato,
            tgo_generator.runways,
        )
        aircraft_generator.generate_flights(
            self.mission.country(self.game.red.country_name),
            self.game.red.ato,
            tgo_generator.runways,
        )
        aircraft_generator.spawn_unused_aircraft(
            self.mission.country(self.game.blue.country_name),
            self.mission.country(self.game.red.country_name),
        )

        for flight in aircraft_generator.flights:
            if not flight.client_units:
                continue
            flight.aircraft_type.assign_channels_for_flight(
                flight, air_support_generator.mission_data
            )

        self.mission_data.flights = aircraft_generator.flights

    def generate_destroyed_units(self) -> None:
        """Add destroyed units to the Mission"""
        if not self.game.settings.perf_destroyed_units:
            return

        for d in self.game.get_destroyed_units():
            try:
                type_name = d["type"]
                if not isinstance(type_name, str):
                    raise TypeError(
                        "Expected the type of the destroyed static to be a string"
                    )
                utype = unit_type_from_name(type_name)
            except KeyError:
                logging.warning(f"Destroyed unit has no type: {d}")
                continue

            pos = Point(cast(float, d["x"]), cast(float, d["z"]), self.mission.terrain)
            if utype is not None and not self.game.position_culled(pos):
                self.mission.static_group(
                    country=self.mission.country(self.game.blue.country_name),
                    name="",
                    _type=utype,
                    hidden=True,
                    position=pos,
                    heading=d["orientation"],
                    dead=True,
                )

    def notify_info_generators(
        self,
    ) -> None:
        """Generates subscribed MissionInfoGenerator objects."""
        mission_data = self.mission_data
        gens: list[MissionInfoGenerator] = [
            KneeboardGenerator(self.mission, self.game),
            BriefingGenerator(self.mission, self.game),
        ]
        for gen in gens:
            for dynamic_runway in mission_data.runways:
                gen.add_dynamic_runway(dynamic_runway)

            for tanker in mission_data.tankers:
                if tanker.blue:
                    gen.add_tanker(tanker)

            for aewc in mission_data.awacs:
                if aewc.blue:
                    gen.add_awacs(aewc)

            for jtac in mission_data.jtacs:
                if jtac.blue:
                    gen.add_jtac(jtac)

            for flight in mission_data.flights:
                gen.add_flight(flight)
            gen.generate()

    def setup_combined_arms(self) -> None:
        self.mission.groundControl.pilot_can_control_vehicles = COMBINED_ARMS_SLOTS > 0
        self.mission.groundControl.blue_tactical_commander = COMBINED_ARMS_SLOTS
        self.mission.groundControl.blue_observer = 1
