from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.utils import Distance, Speed
from .inflight import InFlight
from ..starttype import StartType

if TYPE_CHECKING:
    from game.sim.combat import FrozenCombat


class InCombat(InFlight):
    def __init__(self, previous_state: InFlight, combat: FrozenCombat) -> None:
        super().__init__(
            previous_state.flight,
            previous_state.settings,
            previous_state.waypoint_index,
        )
        self.previous_state = previous_state
        self.combat = combat

    def estimate_position(self) -> Point:
        return self.previous_state.estimate_position()

    def estimate_altitude(self) -> tuple[Distance, str]:
        return self.previous_state.estimate_altitude()

    def estimate_speed(self) -> Speed:
        return self.previous_state.estimate_speed()

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        raise RuntimeError("Cannot simulate combat")

    @property
    def is_at_ip(self) -> bool:
        return False

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    def should_halt_sim(self) -> bool:
        return True

    @property
    def vulnerable_to_intercept(self) -> bool:
        # Interception results in the interceptor joining the existing combat rather
        # than creating a new combat.
        return False

    @property
    def vulnerable_to_sam(self) -> bool:
        # SAM contact results in the SAM joining the existing combat rather than
        # creating a new combat.
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.IN_FLIGHT

    @property
    def description(self) -> str:
        return self.combat.describe()
