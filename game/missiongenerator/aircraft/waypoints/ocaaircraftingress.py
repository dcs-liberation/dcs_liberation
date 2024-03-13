import logging

from dcs.point import MovingPoint
from dcs.task import EngageTargetsInZone, Targets

from game.theater import Airfield
from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder


class OcaAircraftIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        target = self.package.target
        if not isinstance(target, Airfield):
            logging.error(
                "Unexpected target type for OCA Strike mission: %s",
                target.__class__.__name__,
            )
            return

        task = EngageTargetsInZone(
            position=target.position,
            # Al Dhafra is 4 nm across at most. Add a little wiggle room in case
            # the airport position from DCS is not centered.
            radius=int(nautical_miles(3).meters),
            targets=[Targets.All.Air],
        )
        task.params["attackQtyLimit"] = False
        task.params["directionEnabled"] = False
        task.params["altitudeEnabled"] = False
        task.params["groupAttack"] = True
        waypoint.tasks.append(task)
