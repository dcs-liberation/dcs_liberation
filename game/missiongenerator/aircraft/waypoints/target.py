from .pydcswaypointbuilder import PydcsWaypointBuilder


class TargetBuilder(PydcsWaypointBuilder):
    """Waypoint builder for target waypoint types.

    This handles both precise target locations (TARGET_POINT) and target areas
    (TARGET_GROUP_LOC).
    """

    def dcs_name_for_waypoint(self) -> str:
        if self.flight.unit_type.use_f15e_waypoint_names:
            return f"#T {self.waypoint.name}"
        return super().dcs_name_for_waypoint()
