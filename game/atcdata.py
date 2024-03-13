from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from dcs.task import Modulation
from dcs.terrain import Airport

from game.radio.radios import RadioFrequency


@dataclass
class AtcData:
    hf: RadioFrequency
    vhf_fm: RadioFrequency
    vhf_am: RadioFrequency
    uhf: RadioFrequency

    @classmethod
    def from_pydcs(cls, airport: Airport) -> Optional[AtcData]:
        if airport.atc_radio is None:
            return None
        return AtcData(
            RadioFrequency(airport.atc_radio.hf_hz, Modulation.FM),
            RadioFrequency(airport.atc_radio.vhf_low_hz, Modulation.FM),
            RadioFrequency(airport.atc_radio.vhf_high_hz, Modulation.AM),
            RadioFrequency(airport.atc_radio.uhf_hz, Modulation.AM),
        )
