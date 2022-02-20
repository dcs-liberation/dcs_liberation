from __future__ import annotations

from collections.abc import Sequence
from dataclasses import field
from datetime import timedelta
from typing import Optional, TYPE_CHECKING

from dcs import Point
from dcs.unit import Unit
from pydantic.dataclasses import dataclass

from game.ato.flightwaypointtype import FlightWaypointType
from game.theater import LatLon
from game.utils import Distance, meters

if TYPE_CHECKING:
    from game.theater import ConflictTheater, ControlPoint, MissionTarget


@dataclass
class BaseFlightWaypoint:
    name: str
    waypoint_type: FlightWaypointType
    x: float
    y: float
    alt: Distance
    alt_type: str

    is_movable: bool = field(init=False)
    should_mark: bool = field(init=False)
    include_in_path: bool = field(init=False)

    # Do not use unless you're sure it's up to date. Pydantic doesn't have support for
    # serializing lazy properties so this needs to be stored in the class, but because
    # updating it requires a reference to the ConflictTheater it may not always be set,
    # or up to date. Call update_latlng to refresh.
    latlng: LatLon | None = None

    def __post_init__(self) -> None:
        # Target *points* are the exact location of a unit, whereas the target area is
        # only the center of the objective. Allow moving the latter since its exact
        # location isn't very important.
        #
        # Landing, and divert should be changed in the flight settings UI, takeoff
        # cannot be changed because that's where the plane is.
        #
        # Moving the bullseye reference only makes it wrong.
        self.is_movable = self.waypoint_type not in {
            FlightWaypointType.BULLSEYE,
            FlightWaypointType.DIVERT,
            FlightWaypointType.LANDING_POINT,
            FlightWaypointType.TAKEOFF,
            FlightWaypointType.TARGET_POINT,
        }

        # We don't need a marker for the departure waypoint (and it's likely
        # coincident with the landing waypoint, so hard to see). We do want to draw
        # the path from it though.
        #
        # We also don't need the landing waypoint since we'll be drawing that path
        # as well, and it's clear what it is, and only obscured the CP icon.
        #
        # The divert waypoint also obscures the CP. We don't draw the path to it,
        # but it can be seen in the flight settings page, so it's not really a
        # problem to exclude it.
        #
        # Bullseye ought to be (but currently isn't) drawn *once* rather than as a
        # flight waypoint.
        self.should_mark = self.waypoint_type not in {
            FlightWaypointType.BULLSEYE,
            FlightWaypointType.DIVERT,
            FlightWaypointType.LANDING_POINT,
            FlightWaypointType.TAKEOFF,
        }

        self.include_in_path = self.waypoint_type not in {
            FlightWaypointType.BULLSEYE,
            FlightWaypointType.DIVERT,
        }

    @property
    def position(self) -> Point:
        return Point(self.x, self.y)

    def update_latlng(self, theater: ConflictTheater) -> None:
        self.latlng = theater.point_to_ll(self.position)


class FlightWaypoint(BaseFlightWaypoint):
    control_point: ControlPoint | None = None

    # TODO: Merge with pretty_name.
    # Only used in the waypoint list in the flight edit page. No sense
    # having three names. A short and long form is enough.
    description: str = ""

    targets: Sequence[MissionTarget | Unit] = []
    obj_name: str = ""
    pretty_name: str = ""
    only_for_player: bool = False
    flyover: bool = False

    # The minimum amount of fuel remaining at this waypoint in pounds.
    min_fuel: float | None = None

    # These are set very late by the air conflict generator (part of mission
    # generation). We do it late so that we don't need to propagate changes
    # to waypoint times whenever the player alters the package TOT or the
    # flight's offset in the UI.
    tot: timedelta | None = None
    departure_time: timedelta | None = None

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
        super().__init__(
            name="", waypoint_type=waypoint_type, x=x, y=y, alt=alt, alt_type="BARO"
        )
        self.control_point = control_point

    def __hash__(self) -> int:
        return hash(id(self))
