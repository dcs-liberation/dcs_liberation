from __future__ import annotations

import logging
from datetime import timedelta
from typing import List, Optional, Tuple, Union, Iterator

from PySide2.QtCore import Property, QObject, Signal, Slot
from dcs import Point
from dcs.unit import Unit
from dcs.vehicles import vehicle_map
from shapely.geometry import LineString, Point as ShapelyPoint, Polygon, MultiPolygon

from game import Game
from game.dcs.groundunittype import GroundUnitType
from game.flightplan import JoinZoneGeometry
from game.navmesh import NavMesh, NavMeshPoly
from game.profiling import logged_duration
from game.theater import (
    ConflictTheater,
    ControlPoint,
    TheaterGroundObject,
    FrontLine,
    LatLon,
    ControlPointStatus,
)
from game.threatzones import ThreatZones
from game.transfers import MultiGroupTransport, TransportMap
from game.utils import meters, nautical_miles
from gen.ato import AirTaskingOrder
from gen.flights.flight import Flight, FlightWaypoint, FlightWaypointType
from gen.flights.flightplan import (
    FlightPlan,
    PatrollingFlightPlan,
    CasFlightPlan,
)
from game.flightplan.ipzonegeometry import IpZoneGeometry
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel, AtoModel
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu

LeafletLatLon = list[float]
LeafletPoly = list[LeafletLatLon]

MAX_SHIP_DISTANCE = nautical_miles(80)

# Set to True to enable computing expensive debugging information. At the time of
# writing this only controls computing the waypoint placement zones.
ENABLE_EXPENSIVE_DEBUG_TOOLS = False

# **EVERY PROPERTY NEEDS A NOTIFY SIGNAL**
#
# https://bugreports.qt.io/browse/PYSIDE-1426
#
# PySide2 5.15.2 released 6 days before the fix for this was merged, but presumably we
# can clean up after 5.15.3 (or a future version) is released.
#
# Until then, all properties must use a notify signal. For some reason the error doesn't
# show up when running from source, and member properties also are not sufficient.
# Failing to do this will cause every sync of the property to emit an expensive log
# message. This can prevent the UI from being responsive.
#
# A local signal (i.e. `@Property(t, notify=Signal())`) is not sufficient. The class
# needs a named signal for every property, even if it is constant.


def shapely_poly_to_leaflet_points(
    poly: Polygon, theater: ConflictTheater
) -> LeafletPoly:
    if poly.is_empty:
        return []
    return [theater.point_to_ll(Point(x, y)).as_list() for x, y in poly.exterior.coords]


def shapely_to_leaflet_polys(
    poly: Union[Polygon, MultiPolygon], theater: ConflictTheater
) -> list[LeafletPoly]:
    if isinstance(poly, MultiPolygon):
        polys = poly.geoms
    else:
        polys = [poly]
    return [shapely_poly_to_leaflet_points(poly, theater) for poly in polys]


def shapely_line_to_leaflet_points(
    line: LineString, theater: ConflictTheater
) -> list[LeafletLatLon]:
    return [theater.point_to_ll(Point(x, y)).as_list() for x, y in line.coords]


class ControlPointJs(QObject):
    nameChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()
    mobileChanged = Signal()
    destinationChanged = Signal(list)
    categoryChanged = Signal()
    statusChanged = Signal()

    def __init__(
        self,
        control_point: ControlPoint,
        game_model: GameModel,
        theater: ConflictTheater,
    ) -> None:
        super().__init__()
        self.control_point = control_point
        self.game_model = game_model
        self.theater = theater
        self.dialog: Optional[QBaseMenu2] = None

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.control_point.name

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.control_point.captured

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.control_point.category

    @Property(str, notify=statusChanged)
    def status(self) -> str:
        status = self.control_point.status
        if status is ControlPointStatus.Functional:
            return "alive"
        elif status is ControlPointStatus.Damaged:
            return "damaged"
        elif status is ControlPointStatus.Destroyed:
            return "destroyed"
        raise ValueError(f"Unhandled ControlPointStatus: {status.name}")

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.control_point.position)
        return [ll.latitude, ll.longitude]

    @Property(bool, notify=mobileChanged)
    def mobile(self) -> bool:
        return self.control_point.moveable and self.control_point.captured

    @Property(list, notify=destinationChanged)
    def destination(self) -> LeafletLatLon:
        if self.control_point.target_position is None:
            # Qt seems to convert None to [] for list Properties :(
            return []
        return self.theater.point_to_ll(self.control_point.target_position).as_list()

    def destination_in_range(self, destination: Point) -> bool:
        move_distance = meters(
            destination.distance_to_point(self.control_point.position)
        )
        return move_distance <= MAX_SHIP_DISTANCE

    @Slot(list, result=bool)
    def destinationInRange(self, destination: LeafletLatLon) -> bool:
        return self.destination_in_range(self.theater.ll_to_point(LatLon(*destination)))

    @Slot(list, result=str)
    def setDestination(self, destination: LeafletLatLon) -> str:
        if not self.control_point.moveable:
            return f"{self.control_point} is not mobile"
        if not self.control_point.captured:
            return f"{self.control_point} is not owned by player"

        point = self.theater.ll_to_point(LatLon(*destination))
        if not self.destination_in_range(point):
            return (
                f"Cannot move {self.control_point} more than "
                f"{MAX_SHIP_DISTANCE.nautical_miles}nm."
            )
        self.control_point.target_position = point
        self.destinationChanged.emit(destination)
        return ""

    @Slot()
    def cancelTravel(self) -> None:
        self.control_point.target_position = None
        self.destinationChanged.emit([])

    @Slot()
    def showInfoDialog(self) -> None:
        if self.dialog is None:
            self.dialog = QBaseMenu2(None, self.control_point, self.game_model)
        self.dialog.show()

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.control_point)


class GroundObjectJs(QObject):
    nameChanged = Signal()
    controlPointNameChanged = Signal()
    unitsChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()
    samThreatRangesChanged = Signal()
    samDetectionRangesChanged = Signal()
    categoryChanged = Signal()
    deadChanged = Signal()

    def __init__(self, tgo: TheaterGroundObject, game: Game) -> None:
        super().__init__()
        self.tgo = tgo
        self.game = game
        self.theater = game.theater
        self.buildings = self.theater.find_ground_objects_by_obj_name(self.tgo.obj_name)
        self.dialog: Optional[QGroundObjectMenu] = None

    @Slot()
    def showInfoDialog(self) -> None:
        if self.dialog is None:
            self.dialog = QGroundObjectMenu(
                None,
                self.tgo,
                self.buildings,
                self.tgo.control_point,
                self.game,
            )
        self.dialog.show()

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.tgo)

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.tgo.name

    @Property(str, notify=controlPointNameChanged)
    def controlPointName(self) -> str:
        return self.tgo.control_point.name

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.tgo.category

    @staticmethod
    def make_unit_name(unit: Unit, dead: bool) -> str:
        dead_label = " [DEAD]" if dead else ""
        unit_display_name = unit.type
        dcs_unit_type = vehicle_map.get(unit.type)
        if dcs_unit_type is not None:
            # TODO: Make the TGO contain GroundUnitType instead of the pydcs Group.
            # This is a hack because we can't know which variant was used.
            try:
                unit_display_name = next(
                    GroundUnitType.for_dcs_type(dcs_unit_type)
                ).name
            except StopIteration:
                pass
        return f"Unit #{unit.id} - {unit_display_name}{dead_label}"

    @Property(list, notify=unitsChanged)
    def units(self) -> List[str]:
        units = []
        # TGOs with a non-empty group set are non-building TGOs. Building TGOs have no
        # groups set, but instead are one TGO per building "group" (DCS doesn't support
        # groups of statics) all with the same name.
        if self.tgo.groups:
            for unit in self.tgo.units:
                units.append(self.make_unit_name(unit, dead=False))
            for unit in self.tgo.dead_units:
                units.append(self.make_unit_name(unit, dead=True))
        else:
            for building in self.buildings:
                dead = " [DEAD]" if building.is_dead else ""
                units.append(f"{building.dcs_identifier}{dead}")
        return units

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.tgo.control_point.captured

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.tgo.position)
        return [ll.latitude, ll.longitude]

    @Property(bool, notify=deadChanged)
    def dead(self) -> bool:
        if not self.tgo.groups:
            return all(b.is_dead for b in self.buildings)
        return not any(g.units for g in self.tgo.groups)

    @Property(list, notify=samThreatRangesChanged)
    def samThreatRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            threat_range = self.tgo.threat_range(group)
            if threat_range:
                ranges.append(threat_range.meters)
        return ranges

    @Property(list, notify=samDetectionRangesChanged)
    def samDetectionRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            detection_range = self.tgo.detection_range(group)
            if detection_range:
                ranges.append(detection_range.meters)
        return ranges


class SupplyRouteJs(QObject):
    pointsChanged = Signal()
    frontActiveChanged = Signal()
    isSeaChanged = Signal()
    blueChanged = Signal()
    activeTransportsChanged = Signal()

    def __init__(
        self,
        a: ControlPoint,
        b: ControlPoint,
        points: List[LeafletLatLon],
        sea_route: bool,
        game: Game,
    ) -> None:
        super().__init__()
        self.control_point_a = a
        self.control_point_b = b
        self._points = points
        self.sea_route = sea_route
        self.game = game

    def find_in_transport_map(
        self, transport_map: TransportMap
    ) -> List[MultiGroupTransport]:
        transports = []
        transport = transport_map.find_transport(
            self.control_point_a, self.control_point_b
        )
        if transport is not None:
            transports.append(transport)
        transport = transport_map.find_transport(
            self.control_point_b, self.control_point_a
        )
        if transport is not None:
            transports.append(transport)
        return transports

    def find_transports(self) -> List[MultiGroupTransport]:
        if self.sea_route:
            return self.find_in_transport_map(
                self.game.blue.transfers.cargo_ships
            ) + self.find_in_transport_map(self.game.red.transfers.cargo_ships)
        return self.find_in_transport_map(
            self.game.blue.transfers.convoys
        ) + self.find_in_transport_map(self.game.red.transfers.convoys)

    @Property(list, notify=activeTransportsChanged)
    def activeTransports(self) -> List[str]:
        transports = self.find_transports()
        if not transports:
            return []

        descriptions = []
        for transport in transports:
            units = "units" if transport.size > 1 else "unit"
            descriptions.append(
                f"{transport.size} {units} transferring from {transport.origin} to "
                f"{transport.destination}"
            )
        return descriptions

    @Property(list, notify=pointsChanged)
    def points(self) -> List[LeafletLatLon]:
        return self._points

    @Property(bool, notify=frontActiveChanged)
    def frontActive(self) -> bool:
        if self.sea_route:
            return False
        return self.control_point_a.front_is_active(self.control_point_b)

    @Property(bool, notify=isSeaChanged)
    def isSea(self) -> bool:
        return self.sea_route

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.control_point_a.captured


class FrontLineJs(QObject):
    extentsChanged = Signal()

    def __init__(self, front_line: FrontLine, theater: ConflictTheater) -> None:
        super().__init__()
        self.front_line = front_line
        self.theater = theater

    @Property(list, notify=extentsChanged)
    def extents(self) -> List[LeafletLatLon]:
        a = self.theater.point_to_ll(
            self.front_line.position.point_from_heading(
                self.front_line.attack_heading + 90, nautical_miles(2).meters
            )
        )
        b = self.theater.point_to_ll(
            self.front_line.position.point_from_heading(
                self.front_line.attack_heading + 270, nautical_miles(2).meters
            )
        )
        return [[a.latitude, a.longitude], [b.latitude, b.longitude]]

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.front_line)


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


class FlightJs(QObject):
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

    @Property(list, notify=flightPlanChanged)
    def flightPlan(self) -> List[WaypointJs]:
        return self._waypoints

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.flight.departure.captured

    @Property(bool, notify=selectedChanged)
    def selected(self) -> bool:
        return self._selected

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
        return shapely_poly_to_leaflet_points(bubble, self.theater)


class ThreatZonesJs(QObject):
    fullChanged = Signal()
    aircraftChanged = Signal()
    airDefensesChanged = Signal()
    radarSamsChanged = Signal()

    def __init__(
        self,
        full: list[LeafletPoly],
        aircraft: list[LeafletPoly],
        air_defenses: list[LeafletPoly],
        radar_sams: list[LeafletPoly],
    ) -> None:
        super().__init__()
        self._full = full
        self._aircraft = aircraft
        self._air_defenses = air_defenses
        self._radar_sams = radar_sams

    @Property(list, notify=fullChanged)
    def full(self) -> list[LeafletPoly]:
        return self._full

    @Property(list, notify=aircraftChanged)
    def aircraft(self) -> list[LeafletPoly]:
        return self._aircraft

    @Property(list, notify=airDefensesChanged)
    def airDefenses(self) -> list[LeafletPoly]:
        return self._air_defenses

    @Property(list, notify=radarSamsChanged)
    def radarSams(self) -> list[LeafletPoly]:
        return self._radar_sams

    @classmethod
    def from_zones(cls, zones: ThreatZones, theater: ConflictTheater) -> ThreatZonesJs:
        return ThreatZonesJs(
            shapely_to_leaflet_polys(zones.all, theater),
            shapely_to_leaflet_polys(zones.airbases, theater),
            shapely_to_leaflet_polys(zones.air_defenses, theater),
            shapely_to_leaflet_polys(zones.radar_sam_threats, theater),
        )

    @classmethod
    def empty(cls) -> ThreatZonesJs:
        return ThreatZonesJs([], [], [], [])


class ThreatZoneContainerJs(QObject):
    blueChanged = Signal()
    redChanged = Signal()

    def __init__(self, blue: ThreatZonesJs, red: ThreatZonesJs) -> None:
        super().__init__()
        self._blue = blue
        self._red = red

    @Property(ThreatZonesJs, notify=blueChanged)
    def blue(self) -> ThreatZonesJs:
        return self._blue

    @Property(ThreatZonesJs, notify=redChanged)
    def red(self) -> ThreatZonesJs:
        return self._red


class NavMeshPolyJs(QObject):
    polyChanged = Signal()
    threatenedChanged = Signal()

    def __init__(self, poly: LeafletPoly, threatened: bool) -> None:
        super().__init__()
        self._poly = poly
        self._threatened = threatened

    @Property(list, notify=polyChanged)
    def poly(self) -> LeafletPoly:
        return self._poly

    @Property(bool, notify=threatenedChanged)
    def threatened(self) -> bool:
        return self._threatened

    @classmethod
    def from_navmesh(cls, poly: NavMeshPoly, theater: ConflictTheater) -> NavMeshPolyJs:
        return NavMeshPolyJs(
            shapely_poly_to_leaflet_points(poly.poly, theater), poly.threatened
        )


class NavMeshJs(QObject):
    blueChanged = Signal()
    redChanged = Signal()

    def __init__(self, blue: list[NavMeshPolyJs], red: list[NavMeshPolyJs]) -> None:
        super().__init__()
        self._blue = blue
        self._red = red
        # TODO: Boundary markers.
        # TODO: Numbering.
        # TODO: Localization debugging.

    @Property(list, notify=blueChanged)
    def blue(self) -> list[LeafletPoly]:
        return self._blue

    @Property(list, notify=redChanged)
    def red(self) -> list[LeafletPoly]:
        return self._red

    @staticmethod
    def to_polys(navmesh: NavMesh, theater: ConflictTheater) -> list[NavMeshPolyJs]:
        polys = []
        for poly in navmesh.polys:
            polys.append(NavMeshPolyJs.from_navmesh(poly, theater))
        return polys

    @classmethod
    def from_game(cls, game: Game) -> NavMeshJs:
        return NavMeshJs(
            cls.to_polys(game.blue.nav_mesh, game.theater),
            cls.to_polys(game.red.nav_mesh, game.theater),
        )


class MapZonesJs(QObject):
    inclusionZonesChanged = Signal()
    exclusionZonesChanged = Signal()
    seaZonesChanged = Signal()

    def __init__(
        self,
        inclusion_zones: list[LeafletPoly],
        exclusion_zones: list[LeafletPoly],
        sea_zones: list[LeafletPoly],
    ) -> None:
        super().__init__()
        self._inclusion_zones = inclusion_zones
        self._exclusion_zones = exclusion_zones
        self._sea_zones = sea_zones

    @Property(list, notify=inclusionZonesChanged)
    def inclusionZones(self) -> list[LeafletPoly]:
        return self._inclusion_zones

    @Property(list, notify=exclusionZonesChanged)
    def exclusionZones(self) -> list[LeafletPoly]:
        return self._exclusion_zones

    @Property(list, notify=seaZonesChanged)
    def seaZones(self) -> list[LeafletPoly]:
        return self._sea_zones

    @classmethod
    def from_game(cls, game: Game) -> MapZonesJs:
        zones = game.theater.landmap
        return MapZonesJs(
            shapely_to_leaflet_polys(zones.inclusion_zones, game.theater),
            shapely_to_leaflet_polys(zones.exclusion_zones, game.theater),
            shapely_to_leaflet_polys(zones.sea_zones, game.theater),
        )


class UnculledZone(QObject):
    positionChanged = Signal()
    radiusChanged = Signal()

    def __init__(self, position: LeafletLatLon, radius: float) -> None:
        super().__init__()
        self._position = position
        self._radius = radius

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        return self._position

    @Property(float, notify=radiusChanged)
    def radius(self) -> float:
        return self._radius

    @classmethod
    def each_from_game(cls, game: Game) -> Iterator[UnculledZone]:
        for zone in game.get_culling_zones():
            ll = game.theater.point_to_ll(zone)
            yield UnculledZone(
                [ll.latitude, ll.longitude], game.settings.perf_culling_distance * 1000
            )


class IpZonesJs(QObject):
    homeBubbleChanged = Signal()
    ipBubbleChanged = Signal()
    permissibleZoneChanged = Signal()
    safeZoneChanged = Signal()

    def __init__(
        self,
        home_bubble: list[LeafletPoly],
        ip_bubble: list[LeafletPoly],
        permissible_zone: list[LeafletPoly],
        safe_zone: list[LeafletPoly],
    ) -> None:
        super().__init__()
        self._home_bubble = home_bubble
        self._ip_bubble = ip_bubble
        self._permissible_zone = permissible_zone
        self._safe_zone = safe_zone

    @Property(list, notify=homeBubbleChanged)
    def homeBubble(self) -> list[LeafletPoly]:
        return self._home_bubble

    @Property(list, notify=ipBubbleChanged)
    def ipBubble(self) -> list[LeafletPoly]:
        return self._ip_bubble

    @Property(list, notify=permissibleZoneChanged)
    def permissibleZone(self) -> list[LeafletPoly]:
        return self._permissible_zone

    @Property(list, notify=safeZoneChanged)
    def safeZone(self) -> list[LeafletPoly]:
        return self._safe_zone

    @classmethod
    def empty(cls) -> IpZonesJs:
        return IpZonesJs([], [], [], [])

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> IpZonesJs:
        if not ENABLE_EXPENSIVE_DEBUG_TOOLS:
            return IpZonesJs.empty()
        target = flight.package.target
        home = flight.departure
        geometry = IpZoneGeometry(target.position, home.position, game.blue)
        return IpZonesJs(
            shapely_to_leaflet_polys(geometry.home_bubble, game.theater),
            shapely_to_leaflet_polys(geometry.ip_bubble, game.theater),
            shapely_to_leaflet_polys(geometry.permissible_zone, game.theater),
            shapely_to_leaflet_polys(geometry.safe_zone, game.theater),
        )


class JoinZonesJs(QObject):
    homeBubbleChanged = Signal()
    targetBubbleChanged = Signal()
    ipBubbleChanged = Signal()
    excludedZoneChanged = Signal()
    permissibleLineChanged = Signal()

    def __init__(
        self,
        home_bubble: list[LeafletPoly],
        target_bubble: list[LeafletPoly],
        ip_bubble: list[LeafletPoly],
        excluded_zone: list[LeafletPoly],
        permissible_line: list[LeafletLatLon],
    ) -> None:
        super().__init__()
        self._home_bubble = home_bubble
        self._target_bubble = target_bubble
        self._ip_bubble = ip_bubble
        self._excluded_zone = excluded_zone
        self._permissible_line = permissible_line

    @Property(list, notify=homeBubbleChanged)
    def homeBubble(self) -> list[LeafletPoly]:
        return self._home_bubble

    @Property(list, notify=targetBubbleChanged)
    def targetBubble(self) -> list[LeafletPoly]:
        return self._target_bubble

    @Property(list, notify=ipBubbleChanged)
    def ipBubble(self) -> list[LeafletPoly]:
        return self._ip_bubble

    @Property(list, notify=excludedZoneChanged)
    def excludedZone(self) -> list[LeafletPoly]:
        return self._excluded_zone

    @Property(list, notify=permissibleLineChanged)
    def permissibleLine(self) -> list[LeafletLatLon]:
        return self._permissible_line

    @classmethod
    def empty(cls) -> JoinZonesJs:
        return JoinZonesJs([], [], [], [], [])

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> JoinZonesJs:
        if not ENABLE_EXPENSIVE_DEBUG_TOOLS:
            return JoinZonesJs.empty()
        target = flight.package.target
        home = flight.departure
        if flight.package.waypoints is None:
            return JoinZonesJs.empty()
        ip = flight.package.waypoints.ingress
        geometry = JoinZoneGeometry(
            target.position, home.position, ip, game.blue, game.theater
        )
        return JoinZonesJs(
            shapely_to_leaflet_polys(geometry.home_bubble, game.theater),
            shapely_to_leaflet_polys(geometry.target_bubble, game.theater),
            shapely_to_leaflet_polys(geometry.ip_bubble, game.theater),
            shapely_to_leaflet_polys(geometry.excluded_zone, game.theater),
            shapely_line_to_leaflet_points(geometry.permissible_line, game.theater),
        )


class MapModel(QObject):
    cleared = Signal()

    mapCenterChanged = Signal(list)
    controlPointsChanged = Signal()
    groundObjectsChanged = Signal()
    supplyRoutesChanged = Signal()
    flightsChanged = Signal()
    frontLinesChanged = Signal()
    threatZonesChanged = Signal()
    navmeshesChanged = Signal()
    mapZonesChanged = Signal()
    unculledZonesChanged = Signal()
    ipZonesChanged = Signal()
    joinZonesChanged = Signal()

    def __init__(self, game_model: GameModel) -> None:
        super().__init__()
        self.game_model = game_model
        self._map_center = [0, 0]
        self._control_points = []
        self._ground_objects = []
        self._supply_routes = []
        self._flights = []
        self._front_lines = []
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.empty(), ThreatZonesJs.empty()
        )
        self._navmeshes = NavMeshJs([], [])
        self._map_zones = MapZonesJs([], [], [])
        self._unculled_zones = []
        self._ip_zones = IpZonesJs.empty()
        self._join_zones = JoinZonesJs.empty()
        self._selected_flight_index: Optional[Tuple[int, int]] = None
        GameUpdateSignal.get_instance().game_loaded.connect(self.on_game_load)
        GameUpdateSignal.get_instance().flight_paths_changed.connect(self.reset_atos)
        GameUpdateSignal.get_instance().package_selection_changed.connect(
            self.set_package_selection
        )
        GameUpdateSignal.get_instance().flight_selection_changed.connect(
            self.set_flight_selection
        )
        self.reset()

    def clear(self) -> None:
        self._control_points = []
        self._supply_routes = []
        self._ground_objects = []
        self._flights = []
        self._front_lines = []
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.empty(), ThreatZonesJs.empty()
        )
        self._navmeshes = NavMeshJs([], [])
        self._map_zones = MapZonesJs([], [], [])
        self._unculled_zones = []
        self._ip_zones = IpZonesJs.empty()
        self.cleared.emit()

    def set_package_selection(self, index: int) -> None:
        # Optional[int] isn't a valid type for a Qt signal. None will be converted to
        # zero automatically. We use -1 to indicate no selection.
        if index == -1:
            self._selected_flight_index = None
        else:
            self._selected_flight_index = index, 0
        self.reset_atos()

    def set_flight_selection(self, index: int) -> None:
        if self._selected_flight_index is None:
            if index != -1:
                # We don't know what order update_package_selection and
                # update_flight_selection will be called in when the last
                # package is removed. If no flight is selected, it's not a
                # problem to also have no package selected.
                logging.error("Flight was selected with no package selected")
            return

        # Optional[int] isn't a valid type for a Qt signal. None will be converted to
        # zero automatically. We use -1 to indicate no selection.
        if index == -1:
            self._selected_flight_index = self._selected_flight_index[0], None
        self._selected_flight_index = self._selected_flight_index[0], index
        self.reset_atos()

    @staticmethod
    def leaflet_coord_for(point: Point, theater: ConflictTheater) -> LeafletLatLon:
        ll = theater.point_to_ll(point)
        return [ll.latitude, ll.longitude]

    def reset(self) -> None:
        if self.game_model.game is None:
            self.clear()
            return
        with logged_duration("Map reset"):
            self.reset_control_points()
            self.reset_ground_objects()
            self.reset_routes()
            self.reset_atos()
            self.reset_front_lines()
            self.reset_threat_zones()
            self.reset_navmeshes()
            self.reset_map_zones()
            self.reset_unculled_zones()

    def on_game_load(self, game: Optional[Game]) -> None:
        if game is not None:
            self.reset_map_center(game.theater)

    def reset_map_center(self, theater: ConflictTheater) -> None:
        ll = theater.point_to_ll(theater.terrain.map_view_default.position)
        self._map_center = [ll.latitude, ll.longitude]
        self.mapCenterChanged.emit(self._map_center)

    @Property(list, notify=mapCenterChanged)
    def mapCenter(self) -> LeafletLatLon:
        return self._map_center

    def _flights_in_ato(self, ato: AirTaskingOrder, blue: bool) -> List[FlightJs]:
        flights = []
        for p_idx, package in enumerate(ato.packages):
            for f_idx, flight in enumerate(package.flights):
                flights.append(
                    FlightJs(
                        flight,
                        selected=blue and (p_idx, f_idx) == self._selected_flight_index,
                        theater=self.game.theater,
                        ato_model=self.game_model.ato_model_for(blue),
                    )
                )
        return flights

    def _get_selected_flight(self) -> Optional[Flight]:
        for p_idx, package in enumerate(self.game.blue.ato.packages):
            for f_idx, flight in enumerate(package.flights):
                if (p_idx, f_idx) == self._selected_flight_index:
                    return flight
        return None

    def reset_atos(self) -> None:
        self._flights = self._flights_in_ato(
            self.game.blue.ato, blue=True
        ) + self._flights_in_ato(self.game.red.ato, blue=False)
        self.flightsChanged.emit()
        selected_flight = self._get_selected_flight()
        if selected_flight is None:
            self._ip_zones = IpZonesJs.empty()
            self._join_zones = JoinZonesJs.empty()
        else:
            self._ip_zones = IpZonesJs.for_flight(selected_flight, self.game)
            self._join_zones = JoinZonesJs.for_flight(selected_flight, self.game)
        self.ipZonesChanged.emit()
        self.joinZonesChanged.emit()

    @Property(list, notify=flightsChanged)
    def flights(self) -> List[FlightJs]:
        return self._flights

    def reset_control_points(self) -> None:
        self._control_points = [
            ControlPointJs(c, self.game_model, self.game.theater)
            for c in self.game.theater.controlpoints
        ]
        self.controlPointsChanged.emit()

    @Property(list, notify=controlPointsChanged)
    def controlPoints(self) -> List[ControlPointJs]:
        return self._control_points

    def reset_ground_objects(self) -> None:
        seen = set()
        self._ground_objects = []
        for cp in self.game.theater.controlpoints:
            for tgo in cp.ground_objects:
                if tgo.name in seen:
                    continue
                seen.add(tgo.name)

                if tgo.is_control_point:
                    # TGOs that are the CP (CV groups) are an implementation quirk that
                    # we don't need to expose to the UI.
                    continue

                self._ground_objects.append(GroundObjectJs(tgo, self.game))
        self.groundObjectsChanged.emit()

    @Property(list, notify=groundObjectsChanged)
    def groundObjects(self) -> List[GroundObjectJs]:
        return self._ground_objects

    def reset_routes(self) -> None:
        seen = set()
        self._supply_routes = []
        for control_point in self.game.theater.controlpoints:
            seen.add(control_point)
            for destination, convoy_route in control_point.convoy_routes.items():
                if destination in seen:
                    continue
                self._supply_routes.append(
                    SupplyRouteJs(
                        control_point,
                        destination,
                        [
                            self.leaflet_coord_for(p, self.game.theater)
                            for p in convoy_route
                        ],
                        sea_route=False,
                        game=self.game,
                    )
                )
            for destination, shipping_lane in control_point.shipping_lanes.items():
                if destination in seen:
                    continue
                if control_point.is_friendly(destination.captured):
                    self._supply_routes.append(
                        SupplyRouteJs(
                            control_point,
                            destination,
                            [
                                self.leaflet_coord_for(p, self.game.theater)
                                for p in shipping_lane
                            ],
                            sea_route=True,
                            game=self.game,
                        )
                    )
        self.supplyRoutesChanged.emit()

    @Property(list, notify=supplyRoutesChanged)
    def supplyRoutes(self) -> List[SupplyRouteJs]:
        return self._supply_routes

    def reset_front_lines(self) -> None:
        self._front_lines = [
            FrontLineJs(f, self.game.theater) for f in self.game.theater.conflicts()
        ]
        self.frontLinesChanged.emit()

    @Property(list, notify=frontLinesChanged)
    def frontLines(self) -> List[FrontLineJs]:
        return self._front_lines

    def reset_threat_zones(self) -> None:
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.from_zones(
                self.game.threat_zone_for(player=True), self.game.theater
            ),
            ThreatZonesJs.from_zones(
                self.game.threat_zone_for(player=False), self.game.theater
            ),
        )
        self.threatZonesChanged.emit()

    @Property(ThreatZoneContainerJs, notify=threatZonesChanged)
    def threatZones(self) -> ThreatZoneContainerJs:
        return self._threat_zones

    def reset_navmeshes(self) -> None:
        self._navmeshes = NavMeshJs.from_game(self.game)
        self.navmeshesChanged.emit()

    @Property(NavMeshJs, notify=navmeshesChanged)
    def navmeshes(self) -> NavMeshJs:
        return self._navmeshes

    def reset_map_zones(self) -> None:
        self._map_zones = MapZonesJs.from_game(self.game)
        self.mapZonesChanged.emit()

    @Property(MapZonesJs, notify=mapZonesChanged)
    def mapZones(self) -> NavMeshJs:
        return self._map_zones

    def reset_unculled_zones(self) -> None:
        self._unculled_zones = list(UnculledZone.each_from_game(self.game))
        self.unculledZonesChanged.emit()

    @Property(list, notify=unculledZonesChanged)
    def unculledZones(self) -> list[UnculledZone]:
        return self._unculled_zones

    @Property(IpZonesJs, notify=ipZonesChanged)
    def ipZones(self) -> IpZonesJs:
        return self._ip_zones

    @Property(JoinZonesJs, notify=joinZonesChanged)
    def joinZones(self) -> JoinZonesJs:
        return self._join_zones

    @property
    def game(self) -> Game:
        if self.game_model.game is None:
            raise RuntimeError("No game loaded")
        return self.game_model.game
