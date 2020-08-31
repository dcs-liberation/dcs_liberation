from typing import List
from dataclasses import dataclass, field

from .conflictgen import *
from .naming import *
from .radios import RadioFrequency, RadioRegistry
from .tacan import TacanBand, TacanChannel, TacanRegistry

from dcs.mission import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.task import *

TANKER_DISTANCE = 15000
TANKER_ALT = 4572
TANKER_HEADING_OFFSET = 45

AWACS_DISTANCE = 150000
AWACS_ALT = 13000

AWACS_CALLSIGNS = [
    "Overlord",
    "Magic",
    "Wizard",
    "Focus",
    "Darkstar",
]


@dataclass
class TankerCallsign:
    full: str
    short: str


TANKER_CALLSIGNS = [
    TankerCallsign("Texaco", "TEX"),
    TankerCallsign("Arco", "ARC"),
    TankerCallsign("Shell", "SHL"),
]


@dataclass
class AwacsInfo:
    """AWACS information for the kneeboard."""
    callsign: str
    freq: RadioFrequency


@dataclass
class TankerInfo:
    """Tanker information for the kneeboard."""
    callsign: str
    variant: str
    freq: RadioFrequency
    tacan: TacanChannel


@dataclass
class AirSupport:
    awacs: List[AwacsInfo] = field(default_factory=list)
    tankers: List[TankerInfo] = field(default_factory=list)


class AirSupportConflictGenerator:

    def __init__(self, mission: Mission, conflict: Conflict, game,
                 radio_registry: RadioRegistry,
                 tacan_registry: TacanRegistry) -> None:
        self.mission = mission
        self.conflict = conflict
        self.game = game
        self.air_support = AirSupport()
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry

    @classmethod
    def support_tasks(cls) -> typing.Collection[typing.Type[MainTask]]:
        return [Refueling, AWACS]

    def generate(self, is_awacs_enabled):
        player_cp = self.conflict.from_cp if self.conflict.from_cp.captured else self.conflict.to_cp

        for i, tanker_unit_type in enumerate(db.find_unittype(Refueling, self.conflict.attackers_side)):
            callsign = TANKER_CALLSIGNS[i]
            variant = db.unit_type_name(tanker_unit_type)
            freq = self.radio_registry.alloc_uhf()
            tacan = self.tacan_registry.alloc_for_band(TacanBand.Y)
            tanker_heading = self.conflict.to_cp.position.heading_between_point(self.conflict.from_cp.position) + TANKER_HEADING_OFFSET * i
            tanker_position = player_cp.position.point_from_heading(tanker_heading, TANKER_DISTANCE)
            tanker_group = self.mission.refuel_flight(
                country=self.mission.country(self.game.player_country),
                name=namegen.next_tanker_name(self.mission.country(self.game.player_country)),
                airport=None,
                plane_type=tanker_unit_type,
                position=tanker_position,
                altitude=TANKER_ALT,
                race_distance=58000,
                frequency=freq.mhz,
                start_type=StartType.Warm,
                speed=574,
                tacanchannel=str(tacan),
            )

            if tanker_unit_type != IL_78M:
                tanker_group.points[0].tasks.pop() # Override PyDCS tacan channel
                tanker_group.points[0].tasks.append(ActivateBeaconCommand(
                    tacan.number, tacan.band.value, callsign.short, True, tanker_group.units[0].id, True))

            tanker_group.points[0].tasks.append(SetInvisibleCommand(True))
            tanker_group.points[0].tasks.append(SetImmortalCommand(True))

            self.air_support.tankers.append(TankerInfo(callsign.full, variant, freq, tacan))

        if is_awacs_enabled:
            try:
                callsign = AWACS_CALLSIGNS[0]
                freq = self.radio_registry.alloc_uhf()
                awacs_unit = db.find_unittype(AWACS, self.conflict.attackers_side)[0]
                awacs_flight = self.mission.awacs_flight(
                    country=self.mission.country(self.game.player_country),
                    name=namegen.next_awacs_name(self.mission.country(self.game.player_country)),
                    plane_type=awacs_unit,
                    altitude=AWACS_ALT,
                    airport=None,
                    position=self.conflict.position.random_point_within(AWACS_DISTANCE, AWACS_DISTANCE),
                    frequency=freq.mhz,
                    start_type=StartType.Warm,
                )
                awacs_flight.points[0].tasks.append(SetInvisibleCommand(True))
                awacs_flight.points[0].tasks.append(SetImmortalCommand(True))
                self.air_support.awacs.append(AwacsInfo(callsign, freq))
            except:
                print("No AWACS for faction")

