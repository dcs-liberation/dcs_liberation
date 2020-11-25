import logging
from dataclasses import dataclass, field
from typing import List, Type

from dcs.mission import Mission, StartType
from dcs.planes import IL_78M
from dcs.task import (
    AWACS,
    ActivateBeaconCommand,
    MainTask,
    Refueling,
    SetImmortalCommand,
    SetInvisibleCommand,
)

from game import db
from .naming import namegen
from .callsigns import callsign_for_support_unit
from .conflictgen import Conflict
from .radios import RadioFrequency, RadioRegistry
from .tacan import TacanBand, TacanChannel, TacanRegistry

TANKER_DISTANCE = 15000
TANKER_ALT = 4572
TANKER_HEADING_OFFSET = 45

AWACS_DISTANCE = 150000
AWACS_ALT = 13000


@dataclass
class AwacsInfo:
    """AWACS information for the kneeboard."""
    dcsGroupName: str
    callsign: str
    freq: RadioFrequency


@dataclass
class TankerInfo:
    """Tanker information for the kneeboard."""
    dcsGroupName: str
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
    def support_tasks(cls) -> List[Type[MainTask]]:
        return [Refueling, AWACS]

    def generate(self):
        player_cp = self.conflict.from_cp if self.conflict.from_cp.captured else self.conflict.to_cp

        fallback_tanker_number = 0

        for i, tanker_unit_type in enumerate(db.find_unittype(Refueling, self.conflict.attackers_side)):
            variant = db.unit_type_name(tanker_unit_type)
            freq = self.radio_registry.alloc_uhf()
            tacan = self.tacan_registry.alloc_for_band(TacanBand.Y)
            tanker_heading = self.conflict.to_cp.position.heading_between_point(self.conflict.from_cp.position) + TANKER_HEADING_OFFSET * i
            tanker_position = player_cp.position.point_from_heading(tanker_heading, TANKER_DISTANCE)
            tanker_group = self.mission.refuel_flight(
                country=self.mission.country(self.game.player_country),
                name=namegen.next_tanker_name(self.mission.country(self.game.player_country), tanker_unit_type),
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
            tanker_group.set_frequency(freq.mhz)

            callsign = callsign_for_support_unit(tanker_group)
            tacan_callsign = {
                "Texaco": "TEX",
                "Arco": "ARC",
                "Shell": "SHL",
            }.get(callsign)
            if tacan_callsign is None:
                # The dict above is all the callsigns currently in the game, but
                # non-Western countries don't use the callsigns and instead just
                # use numbers. It's possible that none of those nations have
                # TACAN compatible refueling aircraft, but fallback just in
                # case.
                tacan_callsign = f"TK{fallback_tanker_number}"
                fallback_tanker_number += 1

            if tanker_unit_type != IL_78M:
                # Override PyDCS tacan channel.
                tanker_group.points[0].tasks.pop()
                tanker_group.points[0].tasks.append(ActivateBeaconCommand(
                    tacan.number, tacan.band.value, tacan_callsign, True,
                    tanker_group.units[0].id, True))

            tanker_group.points[0].tasks.append(SetInvisibleCommand(True))
            tanker_group.points[0].tasks.append(SetImmortalCommand(True))

            self.air_support.tankers.append(TankerInfo(str(tanker_group.name), callsign, variant, freq, tacan))

        possible_awacs = db.find_unittype(AWACS, self.conflict.attackers_side)

        if len(possible_awacs) > 0:
            awacs_unit = possible_awacs[0]
            freq = self.radio_registry.alloc_uhf()
            
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
            awacs_flight.set_frequency(freq.mhz)

            awacs_flight.points[0].tasks.append(SetInvisibleCommand(True))
            awacs_flight.points[0].tasks.append(SetImmortalCommand(True))

            self.air_support.awacs.append(AwacsInfo(
                str(awacs_flight.name), callsign_for_support_unit(awacs_flight), freq))
        else:
            logging.warning("No AWACS for faction")