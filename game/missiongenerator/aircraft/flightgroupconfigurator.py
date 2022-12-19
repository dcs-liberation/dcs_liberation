from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

from dcs import Mission
from dcs.flyingunit import FlyingUnit
from dcs.unit import Skill
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightType
from game.ato.flightplans.shiprecoverytanker import RecoveryTankerFlightPlan
from game.callsigns import callsign_for_support_unit
from game.data.weapons import Pylon, WeaponType as WeaponTypeEnum
from game.missiongenerator.missiondata import MissionData, AwacsInfo, TankerInfo
from game.missiongenerator.lasercoderegistry import LaserCodeRegistry
from game.missiongenerator.logisticsgenerator import LogisticsGenerator
from game.radio.radios import RadioFrequency, RadioRegistry
from game.radio.tacan import TacanBand, TacanRegistry, TacanUsage
from game.runways import RunwayData
from game.squadrons import Pilot
from game.unitmap import UnitMap
from .aircraftbehavior import AircraftBehavior
from .aircraftpainter import AircraftPainter
from .flightdata import FlightData
from .waypoints import WaypointGenerator
from ...ato.flightplans.aewc import AewcFlightPlan
from ...ato.flightplans.theaterrefueling import TheaterRefuelingFlightPlan

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
        laser_code_registry: LaserCodeRegistry,
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
        self.laser_code_registry = laser_code_registry
        self.mission_data = mission_data
        self.dynamic_runways = dynamic_runways
        self.use_client = use_client
        self.unit_map = unit_map

    def configure(self) -> FlightData:
        AircraftBehavior(self.flight.flight_type).apply_to(self.flight, self.group)
        AircraftPainter(self.flight, self.group).apply_livery()
        self.setup_props()
        self.setup_payload()
        self.setup_fuel()
        flight_channel = self.setup_radios()

        laser_codes: list[Optional[int]] = []
        for unit, pilot in zip(self.group.units, self.flight.roster.pilots):
            self.configure_flight_member(unit, pilot, laser_codes)

        divert = None
        if self.flight.divert is not None:
            divert = self.flight.divert.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            )

        if self.flight.flight_type in [
            FlightType.TRANSPORT,
            FlightType.AIR_ASSAULT,
        ] and self.game.settings.plugin_option("ctld"):
            transfer = None
            if self.flight.flight_type == FlightType.TRANSPORT:
                coalition = self.game.coalition_for(player=self.flight.blue)
                transfer = coalition.transfers.transfer_for_flight(self.flight)
            self.mission_data.logistics.append(
                LogisticsGenerator(
                    self.flight, self.group, self.mission, self.game.settings, transfer
                ).generate_logistics()
            )

        mission_start_time, waypoints = WaypointGenerator(
            self.flight,
            self.group,
            self.mission,
            self.game.conditions.start_time,
            self.time,
            self.game.settings,
            self.mission_data,
            self.unit_map,
        ).create_waypoints()

        return FlightData(
            package=self.flight.package,
            aircraft_type=self.flight.unit_type,
            flight_type=self.flight.flight_type,
            units=self.group.units,
            size=len(self.group.units),
            friendly=self.flight.from_cp.captured,
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
            bingo_fuel=self.flight.flight_plan.bingo_fuel,
            joker_fuel=self.flight.flight_plan.joker_fuel,
            custom_name=self.flight.custom_name,
            laser_codes=laser_codes,
        )

    def configure_flight_member(
        self, unit: FlyingUnit, pilot: Optional[Pilot], laser_codes: list[Optional[int]]
    ) -> None:
        player = pilot is not None and pilot.player
        self.set_skill(unit, pilot)
        if self.flight.loadout.has_weapon_of_type(WeaponTypeEnum.TGP) and player:
            laser_codes.append(self.laser_code_registry.get_next_laser_code())
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
        if isinstance(self.flight.flight_plan, AewcFlightPlan):
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
        elif isinstance(
            self.flight.flight_plan, TheaterRefuelingFlightPlan
        ) or isinstance(self.flight.flight_plan, RecoveryTankerFlightPlan):
            tacan = self.tacan_registry.alloc_for_band(TacanBand.Y, TacanUsage.AirToAir)
            self.mission_data.tankers.append(
                TankerInfo(
                    group_name=str(self.group.name),
                    callsign=callsign,
                    variant=self.flight.unit_type.name,
                    freq=channel,
                    tacan=tacan,
                    start_time=self.flight.flight_plan.patrol_start_time,
                    end_time=self.flight.flight_plan.patrol_end_time,
                    blue=self.flight.departure.captured,
                )
            )

    def set_skill(self, unit: FlyingUnit, pilot: Optional[Pilot]) -> None:
        if pilot is None or not pilot.player:
            unit.skill = self.skill_level_for(unit, pilot)
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
        for prop_id, value in self.flight.props.items():
            for unit in self.group.units:
                unit.set_property(prop_id, value)

    def setup_payload(self) -> None:
        for p in self.group.units:
            p.pylons.clear()

        loadout = self.flight.loadout
        if self.game.settings.restrict_weapons_by_date:
            loadout = loadout.degrade_for_date(self.flight.unit_type, self.game.date)

        for pylon_number, weapon in loadout.pylons.items():
            if weapon is None:
                continue
            pylon = Pylon.for_aircraft(self.flight.unit_type, pylon_number)
            pylon.equip(self.group, weapon)

    def setup_fuel(self) -> None:
        fuel = self.flight.state.estimate_fuel()
        if fuel < 0:
            logging.warning(
                f"Flight {self.flight} is estimated to have no fuel at mission start. "
                "This estimate does not account for external fuel tanks. Setting "
                "starting fuel to 100kg."
            )
            fuel = 100
        for unit, pilot in zip(self.group.units, self.flight.roster.pilots):
            if pilot is not None and pilot.player:
                unit.fuel = fuel
            elif (max_takeoff_fuel := self.flight.max_takeoff_fuel()) is not None:
                unit.fuel = max_takeoff_fuel
            else:
                # pydcs arbitrarily reduces the fuel of in-flight spawns by 10%. We do
                # our own tracking, so undo that.
                # https://github.com/pydcs/dcs/commit/303a81a8e0c778599fe136dd22cb2ae8123639a6
                unit.fuel = self.flight.unit_type.dcs_unit_type.fuel_max
