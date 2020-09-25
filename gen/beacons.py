from dataclasses import dataclass
from enum import auto, IntEnum
import json
from pathlib import Path
from typing import Iterable, Optional

from gen.radios import RadioFrequency
from gen.tacan import TacanBand, TacanChannel


BEACONS_RESOURCE_PATH = Path("resources/dcs/beacons")


class BeaconType(IntEnum):
    BEACON_TYPE_NULL = auto()
    BEACON_TYPE_VOR = auto()
    BEACON_TYPE_DME = auto()
    BEACON_TYPE_VOR_DME = auto()
    BEACON_TYPE_TACAN = auto()
    BEACON_TYPE_VORTAC = auto()
    BEACON_TYPE_RSBN = auto()
    BEACON_TYPE_BROADCAST_STATION = auto()

    BEACON_TYPE_HOMER = auto()
    BEACON_TYPE_AIRPORT_HOMER = auto()
    BEACON_TYPE_AIRPORT_HOMER_WITH_MARKER = auto()
    BEACON_TYPE_ILS_FAR_HOMER = auto()
    BEACON_TYPE_ILS_NEAR_HOMER = auto()

    BEACON_TYPE_ILS_LOCALIZER = auto()
    BEACON_TYPE_ILS_GLIDESLOPE = auto()

    BEACON_TYPE_PRMG_LOCALIZER = auto()
    BEACON_TYPE_PRMG_GLIDESLOPE = auto()

    BEACON_TYPE_ICLS_LOCALIZER = auto()
    BEACON_TYPE_ICLS_GLIDESLOPE = auto()

    BEACON_TYPE_NAUTICAL_HOMER = auto()


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


def load_beacons_for_terrain(name: str) -> Iterable[Beacon]:
    beacons_file = BEACONS_RESOURCE_PATH / f"{name.lower()}.json"
    if not beacons_file.exists():
        raise RuntimeError(f"Beacon file {beacons_file.resolve()} is missing")

    for beacon in json.loads(beacons_file.read_text()):
        yield Beacon(**beacon)
