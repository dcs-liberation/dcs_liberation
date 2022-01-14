from dcs.point import MovingPoint
from dcs.task import OptECMUsing, OptFormation

from .pydcswaypointbuilder import PydcsWaypointBuilder


class SplitPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:

        if not self.flight.flight_type.is_air_to_air:
            # Capture any non A/A type to avoid issues with SPJs that use the primary radar such as the F/A-18C.
            # You can bully them with STT to not be able to fire radar guided missiles at you,
            # so best choice is to not let them perform jamming for now.

            # Let the AI use ECM to defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfOnlyLockByRadar)
            waypoint.tasks.append(ecm_option)

            waypoint.tasks.append(OptFormation.finger_four_close())
