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

    #: Radio channels used by the airfield's ATC.
    atc: AtcData

    #: TACAN channel as a string, i.e. "74X".
    tacan: Optional[str] = None

    #: Dict of runway heading -> ILS frequency.
    ils: Dict[str, RadioFrequency] = field(default_factory=dict)

    def ils_freq(self, runway: str) -> Optional[RadioFrequency]:
        return self.ils.get(runway)


# TODO: Add more airfields.
AIRFIELD_DATA = {
    "Incirlik": AirfieldData(
        AtcData("3.85", "38.6", "129.4", "360.1"),
        "21X",
        {"050": "109.3", "230": "111.7"}
    ),
}
