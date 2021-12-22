from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.utils import Distance, Speed
from .inflight import InFlight
from ..starttype import StartType

if TYPE_CHECKING:
    from game.sim.combat import FrozenCombat
    from game.sim.gameupdateevents import GameUpdateEvents


class InCombat(InFlight):
    def __init__(self, previous_state: InFlight, combat: FrozenCombat) -> None:
        super().__init__(
            previous_state.flight,
            previous_state.settings,
            previous_state.waypoint_index,
        )
        self.previous_state = previous_state
        self.combat = combat

    def exit_combat(self) -> None:
        # TODO: Account for time passed while frozen.
        self.flight.set_state(self.previous_state)

    @property
    def in_combat(self) -> bool:
        return True

    def estimate_position(self) -> Point:
        return self.previous_state.estimate_position()

    def estimate_altitude(self) -> tuple[Distance, str]:
        return self.previous_state.estimate_altitude()

    def estimate_speed(self) -> Speed:
        return self.previous_state.estimate_speed()

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        # Combat ticking is handled elsewhere because combat objects may be shared
        # across multiple flights.
        pass

    @property
    def is_at_ip(self) -> bool:
        return False

    @property
    def is_waiting_for_start(self) -> bool:
        return False

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
