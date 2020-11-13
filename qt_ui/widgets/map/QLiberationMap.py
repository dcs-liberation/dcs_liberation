from __future__ import annotations

import datetime
import logging
from typing import List, Optional, Tuple

from PySide2.QtCore import QPointF, Qt
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
    QGraphicsView,
)
from dcs import Point
from dcs.mapping import point_from_heading

import qt_ui.uiconstants as CONST
from game import Game, db
from game.utils import meter_to_feet
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
from theater import ControlPoint
from theater.frontline import FrontLine
from theater.theatergroundobject import (
    EwrGroundObject,
    MissileSiteGroundObject,
    TheaterGroundObject,
)


class QLiberationMap(QGraphicsView):
    WAYPOINT_SIZE = 4

    instance: Optional[QLiberationMap] = None

    def __init__(self, game_model: GameModel):
        super(QLiberationMap, self).__init__()
        QLiberationMap.instance = self
        self.game_model = game_model
        self.game: Optional[Game] = game_model.game

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
            self.reload_scene()

    """
    
    Uncomment to set up theather reference points
    def keyPressEvent(self, event):
        #super(QLiberationMap, self).keyPressEvent(event)

        numpad_mod = int(event.modifiers()) & QtCore.Qt.KeypadModifier
        i = 0
        for k,v in self.game.theater.reference_points.items():
            if i == 0:
                point_0 = k
            else:
                point_1 = k
            i = i + 1

        if event.key() == QtCore.Qt.Key_Down:
            self.game.theater.reference_points[point_0] = self.game.theater.reference_points[point_0][0] + 10, self.game.theater.reference_points[point_0][1]
        if event.key() == QtCore.Qt.Key_Up:
            self.game.theater.reference_points[point_0] = self.game.theater.reference_points[point_0][0] - 10, self.game.theater.reference_points[point_0][1]
        if event.key() == QtCore.Qt.Key_Left:
            self.game.theater.reference_points[point_0] = self.game.theater.reference_points[point_0][0], self.game.theater.reference_points[point_0][1] + 10
        if event.key() == QtCore.Qt.Key_Right:
            self.game.theater.reference_points[point_0] = self.game.theater.reference_points[point_0][0], self.game.theater.reference_points[point_0][1] - 10


        if event.key() == QtCore.Qt.Key_2 and numpad_mod:
            self.game.theater.reference_points[point_1] = self.game.theater.reference_points[point_1][0] + 10, self.game.theater.reference_points[point_1][1]
        if event.key() == QtCore.Qt.Key_8 and numpad_mod:
            self.game.theater.reference_points[point_1] = self.game.theater.reference_points[point_1][0] - 10, self.game.theater.reference_points[point_1][1]
        if event.key() == QtCore.Qt.Key_4 and numpad_mod:
            self.game.theater.reference_points[point_1] = self.game.theater.reference_points[point_1][0], self.game.theater.reference_points[point_1][1] + 10
        if event.key() == QtCore.Qt.Key_6 and numpad_mod:
            self.game.theater.reference_points[point_1] = self.game.theater.reference_points[point_1][0], self.game.theater.reference_points[point_1][1] - 10

        print(self.game.theater.reference_points)
        self.reload_scene()
    """

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

    def reload_scene(self):
        scene = self.scene()
        scene.clear()

        playerColor = self.game.get_player_color()
        enemyColor = self.game.get_enemy_color()

        self.addBackground()

        # Uncomment below to help set up theater reference points
        #for i, r in enumerate(self.game.theater.reference_points.items()):
        #    text = scene.addText(str(r), font=QFont("Trebuchet MS", 10, weight=5, italic=False))
        #    text.setPos(0, i * 24)

        # Display Culling
        if DisplayOptions.culling and self.game.settings.perf_culling:
            culling_points = self.game_model.game.get_culling_points()
            culling_distance = self.game_model.game.settings.perf_culling_distance
            for point in culling_points:
                culling_distance_point = Point(point.x + culling_distance*1000, point.y + culling_distance*1000)
                distance_point = self._transform_point(culling_distance_point)
                transformed = self._transform_point(point)
                diameter = distance_point[0] - transformed[0]
                scene.addEllipse(transformed[0]-diameter/2, transformed[1]-diameter/2, diameter, diameter, CONST.COLORS["transparent"], CONST.COLORS["light_green_transparent"])

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

            added_objects = []
            for ground_object in cp.ground_objects:
                if ground_object.obj_name in added_objects:
                    continue

                go_pos = self._transform_point(ground_object.position)
                if not ground_object.airbase_group:
                    buildings = self.game.theater.find_ground_objects_by_obj_name(ground_object.obj_name)
                    scene.addItem(QMapGroundObject(self, go_pos[0], go_pos[1], 14, 12, cp, ground_object, self.game, buildings))

                is_missile = isinstance(ground_object, MissileSiteGroundObject)
                is_aa = ground_object.category == "aa" and not is_missile
                is_ewr = isinstance(ground_object, EwrGroundObject)
                is_display_type = is_aa or is_ewr
                should_display = ((DisplayOptions.sam_ranges and cp.captured)
                                  or
                                  (DisplayOptions.enemy_sam_ranges and not cp.captured))

                if is_display_type and should_display:
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
                    if detection_range:
                        # Add detection range circle
                        detection_pos = self._transform_point(Point(ground_object.position.x+detection_range,
                                                                    ground_object.position.y+detection_range))
                        detection_radius = Point(*go_pos).distance_to_point(Point(*detection_pos))
                        if DisplayOptions.detection_range:
                            scene.addEllipse(go_pos[0] - detection_radius/2 + 7, go_pos[1] - detection_radius/2 + 6,
                                             detection_radius, detection_radius, self.detection_pen(cp.captured))
                added_objects.append(ground_object.obj_name)

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
        self.draw_flight_path(scene, prev_pos, pos, is_player, selected)

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

        altitude = meter_to_feet(waypoint.alt)
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

    def scene_create_lines_for_cp(self, cp: ControlPoint, playerColor, enemyColor):
        scene = self.scene()
        pos = self._transform_point(cp.position)
        for connected_cp in cp.connected_points:
            pos2 = self._transform_point(connected_cp.position)
            if not cp.captured:
                color = CONST.COLORS["dark_"+enemyColor]
            elif cp.captured:
                color = CONST.COLORS["dark_"+playerColor]
            else:
                color = CONST.COLORS["dark_"+enemyColor]

            pen = QPen(brush=color)
            pen.setColor(color)
            pen.setWidth(6)
            frontline = FrontLine(cp, connected_cp)
            if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):
                if not cp.captured:
                    scene.addLine(pos[0], pos[1], pos2[0], pos2[1], pen=pen)
                else:
                    posx = frontline.position
                    h = frontline.attack_heading
                    pos2 = self._transform_point(posx)
                    for segment in frontline.segments:
                        seg_a = self._transform_point(segment.point_a)
                        seg_b = self._transform_point(segment.point_b)
                        scene.addLine(seg_a[0], seg_a[1], seg_b[0], seg_b[1], pen=pen)

                    p1 = point_from_heading(pos2[0], pos2[1], h+180, 25)
                    p2 = point_from_heading(pos2[0], pos2[1], h, 25)
                    scene.addItem(QFrontLine(p1[0], p1[1], p2[0], p2[1],
                                             FrontLine(cp, connected_cp)))

            else:
                for segment in frontline.segments:
                        seg_a = self._transform_point(segment.point_a)
                        seg_b = self._transform_point(segment.point_b)
                        scene.addLine(seg_a[0], seg_a[1], seg_b[0], seg_b[1], pen=pen)

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

        #print(self.factorized, factor, self._zoom)

    def _transform_point(self, p: Point, treshold=30) -> (int, int):
        point_a = list(self.game.theater.reference_points.keys())[0]
        point_a_img = self.game.theater.reference_points[point_a]

        point_b = list(self.game.theater.reference_points.keys())[1]
        point_b_img = self.game.theater.reference_points[point_b]

        Y_dist = point_a_img[0] - point_b_img[0]
        lon_dist = point_a[1] - point_b[1]

        X_dist = point_a_img[1] - point_b_img[1]
        lat_dist = point_b[0] - point_a[0]

        Y_scale = float(Y_dist) / float(lon_dist)
        X_scale = float(X_dist) / float(lat_dist)

        # ---
        Y_offset = p.x - point_a[0]
        X_offset = p.y - point_a[1]

        X = point_b_img[1] + X_offset * X_scale
        Y = point_a_img[0] - Y_offset * Y_scale

        #X += 5
        #Y += 5

        return X > treshold and X or treshold, Y > treshold and Y or treshold

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
        if player:
            color = "blue"
        else:
            color = "red"
        qpen = QPen(CONST.COLORS[color])
        return qpen

    def detection_pen(self, player: bool) -> QPen:
        if player:
            color = "purple"
        else:
            color = "yellow"
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

        else:
            # Polygon display mode
            if self.game.theater.landmap is not None:

                for sea_zone in self.game.theater.landmap[2]:
                    print(sea_zone)
                    poly = QPolygonF([QPointF(*self._transform_point(Point(point[0], point[1]))) for point in sea_zone])
                    scene.addPolygon(poly, CONST.COLORS["sea_blue"], CONST.COLORS["sea_blue"])

                for inclusion_zone in self.game.theater.landmap[0]:
                    poly = QPolygonF([QPointF(*self._transform_point(Point(point[0], point[1]))) for point in inclusion_zone])
                    scene.addPolygon(poly, CONST.COLORS["grey"], CONST.COLORS["dark_grey"])

                for exclusion_zone in self.game.theater.landmap[1]:
                    poly = QPolygonF([QPointF(*self._transform_point(Point(point[0], point[1]))) for point in exclusion_zone])
                    scene.addPolygon(poly, CONST.COLORS["grey"], CONST.COLORS["dark_dark_grey"])




