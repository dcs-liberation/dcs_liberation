"""Extra airfield data that is not exposed by pydcs.

Remove once https://github.com/pydcs/dcs/issues/69 tracks getting the missing
data added to pydcs. Until then, missing data can be manually filled in here.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


RadioFrequency = str


@dataclass
class AtcData:
    hf: RadioFrequency
    vhf_fm: RadioFrequency
    vhf_am: RadioFrequency
    uhf: RadioFrequency


@dataclass
class AirfieldData:
    """Additional airfield data not included in pydcs."""

    #: ICAO airport code
    icao: Optional[str] = None

    #: Elevation (in ft).
    elevation: int = 0

    #: Runway length (in ft).
    runway_length: int = 0

    #: TACAN channel as a string, i.e. "74X".
    tacan: Optional[str] = None

    #: TACAN callsign
    tacan_callsign: Optional[str] = None

    #: VOR channel as a string, i.e. "114.90 (MA)".
    vor: Optional[str] = None

    #: RSBN channel as a string, i.e. "ch 28 (KW)".
    rsbn: Optional[str] = None

    #: Radio channels used by the airfield's ATC.
    atc: AtcData = AtcData("", "", "", "")

    #: Dict of runway heading -> ILS frequency.
    ils: Dict[str, RadioFrequency] = field(default_factory=dict)

    #: Dict of runway heading -> PRMG info, i.e "ch 26 (KW)"
    prmg: Dict[str, str] = field(default_factory=dict)

    #: Dict of runway heading -> outer ndb, i.e "408.00 (KW)"
    outer_ndb: Dict[str, str] = field(default_factory=dict)

    #: Dict of runway heading -> inner ndb, i.e "803.00 (K)
    inner_ndb: Dict[str, str] = field(default_factory=dict)

    def ils_freq(self, runway: str) -> Optional[RadioFrequency]:
        return self.ils.get(runway)


# TODO: Add more airfields.
AIRFIELD_DATA = {

    # TODO : CAUCASUS MAP
    "Batumi": AirfieldData(
        "UGSB",
        32, 6792,
        "16X", "BTM",
        "", "",
        AtcData("4.250", "131.000", "40.400", "260.000"),
        {"13": "110.30 (ILU)"},
        {},
        {},
        {}
    ),

    "Kobuleti": AirfieldData(
        "UG5X",
        59, 7406,
        "67X", "KBL",
        "", "",
        AtcData("4.350", "133.000", "40.800", "262.000"),
        {"7": "111.50 (IKB)"},
        {},
        {"7": "870.00 (KT)"},
        {"7": "490.00 (T)"},
    ),

    "Senaki-Kolkhi": AirfieldData(
        "UGKS",
        43, 7256,
        "31X", "TSK",
        "", "",
        AtcData("4.300", "132.000", "40.600", "261.000"),
        {"9": "108.90 (ITS)"},
        {},
        {"9": "335.00 (BI)"},
        {"9": "688.00 (I)"},
    ),

    "Kutaisi": AirfieldData(
        "UGKO",
        147, 7937,
        "44X", "KTS",
        "113.60 (KT)", "",
        AtcData("4.400", "134.000", "41.000", "263.000"),
        {"8": "109.75 (IKS)"},
        {},
        {},
        {},
    ),

    # TODO : PERSIAN GULF MAP
    # TODO : SYRIA MAP
    # "Incirlik": AirfieldData(
    #     AtcData("3.85", "38.6", "129.4", "360.1"),
    #     "21X",
    #     {"050": "109.3", "230": "111.7"}
    # ),
    # TODO : NEVADA MAP
    # TODO : NORMANDY MAP
    # TODO : THE CHANNEL MAP
}
