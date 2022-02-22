"""Extra airfield data that is not exposed by pydcs.

Remove once https://github.com/pydcs/dcs/issues/69 tracks getting the missing
data added to pydcs. Until then, missing data can be manually filled in here.
"""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, Dict, Optional, TYPE_CHECKING, Tuple

import yaml
from dcs.terrain import Airport

from game.radio.radios import RadioFrequency
from game.radio.tacan import TacanChannel

if TYPE_CHECKING:
    from game.theater import ConflictTheater


@dataclass
class AtcData:
    hf: RadioFrequency
    vhf_fm: RadioFrequency
    vhf_am: RadioFrequency
    uhf: RadioFrequency

    @classmethod
    def from_yaml(cls, data: dict[str, Any]) -> Optional[AtcData]:
        atc_data = data.get("atc")
        if atc_data is None:
            return None
        return AtcData(
            RadioFrequency.parse(atc_data["hf"]),
            RadioFrequency.parse(atc_data["vhf_low"]),
            RadioFrequency.parse(atc_data["vhf_high"]),
            RadioFrequency.parse(atc_data["uhf"]),
        )


@dataclass
class AirfieldData:
    """Additional airfield data not included in pydcs."""

    #: Airfield name for the UI. Not stable.
    name: str

    #: pydcs airport ID
    id: int

    #: ICAO airport code
    icao: Optional[str] = None

    #: Elevation (in ft).
    elevation: int = 0

    #: Runway length (in ft).
    runway_length: int = 0

    #: TACAN channel for the airfield.
    tacan: Optional[TacanChannel] = None

    #: TACAN callsign
    tacan_callsign: Optional[str] = None

    #: VOR as a tuple of (callsign, frequency).
    vor: Optional[Tuple[str, RadioFrequency]] = None

    #: RSBN channel as a tuple of (callsign, channel).
    rsbn: Optional[Tuple[str, int]] = None

    #: Radio channels used by the airfield's ATC. Note that not all airfields
    #: have ATCs.
    atc: Optional[AtcData] = None

    #: Dict of runway heading -> ILS tuple of (callsign, frequency).
    ils: Dict[str, Tuple[str, RadioFrequency]] = field(default_factory=dict)

    #: Dict of runway heading -> PRMG tuple of (callsign, channel).
    prmg: Dict[str, Tuple[str, int]] = field(default_factory=dict)

    #: Dict of runway heading -> outer NDB tuple of (callsign, frequency).
    outer_ndb: Dict[str, Tuple[str, RadioFrequency]] = field(default_factory=dict)

    #: Dict of runway heading -> inner NDB tuple of (callsign, frequency).
    inner_ndb: Dict[str, Tuple[str, RadioFrequency]] = field(default_factory=dict)

    _airfields: ClassVar[dict[str, dict[int, AirfieldData]]] = {}

    def ils_freq(self, runway: str) -> Optional[RadioFrequency]:
        ils = self.ils.get(runway)
        if ils is not None:
            return ils[1]
        return None

    @classmethod
    def from_file(cls, airfield_yaml: Path) -> AirfieldData:
        with airfield_yaml.open() as yaml_file:
            data = yaml.safe_load(yaml_file)

        tacan_channel = None
        tacan_callsign = None
        if (tacan := data.get("tacan")) is not None:
            tacan_channel = TacanChannel.parse(tacan["channel"])
            tacan_callsign = tacan["callsign"]

        vor = None
        if (vor_data := data.get("vor")) is not None:
            vor = (vor_data["callsign"], RadioFrequency.parse(vor_data["frequency"]))

        rsbn = None
        if (rsbn_data := data.get("rsbn")) is not None:
            rsbn = (rsbn_data["callsign"], rsbn_data["channel"])

        ils = {}
        prmg = {}
        outer_ndb = {}
        inner_ndb = {}
        for name, runway_data in data.get("runways", {}).items():
            if (ils_data := runway_data.get("ils")) is not None:
                ils[name] = (
                    ils_data["callsign"],
                    RadioFrequency.parse(ils_data["frequency"]),
                )

            if (prmg_data := runway_data.get("prmg")) is not None:
                prmg[name] = (prmg_data["callsign"], prmg_data["channel"])

            if (outer_ndb_data := runway_data.get("outer_ndb")) is not None:
                outer_ndb[name] = (
                    outer_ndb_data["callsign"],
                    RadioFrequency.parse(outer_ndb_data["frequency"]),
                )

            if (inner_ndb_data := runway_data.get("inner_ndb")) is not None:
                inner_ndb[name] = (
                    inner_ndb_data["callsign"],
                    RadioFrequency.parse(inner_ndb_data["frequency"]),
                )

        return AirfieldData(
            data["name"],
            data["id"],
            data.get("icao"),
            data["elevation"],
            data["runway_length"],
            tacan_channel,
            tacan_callsign,
            vor,
            rsbn,
            AtcData.from_yaml(data),
            ils,
            prmg,
            outer_ndb,
            inner_ndb,
        )

    @classmethod
    def _load_for_theater_if_needed(cls, theater: ConflictTheater) -> None:
        if theater.terrain.name in cls._airfields:
            return

        airfields = {}
        base_path = Path("resources/airfields") / theater.terrain.name
        for airfield_yaml in base_path.iterdir():
            data = cls.from_file(airfield_yaml)
            airfields[data.id] = data
        cls._airfields[theater.terrain.name] = airfields

    @classmethod
    def for_airport(cls, theater: ConflictTheater, airport: Airport) -> AirfieldData:
        return cls._airfields[theater.terrain.name][airport.id]

    @classmethod
    def for_theater(cls, theater: ConflictTheater) -> Iterator[AirfieldData]:
        cls._load_for_theater_if_needed(theater)
        yield from cls._airfields[theater.terrain.name].values()
