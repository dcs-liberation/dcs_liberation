import logging

from dcs.point import MovingPoint
from dcs.task import BombingRunway, OptFormation

from game.theater import Airfield
from .pydcswaypointbuilder import PydcsWaypointBuilder


class OcaRunwayIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        target = self.package.target
        if not isinstance(target, Airfield):
            logging.error(
                "Unexpected target type for runway bombing mission: %s",
                target.__class__.__name__,
            )
            return

        waypoint.tasks.append(
            BombingRunway(airport_id=target.airport.id, group_attack=True)
        )
        waypoint.tasks.append(OptFormation.trail_open())
