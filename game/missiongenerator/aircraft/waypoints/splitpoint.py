from dcs.point import MovingPoint
from dcs.task import OptECMUsing

from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SplitPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:

        # Let the AI use ECM to defend themselves.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfOnlyLockByRadar)
        waypoint.tasks.append(ecm_option)
