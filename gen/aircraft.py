from __future__ import annotations
from gen.tacan import TacanBand, TacanRegistry

import logging
import random
from dataclasses import dataclass
from datetime import timedelta
from functools import cached_property
from typing import Dict, List, Optional, TYPE_CHECKING, Type, Union, Iterable

from dcs import helicopters
from dcs.action import AITaskPush, ActivateGroup
from dcs.condition import CoalitionHasAirdrome, TimeAfter
from dcs.country import Country
from dcs.flyingunit import FlyingUnit
from dcs.planes import IL_78M, KC130, KC135MPRS, KC_135, S_3B_Tanker
from dcs.helicopters import UH_1H, helicopter_map
from dcs.mapping import Point
from dcs.mission import Mission, StartType
from dcs.planes import (
    AJS37,
    B_17G,
    B_52H,
    Bf_109K_4,
    C_101CC,
    C_101EB,
    FW_190A8,
    FW_190D9,
    F_14B,
    I_16,
    JF_17,
    Ju_88A4,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    P_51D,
    P_51D_30_NA,
    PlaneType,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_33,
    Tu_22M3,
)
from dcs.point import MovingPoint, PointAction
from dcs.task import (
    AWACS,
    AWACSTaskAction,
    ActivateBeaconCommand,
    AntishipStrike,
    AttackGroup,
    Bombing,
    BombingRunway,
    CAP,
    CAS,
    ControlledTask,
    EPLRS,
    EngageTargets,
    EngageTargetsInZone,
    FighterSweep,
    GroundAttack,
    OptROE,
    OptRTBOnBingoFuel,
    OptRTBOnOutOfAmmo,
    OptReactOnThreat,
    OptRestrictJettison,
    OrbitAction,
    Refueling,
    RunwayAttack,
    StartCommand,
    Tanker,
    Targets,
    Transport,
    WeaponType,
    TargetType,
)
from dcs.terrain.terrain import Airport, NoParkingSlotError
from dcs.triggers import Event, TriggerOnce, TriggerRule
from dcs.unit import Unit, Skill
from dcs.unitgroup import FlyingGroup, ShipGroup, StaticGroup
from dcs.unittype import FlyingType, UnitType

from game import db
from game.data.cap_capabilities_db import GUNFIGHTERS
from game.data.weapons import Pylon
from game.db import GUN_RELIANT_AIRFRAMES
from game.factions.faction import Faction
from game.settings import Settings
from game.squadrons import Pilot, Squadron
from game.theater.controlpoint import (
    Airfield,
    ControlPoint,
    ControlPointType,
    NavalControlPoint,
    OffMapSpawn,
)
from game.theater.missiontarget import MissionTarget
from game.theater.theatergroundobject import TheaterGroundObject
from game.transfers import MultiGroupTransport
from game.unitmap import UnitMap
from game.utils import Distance, meters, nautical_miles
from gen.ato import AirTaskingOrder, Package
from gen.callsigns import create_group_callsign_from_unit
from gen.flights.flight import (
    Flight,
    FlightType,
    FlightWaypoint,
    FlightWaypointType,
)
from gen.radios import MHz, Radio, RadioFrequency, RadioRegistry, get_radio
from gen.runways import RunwayData
from .airsupportgen import AirSupport, AwacsInfo, TankerInfo
from .callsigns import callsign_for_support_unit
from .flights.flightplan import (
    AwacsFlightPlan,
    CasFlightPlan,
    LoiterFlightPlan,
    PatrollingFlightPlan,
    RaceTrackRefuellingFlightPlan,
    SweepFlightPlan,
)
from .flights.traveltime import GroundSpeed, TotEstimator
from .naming import namegen

if TYPE_CHECKING:
    from game import Game

WARM_START_HELI_ALT = meters(500)
WARM_START_ALTITUDE = meters(3000)

RTB_ALTITUDE = meters(800)
RTB_DISTANCE = 5000
HELI_ALT = 500

# Note that fallback radio channels will *not* be reserved. It's possible that
# flights using these will overlap with other channels. This is because we would
# need to make sure we fell back to a frequency that is not used by any beacon
# or ATC, which we don't have the information to predict. Deal with the minor
# annoyance for now since we'll be fleshing out radio info soon enough.
ALLIES_WW2_CHANNEL = MHz(124)
GERMAN_WW2_CHANNEL = MHz(40)
HELICOPTER_CHANNEL = MHz(127)
UHF_FALLBACK_CHANNEL = MHz(251)

TARGET_WAYPOINTS = (
    FlightWaypointType.TARGET_GROUP_LOC,
    FlightWaypointType.TARGET_POINT,
    FlightWaypointType.TARGET_SHIP,
)


# TODO: Get radio information for all the special cases.
def get_fallback_channel(unit_type: UnitType) -> RadioFrequency:
    if unit_type in helicopter_map.values() and unit_type != UH_1H:
        return HELICOPTER_CHANNEL

    german_ww2_aircraft = [
        Bf_109K_4,
        FW_190A8,
        FW_190D9,
        Ju_88A4,
    ]

    if unit_type in german_ww2_aircraft:
        return GERMAN_WW2_CHANNEL

    allied_ww2_aircraft = [
        I_16,
        P_47D_30,
        P_47D_30bl1,
        P_47D_40,
        P_51D,
        P_51D_30_NA,
        SpitfireLFMkIX,
        SpitfireLFMkIXCW,
    ]

    if unit_type in allied_ww2_aircraft:
        return ALLIES_WW2_CHANNEL

    return UHF_FALLBACK_CHANNEL


class ChannelNamer:
    """Base class allowing channel name customization per-aircraft.

    Most aircraft will want to customize this behavior, but the default is
    reasonable for any aircraft with numbered radios.
    """

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        """Returns the name of the channel for the given radio and channel."""
        return f"COMM{radio_id} Ch {channel_id}"


class SingleRadioChannelNamer(ChannelNamer):
    """Channel namer for the aircraft with only a single radio.

    Aircraft like the MiG-19P and the MiG-21bis only have a single radio, so
    it's not necessary for us to name the radio when naming the channel.
    """

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        return f"Ch {channel_id}"


class HueyChannelNamer(ChannelNamer):
    """Channel namer for the UH-1H."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        return f"COM3 Ch {channel_id}"


class MirageChannelNamer(ChannelNamer):
    """Channel namer for the M-2000."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        radio_name = ["V/UHF", "UHF"][radio_id - 1]
        return f"{radio_name} Ch {channel_id}"


class TomcatChannelNamer(ChannelNamer):
    """Channel namer for the F-14."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        radio_name = ["UHF", "VHF/UHF"][radio_id - 1]
        return f"{radio_name} Ch {channel_id}"


class ViggenChannelNamer(ChannelNamer):
    """Channel namer for the AJS37."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        if channel_id >= 4:
            channel_letter = "EFGH"[channel_id - 4]
            return f"FR 24 {channel_letter}"
        return f"FR 22 Special {channel_id}"


class ViperChannelNamer(ChannelNamer):
    """Channel namer for the F-16."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        return f"COM{radio_id} Ch {channel_id}"


class SCR522ChannelNamer(ChannelNamer):
    """
    Channel namer for P-51 & P-47D
    """

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        if channel_id > 3:
            return "?"
        else:
            return f"Button " + "ABCD"[channel_id - 1]


@dataclass(frozen=True)
class ChannelAssignment:
    radio_id: int
    channel: int


@dataclass
class FlightData:
    """Details of a planned flight."""

    #: The package that the flight belongs to.
    package: Package

    #: The country that the flight belongs to.
    country: str

    flight_type: FlightType

    #: All units in the flight.
    units: List[FlyingUnit]

    #: Total number of aircraft in the flight.
    size: int

    #: True if this flight belongs to the player's coalition.
    friendly: bool

    #: Number of seconds after mission start the flight is set to depart.
    departure_delay: timedelta

    #: Arrival airport.
    arrival: RunwayData

    #: Departure airport.
    departure: RunwayData

    #: Diver airport.
    divert: Optional[RunwayData]

    #: Waypoints of the flight plan.
    waypoints: List[FlightWaypoint]

    #: Radio frequency for intra-flight communications.
    intra_flight_channel: RadioFrequency

    #: Map of radio frequencies to their assigned radio and channel, if any.
    frequency_to_channel_map: Dict[RadioFrequency, ChannelAssignment]

    #: Bingo fuel value in lbs.
    bingo_fuel: Optional[int]

    joker_fuel: Optional[int]

    def __init__(
        self,
        package: Package,
        country: str,
        flight_type: FlightType,
        units: List[FlyingUnit],
        size: int,
        friendly: bool,
        departure_delay: timedelta,
        departure: RunwayData,
        arrival: RunwayData,
        divert: Optional[RunwayData],
        waypoints: List[FlightWaypoint],
        intra_flight_channel: RadioFrequency,
        bingo_fuel: Optional[int],
        joker_fuel: Optional[int],
        custom_name: Optional[str],
    ) -> None:
        self.package = package
        self.country = country
        self.flight_type = flight_type
        self.units = units
        self.size = size
        self.friendly = friendly
        self.departure_delay = departure_delay
        self.departure = departure
        self.arrival = arrival
        self.divert = divert
        self.waypoints = waypoints
        self.intra_flight_channel = intra_flight_channel
        self.frequency_to_channel_map = {}
        self.bingo_fuel = bingo_fuel
        self.joker_fuel = joker_fuel
        self.callsign = create_group_callsign_from_unit(self.units[0])
        self.custom_name = custom_name

    @property
    def client_units(self) -> List[FlyingUnit]:
        """List of playable units in the flight."""
        return [u for u in self.units if u.is_human()]

    @property
    def aircraft_type(self) -> FlyingType:
        """Returns the type of aircraft in this flight."""
        return self.units[0].unit_type

    def num_radio_channels(self, radio_id: int) -> int:
        """Returns the number of preset channels for the given radio."""
        # Note: pydcs only initializes the radio presets for client slots.
        return self.client_units[0].num_radio_channels(radio_id)

    def channel_for(self, frequency: RadioFrequency) -> Optional[ChannelAssignment]:
        """Returns the radio and channel number for the given frequency."""
        return self.frequency_to_channel_map.get(frequency, None)

    def assign_channel(
        self, radio_id: int, channel_id: int, frequency: RadioFrequency
    ) -> None:
        """Assigns a preset radio channel to the given frequency."""
        for unit in self.client_units:
            unit.set_radio_channel_preset(radio_id, channel_id, frequency.mhz)

        # One frequency could be bound to multiple channels. Prefer the first,
        # since with the current implementation it will be the lowest numbered
        # channel.
        if frequency not in self.frequency_to_channel_map:
            self.frequency_to_channel_map[frequency] = ChannelAssignment(
                radio_id, channel_id
            )


class RadioChannelAllocator:
    """Base class for radio channel allocators."""

    def assign_channels_for_flight(
        self, flight: FlightData, air_support: AirSupport
    ) -> None:
        """Assigns mission frequencies to preset channels for the flight."""
        raise NotImplementedError


@dataclass(frozen=True)
class CommonRadioChannelAllocator(RadioChannelAllocator):
    """Radio channel allocator suitable for most aircraft.

    Most of the aircraft with preset channels available have one or more radios
    with 20 or more channels available (typically per-radio, but this is not the
    case for the JF-17).
    """

    #: Index of the radio used for intra-flight communications. Matches the
    #: index of the panel_radio field of the pydcs.dcs.planes object.
    inter_flight_radio_index: Optional[int]

    #: Index of the radio used for intra-flight communications. Matches the
    #: index of the panel_radio field of the pydcs.dcs.planes object.
    intra_flight_radio_index: Optional[int]

    def assign_channels_for_flight(
        self, flight: FlightData, air_support: AirSupport
    ) -> None:
        if self.intra_flight_radio_index is not None:
            flight.assign_channel(
                self.intra_flight_radio_index, 1, flight.intra_flight_channel
            )

        if self.inter_flight_radio_index is None:
            return

        # For cases where the inter-flight and intra-flight radios share presets
        # (the JF-17 only has one set of channels, even though it can use two
        # channels simultaneously), start assigning inter-flight channels at 2.
        radio_id = self.inter_flight_radio_index
        if self.intra_flight_radio_index == radio_id:
            first_channel = 2
        else:
            first_channel = 1

        last_channel = flight.num_radio_channels(radio_id)
        channel_alloc = iter(range(first_channel, last_channel + 1))

        if flight.departure.atc is not None:
            flight.assign_channel(radio_id, next(channel_alloc), flight.departure.atc)

        # TODO: If there ever are multiple AWACS, limit to mission relevant.
        for awacs in air_support.awacs:
            flight.assign_channel(radio_id, next(channel_alloc), awacs.freq)

        if flight.arrival != flight.departure and flight.arrival.atc is not None:
            flight.assign_channel(radio_id, next(channel_alloc), flight.arrival.atc)

        try:
            # TODO: Skip incompatible tankers.
            for tanker in air_support.tankers:
                flight.assign_channel(radio_id, next(channel_alloc), tanker.freq)

            if flight.divert is not None and flight.divert.atc is not None:
                flight.assign_channel(radio_id, next(channel_alloc), flight.divert.atc)
        except StopIteration:
            # Any remaining channels are nice-to-haves, but not necessary for
            # the few aircraft with a small number of channels available.
            pass


@dataclass(frozen=True)
class NoOpChannelAllocator(RadioChannelAllocator):
    """Channel allocator for aircraft that don't support preset channels."""

    def assign_channels_for_flight(
        self, flight: FlightData, air_support: AirSupport
    ) -> None:
        pass


@dataclass(frozen=True)
class FarmerRadioChannelAllocator(RadioChannelAllocator):
    """Preset channel allocator for the MiG-19P."""

    def assign_channels_for_flight(
        self, flight: FlightData, air_support: AirSupport
    ) -> None:
        # The Farmer only has 6 preset channels. It also only has a VHF radio,
        # and currently our ATC data and AWACS are only in the UHF band.
        radio_id = 1
        flight.assign_channel(radio_id, 1, flight.intra_flight_channel)
        # TODO: Assign 4-6 to VHF frequencies of departure, arrival, and divert.
        # TODO: Assign 2 and 3 to AWACS if it is VHF.


@dataclass(frozen=True)
class ViggenRadioChannelAllocator(RadioChannelAllocator):
    """Preset channel allocator for the AJS37."""

    def assign_channels_for_flight(
        self, flight: FlightData, air_support: AirSupport
    ) -> None:
        # The Viggen's preset channels are handled differently from other
        # aircraft. The aircraft automatically configures channels for every
        # allied flight in the game (including AWACS) and for every airfield. As
        # such, we don't need to allocate any of those. There are seven presets
        # we can modify, however: three channels for the main radio intended for
        # communication with wingmen, and four emergency channels for the backup
        # radio. We'll set the first channel of the main radio to the
        # intra-flight channel, and the first three emergency channels to each
        # of the flight plan's airfields. The fourth emergency channel is always
        # the guard channel.
        radio_id = 1
        flight.assign_channel(radio_id, 1, flight.intra_flight_channel)
        if flight.departure.atc is not None:
            flight.assign_channel(radio_id, 4, flight.departure.atc)
        if flight.arrival.atc is not None:
            flight.assign_channel(radio_id, 5, flight.arrival.atc)
        # TODO: Assign divert to 6 when we support divert airfields.


@dataclass(frozen=True)
class SCR522RadioChannelAllocator(RadioChannelAllocator):
    """Preset channel allocator for the SCR522 WW2 radios. (4 channels)"""

    def assign_channels_for_flight(
        self, flight: FlightData, air_support: AirSupport
    ) -> None:
        radio_id = 1
        flight.assign_channel(radio_id, 1, flight.intra_flight_channel)
        if flight.departure.atc is not None:
            flight.assign_channel(radio_id, 2, flight.departure.atc)
        if flight.arrival.atc is not None:
            flight.assign_channel(radio_id, 3, flight.arrival.atc)

        # TODO : Some GCI on Channel 4 ?


@dataclass(frozen=True)
class AircraftData:
    """Additional aircraft data not exposed by pydcs."""

    #: The type of radio used for inter-flight communications.
    inter_flight_radio: Radio

    #: The type of radio used for intra-flight communications.
    intra_flight_radio: Radio

    #: The radio preset channel allocator, if the aircraft supports channel
    #: presets. If the aircraft does not support preset channels, this will be
    #: None.
    channel_allocator: Optional[RadioChannelAllocator]

    #: Defines how channels should be named when printed in the kneeboard.
    channel_namer: Type[ChannelNamer] = ChannelNamer


# Indexed by the id field of the pydcs PlaneType.
AIRCRAFT_DATA: Dict[str, AircraftData] = {
    "A-10C": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-164"),
        # VHF for intraflight is not accepted anymore by DCS
        # (see https://forums.eagle.ru/showthread.php?p=4499738).
        intra_flight_radio=get_radio("AN/ARC-164"),
        channel_allocator=NoOpChannelAllocator(),
    ),
    "AJS37": AircraftData(
        # The AJS37 has somewhat unique radio configuration. Two backup radio
        # (FR 24) can only operate simultaneously with the main radio in guard
        # mode. As such, we only use the main radio for both inter- and intra-
        # flight communication.
        inter_flight_radio=get_radio("FR 22"),
        intra_flight_radio=get_radio("FR 22"),
        channel_allocator=ViggenRadioChannelAllocator(),
        channel_namer=ViggenChannelNamer,
    ),
    "AV8BNA": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-210"),
        intra_flight_radio=get_radio("AN/ARC-210"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=2, intra_flight_radio_index=1
        ),
    ),
    "F-14B": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-159"),
        intra_flight_radio=get_radio("AN/ARC-182"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=2
        ),
        channel_namer=TomcatChannelNamer,
    ),
    "F-16C_50": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-164"),
        intra_flight_radio=get_radio("AN/ARC-222"),
        # COM2 is the AN/ARC-222, which is the VHF radio we want to use for
        # intra-flight communication to leave COM1 open for UHF inter-flight.
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=2
        ),
        channel_namer=ViperChannelNamer,
    ),
    "FA-18C_hornet": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-210"),
        intra_flight_radio=get_radio("AN/ARC-210"),
        # DCS will clobber channel 1 of the first radio compatible with the
        # flight's assigned frequency. Since the F/A-18's two radios are both
        # AN/ARC-210s, radio 1 will be compatible regardless of which frequency
        # is assigned, so we must use radio 1 for the intra-flight radio.
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=2, intra_flight_radio_index=1
        ),
    ),
    "JF-17": AircraftData(
        inter_flight_radio=get_radio("R&S M3AR UHF"),
        intra_flight_radio=get_radio("R&S M3AR VHF"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        # Same naming pattern as the Viper, so just reuse that.
        channel_namer=ViperChannelNamer,
    ),
    "Ka-50": AircraftData(
        inter_flight_radio=get_radio("R-800L1"),
        intra_flight_radio=get_radio("R-800L1"),
        # The R-800L1 doesn't have preset channels, and the other radio is for
        # communications with FAC and ground units, which don't currently have
        # radios assigned, so no channels to configure.
        channel_allocator=NoOpChannelAllocator(),
    ),
    "M-2000C": AircraftData(
        inter_flight_radio=get_radio("TRT ERA 7000 V/UHF"),
        intra_flight_radio=get_radio("TRT ERA 7200 UHF"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=2
        ),
        channel_namer=MirageChannelNamer,
    ),
    "MiG-15bis": AircraftData(
        inter_flight_radio=get_radio("RSI-6K HF"),
        intra_flight_radio=get_radio("RSI-6K HF"),
        channel_allocator=NoOpChannelAllocator(),
    ),
    "MiG-19P": AircraftData(
        inter_flight_radio=get_radio("RSIU-4V"),
        intra_flight_radio=get_radio("RSIU-4V"),
        channel_allocator=FarmerRadioChannelAllocator(),
        channel_namer=SingleRadioChannelNamer,
    ),
    "MiG-21Bis": AircraftData(
        inter_flight_radio=get_radio("RSIU-5V"),
        intra_flight_radio=get_radio("RSIU-5V"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        channel_namer=SingleRadioChannelNamer,
    ),
    "P-51D": AircraftData(
        inter_flight_radio=get_radio("SCR522"),
        intra_flight_radio=get_radio("SCR522"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        channel_namer=SCR522ChannelNamer,
    ),
    "UH-1H": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-51BX"),
        # Ideally this would use the AN/ARC-131 because that radio is supposed
        # to be used for flight comms, but DCS won't allow it as the flight's
        # frequency, nor will it allow the AN/ARC-134.
        intra_flight_radio=get_radio("AN/ARC-51BX"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        channel_namer=HueyChannelNamer,
    ),
    "F-22A": AircraftData(
        inter_flight_radio=get_radio("SCR-522"),
        intra_flight_radio=get_radio("SCR-522"),
        channel_allocator=None,
        channel_namer=SCR522ChannelNamer,
    ),
    "JAS39Gripen": AircraftData(
        inter_flight_radio=get_radio("R&S Series 6000"),
        intra_flight_radio=get_radio("R&S Series 6000"),
        channel_allocator=None,
    ),
}
AIRCRAFT_DATA["A-10C_2"] = AIRCRAFT_DATA["A-10C"]
AIRCRAFT_DATA["P-51D-30-NA"] = AIRCRAFT_DATA["P-51D"]
AIRCRAFT_DATA["P-47D-30"] = AIRCRAFT_DATA["P-51D"]
AIRCRAFT_DATA["JAS39Gripen_AG"] = AIRCRAFT_DATA["JAS39Gripen"]


class AircraftConflictGenerator:
    def __init__(
        self,
        mission: Mission,
        settings: Settings,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        unit_map: UnitMap,
        air_support: AirSupport,
    ) -> None:
        self.m = mission
        self.game = game
        self.settings = settings
        self.radio_registry = radio_registry
        self.tacan_registy = tacan_registry
        self.unit_map = unit_map
        self.flights: List[FlightData] = []
        self.air_support = air_support

    @cached_property
    def use_client(self) -> bool:
        """True if Client should be used instead of Player."""
        blue_clients = self.client_slots_in_ato(self.game.blue_ato)
        red_clients = self.client_slots_in_ato(self.game.red_ato)
        return blue_clients + red_clients > 1

    @staticmethod
    def client_slots_in_ato(ato: AirTaskingOrder) -> int:
        total = 0
        for package in ato.packages:
            for flight in package.flights:
                total += flight.client_count
        return total

    def get_intra_flight_channel(self, airframe: UnitType) -> RadioFrequency:
        """Allocates an intra-flight channel to a group.

        Args:
            airframe: The type of aircraft a channel should be allocated for.

        Returns:
            The frequency of the intra-flight channel.
        """
        try:
            aircraft_data = AIRCRAFT_DATA[airframe.id]
            return self.radio_registry.alloc_for_radio(aircraft_data.intra_flight_radio)
        except KeyError:
            return get_fallback_channel(airframe)

    @staticmethod
    def _start_type(start_type: str) -> StartType:
        if start_type == "Runway":
            return StartType.Runway
        elif start_type == "Cold":
            return StartType.Cold
        return StartType.Warm

    def skill_level_for(
        self, unit: FlyingUnit, pilot: Optional[Pilot], blue: bool
    ) -> Skill:
        if blue:
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
        new_level = min(current_level + increase, len(levels) - 1)
        return levels[new_level]

    def set_skill(self, unit: FlyingUnit, pilot: Optional[Pilot], blue: bool) -> None:
        if pilot is None or not pilot.player:
            unit.skill = self.skill_level_for(unit, pilot, blue)
            return

        if self.use_client:
            unit.set_client()
        else:
            unit.set_player()

    @staticmethod
    def livery_from_db(flight: Flight) -> Optional[str]:
        return db.PLANE_LIVERY_OVERRIDES.get(flight.unit_type)

    def livery_from_faction(self, flight: Flight) -> Optional[str]:
        faction = self.game.faction_for(player=flight.departure.captured)
        if (choices := faction.liveries_overrides.get(flight.unit_type)) is not None:
            return random.choice(choices)
        return None

    @staticmethod
    def livery_from_squadron(flight: Flight) -> Optional[str]:
        return flight.squadron.livery

    def livery_for(self, flight: Flight) -> Optional[str]:
        if (livery := self.livery_from_squadron(flight)) is not None:
            return livery
        if (livery := self.livery_from_faction(flight)) is not None:
            return livery
        if (livery := self.livery_from_db(flight)) is not None:
            return livery
        return None

    def _setup_livery(self, flight: Flight, group: FlyingGroup) -> None:
        livery = self.livery_for(flight)
        if livery is None:
            return
        for unit in group.units:
            unit.livery_id = livery

    def _setup_group(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        unit_type = group.units[0].unit_type

        self._setup_payload(flight, group)
        self._setup_livery(flight, group)

        for unit, pilot in zip(group.units, flight.roster.pilots):
            player = pilot is not None and pilot.player
            self.set_skill(unit, pilot, blue=flight.departure.captured)
            # Do not generate player group with late activation.
            if player and group.late_activation:
                group.late_activation = False

            # Set up F-14 Client to have pre-stored alignment
            if unit_type is F_14B:
                unit.set_property(F_14B.Properties.INSAlignmentStored.id, True)

        group.points[0].tasks.append(
            OptReactOnThreat(OptReactOnThreat.Values.EvadeFire)
        )

        if flight.flight_type == FlightType.AEWC or FlightType.REFUELING:
            channel = self.radio_registry.alloc_uhf()
        else:
            channel = self.get_intra_flight_channel(unit_type)
        group.set_frequency(channel.mhz)

        divert = None
        if flight.divert is not None:
            divert = flight.divert.active_runway(self.game.conditions, dynamic_runways)

        self.flights.append(
            FlightData(
                package=package,
                country=self.game.faction_for(player=flight.departure.captured).country,
                flight_type=flight.flight_type,
                units=group.units,
                size=len(group.units),
                friendly=flight.from_cp.captured,
                # Set later.
                departure_delay=timedelta(),
                departure=flight.departure.active_runway(
                    self.game.conditions, dynamic_runways
                ),
                arrival=flight.arrival.active_runway(
                    self.game.conditions, dynamic_runways
                ),
                divert=divert,
                # Waypoints are added later, after they've had their TOTs set.
                waypoints=[],
                intra_flight_channel=channel,
                bingo_fuel=flight.flight_plan.bingo_fuel,
                joker_fuel=flight.flight_plan.joker_fuel,
                custom_name=flight.custom_name,
            )
        )

        # Special case so Su 33 and C101 can take off
        if unit_type in [Su_33, C_101EB, C_101CC]:
            self.set_reduced_fuel(flight, group, unit_type)

        if isinstance(flight.flight_plan, AwacsFlightPlan):
            callsign = callsign_for_support_unit(group)

            self.air_support.awacs.append(
                AwacsInfo(
                    group_name=str(group.name),
                    callsign=callsign,
                    freq=channel,
                    depature_location=flight.departure.name,
                    end_time=flight.flight_plan.mission_departure_time,
                    start_time=flight.flight_plan.mission_start_time,
                    blue=flight.departure.captured,
                )
            )

        if isinstance(flight.flight_plan, RaceTrackRefuellingFlightPlan):
            callsign = callsign_for_support_unit(group)

            tacan = self.tacan_registy.alloc_for_band(TacanBand.Y)
            variant = db.unit_type_name(flight.flight_plan.flight.unit_type)
            self.air_support.tankers.append(
                TankerInfo(
                    group_name=str(group.name),
                    callsign=callsign,
                    variant=variant,
                    freq=channel,
                    tacan=tacan,
                    start_time=flight.flight_plan.racetrack_start_time,
                    end_time=flight.flight_plan.racetrack_end_time,
                    blue=flight.departure.captured,
                )
            )

    def _generate_at_airport(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        airport: Optional[Airport] = None,
    ) -> FlyingGroup:
        assert count > 0

        logging.info("airgen: {} for {} at {}".format(unit_type, side.id, airport))
        return self.m.flight_group_from_airport(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=airport,
            maintask=None,
            start_type=self._start_type(start_type),
            group_size=count,
            parking_slots=None,
        )

    def _generate_inflight(
        self, name: str, side: Country, flight: Flight, origin: ControlPoint
    ) -> FlyingGroup:
        assert flight.count > 0
        at = origin.position

        alt_type = "RADIO"
        if isinstance(origin, OffMapSpawn):
            alt = flight.flight_plan.waypoints[0].alt
            alt_type = flight.flight_plan.waypoints[0].alt_type
        elif flight.unit_type in helicopters.helicopter_map.values():
            alt = WARM_START_HELI_ALT
        else:
            alt = WARM_START_ALTITUDE

        speed = GroundSpeed.for_flight(flight, alt)

        pos = Point(at.x + random.randint(100, 1000), at.y + random.randint(100, 1000))

        logging.info(
            "airgen: {} for {} at {} at {}".format(
                flight.unit_type, side.id, alt, int(speed.kph)
            )
        )
        group = self.m.flight_group(
            country=side,
            name=name,
            aircraft_type=flight.unit_type,
            airport=None,
            position=pos,
            altitude=alt.meters,
            speed=speed.kph,
            maintask=None,
            group_size=flight.count,
        )

        group.points[0].alt_type = alt_type
        return group

    def _generate_at_group(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        at: Union[ShipGroup, StaticGroup],
    ) -> FlyingGroup:
        assert count > 0

        logging.info("airgen: {} for {} at unit {}".format(unit_type, side.id, at))
        return self.m.flight_group_from_unit(
            country=side,
            name=name,
            aircraft_type=unit_type,
            pad_group=at,
            maintask=None,
            start_type=self._start_type(start_type),
            group_size=count,
        )

    def _add_radio_waypoint(
        self, group: FlyingGroup, position, altitude: Distance, airspeed: int = 600
    ) -> MovingPoint:
        point = group.add_waypoint(position, altitude.meters, airspeed)
        point.alt_type = "RADIO"
        return point

    def _rtb_for(
        self,
        group: FlyingGroup,
        cp: ControlPoint,
        at: Optional[db.StartingPosition] = None,
    ):
        if at is None:
            at = cp.at
        position = at if isinstance(at, Point) else at.position

        last_waypoint = group.points[-1]
        if last_waypoint is not None:
            heading = position.heading_between_point(last_waypoint.position)
            tod_location = position.point_from_heading(heading, RTB_DISTANCE)
            self._add_radio_waypoint(group, tod_location, last_waypoint.alt)

        destination_waypoint = self._add_radio_waypoint(group, position, RTB_ALTITUDE)
        if isinstance(at, Airport):
            group.land_at(at)
        return destination_waypoint

    def _at_position(self, at) -> Point:
        if isinstance(at, Point):
            return at
        elif isinstance(at, ShipGroup):
            return at.position
        elif issubclass(at, Airport):
            return at.position
        else:
            assert False

    def _setup_payload(self, flight: Flight, group: FlyingGroup) -> None:
        for p in group.units:
            p.pylons.clear()

        loadout = flight.loadout
        if self.game.settings.restrict_weapons_by_date:
            loadout = loadout.degrade_for_date(flight.unit_type, self.game.date)

        for pylon_number, weapon in loadout.pylons.items():
            if weapon is None:
                continue
            pylon = Pylon.for_aircraft(flight.unit_type, pylon_number)
            pylon.equip(group, weapon)

    def clear_parking_slots(self) -> None:
        for cp in self.game.theater.controlpoints:
            for parking_slot in cp.parking_slots:
                parking_slot.unit_id = None

    def generate_flights(
        self, country, ato: AirTaskingOrder, dynamic_runways: Dict[str, RunwayData]
    ) -> None:

        for package in ato.packages:
            if not package.flights:
                continue
            for flight in package.flights:
                logging.info(f"Generating flight: {flight.unit_type}")
                group = self.generate_planned_flight(flight.from_cp, country, flight)
                self.unit_map.add_aircraft(group, flight)
                self.setup_flight_group(group, package, flight, dynamic_runways)
                self.create_waypoints(group, package, flight)

    def spawn_unused_aircraft(
        self, player_country: Country, enemy_country: Country
    ) -> None:
        inventories = self.game.aircraft_inventory.inventories
        for control_point, inventory in inventories.items():
            if not isinstance(control_point, Airfield):
                continue

            if control_point.captured:
                country = player_country
                faction = self.game.player_faction
            else:
                country = enemy_country
                faction = self.game.enemy_faction

            for aircraft, available in inventory.all_aircraft:
                try:
                    self._spawn_unused_at(
                        control_point, country, faction, aircraft, available
                    )
                except NoParkingSlotError:
                    # If we run out of parking, stop spawning aircraft.
                    return

    def _spawn_unused_at(
        self,
        control_point: Airfield,
        country: Country,
        faction: Faction,
        aircraft: Type[FlyingType],
        number: int,
    ) -> None:
        for _ in range(number):
            # Creating a flight even those this isn't a fragged mission lets us
            # reuse the existing debriefing code.
            # TODO: Special flight type?
            flight = Flight(
                Package(control_point),
                faction.country,
                self.game.air_wing_for(control_point.captured).squadron_for(aircraft),
                1,
                FlightType.BARCAP,
                "Cold",
                departure=control_point,
                arrival=control_point,
                divert=None,
            )

            group = self._generate_at_airport(
                name=namegen.next_aircraft_name(country, control_point.id, flight),
                side=country,
                unit_type=aircraft,
                count=1,
                start_type="Cold",
                airport=control_point.airport,
            )

            if aircraft in faction.liveries_overrides:
                livery = random.choice(faction.liveries_overrides[aircraft])
                for unit in group.units:
                    unit.livery_id = livery

            group.uncontrolled = True
            self.unit_map.add_aircraft(group, flight)

    def set_activation_time(
        self, flight: Flight, group: FlyingGroup, delay: timedelta
    ) -> None:
        # Note: Late activation causes the waypoint TOTs to look *weird* in the
        # mission editor. Waypoint times will be relative to the group
        # activation time rather than in absolute local time. A flight delayed
        # until 09:10 when the overall mission start time is 09:00, with a join
        # time of 09:30 will show the join time as 00:30, not 09:30.
        group.late_activation = True

        activation_trigger = TriggerOnce(
            Event.NoEvent, f"FlightLateActivationTrigger{group.id}"
        )
        activation_trigger.add_condition(TimeAfter(seconds=int(delay.total_seconds())))

        self.prevent_spawn_at_hostile_airbase(flight, activation_trigger)
        activation_trigger.add_action(ActivateGroup(group.id))
        self.m.triggerrules.triggers.append(activation_trigger)

    def set_startup_time(
        self, flight: Flight, group: FlyingGroup, delay: timedelta
    ) -> None:
        # Uncontrolled causes the AI unit to spawn, but not begin startup.
        group.uncontrolled = True

        activation_trigger = TriggerOnce(Event.NoEvent, f"FlightStartTrigger{group.id}")
        activation_trigger.add_condition(TimeAfter(seconds=int(delay.total_seconds())))

        self.prevent_spawn_at_hostile_airbase(flight, activation_trigger)
        group.add_trigger_action(StartCommand())
        activation_trigger.add_action(AITaskPush(group.id, len(group.tasks)))
        self.m.triggerrules.triggers.append(activation_trigger)

    def prevent_spawn_at_hostile_airbase(
        self, flight: Flight, trigger: TriggerRule
    ) -> None:
        # Prevent delayed flights from spawning at airbases if they were
        # captured before they've spawned.
        if flight.from_cp.cptype != ControlPointType.AIRBASE:
            return

        if flight.from_cp.captured:
            coalition = self.game.get_player_coalition_id()
        else:
            coalition = self.game.get_enemy_coalition_id()

        trigger.add_condition(CoalitionHasAirdrome(coalition, flight.from_cp.id))

    def generate_planned_flight(self, cp, country, flight: Flight):
        name = namegen.next_aircraft_name(country, cp.id, flight)
        try:
            if flight.start_type == "In Flight":
                group = self._generate_inflight(
                    name=name, side=country, flight=flight, origin=cp
                )
            elif isinstance(cp, NavalControlPoint):
                group_name = cp.get_carrier_group_name()
                group = self._generate_at_group(
                    name=name,
                    side=country,
                    unit_type=flight.unit_type,
                    count=flight.count,
                    start_type=flight.start_type,
                    at=self.m.find_group(group_name),
                )
            else:
                if not isinstance(cp, Airfield):
                    raise RuntimeError(
                        f"Attempted to spawn at airfield for non-airfield {cp}"
                    )
                group = self._generate_at_airport(
                    name=name,
                    side=country,
                    unit_type=flight.unit_type,
                    count=flight.count,
                    start_type=flight.start_type,
                    airport=cp.airport,
                )
        except Exception as e:
            # Generated when there is no place on Runway or on Parking Slots
            logging.error(e)
            logging.warning(
                "No room on runway or parking slots. Starting from the air."
            )
            flight.start_type = "In Flight"
            group = self._generate_inflight(
                name=name, side=country, flight=flight, origin=cp
            )
            group.points[0].alt = 1500

        return group

    @staticmethod
    def set_reduced_fuel(
        flight: Flight, group: FlyingGroup, unit_type: Type[PlaneType]
    ) -> None:
        if unit_type is Su_33:
            for unit in group.units:
                if flight.flight_type is not CAP:
                    unit.fuel = Su_33.fuel_max / 2.2
                else:
                    unit.fuel = Su_33.fuel_max * 0.8
        elif unit_type in [C_101EB, C_101CC]:
            for unit in group.units:
                unit.fuel = unit_type.fuel_max * 0.5
        else:
            raise RuntimeError(f"No reduced fuel case for type {unit_type}")

    @staticmethod
    def flight_always_keeps_gun(flight: Flight) -> bool:
        # Never take bullets from players. They're smart enough to know when to use it
        # and when to RTB.
        if flight.client_count > 0:
            return True

        return flight.unit_type in GUN_RELIANT_AIRFRAMES

    def configure_behavior(
        self,
        flight: Flight,
        group: FlyingGroup,
        react_on_threat: Optional[OptReactOnThreat.Values] = None,
        roe: Optional[OptROE.Values] = None,
        rtb_winchester: Optional[OptRTBOnOutOfAmmo.Values] = None,
        restrict_jettison: Optional[bool] = None,
        mission_uses_gun: bool = True,
    ) -> None:
        group.points[0].tasks.clear()
        if react_on_threat is not None:
            group.points[0].tasks.append(OptReactOnThreat(react_on_threat))
        if roe is not None:
            group.points[0].tasks.append(OptROE(roe))
        if restrict_jettison is not None:
            group.points[0].tasks.append(OptRestrictJettison(restrict_jettison))
        if rtb_winchester is not None:
            group.points[0].tasks.append(OptRTBOnOutOfAmmo(rtb_winchester))

        # Confiscate the bullets of AI missions that do not rely on the gun. There is no
        # "all but gun" RTB winchester option, so air to ground missions with mixed
        # weapon types will insist on using all of their bullets after running out of
        # missiles and bombs. Take away their bullets so they don't strafe a Tor.
        #
        # Exceptions are made for player flights and for airframes where the gun is
        # essential like the A-10 or warbirds.
        if not mission_uses_gun and not self.flight_always_keeps_gun(flight):
            for unit in group.units:
                unit.gun = 0

        group.points[0].tasks.append(OptRTBOnBingoFuel(True))
        # Do not restrict afterburner.
        # https://forums.eagle.ru/forum/english/digital-combat-simulator/dcs-world-2-5/bugs-and-problems-ai/ai-ad/7121294-ai-stuck-at-high-aoa-after-making-sharp-turn-if-afterburner-is-restricted

    @staticmethod
    def configure_eplrs(group: FlyingGroup, flight: Flight) -> None:
        if hasattr(flight.unit_type, "eplrs"):
            if flight.unit_type.eplrs:
                group.points[0].tasks.append(EPLRS(group.id))

    def configure_cap(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = CAP.name
        self._setup_group(group, package, flight, dynamic_runways)

        if flight.unit_type not in GUNFIGHTERS:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_sweep(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = FighterSweep.name
        self._setup_group(group, package, flight, dynamic_runways)

        if flight.unit_type not in GUNFIGHTERS:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_cas(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.Unguided,
            restrict_jettison=True,
        )

    def configure_dead(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # Only CAS and SEAD are capable of the Attack Group task. SEAD is arguably more
        # appropriate but it has an extremely limited list of capable aircraft, whereas
        # CAS has a much wider selection of units.
        #
        # Note that the only effect that the DCS task type has is in determining which
        # waypoint actions the group may perform.
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.All,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_sead(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # CAS is able to perform all the same tasks as SEAD using a superset of the
        # available aircraft, and F-14s are not able to be SEAD despite having TALDs.
        # https://forums.eagle.ru/topic/272112-cannot-assign-f-14-to-sead/
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            # ASM includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.ASM,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_strike(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = GroundAttack.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_anti_ship(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = AntishipStrike.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_runway_attack(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = RunwayAttack.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_oca_strike(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
        )

    def configure_awacs(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = AWACS.name

        if not isinstance(flight.flight_plan, AwacsFlightPlan):
            logging.error(
                f"Cannot configure AEW&C tasks for {flight} because it does not have an AEW&C flight plan."
            )
            return

        self._setup_group(group, package, flight, dynamic_runways)

        # Awacs task action
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

        group.points[0].tasks.append(AWACSTaskAction())

    def configure_refueling(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = Refueling.name

        if not isinstance(flight.flight_plan, RaceTrackRefuellingFlightPlan):
            logging.error(
                f"Cannot configure racetrack refueling tasks for {flight} because it does not have an racetrack refueling flight plan."
            )
            return

        self._setup_group(group, package, flight, dynamic_runways)

        # Tanker task action
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_escort(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # Escort groups are actually given the CAP task so they can perform the
        # Search Then Engage task, which we have to use instead of the Escort
        # task for the reasons explained in JoinPointBuilder.
        group.task = CAP.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight, group, roe=OptROE.Values.OpenFire, restrict_jettison=True
        )

    def configure_sead_escort(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # CAS is able to perform all the same tasks as SEAD using a superset of the
        # available aircraft, and F-14s are not able to be SEAD despite having TALDs.
        # https://forums.eagle.ru/topic/272112-cannot-assign-f-14-to-sead/
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            roe=OptROE.Values.OpenFire,
            # ASM includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.ASM,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_transport(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = Transport.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_unknown_task(self, group: FlyingGroup, flight: Flight) -> None:
        logging.error(f"Unhandled flight type: {flight.flight_type}")
        self.configure_behavior(flight, group)

    def setup_flight_group(
        self,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        flight_type = flight.flight_type
        if flight_type in [
            FlightType.BARCAP,
            FlightType.TARCAP,
            FlightType.INTERCEPTION,
        ]:
            self.configure_cap(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.SWEEP:
            self.configure_sweep(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.AEWC:
            self.configure_awacs(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.REFUELING:
            self.configure_refueling(group, package, flight, dynamic_runways)
        elif flight_type in [FlightType.CAS, FlightType.BAI]:
            self.configure_cas(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.DEAD:
            self.configure_dead(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.SEAD:
            self.configure_sead(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.SEAD_ESCORT:
            self.configure_sead_escort(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.STRIKE:
            self.configure_strike(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.ANTISHIP:
            self.configure_anti_ship(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.ESCORT:
            self.configure_escort(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.OCA_RUNWAY:
            self.configure_runway_attack(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.OCA_AIRCRAFT:
            self.configure_oca_strike(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.TRANSPORT:
            self.configure_transport(group, package, flight, dynamic_runways)
        else:
            self.configure_unknown_task(group, flight)

        self.configure_eplrs(group, flight)

    def create_waypoints(
        self, group: FlyingGroup, package: Package, flight: Flight
    ) -> None:

        for waypoint in flight.points:
            waypoint.tot = None

        takeoff_point = FlightWaypoint.from_pydcs(group.points[0], flight.from_cp)
        self.set_takeoff_time(takeoff_point, package, flight, group)

        filtered_points = []  # type: List[FlightWaypoint]

        for point in flight.points:
            if point.only_for_player and not flight.client_count:
                continue
            filtered_points.append(point)
        # Only add 1 target waypoint for Viggens.  This only affects player flights,
        # the Viggen can't have more than 9 waypoints which leaves us with two target point
        # under the current flight plans.
        # TODO: Make this smarter, it currently selects a random unit in the group for target,
        # this could be updated to make it pick the "best" two targets in the group.
        if flight.unit_type is AJS37 and flight.client_count:
            viggen_target_points = [
                (idx, point)
                for idx, point in enumerate(filtered_points)
                if point.waypoint_type in TARGET_WAYPOINTS
            ]
            if viggen_target_points:
                keep_target = viggen_target_points[
                    random.randint(0, len(viggen_target_points) - 1)
                ]
                filtered_points = [
                    point
                    for idx, point in enumerate(filtered_points)
                    if (
                        point.waypoint_type not in TARGET_WAYPOINTS
                        or idx == keep_target[0]
                    )
                ]

        for idx, point in enumerate(filtered_points):
            PydcsWaypointBuilder.for_waypoint(
                point, group, package, flight, self.m, self.air_support
            ).build()

        # Set here rather than when the FlightData is created so they waypoints
        # have their TOTs set.
        self.flights[-1].waypoints = [takeoff_point] + flight.points

    def should_delay_flight(self, flight: Flight, start_time: timedelta) -> bool:
        if start_time.total_seconds() <= 0:
            return False

        if not flight.client_count:
            return True

        if start_time < timedelta(minutes=10):
            # Don't bother delaying client flights with short start delays. Much
            # more than ten minutes starts to eat into fuel a bit more
            # (espeicially for something fuel limited like a Harrier).
            return False

        return not self.settings.never_delay_player_flights

    def set_takeoff_time(
        self,
        waypoint: FlightWaypoint,
        package: Package,
        flight: Flight,
        group: FlyingGroup,
    ) -> None:
        estimator = TotEstimator(package)
        start_time = estimator.mission_start_time(flight)

        if self.should_delay_flight(flight, start_time):
            if self.should_activate_late(flight):
                # Late activation causes the aircraft to not be spawned
                # until triggered.
                self.set_activation_time(flight, group, start_time)
            elif flight.start_type == "Cold":
                # Setting the start time causes the AI to wait until the
                # specified time to begin their startup sequence.
                self.set_startup_time(flight, group, start_time)

        # And setting *our* waypoint TOT causes the takeoff time to show up in
        # the player's kneeboard.
        waypoint.tot = flight.flight_plan.takeoff_time()
        # And finally assign it to the FlightData info so it shows correctly in
        # the briefing.
        self.flights[-1].departure_delay = start_time

    @staticmethod
    def should_activate_late(flight: Flight) -> bool:
        if flight.start_type != "Cold":
            # Avoid spawning aircraft in the air or on the runway until it's
            # time for their mission. Also avoid burning through gas spawning
            # hot aircraft hours before their takeoff time.
            return True

        if flight.from_cp.is_fleet:
            # Carrier spawns will crowd the carrier deck, especially without
            # super carrier.
            # TODO: Is there enough parking on the supercarrier?
            return True

        return False


class PydcsWaypointBuilder:
    def __init__(
        self,
        waypoint: FlightWaypoint,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        mission: Mission,
        air_support: AirSupport,
    ) -> None:
        self.waypoint = waypoint
        self.group = group
        self.package = package
        self.flight = flight
        self.mission = mission
        self.air_support = air_support

    def build(self) -> MovingPoint:
        waypoint = self.group.add_waypoint(
            Point(self.waypoint.x, self.waypoint.y),
            self.waypoint.alt.meters,
            name=self.waypoint.name,
        )

        if self.waypoint.flyover:
            waypoint.action = PointAction.FlyOverPoint
            # It seems we need to leave waypoint.type exactly as it is even
            # though it's set to "Turning Point". If I set this to "Fly Over
            # Point" and then save the mission in the ME DCS resets it.

        waypoint.alt_type = self.waypoint.alt_type
        tot = self.flight.flight_plan.tot_for_waypoint(self.waypoint)
        if tot is not None:
            self.set_waypoint_tot(waypoint, tot)
        return waypoint

    def set_waypoint_tot(self, waypoint: MovingPoint, tot: timedelta) -> None:
        self.waypoint.tot = tot
        if not self._viggen_client_tot():
            waypoint.ETA = int(tot.total_seconds())
            waypoint.ETA_locked = True
            waypoint.speed_locked = False

    @classmethod
    def for_waypoint(
        cls,
        waypoint: FlightWaypoint,
        group: FlyingGroup,
        package: Package,
        flight: Flight,
        mission: Mission,
        air_support: AirSupport,
    ) -> PydcsWaypointBuilder:
        builders = {
            FlightWaypointType.DROP_OFF: CargoStopBuilder,
            FlightWaypointType.INGRESS_BAI: BaiIngressBuilder,
            FlightWaypointType.INGRESS_CAS: CasIngressBuilder,
            FlightWaypointType.INGRESS_DEAD: DeadIngressBuilder,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT: OcaAircraftIngressBuilder,
            FlightWaypointType.INGRESS_OCA_RUNWAY: OcaRunwayIngressBuilder,
            FlightWaypointType.INGRESS_SEAD: SeadIngressBuilder,
            FlightWaypointType.INGRESS_STRIKE: StrikeIngressBuilder,
            FlightWaypointType.INGRESS_SWEEP: SweepIngressBuilder,
            FlightWaypointType.JOIN: JoinPointBuilder,
            FlightWaypointType.LANDING_POINT: LandingPointBuilder,
            FlightWaypointType.LOITER: HoldPointBuilder,
            FlightWaypointType.PATROL: RaceTrackEndBuilder,
            FlightWaypointType.PATROL_TRACK: RaceTrackBuilder,
            FlightWaypointType.PICKUP: CargoStopBuilder,
            FlightWaypointType.TANKER_RACETRACK_START: TankerRaceTrackStartBuilder,
            FlightWaypointType.TANKER_RACETRACK_STOP: TankerRaceTrackStopBuilder,
        }
        builder = builders.get(waypoint.waypoint_type, DefaultWaypointBuilder)
        return builder(waypoint, group, package, flight, mission, air_support)

    def _viggen_client_tot(self) -> bool:
        """Viggen player aircraft consider any waypoint with a TOT set to be a target ("M") waypoint.
        If the flight is a player controlled Viggen flight, no TOT should be set on any waypoint except actual target waypoints.
        """
        if (self.flight.client_count > 0 and self.flight.unit_type == AJS37) and (
            self.waypoint.waypoint_type not in TARGET_WAYPOINTS
        ):
            return True
        else:
            return False

    def register_special_waypoints(
        self, targets: Iterable[Union[MissionTarget, Unit]]
    ) -> None:
        """Create special target waypoints for various aircraft"""
        for i, t in enumerate(targets):
            if self.group.units[0].unit_type == JF_17 and i < 4:
                self.group.add_nav_target_point(t.position, "PP" + str(i + 1))
            if self.group.units[0].unit_type == F_14B and i == 0:
                self.group.add_nav_target_point(t.position, "ST")


class DefaultWaypointBuilder(PydcsWaypointBuilder):
    pass


class HoldPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        loiter = ControlledTask(
            OrbitAction(altitude=waypoint.alt, pattern=OrbitAction.OrbitPattern.Circle)
        )
        if not isinstance(self.flight.flight_plan, LoiterFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot configure hold for for {self.flight} because "
                f"{flight_plan_type} does not define a push time. AI will push "
                "immediately and may flight unsuitable speeds."
            )
            return waypoint
        push_time = self.flight.flight_plan.push_time
        self.waypoint.departure_time = push_time
        loiter.stop_after_time(int(push_time.total_seconds()))
        waypoint.add_task(loiter)
        return waypoint


class BaiIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        # TODO: Add common "UnitGroupTarget" base type.
        group_names = []
        target = self.package.target
        if isinstance(target, TheaterGroundObject):
            for group in target.groups:
                group_names.append(group.name)
        elif isinstance(target, MultiGroupTransport):
            group_names.append(target.name)
        else:
            logging.error(
                "Unexpected target type for BAI mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        for group_name in group_names:
            group = self.mission.find_group(group_name)
            if group is None:
                logging.error("Could not find group for BAI mission %s", group_name)
                continue

            task = AttackGroup(group.id, weapon_type=WeaponType.Auto)
            task.params["attackQtyLimit"] = False
            task.params["directionEnabled"] = False
            task.params["altitudeEnabled"] = False
            task.params["groupAttack"] = True
            waypoint.tasks.append(task)
        return waypoint


class CasIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        if isinstance(self.flight.flight_plan, CasFlightPlan):
            waypoint.add_task(
                EngageTargetsInZone(
                    position=self.flight.flight_plan.target,
                    radius=int(self.flight.flight_plan.engagement_distance.meters),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )
        else:
            logging.error("No CAS waypoint found. Falling back to search and engage")
            waypoint.add_task(
                EngageTargets(
                    max_distance=int(nautical_miles(10).meters),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )
        return waypoint


class DeadIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        self.register_special_waypoints(self.waypoint.targets)

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for DEAD mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        for group in target.groups:
            miz_group = self.mission.find_group(group.name)
            if miz_group is None:
                logging.error(f"Could not find group for DEAD mission {group.name}")
                continue

            task = AttackGroup(miz_group.id, weapon_type=WeaponType.Auto)
            task.params["expend"] = "All"
            task.params["attackQtyLimit"] = False
            task.params["directionEnabled"] = False
            task.params["altitudeEnabled"] = False
            task.params["groupAttack"] = True
            waypoint.tasks.append(task)
        return waypoint


class OcaAircraftIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        target = self.package.target
        if not isinstance(target, Airfield):
            logging.error(
                "Unexpected target type for OCA Strike mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        task = EngageTargetsInZone(
            position=target.position,
            # Al Dhafra is 4 nm across at most. Add a little wiggle room in case
            # the airport position from DCS is not centered.
            radius=int(nautical_miles(3).meters),
            targets=[Targets.All.Air],
        )
        task.params["attackQtyLimit"] = False
        task.params["directionEnabled"] = False
        task.params["altitudeEnabled"] = False
        task.params["groupAttack"] = True
        waypoint.tasks.append(task)
        return waypoint


class OcaRunwayIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        target = self.package.target
        if not isinstance(target, Airfield):
            logging.error(
                "Unexpected target type for runway bombing mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        waypoint.tasks.append(
            BombingRunway(airport_id=target.airport.id, group_attack=True)
        )
        return waypoint


class SeadIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        self.register_special_waypoints(self.waypoint.targets)

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for SEAD mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        for group in target.groups:
            miz_group = self.mission.find_group(group.name)
            if miz_group is None:
                logging.error(f"Could not find group for SEAD mission {group.name}")
                continue

            task = AttackGroup(miz_group.id, weapon_type=WeaponType.Guided)
            task.params["expend"] = "All"
            task.params["attackQtyLimit"] = False
            task.params["directionEnabled"] = False
            task.params["altitudeEnabled"] = False
            task.params["groupAttack"] = True
            waypoint.tasks.append(task)
        return waypoint


class StrikeIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        if self.group.units[0].unit_type in [B_17G, B_52H, Tu_22M3]:
            return self.build_bombing()
        else:
            return self.build_strike()

    def build_bombing(self) -> MovingPoint:
        waypoint = super().build()

        targets = self.waypoint.targets
        if not targets:
            return waypoint

        center = Point(0, 0)
        for target in targets:
            center.x += target.position.x
            center.y += target.position.y
        center.x /= len(targets)
        center.y /= len(targets)
        bombing = Bombing(center, weapon_type=WeaponType.Bombs)
        bombing.params["expend"] = "All"
        bombing.params["attackQtyLimit"] = False
        bombing.params["directionEnabled"] = False
        bombing.params["altitudeEnabled"] = False
        bombing.params["groupAttack"] = True
        waypoint.tasks.append(bombing)
        return waypoint

    def build_strike(self) -> MovingPoint:
        waypoint = super().build()
        for target in self.waypoint.targets:
            bombing = Bombing(target.position, weapon_type=WeaponType.Auto)
            # If there is only one target, drop all ordnance in one pass.
            if len(self.waypoint.targets) == 1:
                bombing.params["expend"] = "All"
            bombing.params["groupAttack"] = True
            waypoint.tasks.append(bombing)

            # Register special waypoints
            self.register_special_waypoints(self.waypoint.targets)
        return waypoint


class SweepIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, SweepFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create sweep for {self.flight} because "
                f"{flight_plan_type} is not a sweep flight plan."
            )
            return waypoint

        waypoint.tasks.append(
            EngageTargets(
                max_distance=int(nautical_miles(50).meters),
                targets=[
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )
        )

        return waypoint


class JoinPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        if self.flight.flight_type == FlightType.ESCORT:
            self.configure_escort_tasks(
                waypoint,
                [
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )
        elif self.flight.flight_type == FlightType.SEAD_ESCORT:
            self.configure_escort_tasks(
                waypoint, [Targets.All.GroundUnits.AirDefence.AAA.SAMRelated]
            )
        return waypoint

    @staticmethod
    def configure_escort_tasks(
        waypoint: MovingPoint, target_types: List[Type[TargetType]]
    ) -> None:
        # Ideally we would use the escort mission type and escort task to have
        # the AI automatically but the AI only escorts AI flights while they are
        # traveling between waypoints. When an AI flight performs an attack
        # (such as attacking the mission target), AI escorts wander aimlessly
        # until the escorted group resumes its flight plan.
        #
        # As such, we instead use the Search Then Engage task, which is an
        # enroute task that causes the AI to follow their flight plan and engage
        # enemies of the set type within a certain distance. The downside to
        # this approach is that AI escorts are no longer related to the group
        # they are escorting, aside from the fact that they fly a similar flight
        # plan at the same time. With Escort, the escorts will follow the
        # escorted group out of the area. The strike element may or may not fly
        # directly over the target, and they may or may not require multiple
        # attack runs. For the escort flight we must just assume a flight plan
        # for the escort to fly. If the strike flight doesn't need to overfly
        # the target, the escorts are needlessly going in harms way. If the
        # strike flight needs multiple passes, the escorts may leave before the
        # escorted aircraft do.
        #
        # Another possible option would be to use Search Then Engage for join ->
        # ingress and egress -> split, but use a Search Then Engage in Zone task
        # for the target area that is set to end on a flag flip that occurs when
        # the strike aircraft finish their attack task.
        #
        # https://forums.eagle.ru/topic/251798-options-for-alternate-ai-escort-behavior
        waypoint.add_task(
            ControlledTask(
                EngageTargets(
                    # TODO: From doctrine.
                    max_distance=int(nautical_miles(30).meters),
                    targets=target_types,
                )
            )
        )

        # We could set this task to end at the split point. pydcs doesn't
        # currently support that task end condition though, and we don't really
        # need it.


class LandingPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.type = "Land"
        waypoint.action = PointAction.Landing
        return waypoint


class CargoStopBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.type = "LandingReFuAr"
        waypoint.action = PointAction.LandingReFuAr
        waypoint.landing_refuel_rearm_time = 2  # Minutes.
        return waypoint


class RaceTrackBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        flight_plan = self.flight.flight_plan

        if not isinstance(flight_plan, PatrollingFlightPlan):
            flight_plan_type = flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a patrol."
            )
            return waypoint

        # NB: It's important that the engage task comes before the orbit task.
        # Though they're on the same waypoint, if the orbit task comes first it
        # is their first priority and they will not engage any targets because
        # they're fully focused on orbiting. If the STE task is first, they will
        # engage targets if available and orbit if they find nothing to shoot.

        # TODO: Move the properties of this task into the flight plan?
        # CAP is the only current user of this so it's not a big deal, but might
        # be good to make this usable for things like BAI when we add that
        # later.
        cap_types = {FlightType.BARCAP, FlightType.TARCAP}
        if self.flight.flight_type in cap_types:
            engagement_distance = int(flight_plan.engagement_distance.meters)
            waypoint.tasks.append(
                EngageTargets(
                    max_distance=engagement_distance, targets=[Targets.All.Air]
                )
            )

        racetrack = ControlledTask(
            OrbitAction(
                altitude=waypoint.alt, pattern=OrbitAction.OrbitPattern.RaceTrack
            )
        )
        self.set_waypoint_tot(waypoint, flight_plan.patrol_start_time)
        racetrack.stop_after_time(int(flight_plan.patrol_end_time.total_seconds()))
        waypoint.add_task(racetrack)

        return waypoint


class RaceTrackEndBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a patrol."
            )
            return waypoint

        self.waypoint.departure_time = self.flight.flight_plan.patrol_end_time
        return waypoint


class TankerRaceTrackStartBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        flight_plan = self.flight.flight_plan

        if not isinstance(flight_plan, RaceTrackRefuellingFlightPlan):
            flight_plan_type = flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a refuelling racetrack."
            )
            return waypoint

        tanker_type = self.flight.unit_type

        if self.flight.flight_plan.tot_waypoint is not None:
            altitude = self.flight.flight_plan.tot_waypoint.alt.meters
        else:
            # Minimum planned altitude of any type.
            altitude = Distance.from_feet(12000).meters

        if tanker_type is KC_135:
            # Around 300 knots IAS, at 24000 feet.
            racetrack_orbit_speed = 825
        elif tanker_type is KC135MPRS:
            # Around 300 knots IAS, at 23000 feet.
            racetrack_orbit_speed = 810
        elif tanker_type is KC130:
            # Around 210 knots IAS, at 22000 feet.  KC130 doesn't have the performance to fly fast at altitude.
            racetrack_orbit_speed = 680
        elif tanker_type is S_3B_Tanker:
            # Around 265 knots IAS, at 12000 feet.
            racetrack_orbit_speed = 590
        elif tanker_type is IL_78M:
            # Around 280 knots IAS, at 21000 feet.
            racetrack_orbit_speed = 730

        racetrack = ControlledTask(
            OrbitAction(
                altitude=altitude,
                speed=racetrack_orbit_speed,
                pattern=OrbitAction.OrbitPattern.RaceTrack,
            )
        )

        self.set_waypoint_tot(waypoint, flight_plan.racetrack_start_time)
        racetrack.stop_after_time(
            int(flight_plan.mission_departure_time.total_seconds())
        )

        waypoint.add_task(Tanker())
        waypoint.add_task(racetrack)

        tanker_unit_type = self.flight.unit_type

        if tanker_unit_type != IL_78M:

            this_tanker = self.air_support.tankers[len(self.air_support.tankers) - 1]
            tacan = this_tanker.tacan
            callsign = callsign_for_support_unit(self.group)
            tacan_callsign = {
                "Texaco": "TEX",
                "Arco": "ARC",
                "Shell": "SHL",
            }.get(callsign)

            activate_tacan_task = ActivateBeaconCommand(
                tacan.number,
                tacan.band.value,
                tacan_callsign,
                True,
                self.group.units[0].id,
                True,
            )

            waypoint.add_task(activate_tacan_task)

        return waypoint


class TankerRaceTrackStopBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, RaceTrackRefuellingFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a tanker racetrack."
            )
            return waypoint

        self.waypoint.departure_time = self.flight.flight_plan.mission_departure_time
        return waypoint
