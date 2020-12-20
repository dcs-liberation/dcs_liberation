from __future__ import annotations

import datetime
import logging
import math
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

import qt_ui.uiconstants as CONST
from game import Game, db
from game.theater import ControlPoint, Enum
from game.theater.conflicttheater import FrontLine, ReferencePoint
from game.theater.theatergroundobject import (
    TheaterGroundObject,
)
from game.utils import Distance, meters, nautical_miles
from game.weather import TimeOfDay
from gen import Conflict
from gen.flights.flight import Flight, FlightWaypoint, FlightWaypointType
from gen.flights.flightplan import FlightPlan
from qt_ui.displayoptions import DisplayOptions
from qt_ui.models import GameModel
from qt_ui.widgets.map.QFrontLine import QFrontLine
from qt_ui.widgets.map.QLiberationScene import QLiberationScene
from qt_ui.widgets.map.QMapControlPoint import QMapControlPoint
from qt_ui.widgets.map.QMapGroundObject import QMapGroundObject
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

MAX_SHIP_DISTANCE = nautical_miles(80)

def binomial(i: int, n: int) -> float:
    """Binomial coefficient"""
    return math.factorial(n) / float(
        math.factorial(i) * math.factorial(n - i))


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


def bezier_curve_range(n: int, points: Iterable[Tuple[float, float]]) -> Iterator[Tuple[float, float]]:
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
        self.movement_line = QtWidgets.QGraphicsLineItem(QtCore.QLineF(QPointF(0,0),QPointF(0,0)))
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
                    logging.error(
                        "Flight was selected with no package selected")
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
                        self.game.theater.reference_points[0],
                        Point(0, distance))
                if event.key() == QtCore.Qt.Key_Up:
                    self.update_reference_point(
                        self.game.theater.reference_points[0],
                        Point(0, -distance))
                if event.key() == QtCore.Qt.Key_Left:
                    self.update_reference_point(
                        self.game.theater.reference_points[0],
                        Point(-distance, 0))
                if event.key() == QtCore.Qt.Key_Right:
                    self.update_reference_point(
                        self.game.theater.reference_points[0],
                        Point(distance, 0))

                if event.key() == QtCore.Qt.Key_S:
                    self.update_reference_point(
                        self.game.theater.reference_points[1],
                        Point(0, distance))
                if event.key() == QtCore.Qt.Key_W:
                    self.update_reference_point(
                        self.game.theater.reference_points[1],
                        Point(0, -distance))
                if event.key() == QtCore.Qt.Key_A:
                    self.update_reference_point(
                        self.game.theater.reference_points[1],
                        Point(-distance, 0))
                if event.key() == QtCore.Qt.Key_D:
                    self.update_reference_point(
                        self.game.theater.reference_points[1],
                        Point(distance, 0))

                logging.debug(
                    f"Reference points: {self.game.theater.reference_points}")
                self.reload_scene()

    @staticmethod
    def update_reference_point(point: ReferencePoint, change: Point) -> None:
        point.image_coordinates += change

    @staticmethod
    def aa_ranges(ground_object: TheaterGroundObject) -> Tuple[int, int]:
        detection_range = 0
        threat_range = 0
        for g in ground_object.groups:
            for u in g.units:
                unit = db.unit_type_from_name(u.type)
                if unit is None:
                    logging.error(f"Unknown unit type {u.type}")
                    continue

                # Some units in pydcs have detection_range and threat_range
                # defined, but explicitly set to None.
                unit_detection_range = getattr(unit, "detection_range", None)
                if unit_detection_range is not None:
                    detection_range = max(detection_range, unit_detection_range)

                unit_threat_range = getattr(unit, "threat_range", None)
                if unit_threat_range is not None:
                    threat_range = max(threat_range, unit_threat_range)

        return detection_range, threat_range

    def display_culling(self, scene: QGraphicsScene) -> None:
        """Draws the culling distance rings on the map"""
        culling_points = self.game_model.game.get_culling_points()
        culling_distance = self.game_model.game.settings.perf_culling_distance
        for point in culling_points:
            culling_distance_point = Point(point.x + culling_distance*1000, point.y + culling_distance*1000)
            distance_point = self._transform_point(culling_distance_point)
            transformed = self._transform_point(point)
            radius = distance_point[0] - transformed[0]
            scene.addEllipse(transformed[0]-radius, transformed[1]-radius, 2*radius, 2*radius, CONST.COLORS["transparent"], CONST.COLORS["light_green_transparent"])

    @staticmethod
    def should_display_ground_objects_at(cp: ControlPoint) -> bool:
        return ((DisplayOptions.sam_ranges and cp.captured) or
                (DisplayOptions.enemy_sam_ranges and not cp.captured))

    def draw_threat_range(self, scene: QGraphicsScene, ground_object: TheaterGroundObject, cp: ControlPoint) -> None:
        go_pos = self._transform_point(ground_object.position)
        detection_range, threat_range = self.aa_ranges(
            ground_object
        )
        if threat_range:
            threat_pos = self._transform_point(Point(ground_object.position.x+threat_range,
                                                        ground_object.position.y+threat_range))
            threat_radius = Point(*go_pos).distance_to_point(Point(*threat_pos))

            # Add threat range circle
            scene.addEllipse(go_pos[0] - threat_radius / 2 + 7, go_pos[1] - threat_radius / 2 + 6,
                                threat_radius, threat_radius, self.threat_pen(cp.captured))

        if detection_range and DisplayOptions.detection_range:
            # Add detection range circle
            detection_pos = self._transform_point(Point(ground_object.position.x+detection_range,
                                                        ground_object.position.y+detection_range))
            detection_radius = Point(*go_pos).distance_to_point(Point(*detection_pos))
            scene.addEllipse(go_pos[0] - detection_radius/2 + 7, go_pos[1] - detection_radius/2 + 6,
                                detection_radius, detection_radius, self.detection_pen(cp.captured))

    def draw_ground_objects(self, scene: QGraphicsScene, cp: ControlPoint) -> None:
        added_objects = []
        for ground_object in cp.ground_objects:
            if ground_object.obj_name in added_objects:
                continue

            go_pos = self._transform_point(ground_object.position)
            if not ground_object.airbase_group:
                buildings = self.game.theater.find_ground_objects_by_obj_name(ground_object.obj_name)
                scene.addItem(QMapGroundObject(self, go_pos[0], go_pos[1], 14, 12, cp, ground_object, self.game, buildings))

            should_display = self.should_display_ground_objects_at(cp)
            if ground_object.might_have_aa and should_display:
               self.draw_threat_range(scene, ground_object, cp)
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

        for cp in self.game.theater.controlpoints:

            pos = self._transform_point(cp.position)

            scene.addItem(QMapControlPoint(self, pos[0] - CONST.CP_SIZE / 2,
                                           pos[1] - CONST.CP_SIZE / 2,
                                           CONST.CP_SIZE,
                                           CONST.CP_SIZE, cp, self.game_model))

            if cp.captured:
                pen = QPen(brush=CONST.COLORS[playerColor])
                brush = CONST.COLORS[playerColor+"_transparent"]
            else:
                pen = QPen(brush=CONST.COLORS[enemyColor])
                brush = CONST.COLORS[enemyColor+"_transparent"]

            self.draw_ground_objects(scene, cp)

            if cp.target_position is not None:
                proj = self._transform_point(cp.target_position)
                scene.addLine(QLineF(QPointF(pos[0], pos[1]), QPointF(proj[0], proj[1])),
                              QPen(CONST.COLORS["green"], width=10, s=Qt.DashDotLine))

        for cp in self.game.theater.enemy_points():
            if DisplayOptions.lines:
                self.scene_create_lines_for_cp(cp, playerColor, enemyColor)

        for cp in self.game.theater.player_points():
            if DisplayOptions.lines:
                self.scene_create_lines_for_cp(cp, playerColor, enemyColor)

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

    def draw_flight_plan(self, scene: QGraphicsScene, flight: Flight,
                         selected: bool) -> None:
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
            self.draw_flight_path(scene, prev_pos, new_pos, is_player,
                                  selected)
            self.draw_waypoint(scene, new_pos, is_player, selected)
            if selected and DisplayOptions.waypoint_info:
                if point.waypoint_type in target_types:
                    if drew_target:
                        # Don't draw dozens of targets over each other.
                        continue
                    drew_target = True
                self.draw_waypoint_info(scene, idx + 1, point, new_pos,
                                        flight.flight_plan)
            prev_pos = tuple(new_pos)

    def draw_waypoint(self, scene: QGraphicsScene, position: Tuple[int, int],
                      player: bool, selected: bool) -> None:
        waypoint_pen = self.waypoint_pen(player, selected)
        waypoint_brush = self.waypoint_brush(player, selected)
        self.flight_path_items.append(scene.addEllipse(
            position[0], position[1], self.WAYPOINT_SIZE,
            self.WAYPOINT_SIZE, waypoint_pen, waypoint_brush
        ))

    def draw_waypoint_info(self, scene: QGraphicsScene, number: int,
                           waypoint: FlightWaypoint, position: Tuple[int, int],
                           flight_plan: FlightPlan) -> None:

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

        text = "\n".join([
            f"{number} {waypoint.name}",
            f"{altitude} ft {altitude_type}",
            tot,
        ])

        item = scene.addSimpleText(text, self.waypoint_info_font)
        item.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        item.setBrush(brush)
        item.setPen(pen)
        item.moveBy(position[0] + 8, position[1])
        item.setZValue(2)
        self.flight_path_items.append(item)

    def draw_flight_path(self, scene: QGraphicsScene, pos0: Tuple[int, int],
                         pos1: Tuple[int, int], player: bool,
                         selected: bool) -> None:
        flight_path_pen = self.flight_path_pen(player, selected)
        # Draw the line to the *middle* of the waypoint.
        offset = self.WAYPOINT_SIZE // 2
        self.flight_path_items.append(scene.addLine(
            pos0[0] + offset, pos0[1] + offset,
            pos1[0] + offset, pos1[1] + offset,
            flight_path_pen
        ))

    def draw_bezier_frontline(self, scene: QGraphicsScene, pen:QPen, frontline: FrontLine) -> None:
        """
        Thanks to Alquimista for sharing a python implementation of the bezier algorithm this is adapted from.
        https://gist.github.com/Alquimista/1274149#file-bezdraw-py
        """
        bezier_fixed_points = []
        for segment in frontline.segments:
            bezier_fixed_points.append(self._transform_point(segment.point_a))
            bezier_fixed_points.append(self._transform_point(segment.point_b))

        old_point = bezier_fixed_points[0]
        for point in bezier_curve_range(int(len(bezier_fixed_points) * 2), bezier_fixed_points):
            scene.addLine(old_point[0], old_point[1], point[0], point[1], pen=pen)
            old_point = point

    def scene_create_lines_for_cp(self, cp: ControlPoint, playerColor, enemyColor):
        scene = self.scene()
        for connected_cp in cp.connected_points:
            pos2 = self._transform_point(connected_cp.position)
            if not cp.captured:
                color = CONST.COLORS["dark_"+enemyColor]
            else:
                color = CONST.COLORS["dark_"+playerColor]
            pen = QPen(brush=color)
            pen.setColor(color)
            pen.setWidth(6)
            frontline = FrontLine(cp, connected_cp, self.game.theater)
            if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):
                if DisplayOptions.actual_frontline_pos:
                    self.draw_actual_frontline(frontline, scene, pen)
                else:
                    self.draw_frontline_approximation(frontline, scene, pen)
            else:
                self.draw_bezier_frontline(scene, pen, frontline)

    def draw_frontline_approximation(self, frontline: FrontLine, scene: QGraphicsScene, pen: QPen) -> None:
        posx = frontline.position
        h = frontline.attack_heading
        pos2 = self._transform_point(posx)
        self.draw_bezier_frontline(scene, pen, frontline)
        p1 = point_from_heading(pos2[0], pos2[1], h+180, 25)
        p2 = point_from_heading(pos2[0], pos2[1], h, 25)
        scene.addItem(
            QFrontLine(
                p1[0],
                p1[1],
                p2[0],
                p2[1],
                frontline,
                self.game_model
            )
        )

    def draw_actual_frontline(self, frontline: FrontLine, scene: QGraphicsScene, pen: QPen) -> None:
        self.draw_bezier_frontline(scene, pen, frontline)
        vector = Conflict.frontline_vector(
            frontline.control_point_a,
            frontline.control_point_b,
            self.game.theater
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
                self.game_model
            )
        )

    def draw_scale(self, scale_distance_nm=20, number_of_points=4):

        PADDING = 14
        POS_X = 0
        POS_Y = 10
        BIG_LINE = 5
        SMALL_LINE = 2

        dist = self.distance_to_pixels(nautical_miles(scale_distance_nm))
        self.scene().addRect(POS_X, POS_Y-PADDING, PADDING*2 + dist, BIG_LINE*2+3*PADDING, pen=CONST.COLORS["black"], brush=CONST.COLORS["black"])
        l = self.scene().addLine(POS_X + PADDING, POS_Y + BIG_LINE*2, POS_X + PADDING + dist, POS_Y + BIG_LINE*2)

        text = self.scene().addText("0nm", font=QFont("Trebuchet MS", 6, weight=5, italic=False))
        text.setPos(POS_X, POS_Y + BIG_LINE*2)
        text.setDefaultTextColor(Qt.white)

        text2 = self.scene().addText(str(scale_distance_nm) + "nm", font=QFont("Trebuchet MS", 6, weight=5, italic=False))
        text2.setPos(POS_X + dist, POS_Y + BIG_LINE * 2)
        text2.setDefaultTextColor(Qt.white)

        l.setPen(CONST.COLORS["white"])
        for i in range(number_of_points+1):
            d = float(i)/float(number_of_points)
            if i == 0 or i == number_of_points:
                h = BIG_LINE
            else:
                h = SMALL_LINE

            l = self.scene().addLine(POS_X + PADDING + d * dist, POS_Y + BIG_LINE*2, POS_X + PADDING + d * dist, POS_Y + BIG_LINE - h)
            l.setPen(CONST.COLORS["white"])

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
            point_b.world_coordinates - point_a.world_coordinates)
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
        scaled = self._transpose_point(
            Point(offset.x / scale.x, offset.y / scale.y))
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

                for sea_zone in self.game.theater.landmap[2]:
                    print(sea_zone)
                    poly = QPolygonF([QPointF(*self._transform_point(Point(point[0], point[1]))) for point in sea_zone.exterior.coords])
                    if self.reference_point_setup_mode:
                        color = "sea_blue_transparent"
                    else:
                        color = "sea_blue"
                    scene.addPolygon(poly, CONST.COLORS[color], CONST.COLORS[color])

                for inclusion_zone in self.game.theater.landmap[0]:
                    poly = QPolygonF([QPointF(*self._transform_point(Point(point[0], point[1]))) for point in inclusion_zone.exterior.coords])
                    if self.reference_point_setup_mode:
                        scene.addPolygon(poly, CONST.COLORS["grey_transparent"], CONST.COLORS["dark_grey_transparent"])
                    else:
                        scene.addPolygon(poly, CONST.COLORS["grey"], CONST.COLORS["dark_grey"])

                for exclusion_zone in self.game.theater.landmap[1]:
                    poly = QPolygonF([QPointF(*self._transform_point(Point(point[0], point[1]))) for point in exclusion_zone.exterior.coords])
                    if self.reference_point_setup_mode:
                        scene.addPolygon(poly, CONST.COLORS["grey_transparent"], CONST.COLORS["dark_dark_grey_transparent"])
                    else:
                        scene.addPolygon(poly, CONST.COLORS["grey"], CONST.COLORS["dark_dark_grey"])

        # Uncomment to display plan projection test
        # self.projection_test()
        self.draw_scale()

        if self.reference_point_setup_mode:
            for i, point in enumerate(self.game.theater.reference_points):
                self.scene().addRect(
                    QRectF(point.image_coordinates.x, point.image_coordinates.y,
                           25, 25), pen=CONST.COLORS["red"],
                    brush=CONST.COLORS["red"])
                text = self.scene().addText(
                    f"P{i} = {point.image_coordinates}",
                    font=QFont("Trebuchet MS", 14, weight=8, italic=False))
                text.setDefaultTextColor(CONST.COLORS["red"])
                text.setPos(point.image_coordinates.x + 26,
                            point.image_coordinates.y)

                # Set to True to visually debug _transform_point.
                draw_transformed = False
                if draw_transformed:
                    x, y = self._transform_point(point.world_coordinates)
                    self.scene().addRect(
                        QRectF(x, y, 25, 25),
                        pen=CONST.COLORS["red"],
                        brush=CONST.COLORS["red"])
                    text = self.scene().addText(
                        f"P{i}' = {x}, {y}",
                        font=QFont("Trebuchet MS", 14, weight=8, italic=False))
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
        self.movement_line = QtWidgets.QGraphicsLineItem(QLineF(QPointF(*position), QPointF(*position)))
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
        if self.state == QLiberationMapState.MOVING_UNIT:
            self.setCursor(Qt.PointingHandCursor)
            self.movement_line.setLine(
                QLineF(self.movement_line.line().p1(), event.scenePos()))

            pos = Point(event.scenePos().x(), event.scenePos().y())
            if self.is_valid_ship_pos(pos):
                self.movement_line.setPen(CONST.COLORS["green"])
            else:
                self.movement_line.setPen(CONST.COLORS["red"])

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