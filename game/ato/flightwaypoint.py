from __future__ import annotations

from datetime import timedelta
from typing import Optional, Sequence, TYPE_CHECKING, Union

from dcs import Point
from dcs.point import MovingPoint, PointAction
from dcs.unit import Unit

from game.utils import Distance, meters
from game.ato.flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from game.theater import ControlPoint, MissionTarget, GroundUnit


class FlightWaypoint:
    def __init__(
        self,
        waypoint_type: FlightWaypointType,
        x: float,
        y: float,
        alt: Distance = meters(0),
        control_point: Optional[ControlPoint] = None,
    ) -> None:
        """Creates a flight waypoint.

        Args:
            waypoint_type: The waypoint type.
            x: X coordinate of the waypoint.
            y: Y coordinate of the waypoint.
            alt: Altitude of the waypoint. By default this is MSL, but it can be
            changed to AGL by setting alt_type to "RADIO"
            control_point: The control point to associate with this waypoint. Needed for
            landing points.
        """
        self.waypoint_type = waypoint_type
        self.x = x
        self.y = y
        self.alt = alt
        self.control_point = control_point
        self.alt_type = "BARO"
        self.name = ""
        # TODO: Merge with pretty_name.
        # Only used in the waypoint list in the flight edit page. No sense
        # having three names. A short and long form is enough.
        self.description = ""
        self.targets: list[GroundUnit] = []
        self.obj_name = ""
        self.pretty_name = ""
        self.only_for_player = False
        self.flyover = False
        # The minimum amount of fuel remaining at this waypoint in pounds.
        self.min_fuel: Optional[float] = None

        # These are set very late by the air conflict generator (part of mission
        # generation). We do it late so that we don't need to propagate changes
        # to waypoint times whenever the player alters the package TOT or the
        # flight's offset in the UI.
        self.tot: Optional[timedelta] = None
        self.departure_time: Optional[timedelta] = None

    @property
    def position(self) -> Point:
        return Point(self.x, self.y)
