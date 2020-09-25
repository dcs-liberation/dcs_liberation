"""Battlefield front lines."""
from typing import Tuple

from . import ControlPoint, MissionTarget


class FrontLine(MissionTarget):
    """Defines a front line location between two control points.

    Front lines are the area where ground combat happens.
    """

    def __init__(self, control_point_a: ControlPoint,
                 control_point_b: ControlPoint) -> None:
        self.control_point_a = control_point_a
        self.control_point_b = control_point_b

    @property
    def control_points(self) -> Tuple[ControlPoint, ControlPoint]:
        """Returns a tuple of the two control points."""
        return self.control_point_a, self.control_point_b

    @property
    def name(self) -> str:
        a = self.control_point_a.name
        b = self.control_point_b.name
        return f"Front line {a}/{b}"
