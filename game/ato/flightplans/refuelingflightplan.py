from abc import ABC

from game.utils import Distance, Speed, knots, meters
from .patrolling import PatrollingFlightPlan, PatrollingLayout


class RefuelingFlightPlan(PatrollingFlightPlan[PatrollingLayout], ABC):
    @property
    def patrol_speed(self) -> Speed:
        # TODO: Could use self.flight.unit_type.preferred_patrol_speed(altitude).
        if self.flight.unit_type.patrol_speed is not None:
            return self.flight.unit_type.patrol_speed
        # ~280 knots IAS at 21000.
        return knots(400)

    @property
    def engagement_distance(self) -> Distance:
        # TODO: Factor out a common base of the combat and non-combat race-tracks.
        # No harm in setting this, but we ought to clean up a bit.
        return meters(0)
