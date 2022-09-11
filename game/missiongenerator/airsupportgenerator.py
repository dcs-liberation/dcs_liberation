from __future__ import annotations

import logging
from typing import List, TYPE_CHECKING, Tuple, Type

from dcs.mission import Mission, StartType
from dcs.planes import IL_78M, KC130, KC135MPRS, KC_135, PlaneType
from dcs.task import (
    AWACS,
    ActivateBeaconCommand,
    MainTask,
    Refueling,
    SetImmortalCommand,
    SetInvisibleCommand,
)
from dcs.unittype import UnitType

from game.ato.ai_flight_planner_db import AEWC_CAPABLE
from game.callsigns import callsign_for_support_unit
from game.naming import namegen
from game.radio.radios import RadioRegistry
from game.radio.tacan import TacanBand, TacanRegistry, TacanUsage
from game.utils import Heading
from .airconflictdescription import AirConflictDescription
from .missiondata import AwacsInfo, MissionData, TankerInfo

if TYPE_CHECKING:
    from game import Game

TANKER_DISTANCE = 15000
TANKER_ALT = 4572
TANKER_HEADING_OFFSET = 45

AWACS_DISTANCE = 150000
AWACS_ALT = 13000


class AirSupportGenerator:
    def __init__(
        self,
        mission: Mission,
        conflict: AirConflictDescription,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        mission_data: MissionData,
    ) -> None:
        self.mission = mission
        self.conflict = conflict
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.mission_data = mission_data

    @classmethod
    def support_tasks(cls) -> List[Type[MainTask]]:
        return [Refueling, AWACS]

    @staticmethod
    def _get_tanker_params(unit_type: Type[UnitType]) -> Tuple[int, int]:
        if unit_type is KC130:
            return TANKER_ALT - 500, 596
        elif unit_type is KC_135:
            return TANKER_ALT, 770
        elif unit_type is KC135MPRS:
            return TANKER_ALT + 500, 596
        return TANKER_ALT, 574

    def generate(self) -> None:
        player_cp = (
            self.conflict.blue_cp
            if self.conflict.blue_cp.captured
            else self.conflict.red_cp
        )

        country = self.mission.country(self.game.blue.country_name)

        if not self.game.settings.disable_legacy_tanker:
            fallback_tanker_number = 0

            for i, tanker_unit_type in enumerate(
                self.game.faction_for(player=True).tankers
            ):
                unit_type = tanker_unit_type.dcs_unit_type
                if not issubclass(unit_type, PlaneType):
                    logging.warning(f"Refueling aircraft {unit_type} must be a plane")
                    continue

                # TODO: Make loiter altitude a property of the unit type.
                alt, airspeed = self._get_tanker_params(tanker_unit_type.dcs_unit_type)
                freq = self.radio_registry.alloc_uhf()
                tacan = self.tacan_registry.alloc_for_band(
                    TacanBand.Y, TacanUsage.AirToAir
                )
                tanker_heading = Heading.from_degrees(
                    self.conflict.red_cp.position.heading_between_point(
                        self.conflict.blue_cp.position
                    )
                    + TANKER_HEADING_OFFSET * i
                )
                tanker_position = player_cp.position.point_from_heading(
                    tanker_heading.degrees, TANKER_DISTANCE
                )
                tanker_group = self.mission.refuel_flight(
                    country=country,
                    name=namegen.next_tanker_name(country, tanker_unit_type),
                    airport=None,
                    plane_type=unit_type,
                    position=tanker_position,
                    altitude=alt,
                    race_distance=58000,
                    frequency=freq.mhz,
                    start_type=StartType.Warm,
                    speed=airspeed,
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
                    tanker_group.points[0].tasks.append(
                        ActivateBeaconCommand(
                            tacan.number,
                            tacan.band.value,
                            tacan_callsign,
                            True,
                            tanker_group.units[0].id,
                            True,
                        )
                    )

                tanker_group.points[0].tasks.append(SetInvisibleCommand(True))
                tanker_group.points[0].tasks.append(SetImmortalCommand(True))

                self.mission_data.tankers.append(
                    TankerInfo(
                        group_name=str(tanker_group.name),
                        callsign=callsign,
                        variant=tanker_unit_type.name,
                        freq=freq,
                        tacan=tacan,
                        start_time=None,
                        end_time=None,
                        blue=True,
                    )
                )

        if not self.game.settings.disable_legacy_aewc:
            possible_awacs = [
                a
                for a in self.game.faction_for(player=True).aircrafts
                if a in AEWC_CAPABLE
            ]

            if not possible_awacs:
                logging.warning("No AWACS for faction")
                return

            awacs_unit = possible_awacs[0]
            freq = self.radio_registry.alloc_uhf()

            unit_type = awacs_unit.dcs_unit_type
            if not issubclass(unit_type, PlaneType):
                logging.warning(f"AWACS aircraft {unit_type} must be a plane")
                return

            awacs_flight = self.mission.awacs_flight(
                country=country,
                name=namegen.next_awacs_name(country),
                plane_type=unit_type,
                altitude=AWACS_ALT,
                airport=None,
                position=self.conflict.center.random_point_within(
                    AWACS_DISTANCE, AWACS_DISTANCE
                ),
                frequency=freq.mhz,
                start_type=StartType.Warm,
            )
            awacs_flight.set_frequency(freq.mhz)

            awacs_flight.points[0].tasks.append(SetInvisibleCommand(True))
            awacs_flight.points[0].tasks.append(SetImmortalCommand(True))

            self.mission_data.awacs.append(
                AwacsInfo(
                    group_name=str(awacs_flight.name),
                    callsign=callsign_for_support_unit(awacs_flight),
                    freq=freq,
                    depature_location=None,
                    start_time=None,
                    end_time=None,
                    blue=True,
                )
            )
