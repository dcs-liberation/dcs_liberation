import logging

from dcs.point import MovingPoint

from game.ato.flightplans.patrolling import PatrollingFlightPlan
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RaceTrackEndBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a patrol."
            )
            return waypoint

        self.waypoint.departure_time = self.flight.flight_plan.patrol_end_time
        return waypoint
