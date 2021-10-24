import logging

from dcs.point import MovingPoint
from dcs.task import EngageTargets, Targets

from game.utils import nautical_miles
from gen.flights.flightplan import SweepFlightPlan
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SweepIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, SweepFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create sweep for {self.flight} because "
                f"{flight_plan_type} is not a sweep flight plan."
            )
            return waypoint

        waypoint.tasks.append(
            EngageTargets(
                max_distance=int(nautical_miles(50).meters),
                targets=[
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )
        )

        return waypoint
