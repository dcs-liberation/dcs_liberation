import logging

from dcs.point import MovingPoint
from dcs.task import EngageTargets, OptFormation, Targets

from game.ato.flightplans.sweep import SweepFlightPlan
from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SweepIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if not isinstance(self.flight.flight_plan, SweepFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create sweep for {self.flight} because "
                f"{flight_plan_type} is not a sweep flight plan."
            )
            return

        waypoint.tasks.append(
            EngageTargets(
                max_distance=int(nautical_miles(50).meters),
                targets=[
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )
        )

        if self.flight.count < 4:
            waypoint.tasks.append(OptFormation.line_abreast_open())
        else:
            waypoint.tasks.append(OptFormation.spread_four_open())
