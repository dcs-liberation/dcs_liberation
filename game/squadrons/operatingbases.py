from __future__ import annotations

import dataclasses
from dataclasses import dataclass

from game.dcs.aircrafttype import AircraftType


@dataclass(frozen=True)
class OperatingBases:
    shore: bool
    carrier: bool
    lha: bool

    @classmethod
    def default_for_aircraft(cls, aircraft: AircraftType) -> OperatingBases:
        if aircraft.dcs_unit_type.helicopter:
            # Helicopters operate from anywhere by default.
            return OperatingBases(shore=True, carrier=True, lha=True)
        if aircraft.lha_capable:
            # Marine aircraft operate from LHAs and the shore by default.
            return OperatingBases(shore=True, carrier=False, lha=True)
        if aircraft.carrier_capable:
            # Carrier aircraft operate from carriers by default.
            return OperatingBases(shore=False, carrier=True, lha=False)
        # And the rest are only capable of shore operation.
        return OperatingBases(shore=True, carrier=False, lha=False)

    @classmethod
    def from_yaml(cls, aircraft: AircraftType, data: dict[str, bool]) -> OperatingBases:
        return dataclasses.replace(
            OperatingBases.default_for_aircraft(aircraft), **data
        )
