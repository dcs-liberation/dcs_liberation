"""Battlefield front lines."""
from typing import Tuple

from dcs.mapping import Point
from . import ControlPoint, MissionTarget

# TODO: Dedup by moving everything to using this class.
FRONTLINE_MIN_CP_DISTANCE = 5000


def compute_position(control_point_a: ControlPoint,
                     control_point_b: ControlPoint) -> Point:
    a = control_point_a.position
    b = control_point_b.position
    attack_heading = a.heading_between_point(b)
    attack_distance = a.distance_to_point(b)
    middle_point = a.point_from_heading(attack_heading, attack_distance / 2)

    strength_delta = float(control_point_a.base.strength -
                           control_point_b.base.strength)
    position = middle_point.point_from_heading(attack_heading,
                                               strength_delta *
                                               attack_distance / 2 -
                                               FRONTLINE_MIN_CP_DISTANCE)
    return position


class FrontLine(MissionTarget):
    """Defines a front line location between two control points.

    Front lines are the area where ground combat happens.
    """

    def __init__(self, control_point_a: ControlPoint,
                 control_point_b: ControlPoint) -> None:
        super().__init__(f"Front line {control_point_a}/{control_point_b}",
                         compute_position(control_point_a, control_point_b))
        self.control_point_a = control_point_a
        self.control_point_b = control_point_b

    @property
    def control_points(self) -> Tuple[ControlPoint, ControlPoint]:
        """Returns a tuple of the two control points."""
        return self.control_point_a, self.control_point_b

    def is_friendly(self, to_player: bool) -> bool:
        return False
