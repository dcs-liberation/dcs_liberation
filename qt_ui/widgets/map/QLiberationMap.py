from __future__ import annotations

import datetime
import logging
import math
from functools import singledispatchmethod
from typing import Iterable, Iterator, List, Optional, Tuple

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QLineF, QPointF, QRectF, Qt
from PySide2.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPen,
    QPixmap,
    QPolygonF,
    QWheelEvent,
)
from PySide2.QtWidgets import (
    QFrame,
    QGraphicsItem,
    QGraphicsOpacityEffect,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QGraphicsView,
)
from dcs import Point
from dcs.mapping import point_from_heading
from dcs.planes import F_16C_50
from dcs.unitgroup import Group
from shapely.geometry import (
    LineString,
    MultiPolygon,
    Point as ShapelyPoint,
    Polygon,
)

import qt_ui.uiconstants as CONST
from game import Game
from game.navmesh import NavMesh
from game.theater import ControlPoint, Enum
from game.theater.conflicttheater import FrontLine, ReferencePoint
from game.theater.theatergroundobject import (
    TheaterGroundObject,
)
from game.transfers import Convoy
from game.utils import Distance, meters, nautical_miles, pairwise
from game.weather import TimeOfDay
from gen import Conflict, Package
from gen.flights.flight import (
    Flight,
    FlightType,
    FlightWaypoint,
    FlightWaypointType,
)
from gen.flights.flightplan import (
    FlightPlan,
    FlightPlanBuilder,
    InvalidObjectiveLocation,
    PatrollingFlightPlan,
)
from gen.flights.traveltime import TotEstimator
from qt_ui.displayoptions import DisplayOptions, ThreatZoneOptions
from qt_ui.models import GameModel
from qt_ui.widgets.map.QFrontLine import QFrontLine
from qt_ui.widgets.map.QLiberationScene import QLiberationScene
from qt_ui.widgets.map.QMapControlPoint import QMapControlPoint
from qt_ui.widgets.map.QMapGroundObject import QMapGroundObject
from qt_ui.widgets.map.ShippingLaneSegment import ShippingLaneSegment
from qt_ui.widgets.map.SupplyRouteSegment import SupplyRouteSegment
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

MAX_SHIP_DISTANCE = nautical_miles(80)


MapPoint = Tuple[float, float]


def binomial(i: int, n: int) -> float:
    """Binomial coefficient"""
    return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))


def bernstein(t: float, i: int, n: int) -> float:
    """Bernstein polynom"""
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t: float, points: Iterable[Tuple[float, float]]) -> Tuple[float, float]:
    """Calculate coordinate of a point in the bezier curve"""
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bern = bernstein(t, i, n)
        x += pos[0] * bern
        y += pos[1] * bern
    return x, y


def bezier_curve_range(
    n: int, points: Iterable[Tuple[float, float]]
) -> Iterator[Tuple[float, float]]:
    """Range of points in a curve bezier"""
    for i in range(n):
        t = i / float(n - 1)
        yield bezier(t, points)


class QLiberationMapState(Enum):
    NORMAL = 0
    MOVING_UNIT = 1


class QLiberationMap(QGraphicsView):

    WAYPOINT_SIZE = 4
    reference_point_setup_mode = False
    instance: Optional[QLiberationMap] = None

    def __init__(self, game_model: GameModel):
        super(QLiberationMap, self).__init__()
        QLiberationMap.instance = self
        self.game_model = game_model
        self.game: Optional[Game] = game_model.game
        self.state = QLiberationMapState.NORMAL

        self.waypoint_info_font = QFont()
        self.waypoint_info_font.setPointSize(12)

        self.flight_path_items: List[QGraphicsItem] = []
        # A tuple of (package index, flight index), or none.
        self.selected_flight: Optional[Tuple[int, int]] = None

        self.setMinimumSize(800, 600)
        self.setMaximumHeight(2160)
        self._zoom = 0
        self.factor = 1
        self.factorized = 1
        self.init_scene()
        self.setGame(game_model.game)

        # Object displayed when unit is selected
        self.movement_line = QtWidgets.QGraphicsLineItem(
            QtCore.QLineF(QPointF(0, 0), QPointF(0, 0))
        )
        self.movement_line.setPen(QPen(CONST.COLORS["orange"], width=10.0))
        self.selected_cp: QMapControlPoint = None

        GameUpdateSignal.get_instance().flight_paths_changed.connect(
            lambda: self.draw_flight_plans(self.scene())
        )

        def update_package_selection(index: int) -> None:
            # Optional[int] isn't a valid type for a Qt signal. None will be
            # converted to zero automatically. We use -1 to indicate no
            # selection.
            if index == -1:
                self.selected_flight = None
            else:
                self.selected_flight = index, 0
            self.draw_flight_plans(self.scene())

        GameUpdateSignal.get_instance().package_selection_changed.connect(
            update_package_selection
        )

        def update_flight_selection(index: int) -> None:
            if self.selected_flight is None:
                if index != -1:
                    # We don't know what order update_package_selection and
                    # update_flight_selection will be called in when the last
                    # package is removed. If no flight is selected, it's not a
                    # problem to also have no package selected.
                    logging.error("Flight was selected with no package selected")
                return

            # Optional[int] isn't a valid type for a Qt signal. None will be
            # converted to zero automatically. We use -1 to indicate no
            # selection.
            if index == -1:
                self.selected_flight = self.selected_flight[0], None
            self.selected_flight = self.selected_flight[0], index
            self.draw_flight_plans(self.scene())

        GameUpdateSignal.get_instance().flight_selection_changed.connect(
            update_flight_selection
        )

        self.nm_to_pixel_ratio: int = 0

        self.navmesh_highlight: Optional[QPolygonF] = None
        self.shortest_path_segments: List[QLineF] = []

    def init_scene(self):
        scene = QLiberationScene(self)
        self.setScene(scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def setGame(self, game: Optional[Game]):
        self.game = game
        if self.game is not None:
            logging.debug("Reloading Map Canvas")
            self.nm_to_pixel_ratio = self.distance_to_pixels(nautical_miles(1))
            self.reload_scene()

    """
    
    Uncomment to set up theather reference points"""

    def keyPressEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if not self.reference_point_setup_mode:
            if modifiers == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_R:
                self.reference_point_setup_mode = True
                self.reload_scene()
            else:
                super(QLiberationMap, self).keyPressEvent(event)
        else:
            if modifiers == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_R:
                self.reference_point_setup_mode = False
                self.reload_scene()
            else:
                distance = 1
                modifiers = int(event.modifiers())
                if modifiers & QtCore.Qt.ShiftModifier:
                    distance *= 10
                elif modifiers & QtCore.Qt.ControlModifier:
                    distance *= 100

                if event.key() == QtCore.Qt.Key_Down:
                    self.update_reference_point(
                        self.game.theater.reference_points[0], Point(0, distance)
                    )
                if event.key() == QtCore.Qt.Key_Up:
                    self.update_reference_point(
                        self.game.theater.reference_points[0], Point(0, -distance)
                    )
                if event.key() == QtCore.Qt.Key_Left:
                    self.update_reference_point(
                        self.game.theater.reference_points[0], Point(-distance, 0)
                    )
                if event.key() == QtCore.Qt.Key_Right:
                    self.update_reference_point(
                        self.game.theater.reference_points[0], Point(distance, 0)
                    )

                if event.key() == QtCore.Qt.Key_S:
                    self.update_reference_point(
                        self.game.theater.reference_points[1], Point(0, distance)
                    )
                if event.key() == QtCore.Qt.Key_W:
                    self.update_reference_point(
                        self.game.theater.reference_points[1], Point(0, -distance)
                    )
                if event.key() == QtCore.Qt.Key_A:
                    self.update_reference_point(
                        self.game.theater.reference_points[1], Point(-distance, 0)
                    )
                if event.key() == QtCore.Qt.Key_D:
                    self.update_reference_point(
                        self.game.theater.reference_points[1], Point(distance, 0)
                    )

                logging.debug(f"Reference points: {self.game.theater.reference_points}")
                self.reload_scene()

    @staticmethod
    def update_reference_point(point: ReferencePoint, change: Point) -> None:
        point.image_coordinates += change

    def display_culling(self, scene: QGraphicsScene) -> None:
        """Draws the culling distance rings on the map"""
        culling_points = self.game_model.game.get_culling_points()
        culling_zones = self.game_model.game.get_culling_zones()
        culling_distance = self.game_model.game.settings.perf_culling_distance
        for point in culling_points:
            culling_distance_point = Point(point.x + 2500, point.y + 2500)
            distance_point = self._transform_point(culling_distance_point)
            transformed = self._transform_point(point)
            radius = distance_point[0] - transformed[0]
            scene.addEllipse(
                transformed[0] - radius,
                transformed[1] - radius,
                2 * radius,
                2 * radius,
                CONST.COLORS["transparent"],
                CONST.COLORS["light_green_transparent"],
            )
        for zone in culling_zones:
            culling_distance_zone = Point(
                zone.x + culling_distance * 1000, zone.y + culling_distance * 1000
            )
            distance_zone = self._transform_point(culling_distance_zone)
            transformed = self._transform_point(zone)
            radius = distance_zone[0] - transformed[0]
            scene.addEllipse(
                transformed[0] - radius,
                transformed[1] - radius,
                2 * radius,
                2 * radius,
                CONST.COLORS["transparent"],
                CONST.COLORS["light_green_transparent"],
            )

    def draw_shapely_poly(
        self, scene: QGraphicsScene, poly: Polygon, pen: QPen, brush: QBrush
    ) -> Optional[QPolygonF]:
        if poly.is_empty:
            return None
        points = []
        for x, y in poly.exterior.coords:
            x, y = self._transform_point(Point(x, y))
            points.append(QPointF(x, y))
        return scene.addPolygon(QPolygonF(points), pen, brush)

    def draw_threat_zone(
        self, scene: QGraphicsScene, poly: Polygon, player: bool
    ) -> None:
        if player:
            brush = QColor(0, 132, 255, 100)
        else:
            brush = QColor(227, 32, 0, 100)
        self.draw_shapely_poly(scene, poly, CONST.COLORS["transparent"], brush)

    def display_threat_zones(
        self, scene: QGraphicsScene, options: ThreatZoneOptions, player: bool
    ) -> None:
        """Draws the threat zones on the map."""
        threat_zones = self.game.threat_zone_for(player)
        if options.all:
            threat_poly = threat_zones.all
        elif options.aircraft:
            threat_poly = threat_zones.airbases
        elif options.air_defenses:
            threat_poly = threat_zones.air_defenses
        else:
            return

        if isinstance(threat_poly, MultiPolygon):
            polys = threat_poly.geoms
        else:
            polys = [threat_poly]
        for poly in polys:
            self.draw_threat_zone(scene, poly, player)

    def draw_navmesh_neighbor_line(
        self, scene: QGraphicsScene, poly: Polygon, begin: ShapelyPoint
    ) -> None:
        vertex = Point(begin.x, begin.y)
        centroid = poly.centroid
        direction = Point(centroid.x, centroid.y)
        end = vertex.point_from_heading(
            vertex.heading_between_point(direction), nautical_miles(2).meters
        )

        scene.addLine(
            QLineF(
                QPointF(*self._transform_point(vertex)),
                QPointF(*self._transform_point(end)),
            ),
            CONST.COLORS["yellow"],
        )

    @singledispatchmethod
    def draw_navmesh_border(
        self, intersection, scene: QGraphicsScene, poly: Polygon
    ) -> None:
        raise NotImplementedError(
            "draw_navmesh_border not implemented for %s",
            intersection.__class__.__name__,
        )

    @draw_navmesh_border.register
    def draw_navmesh_point_border(
        self, intersection: ShapelyPoint, scene: QGraphicsScene, poly: Polygon
    ) -> None:
        # Draw a line from the vertex toward the center of the polygon.
        self.draw_navmesh_neighbor_line(scene, poly, intersection)

    @draw_navmesh_border.register
    def draw_navmesh_edge_border(
        self, intersection: LineString, scene: QGraphicsScene, poly: Polygon
    ) -> None:
        # Draw a line from the center of the edge toward the center of the
        # polygon.
        edge_center = intersection.interpolate(0.5, normalized=True)
        self.draw_navmesh_neighbor_line(scene, poly, edge_center)

    def display_navmesh(self, scene: QGraphicsScene, player: bool) -> None:
        for navpoly in self.game.navmesh_for(player).polys:
            self.draw_shapely_poly(
                scene, navpoly.poly, CONST.COLORS["black"], CONST.COLORS["transparent"]
            )

            position = self._transform_point(
                Point(navpoly.poly.centroid.x, navpoly.poly.centroid.y)
            )
            text = scene.addSimpleText(
                f"Navmesh {navpoly.ident}", self.waypoint_info_font
            )
            text.setBrush(QColor(255, 255, 255))
            text.setPen(QColor(255, 255, 255))
            text.moveBy(position[0] + 8, position[1])
            text.setZValue(2)

            for border in navpoly.neighbors.values():
                self.draw_navmesh_border(border, scene, navpoly.poly)

    def highlight_mouse_navmesh(
        self, scene: QGraphicsScene, navmesh: NavMesh, mouse_position: Point
    ) -> None:
        if self.navmesh_highlight is not None:
            try:
                scene.removeItem(self.navmesh_highlight)
            except RuntimeError:
                pass
        navpoly = navmesh.localize(mouse_position)
        if navpoly is None:
            return
        self.navmesh_highlight = self.draw_shapely_poly(
            scene,
            navpoly.poly,
            CONST.COLORS["transparent"],
            CONST.COLORS["light_green_transparent"],
        )

    def draw_shortest_path(
        self, scene: QGraphicsScene, navmesh: NavMesh, destination: Point, player: bool
    ) -> None:
        for line in self.shortest_path_segments:
            try:
                scene.removeItem(line)
            except RuntimeError:
                pass

        if player:
            origin = self.game.theater.player_points()[0]
        else:
            origin = self.game.theater.enemy_points()[0]

        prev_pos = self._transform_point(origin.position)
        try:
            path = navmesh.shortest_path(origin.position, destination)
        except ValueError:
            return
        for waypoint in path[1:]:
            new_pos = self._transform_point(waypoint)
            flight_path_pen = self.flight_path_pen(player, selected=True)
            # Draw the line to the *middle* of the waypoint.
            offset = self.WAYPOINT_SIZE // 2
            self.shortest_path_segments.append(
                scene.addLine(
                    prev_pos[0] + offset,
                    prev_pos[1] + offset,
                    new_pos[0] + offset,
                    new_pos[1] + offset,
                    flight_path_pen,
                )
            )

            self.shortest_path_segments.append(
                scene.addEllipse(
                    new_pos[0],
                    new_pos[1],
                    self.WAYPOINT_SIZE,
                    self.WAYPOINT_SIZE,
                    flight_path_pen,
                    flight_path_pen,
                )
            )

            prev_pos = new_pos

    def draw_test_flight_plan(
        self,
        scene: QGraphicsScene,
        task: FlightType,
        point_near_target: Point,
        player: bool,
    ) -> None:
        for line in self.shortest_path_segments:
            try:
                scene.removeItem(line)
            except RuntimeError:
                pass

        self.clear_flight_paths(scene)

        target = self.game.theater.closest_target(point_near_target)

        if player:
            origin = self.game.theater.player_points()[0]
        else:
            origin = self.game.theater.enemy_points()[0]

        package = Package(target)
        flight = Flight(
            package,
            self.game.player_country if player else self.game.enemy_country,
            F_16C_50,
            2,
            task,
            start_type="Warm",
            departure=origin,
            arrival=origin,
            divert=None,
        )
        package.add_flight(flight)
        planner = FlightPlanBuilder(self.game, package, is_player=player)
        try:
            planner.populate_flight_plan(flight)
        except InvalidObjectiveLocation:
            return

        package.time_over_target = TotEstimator(package).earliest_tot()
        self.draw_flight_plan(scene, flight, selected=True)

    @staticmethod
    def should_display_ground_objects_at(cp: ControlPoint) -> bool:
        return (DisplayOptions.sam_ranges and cp.captured) or (
            DisplayOptions.enemy_sam_ranges and not cp.captured
        )

    def draw_threat_range(
        self,
        scene: QGraphicsScene,
        group: Group,
        ground_object: TheaterGroundObject,
        cp: ControlPoint,
    ) -> None:
        go_pos = self._transform_point(ground_object.position)
        detection_range = ground_object.detection_range(group)
        threat_range = ground_object.threat_range(group)
        if threat_range:
            threat_pos = self._transform_point(
                ground_object.position + Point(threat_range.meters, threat_range.meters)
            )
            threat_radius = Point(*go_pos).distance_to_point(Point(*threat_pos))

            # Add threat range circle
            scene.addEllipse(
                go_pos[0] - threat_radius / 2 + 7,
                go_pos[1] - threat_radius / 2 + 6,
                threat_radius,
                threat_radius,
                self.threat_pen(cp.captured),
            )

        if detection_range and DisplayOptions.detection_range:
            # Add detection range circle
            detection_pos = self._transform_point(
                ground_object.position
                + Point(detection_range.meters, detection_range.meters)
            )
            detection_radius = Point(*go_pos).distance_to_point(Point(*detection_pos))
            scene.addEllipse(
                go_pos[0] - detection_radius / 2 + 7,
                go_pos[1] - detection_radius / 2 + 6,
                detection_radius,
                detection_radius,
                self.detection_pen(cp.captured),
            )

    def draw_ground_objects(self, scene: QGraphicsScene, cp: ControlPoint) -> None:
        added_objects = []
        for ground_object in cp.ground_objects:
            if ground_object.obj_name in added_objects:
                continue

            go_pos = self._transform_point(ground_object.position)
            if not ground_object.airbase_group:
                buildings = self.game.theater.find_ground_objects_by_obj_name(
                    ground_object.obj_name
                )
                scene.addItem(
                    QMapGroundObject(
                        self,
                        go_pos[0],
                        go_pos[1],
                        14,
                        12,
                        cp,
                        ground_object,
                        self.game,
                        buildings,
                    )
                )

            should_display = self.should_display_ground_objects_at(cp)
            if ground_object.might_have_aa and should_display:
                for group in ground_object.groups:
                    self.draw_threat_range(scene, group, ground_object, cp)
            added_objects.append(ground_object.obj_name)

    def reload_scene(self):
        scene = self.scene()
        scene.clear()

        playerColor = self.game.get_player_color()
        enemyColor = self.game.get_enemy_color()

        self.addBackground()

        # Display Culling
        if DisplayOptions.culling and self.game.settings.perf_culling:
            self.display_culling(scene)

        self.display_threat_zones(scene, DisplayOptions.blue_threat_zones, player=True)
        self.display_threat_zones(scene, DisplayOptions.red_threat_zones, player=False)

        if DisplayOptions.navmeshes.blue_navmesh:
            self.display_navmesh(scene, player=True)
        if DisplayOptions.navmeshes.red_navmesh:
            self.display_navmesh(scene, player=False)

        for cp in self.game.theater.controlpoints:

            pos = self._transform_point(cp.position)

            scene.addItem(
                QMapControlPoint(
                    self,
                    pos[0] - CONST.CP_SIZE / 2,
                    pos[1] - CONST.CP_SIZE / 2,
                    CONST.CP_SIZE,
                    CONST.CP_SIZE,
                    cp,
                    self.game_model,
                )
            )

            if cp.captured:
                pen = QPen(brush=CONST.COLORS[playerColor])
                brush = CONST.COLORS[playerColor + "_transparent"]
            else:
                pen = QPen(brush=CONST.COLORS[enemyColor])
                brush = CONST.COLORS[enemyColor + "_transparent"]

            self.draw_ground_objects(scene, cp)

            if cp.target_position is not None:
                proj = self._transform_point(cp.target_position)
                scene.addLine(
                    QLineF(QPointF(pos[0], pos[1]), QPointF(proj[0], proj[1])),
                    QPen(CONST.COLORS["green"], width=10, s=Qt.DashDotLine),
                )

        self.draw_supply_routes()
        self.draw_flight_plans(scene)

        for cp in self.game.theater.controlpoints:
            pos = self._transform_point(cp.position)
            text = scene.addText(cp.name, font=CONST.FONT_MAP)
            text.setPos(pos[0] + CONST.CP_SIZE, pos[1] - CONST.CP_SIZE / 2)
            text = scene.addText(cp.name, font=CONST.FONT_MAP)
            text.setDefaultTextColor(Qt.white)
            text.setPos(pos[0] + CONST.CP_SIZE + 1, pos[1] - CONST.CP_SIZE / 2 + 1)

    def clear_flight_paths(self, scene: QGraphicsScene) -> None:
        for item in self.flight_path_items:
            try:
                scene.removeItem(item)
            except RuntimeError:
                # Something may have caused those items to already be removed.
                pass
        self.flight_path_items.clear()

    def draw_flight_plans(self, scene: QGraphicsScene) -> None:
        self.clear_flight_paths(scene)
        if DisplayOptions.flight_paths.hide:
            return
        packages = list(self.game_model.ato_model.packages)
        if self.game.settings.show_red_ato:
            packages.extend(self.game_model.red_ato_model.packages)
        for p_idx, package_model in enumerate(packages):
            for f_idx, flight in enumerate(package_model.flights):
                if self.selected_flight is None:
                    selected = False
                else:
                    selected = (p_idx, f_idx) == self.selected_flight
                if DisplayOptions.flight_paths.only_selected and not selected:
                    continue
                self.draw_flight_plan(scene, flight, selected)

    def draw_flight_plan(
        self, scene: QGraphicsScene, flight: Flight, selected: bool
    ) -> None:
        is_player = flight.from_cp.captured
        pos = self._transform_point(flight.from_cp.position)

        self.draw_waypoint(scene, pos, is_player, selected)
        prev_pos = tuple(pos)
        drew_target = False
        target_types = (
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_SHIP,
        )
        for idx, point in enumerate(flight.flight_plan.waypoints[1:]):
            if point.waypoint_type == FlightWaypointType.DIVERT:
                # Don't clutter the map showing divert points.
                continue

            new_pos = self._transform_point(Point(point.x, point.y))
            self.draw_flight_path(scene, prev_pos, new_pos, is_player, selected)
            self.draw_waypoint(scene, new_pos, is_player, selected)
            if selected and DisplayOptions.waypoint_info:
                if point.waypoint_type in target_types:
                    if drew_target:
                        # Don't draw dozens of targets over each other.
                        continue
                    drew_target = True
                self.draw_waypoint_info(
                    scene, idx + 1, point, new_pos, flight.flight_plan
                )
            prev_pos = tuple(new_pos)

        if selected and DisplayOptions.patrol_engagement_range:
            self.draw_patrol_commit_range(scene, flight)

    def draw_patrol_commit_range(self, scene: QGraphicsScene, flight: Flight) -> None:
        if not isinstance(flight.flight_plan, PatrollingFlightPlan):
            return
        start = flight.flight_plan.patrol_start
        end = flight.flight_plan.patrol_end
        line = LineString(
            [
                ShapelyPoint(start.x, start.y),
                ShapelyPoint(end.x, end.y),
            ]
        )
        doctrine = self.game.faction_for(flight.departure.captured).doctrine
        bubble = line.buffer(doctrine.cap_engagement_range.meters)
        self.flight_path_items.append(
            self.draw_shapely_poly(
                scene, bubble, CONST.COLORS["yellow"], CONST.COLORS["transparent"]
            )
        )

    def draw_waypoint(
        self,
        scene: QGraphicsScene,
        position: Tuple[float, float],
        player: bool,
        selected: bool,
    ) -> None:
        waypoint_pen = self.waypoint_pen(player, selected)
        waypoint_brush = self.waypoint_brush(player, selected)
        self.flight_path_items.append(
            scene.addEllipse(
                position[0],
                position[1],
                self.WAYPOINT_SIZE,
                self.WAYPOINT_SIZE,
                waypoint_pen,
                waypoint_brush,
            )
        )

    def draw_waypoint_info(
        self,
        scene: QGraphicsScene,
        number: int,
        waypoint: FlightWaypoint,
        position: Tuple[int, int],
        flight_plan: FlightPlan,
    ) -> None:

        altitude = int(waypoint.alt.feet)
        altitude_type = "AGL" if waypoint.alt_type == "RADIO" else "MSL"

        prefix = "TOT"
        time = flight_plan.tot_for_waypoint(waypoint)
        if time is None:
            prefix = "Depart"
            time = flight_plan.depart_time_for_waypoint(waypoint)
        if time is None:
            tot = ""
        else:
            time = datetime.timedelta(seconds=int(time.total_seconds()))
            tot = f"{prefix} T+{time}"

        pen = QPen(QColor("black"), 0.3)
        brush = QColor("white")

        text = "\n".join(
            [
                f"{number} {waypoint.name}",
                f"{altitude} ft {altitude_type}",
                tot,
            ]
        )

        item = scene.addSimpleText(text, self.waypoint_info_font)
        item.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        item.setBrush(brush)
        item.setPen(pen)
        item.moveBy(position[0] + 8, position[1])
        item.setZValue(2)
        self.flight_path_items.append(item)

    def draw_flight_path(
        self,
        scene: QGraphicsScene,
        pos0: Tuple[float, float],
        pos1: Tuple[float, float],
        player: bool,
        selected: bool,
    ) -> None:
        flight_path_pen = self.flight_path_pen(player, selected)
        # Draw the line to the *middle* of the waypoint.
        offset = self.WAYPOINT_SIZE // 2
        self.flight_path_items.append(
            scene.addLine(
                pos0[0] + offset,
                pos0[1] + offset,
                pos1[0] + offset,
                pos1[1] + offset,
                flight_path_pen,
            )
        )

    def bezier_points(
        self, points: Iterable[Point]
    ) -> Iterator[Tuple[MapPoint, MapPoint]]:
        # Thanks to Alquimista for sharing a python implementation of the bezier
        # algorithm this is adapted from.
        # https://gist.github.com/Alquimista/1274149#file-bezdraw-py
        bezier_fixed_points = []
        for a, b in pairwise(points):
            bezier_fixed_points.append(self._transform_point(a))
            bezier_fixed_points.append(self._transform_point(b))

        old_point = bezier_fixed_points[0]
        for point in bezier_curve_range(
            int(len(bezier_fixed_points) * 2), bezier_fixed_points
        ):
            yield old_point, point
            old_point = point

    def draw_bezier_frontline(
        self,
        scene: QGraphicsScene,
        frontline: FrontLine,
        convoys: List[Convoy],
    ) -> None:
        for a, b in self.bezier_points(frontline.points):
            scene.addItem(
                SupplyRouteSegment(
                    a[0],
                    a[1],
                    b[0],
                    b[1],
                    frontline.control_point_a,
                    frontline.control_point_b,
                    convoys,
                )
            )

    def draw_supply_routes(self) -> None:
        if not DisplayOptions.lines:
            return

        seen = set()
        for cp in self.game.theater.controlpoints:
            seen.add(cp)
            for connected in cp.connected_points:
                if connected in seen:
                    continue
                self.draw_supply_route_between(cp, connected)
            for destination, shipping_lane in cp.shipping_lanes.items():
                if destination in seen:
                    continue
                if cp.is_friendly(destination.captured):
                    self.draw_shipping_lane_between(cp, destination)

    def draw_shipping_lane_between(self, a: ControlPoint, b: ControlPoint) -> None:
        scene = self.scene()
        for pa, pb in self.bezier_points(a.shipping_lanes[b]):
            scene.addItem(ShippingLaneSegment(pa[0], pa[1], pb[0], pb[1], a, b))

    def draw_supply_route_between(self, a: ControlPoint, b: ControlPoint) -> None:
        scene = self.scene()

        convoy_map = self.game.transfers.convoys
        convoys = []
        convoy = convoy_map.find_convoy(a, b)
        if convoy is not None:
            convoys.append(convoy)
        convoy = convoy_map.find_convoy(b, a)
        if convoy is not None:
            convoys.append(convoy)

        frontline = FrontLine(a, b, self.game.theater)
        if a.front_is_active(b):
            if DisplayOptions.actual_frontline_pos:
                self.draw_actual_frontline(scene, frontline, convoys)
            else:
                self.draw_frontline_approximation(scene, frontline, convoys)
        else:
            self.draw_bezier_frontline(scene, frontline, convoys)

    def draw_frontline_approximation(
        self,
        scene: QGraphicsScene,
        frontline: FrontLine,
        convoys: List[Convoy],
    ) -> None:
        posx = frontline.position
        h = frontline.attack_heading
        pos2 = self._transform_point(posx)
        self.draw_bezier_frontline(scene, frontline, convoys)
        p1 = point_from_heading(pos2[0], pos2[1], h + 180, 25)
        p2 = point_from_heading(pos2[0], pos2[1], h, 25)
        scene.addItem(
            QFrontLine(p1[0], p1[1], p2[0], p2[1], frontline, self.game_model)
        )

    def draw_actual_frontline(
        self,
        scene: QGraphicsScene,
        frontline: FrontLine,
        convoys: List[Convoy],
    ) -> None:
        self.draw_bezier_frontline(scene, frontline, convoys)
        vector = Conflict.frontline_vector(
            frontline.control_point_a, frontline.control_point_b, self.game.theater
        )
        left_pos = self._transform_point(vector[0])
        right_pos = self._transform_point(
            vector[0].point_from_heading(vector[1], vector[2])
        )
        scene.addItem(
            QFrontLine(
                left_pos[0],
                left_pos[1],
                right_pos[0],
                right_pos[1],
                frontline,
                self.game_model,
            )
        )

    def draw_scale(self, scale_distance_nm=20, number_of_points=4):

        PADDING = 14
        POS_X = 0
        POS_Y = 10
        BIG_LINE = 5
        SMALL_LINE = 2

        dist = self.distance_to_pixels(nautical_miles(scale_distance_nm))
        l = self.scene().addLine(
            POS_X + PADDING,
            POS_Y + BIG_LINE * 2,
            POS_X + PADDING + dist,
            POS_Y + BIG_LINE * 2,
        )
        l.setPen(CONST.COLORS["black"])

        lw = self.scene().addLine(
            POS_X + PADDING + 1,
            POS_Y + BIG_LINE * 2 + 1,
            POS_X + PADDING + dist + 1,
            POS_Y + BIG_LINE * 2 + 1,
        )
        lw.setPen(CONST.COLORS["white"])

        text = self.scene().addText(
            "0nm", font=QFont("Trebuchet MS", 6, weight=5, italic=False)
        )
        text.setPos(POS_X, POS_Y + BIG_LINE * 2)
        text.setDefaultTextColor(Qt.black)

        text_white = self.scene().addText(
            "0nm", font=QFont("Trebuchet MS", 6, weight=5, italic=False)
        )
        text_white.setPos(POS_X + 1, POS_Y + BIG_LINE * 2)
        text_white.setDefaultTextColor(Qt.white)

        text2 = self.scene().addText(
            str(scale_distance_nm) + "nm",
            font=QFont("Trebuchet MS", 6, weight=5, italic=False),
        )
        text2.setPos(POS_X + dist, POS_Y + BIG_LINE * 2)
        text2.setDefaultTextColor(Qt.black)

        text2_white = self.scene().addText(
            str(scale_distance_nm) + "nm",
            font=QFont("Trebuchet MS", 6, weight=5, italic=False),
        )
        text2_white.setPos(POS_X + dist + 1, POS_Y + BIG_LINE * 2)
        text2_white.setDefaultTextColor(Qt.white)

        for i in range(number_of_points + 1):
            d = float(i) / float(number_of_points)
            if i == 0 or i == number_of_points:
                h = BIG_LINE
            else:
                h = SMALL_LINE

            l = self.scene().addLine(
                POS_X + PADDING + d * dist,
                POS_Y + BIG_LINE * 2,
                POS_X + PADDING + d * dist,
                POS_Y + BIG_LINE - h,
            )
            l.setPen(CONST.COLORS["black"])

            lw = self.scene().addLine(
                POS_X + PADDING + d * dist + 1,
                POS_Y + BIG_LINE * 2,
                POS_X + PADDING + d * dist + 1,
                POS_Y + BIG_LINE - h,
            )
            lw.setPen(CONST.COLORS["white"])

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
            if self._zoom < 10:
                self.scale(factor, factor)
                self.factorized *= factor
            else:
                self._zoom = 9
        else:
            factor = 0.8
            self._zoom -= 1
            if self._zoom > -5:
                self.scale(factor, factor)
                self.factorized *= factor
            else:
                self._zoom = -4

    @staticmethod
    def _transpose_point(p: Point) -> Point:
        return Point(p.y, p.x)

    def _scaling_factor(self) -> Point:
        point_a = self.game.theater.reference_points[0]
        point_b = self.game.theater.reference_points[1]

        world_distance = self._transpose_point(
            point_b.world_coordinates - point_a.world_coordinates
        )
        image_distance = point_b.image_coordinates - point_a.image_coordinates

        x_scale = image_distance.x / world_distance.x
        y_scale = image_distance.y / world_distance.y
        return Point(x_scale, y_scale)

    # TODO: Move this and its inverse into ConflictTheater.
    def _transform_point(self, world_point: Point) -> Tuple[float, float]:
        """Transforms world coordinates to image coordinates.

        World coordinates are transposed. X increases toward the North, Y
        increases toward the East. The origin point depends on the map.

        Image coordinates originate from the top left. X increases to the right,
        Y increases toward the bottom.

        The two points should be as distant as possible in both latitude and
        logitude, and tuning the reference points will be simpler if they are in
        geographically recognizable locations. For example, the Caucasus map is
        aligned using the first point on Gelendzhik and the second on Batumi.

        The distances between each point are computed and a scaling factor is
        determined from that. The given point is then offset from the first
        point using the scaling factor.

        X is latitude, increasing northward.
        Y is longitude, increasing eastward.
        """
        point_a = self.game.theater.reference_points[0]
        scale = self._scaling_factor()

        offset = self._transpose_point(point_a.world_coordinates - world_point)
        scaled = Point(offset.x * scale.x, offset.y * scale.y)
        transformed = point_a.image_coordinates - scaled
        return transformed.x, transformed.y

    def _scene_to_dcs_coords(self, scene_point: Point) -> Point:
        point_a = self.game.theater.reference_points[0]
        scale = self._scaling_factor()

        offset = point_a.image_coordinates - scene_point
        scaled = self._transpose_point(Point(offset.x / scale.x, offset.y / scale.y))
        return point_a.world_coordinates - scaled

    def distance_to_pixels(self, distance: Distance) -> int:
        p1 = Point(0, 0)
        p2 = Point(0, distance.meters)
        p1a = Point(*self._transform_point(p1))
        p2a = Point(*self._transform_point(p2))
        return int(p1a.distance_to_point(p2a))

    def highlight_color(self, transparent: Optional[bool] = False) -> QColor:
        return QColor(255, 255, 0, 20 if transparent else 255)

    def base_faction_color_name(self, player: bool) -> str:
        if player:
            return self.game.get_player_color()
        else:
            return self.game.get_enemy_color()

    def waypoint_pen(self, player: bool, selected: bool) -> QColor:
        if selected and DisplayOptions.flight_paths.all:
            return self.highlight_color()
        name = self.base_faction_color_name(player)
        return CONST.COLORS[name]

    def waypoint_brush(self, player: bool, selected: bool) -> QColor:
        if selected and DisplayOptions.flight_paths.all:
            return self.highlight_color(transparent=True)
        name = self.base_faction_color_name(player)
        return CONST.COLORS[f"{name}_transparent"]

    def threat_pen(self, player: bool) -> QPen:
        color = "blue" if player else "red"
        return QPen(CONST.COLORS[color])

    def detection_pen(self, player: bool) -> QPen:
        color = "purple" if player else "yellow"
        qpen = QPen(CONST.COLORS[color])
        qpen.setStyle(Qt.DotLine)
        return qpen

    def flight_path_pen(self, player: bool, selected: bool) -> QPen:
        if selected and DisplayOptions.flight_paths.all:
            return self.highlight_color()

        name = self.base_faction_color_name(player)
        color = CONST.COLORS[name]
        pen = QPen(brush=color)
        pen.setColor(color)
        pen.setWidth(1)
        pen.setStyle(Qt.DashDotLine)
        return pen

    def addBackground(self):
        scene = self.scene()

        if not DisplayOptions.map_poly:
            bg = QPixmap("./resources/" + self.game.theater.overview_image)
            scene.addPixmap(bg)

            # Apply graphical effects to simulate current daytime
            if self.game.current_turn_time_of_day == TimeOfDay.Day:
                pass
            elif self.game.current_turn_time_of_day == TimeOfDay.Night:
                ov = QPixmap(bg.width(), bg.height())
                ov.fill(CONST.COLORS["night_overlay"])
                overlay = scene.addPixmap(ov)
                effect = QGraphicsOpacityEffect()
                effect.setOpacity(0.7)
                overlay.setGraphicsEffect(effect)
            else:
                ov = QPixmap(bg.width(), bg.height())
                ov.fill(CONST.COLORS["dawn_dust_overlay"])
                overlay = scene.addPixmap(ov)
                effect = QGraphicsOpacityEffect()
                effect.setOpacity(0.3)
                overlay.setGraphicsEffect(effect)

        if DisplayOptions.map_poly or self.reference_point_setup_mode:
            # Polygon display mode
            if self.game.theater.landmap is not None:

                for sea_zone in self.game.theater.landmap.sea_zones:
                    print(sea_zone)
                    poly = QPolygonF(
                        [
                            QPointF(*self._transform_point(Point(point[0], point[1])))
                            for point in sea_zone.exterior.coords
                        ]
                    )
                    if self.reference_point_setup_mode:
                        color = "sea_blue_transparent"
                    else:
                        color = "sea_blue"
                    scene.addPolygon(poly, CONST.COLORS[color], CONST.COLORS[color])

                for inclusion_zone in self.game.theater.landmap.inclusion_zones:
                    poly = QPolygonF(
                        [
                            QPointF(*self._transform_point(Point(point[0], point[1])))
                            for point in inclusion_zone.exterior.coords
                        ]
                    )
                    if self.reference_point_setup_mode:
                        scene.addPolygon(
                            poly,
                            CONST.COLORS["grey_transparent"],
                            CONST.COLORS["dark_grey_transparent"],
                        )
                    else:
                        scene.addPolygon(
                            poly, CONST.COLORS["grey"], CONST.COLORS["dark_grey"]
                        )

                for exclusion_zone in self.game.theater.landmap.exclusion_zones:
                    poly = QPolygonF(
                        [
                            QPointF(*self._transform_point(Point(point[0], point[1])))
                            for point in exclusion_zone.exterior.coords
                        ]
                    )
                    if self.reference_point_setup_mode:
                        scene.addPolygon(
                            poly,
                            CONST.COLORS["grey_transparent"],
                            CONST.COLORS["dark_dark_grey_transparent"],
                        )
                    else:
                        scene.addPolygon(
                            poly, CONST.COLORS["grey"], CONST.COLORS["dark_dark_grey"]
                        )

        # Uncomment to display plan projection test
        # self.projection_test()
        self.draw_scale()

        if self.reference_point_setup_mode:
            for i, point in enumerate(self.game.theater.reference_points):
                self.scene().addRect(
                    QRectF(
                        point.image_coordinates.x, point.image_coordinates.y, 25, 25
                    ),
                    pen=CONST.COLORS["red"],
                    brush=CONST.COLORS["red"],
                )
                text = self.scene().addText(
                    f"P{i} = {point.image_coordinates}",
                    font=QFont("Trebuchet MS", 14, weight=8, italic=False),
                )
                text.setDefaultTextColor(CONST.COLORS["red"])
                text.setPos(point.image_coordinates.x + 26, point.image_coordinates.y)

                # Set to True to visually debug _transform_point.
                draw_transformed = False
                if draw_transformed:
                    x, y = self._transform_point(point.world_coordinates)
                    self.scene().addRect(
                        QRectF(x, y, 25, 25),
                        pen=CONST.COLORS["red"],
                        brush=CONST.COLORS["red"],
                    )
                    text = self.scene().addText(
                        f"P{i}' = {x}, {y}",
                        font=QFont("Trebuchet MS", 14, weight=8, italic=False),
                    )
                    text.setDefaultTextColor(CONST.COLORS["red"])
                    text.setPos(x + 26, y)

    def projection_test(self):
        for i in range(100):
            for j in range(100):
                x = i * 100.0
                y = j * 100.0
                original = Point(x, y)
                proj = self._scene_to_dcs_coords(original)
                unproj = self._transform_point(proj)
                converted = Point(*unproj)
                assert math.isclose(original.x, converted.x, abs_tol=0.00000001)
                assert math.isclose(original.y, converted.y, abs_tol=0.00000001)

    def setSelectedUnit(self, selected_cp: QMapControlPoint):
        self.state = QLiberationMapState.MOVING_UNIT
        self.selected_cp = selected_cp
        position = self._transform_point(selected_cp.control_point.position)
        self.movement_line = QtWidgets.QGraphicsLineItem(
            QLineF(QPointF(*position), QPointF(*position))
        )
        self.scene().addItem(self.movement_line)

    def is_valid_ship_pos(self, scene_position: Point) -> bool:
        world_destination = self._scene_to_dcs_coords(scene_position)
        distance = self.selected_cp.control_point.position.distance_to_point(
            world_destination
        )
        if meters(distance) > MAX_SHIP_DISTANCE:
            return False
        return self.game.theater.is_in_sea(world_destination)

    def sceneMouseMovedEvent(self, event: QGraphicsSceneMouseEvent):
        if self.game is None:
            return

        mouse_position = Point(event.scenePos().x(), event.scenePos().y())
        if self.state == QLiberationMapState.MOVING_UNIT:
            self.setCursor(Qt.PointingHandCursor)
            self.movement_line.setLine(
                QLineF(self.movement_line.line().p1(), event.scenePos())
            )

            if self.is_valid_ship_pos(mouse_position):
                self.movement_line.setPen(CONST.COLORS["green"])
            else:
                self.movement_line.setPen(CONST.COLORS["red"])

        mouse_world_pos = self._scene_to_dcs_coords(mouse_position)
        if DisplayOptions.navmeshes.blue_navmesh:
            self.highlight_mouse_navmesh(
                self.scene(),
                self.game.blue_navmesh,
                self._scene_to_dcs_coords(mouse_position),
            )
            if DisplayOptions.path_debug.shortest_path:
                self.draw_shortest_path(
                    self.scene(), self.game.blue_navmesh, mouse_world_pos, player=True
                )

        if DisplayOptions.navmeshes.red_navmesh:
            self.highlight_mouse_navmesh(
                self.scene(), self.game.red_navmesh, mouse_world_pos
            )

        debug_blue = DisplayOptions.path_debug_faction.blue
        if DisplayOptions.path_debug.shortest_path:
            self.draw_shortest_path(
                self.scene(),
                self.game.navmesh_for(player=debug_blue),
                mouse_world_pos,
                player=False,
            )
        elif not DisplayOptions.path_debug.hide:
            if DisplayOptions.path_debug.barcap:
                task = FlightType.BARCAP
            elif DisplayOptions.path_debug.cas:
                task = FlightType.CAS
            elif DisplayOptions.path_debug.sweep:
                task = FlightType.SWEEP
            elif DisplayOptions.path_debug.strike:
                task = FlightType.STRIKE
            elif DisplayOptions.path_debug.tarcap:
                task = FlightType.TARCAP
            else:
                raise ValueError("Unexpected value for DisplayOptions.path_debug")
            self.draw_test_flight_plan(
                self.scene(), task, mouse_world_pos, player=debug_blue
            )

    def sceneMousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.state == QLiberationMapState.MOVING_UNIT:
            if event.buttons() == Qt.RightButton:
                pass
            elif event.buttons() == Qt.LeftButton:
                if self.selected_cp is not None:
                    # Set movement position for the cp
                    pos = event.scenePos()
                    point = Point(int(pos.x()), int(pos.y()))
                    proj = self._scene_to_dcs_coords(point)

                    if self.is_valid_ship_pos(point):
                        self.selected_cp.control_point.target_position = proj
                    else:
                        self.selected_cp.control_point.target_position = None

                    GameUpdateSignal.get_instance().updateGame(self.game_model.game)
            else:
                return
            self.state = QLiberationMapState.NORMAL
            try:
                self.scene().removeItem(self.movement_line)
            except:
                pass
            self.selected_cp = None
