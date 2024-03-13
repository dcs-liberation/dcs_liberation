from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from game.unitmap import FlyingUnit

if TYPE_CHECKING:
    from game.ato import Flight
    from game.squadrons import Pilot


# TODO: Serialize for bug reproducibility.
# Any bugs filed that can only be reproduced with auto-resolved combat results will not
# be reproducible since we cannot replay the auto-resolution that the player saw. We
# need to be able to serialize this data so bug repro can include the auto-resolved
# results.
@dataclass
class SimulationResults:
    air_losses: list[FlyingUnit] = field(default_factory=list)

    def kill_pilot(self, flight: Flight, pilot: Pilot) -> None:
        self.air_losses.append(FlyingUnit(flight, pilot))
