from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from PySide2.QtCore import Property, QObject, Signal, Slot

from game.ato import Flight, FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.theater import ConflictTheater, LatLon
from gen.flights.flightplan import FlightPlan
from qt_ui.models import AtoModel
from .leaflet import LeafletLatLon

if TYPE_CHECKING:
    from .flightjs import FlightJs


class WaypointJs(QObject):
    numberChanged = Signal()
    positionChanged = Signal()
    altitudeFtChanged = Signal()
    altitudeReferenceChanged = Signal()
    nameChanged = Signal()
    timingChanged = Signal()
    isTargetPointChanged = Signal()
    isTakeoffChanged = Signal()
    isLandingChanged = Signal()
    isDivertChanged = Signal()
    isBullseyeChanged = Signal()

    def __init__(
        self,
        waypoint: FlightWaypoint,
        number: int,
        flight_model: FlightJs,
        theater: ConflictTheater,
        ato_model: AtoModel,
    ) -> None:
        super().__init__()
        self.waypoint = waypoint
        self._number = number
        self.flight_model = flight_model
        self.theater = theater
        self.ato_model = ato_model

    @property
    def flight(self) -> Flight:
        return self.flight_model.flight

    @property
    def flight_plan(self) -> FlightPlan:
        return self.flight.flight_plan

    @Property(int, notify=numberChanged)
    def number(self) -> int:
        return self._number

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.waypoint.position)
        return [ll.latitude, ll.longitude]

    @Property(int, notify=altitudeFtChanged)
    def altitudeFt(self) -> int:
        return int(self.waypoint.alt.feet)

    @Property(str, notify=altitudeReferenceChanged)
    def altitudeReference(self) -> str:
        return "AGL" if self.waypoint.alt_type == "RADIO" else "MSL"

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.waypoint.name

    @Property(str, notify=timingChanged)
    def timing(self) -> str:
        prefix = "TOT"
        time = self.flight_plan.tot_for_waypoint(self.waypoint)
        if time is None:
            prefix = "Depart"
            time = self.flight_plan.depart_time_for_waypoint(self.waypoint)
        if time is None:
            return ""
        return f"{prefix} T+{timedelta(seconds=int(time.total_seconds()))}"

    @Property(bool, notify=isTargetPointChanged)
    def isTargetPoint(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.TARGET_POINT

    @Property(bool, notify=isTakeoffChanged)
    def isTakeoff(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.TAKEOFF

    @Property(bool, notify=isLandingChanged)
    def isLanding(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.LANDING_POINT

    @Property(bool, notify=isDivertChanged)
    def isDivert(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.DIVERT

    @Property(bool, notify=isBullseyeChanged)
    def isBullseye(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.BULLSEYE

    @Slot(list, result=str)
    def setPosition(self, position: LeafletLatLon) -> str:
        point = self.theater.ll_to_point(LatLon(*position))
        self.waypoint.x = point.x
        self.waypoint.y = point.y
        package = self.ato_model.find_matching_package_model(self.flight.package)
        if package is None:
            return "Could not find package model containing modified flight"
        package.update_tot()
        self.positionChanged.emit()
        self.flight_model.commitBoundaryChanged.emit()
        return ""
