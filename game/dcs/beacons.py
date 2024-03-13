from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game.radio.radios import RadioFrequency
from game.radio.tacan import TacanBand, TacanChannel

if TYPE_CHECKING:
    from game.theater import ConflictTheater

BEACONS_RESOURCE_PATH = Path("resources/dcs/beacons")


class BeaconType(IntEnum):
    BEACON_TYPE_NULL = 0
    BEACON_TYPE_VOR = 1
    BEACON_TYPE_DME = 2
    BEACON_TYPE_VOR_DME = 3
    BEACON_TYPE_TACAN = 4
    BEACON_TYPE_VORTAC = 5
    BEACON_TYPE_RSBN = 6
    BEACON_TYPE_BROADCAST_STATION = 7

    BEACON_TYPE_HOMER = 8
    BEACON_TYPE_AIRPORT_HOMER = 9
    BEACON_TYPE_AIRPORT_HOMER_WITH_MARKER = 10
    BEACON_TYPE_ILS_FAR_HOMER = 11
    BEACON_TYPE_ILS_NEAR_HOMER = 12

    BEACON_TYPE_ILS_LOCALIZER = 13
    BEACON_TYPE_ILS_GLIDESLOPE = 14

    BEACON_TYPE_PRMG_LOCALIZER = 15
    BEACON_TYPE_PRMG_GLIDESLOPE = 16

    BEACON_TYPE_ICLS_LOCALIZER = 17
    BEACON_TYPE_ICLS_GLIDESLOPE = 18

    BEACON_TYPE_NAUTICAL_HOMER = 19


@dataclass(frozen=True)
class Beacon:
    name: str
    callsign: str
    beacon_type: BeaconType
    hertz: int
    channel: Optional[int]

    @property
    def frequency(self) -> RadioFrequency:
        return RadioFrequency(self.hertz)

    @property
    def is_tacan(self) -> bool:
        return self.beacon_type in (
            BeaconType.BEACON_TYPE_VORTAC,
            BeaconType.BEACON_TYPE_TACAN,
        )

    @property
    def tacan_channel(self) -> TacanChannel:
        assert self.is_tacan
        assert self.channel is not None
        return TacanChannel(self.channel, TacanBand.X)


class Beacons:
    _by_terrain: dict[str, dict[str, Beacon]] = {}

    @classmethod
    def _load_for_theater_if_needed(cls, theater: ConflictTheater) -> None:
        if theater.terrain.name in cls._by_terrain:
            return

        beacons_file = BEACONS_RESOURCE_PATH / f"{theater.terrain.name.lower()}.json"
        if not beacons_file.exists():
            raise RuntimeError(f"Beacon file {beacons_file.resolve()} is missing")

        beacons = {}
        for bid, beacon in json.loads(beacons_file.read_text()).items():
            beacons[bid] = Beacon(
                name=beacon["name"],
                callsign=beacon["callsign"],
                beacon_type=BeaconType(beacon["beacon_type"]),
                hertz=beacon["hertz"],
                channel=beacon["channel"],
            )
        cls._by_terrain[theater.terrain.name] = beacons

    @classmethod
    def _dict_for_theater(cls, theater: ConflictTheater) -> dict[str, Beacon]:
        cls._load_for_theater_if_needed(theater)
        return cls._by_terrain[theater.terrain.name]

    @classmethod
    def iter_theater(cls, theater: ConflictTheater) -> Iterator[Beacon]:
        yield from cls._dict_for_theater(theater).values()

    @classmethod
    def with_id(cls, beacon_id: str, theater: ConflictTheater) -> Beacon:
        return cls._dict_for_theater(theater)[beacon_id]
