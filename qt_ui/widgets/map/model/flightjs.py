from __future__ import annotations

from typing import List

from PySide2.QtCore import Property, QObject, Signal, Slot
from shapely.geometry import LineString, Point as ShapelyPoint

from game.ato import Flight, FlightWaypoint
from game.ato.flightstate import InFlight
from game.ato.flightwaypointtype import FlightWaypointType
from game.theater import ConflictTheater
from game.utils import meters
from gen.flights.flightplan import CasFlightPlan, PatrollingFlightPlan
from qt_ui.models import AtoModel
from .leaflet import LeafletLatLon, LeafletPoly
from .shapelyutil import ShapelyUtil
from .waypointjs import WaypointJs


class FlightJs(QObject):
    positionChanged = Signal()
    flightPlanChanged = Signal()
    blueChanged = Signal()
    selectedChanged = Signal()
    commitBoundaryChanged = Signal()

    originChanged = Signal()

    @Property(list, notify=originChanged)
    def origin(self) -> LeafletLatLon:
        return self._waypoints[0].position

    targetChanged = Signal()

    @Property(list, notify=targetChanged)
    def target(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.flight.package.target.position)
        return [ll.latitude, ll.longitude]

    def __init__(
        self,
        flight: Flight,
        selected: bool,
        theater: ConflictTheater,
        ato_model: AtoModel,
    ) -> None:
        super().__init__()
        self.flight = flight
        self._selected = selected
        self.theater = theater
        self.ato_model = ato_model
        self._waypoints = self.make_waypoints()

    def update_waypoints(self) -> None:
        for waypoint in self._waypoints:
            waypoint.timingChanged.emit()

    def make_waypoints(self) -> List[WaypointJs]:
        departure = FlightWaypoint(
            FlightWaypointType.TAKEOFF,
            self.flight.departure.position.x,
            self.flight.departure.position.y,
            meters(0),
        )
        departure.alt_type = "RADIO"
        waypoints = []
        for idx, point in enumerate([departure] + self.flight.points):
            waypoint = WaypointJs(point, idx, self, self.theater, self.ato_model)
            waypoint.positionChanged.connect(self.update_waypoints)
            waypoints.append(waypoint)
        return waypoints

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        if isinstance(self.flight.state, InFlight):
            ll = self.theater.point_to_ll(self.flight.state.estimate_position())
            return [ll.latitude, ll.longitude]
        return []

    @Property(list, notify=flightPlanChanged)
    def flightPlan(self) -> List[WaypointJs]:
        return self._waypoints

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.flight.departure.captured

    @Property(bool, notify=selectedChanged)
    def selected(self) -> bool:
        return self._selected

    @Slot(result=bool)
    def flightIsInAto(self) -> bool:
        if self.flight.package not in self.flight.squadron.coalition.ato.packages:
            return False
        if self.flight not in self.flight.package.flights:
            return False
        return True

    def set_selected(self, value: bool) -> None:
        self._selected = value
        self.selectedChanged.emit()

    @Property(list, notify=commitBoundaryChanged)
    def commitBoundary(self) -> LeafletPoly:
        if not isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            return []
        start = self.flight.flight_plan.patrol_start
        end = self.flight.flight_plan.patrol_end
        if isinstance(self.flight.flight_plan, CasFlightPlan):
            center = self.flight.flight_plan.target.position
            commit_center = ShapelyPoint(center.x, center.y)
        else:
            commit_center = LineString(
                [
                    ShapelyPoint(start.x, start.y),
                    ShapelyPoint(end.x, end.y),
                ]
            )
        bubble = commit_center.buffer(
            self.flight.flight_plan.engagement_distance.meters
        )
        return ShapelyUtil.poly_to_leaflet(bubble, self.theater)
