from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

from dcs import Mission, Point
from dcs.flyingunit import FlyingUnit
from dcs.unit import Skill
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightType
from game.callsigns import callsign_for_support_unit
from game.data.weapons import Pylon
from game.datalink.sourcetracknumber import SourceTrackNumber
from game.datalink.sourcetracknumberprefix import SourceTrackNumberPrefix
from game.missiongenerator.logisticsgenerator import LogisticsGenerator
from game.missiongenerator.missiondata import AwacsInfo, MissionData, TankerInfo
from game.radio.radios import RadioFrequency, RadioRegistry
from game.radio.tacan import TacanBand, TacanRegistry, TacanUsage
from game.runways import RunwayData
from game.squadrons import Pilot
from game.unitmap import UnitMap
from .aircraftbehavior import AircraftBehavior
from .aircraftpainter import AircraftPainter
from .bingoestimator import BingoEstimator
from .flightdata import FlightData
from .waypoints import WaypointGenerator
from ...ato.flightmember import FlightMember

if TYPE_CHECKING:
    from game import Game


class FlightGroupConfigurator:
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        game: Game,
        mission: Mission,
        time: datetime,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        stn_prefix: SourceTrackNumberPrefix,
        mission_data: MissionData,
        dynamic_runways: dict[str, RunwayData],
        use_client: bool,
        unit_map: UnitMap,
    ) -> None:
        self.flight = flight
        self.group = group
        self.game = game
        self.mission = mission
        self.time = time
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.stn_prefix = stn_prefix
        self.mission_data = mission_data
        self.dynamic_runways = dynamic_runways
        self.use_client = use_client
        self.unit_map = unit_map

    def configure(self) -> FlightData:
        AircraftBehavior(self.flight.flight_type).apply_to(self.flight, self.group)
        AircraftPainter(self.flight, self.group).apply_livery()
        self.setup_props()
        self.setup_payloads()
        self.setup_fuel()
        flight_channel = self.setup_radios()

        laser_codes: list[Optional[int]] = []
        stns = []
        for idx, (unit, member) in enumerate(
            zip(self.group.units, self.flight.iter_members())
        ):
            self.configure_flight_member(unit, member, laser_codes)
            stns.append(SourceTrackNumber(self.stn_prefix, idx))

        divert = None
        if self.flight.divert is not None:
            divert = self.flight.divert.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            )

        if self.flight.flight_type in [
            FlightType.TRANSPORT,
            FlightType.AIR_ASSAULT,
        ] and self.game.lua_plugin_manager.is_plugin_enabled("ctld"):
            transfer = None
            if self.flight.flight_type == FlightType.TRANSPORT:
                coalition = self.game.coalition_for(player=self.flight.blue)
                transfer = coalition.transfers.transfer_for_flight(self.flight)
            self.mission_data.logistics.append(
                LogisticsGenerator(
                    self.flight,
                    self.group,
                    self.mission,
                    self.game.lua_plugin_manager,
                    transfer,
                ).generate_logistics()
            )

        mission_start_time, waypoints = WaypointGenerator(
            self.flight,
            self.group,
            self.mission,
            self.time,
            self.game.settings,
            self.mission_data,
            self.unit_map,
        ).create_waypoints()

        divert_position: Point | None = None
        if self.flight.divert is not None:
            divert_position = self.flight.divert.position
        bingo_estimator = BingoEstimator(
            self.flight.unit_type.fuel_consumption,
            self.flight.arrival.position,
            divert_position,
            self.flight.flight_plan.waypoints,
        )

        return FlightData(
            package=self.flight.package,
            aircraft_type=self.flight.unit_type,
            flight_type=self.flight.flight_type,
            units=self.group.units,
            size=len(self.group.units),
            friendly=self.flight.departure.captured,
            departure_delay=mission_start_time,
            departure=self.flight.departure.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            ),
            arrival=self.flight.arrival.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            ),
            divert=divert,
            waypoints=waypoints,
            intra_flight_channel=flight_channel,
            bingo_fuel=bingo_estimator.estimate_bingo(),
            joker_fuel=bingo_estimator.estimate_joker(),
            custom_name=self.flight.custom_name,
            laser_codes=laser_codes,
            source_track_numbers=stns,
        )

    def configure_flight_member(
        self, unit: FlyingUnit, member: FlightMember, laser_codes: list[Optional[int]]
    ) -> None:
        self.set_skill(unit, member)
        if (code := member.tgp_laser_code) is not None:
            laser_codes.append(code.code)
        else:
            laser_codes.append(None)

    def setup_radios(self) -> RadioFrequency:
        if self.flight.flight_type in {FlightType.AEWC, FlightType.REFUELING}:
            channel = self.radio_registry.alloc_uhf()
            self.register_air_support(channel)
        else:
            channel = self.flight.unit_type.alloc_flight_radio(self.radio_registry)

        self.group.set_frequency(channel.mhz)
        return channel

    def register_air_support(self, channel: RadioFrequency) -> None:
        callsign = callsign_for_support_unit(self.group)
        if self.flight.flight_type is FlightType.AEWC:
            self.mission_data.awacs.append(
                AwacsInfo(
                    group_name=str(self.group.name),
                    callsign=callsign,
                    freq=channel,
                    depature_location=self.flight.departure.name,
                    end_time=self.flight.flight_plan.mission_departure_time,
                    start_time=self.flight.flight_plan.takeoff_time(),
                    blue=self.flight.departure.captured,
                )
            )
        elif self.flight.flight_type is FlightType.REFUELING:
            tacan = self.tacan_registry.alloc_for_band(TacanBand.Y, TacanUsage.AirToAir)
            self.mission_data.tankers.append(
                TankerInfo(
                    group_name=str(self.group.name),
                    callsign=callsign,
                    variant=self.flight.unit_type.display_name,
                    freq=channel,
                    tacan=tacan,
                    start_time=self.flight.flight_plan.mission_begin_on_station_time,
                    end_time=self.flight.flight_plan.mission_departure_time,
                    blue=self.flight.departure.captured,
                )
            )

    def set_skill(self, unit: FlyingUnit, member: FlightMember) -> None:
        if not member.is_player:
            unit.skill = self.skill_level_for(unit, member.pilot)
            return

        if self.use_client:
            unit.set_client()
        else:
            unit.set_player()

    def skill_level_for(self, unit: FlyingUnit, pilot: Optional[Pilot]) -> Skill:
        if self.flight.squadron.player:
            base_skill = Skill(self.game.settings.player_skill)
        else:
            base_skill = Skill(self.game.settings.enemy_skill)

        if pilot is None:
            logging.error(f"Cannot determine skill level: {unit.name} has not pilot")
            return base_skill

        levels = [
            Skill.Average,
            Skill.Good,
            Skill.High,
            Skill.Excellent,
        ]
        current_level = levels.index(base_skill)
        missions_for_skill_increase = 4
        increase = pilot.record.missions_flown // missions_for_skill_increase
        capped_increase = min(current_level + increase, len(levels) - 1)

        if self.game.settings.ai_pilot_levelling:
            new_level = capped_increase
        else:
            new_level = current_level

        return levels[new_level]

    def setup_props(self) -> None:
        for unit, member in zip(self.group.units, self.flight.iter_members()):
            props = dict(member.properties)
            if (code := member.weapon_laser_code) is not None:
                for laser_code_config in self.flight.unit_type.laser_code_configs:
                    props.update(laser_code_config.property_dict_for_code(code.code))
            for prop_id, value in props.items():
                unit.set_property(prop_id, value)

    def setup_payloads(self) -> None:
        for unit, member in zip(self.group.units, self.flight.iter_members()):
            self.setup_payload(unit, member)

    def setup_payload(self, unit: FlyingUnit, member: FlightMember) -> None:
        unit.pylons.clear()

        loadout = member.loadout
        if self.game.settings.restrict_weapons_by_date:
            loadout = loadout.degrade_for_date(self.flight.unit_type, self.game.date)

        for pylon_number, weapon in loadout.pylons.items():
            if weapon is None:
                continue
            pylon = Pylon.for_aircraft(self.flight.unit_type, pylon_number)
            pylon.equip(unit, weapon)

    def setup_fuel(self) -> None:
        fuel = self.flight.state.estimate_fuel()
        if fuel < 0:
            logging.warning(
                f"Flight {self.flight} is estimated to have no fuel at mission start. "
                "This estimate does not account for external fuel tanks. Setting "
                "starting fuel to 100kg."
            )
            fuel = 100
        for unit, pilot in zip(self.group.units, self.flight.roster.iter_pilots()):
            if pilot is not None and pilot.player:
                unit.fuel = fuel
            elif (max_takeoff_fuel := self.flight.max_takeoff_fuel()) is not None:
                unit.fuel = max_takeoff_fuel
            else:
                # pydcs arbitrarily reduces the fuel of in-flight spawns by 10%. We do
                # our own tracking, so undo that.
                # https://github.com/pydcs/dcs/commit/303a81a8e0c778599fe136dd22cb2ae8123639a6
                unit.fuel = self.flight.unit_type.dcs_unit_type.fuel_max
