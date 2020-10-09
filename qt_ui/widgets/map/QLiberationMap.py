from __future__ import annotations

import logging
from typing import List, Optional, Tuple

from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor, QPen, QPixmap, QWheelEvent
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
from game.data.radar_db import UNITS_WITH_RADAR
from gen import Conflict
from gen.flights.flight import Flight
from qt_ui.displayoptions import DisplayOptions
from qt_ui.models import GameModel
from qt_ui.widgets.map.QFrontLine import QFrontLine
from qt_ui.widgets.map.QLiberationScene import QLiberationScene
from qt_ui.widgets.map.QMapControlPoint import QMapControlPoint
from qt_ui.widgets.map.QMapGroundObject import QMapGroundObject
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from theater import ControlPoint, FrontLine


class QLiberationMap(QGraphicsView):
    WAYPOINT_SIZE = 4

    instance: Optional[QLiberationMap] = None

    def __init__(self, game_model: GameModel):
        super(QLiberationMap, self).__init__()
        QLiberationMap.instance = self
        self.game_model = game_model
        self.game: Optional[Game] = game_model.game

        self.flight_path_items: List[QGraphicsItem] = []

        self.setMinimumSize(800,600)
        self.setMaximumHeight(2160)
        self._zoom = 0
        self.factor = 1
        self.factorized = 1
        self.init_scene()
        self.connectSignals()
        self.setGame(game_model.game)

        GameUpdateSignal.get_instance().flight_paths_changed.connect(
            lambda: self.draw_flight_plans(self.scene())
        )

    def init_scene(self):
        scene = QLiberationScene(self)
        self.setScene(scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def connectSignals(self):
        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)

    def setGame(self, game: Optional[Game]):
        self.game = game
        logging.debug("Reloading Map Canvas")
        if self.game is not None:
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

                is_aa = ground_object.category == "aa"
                if is_aa and DisplayOptions.sam_ranges:
                    max_range = 0
                    has_radar = False
                    if ground_object.groups:
                        for g in ground_object.groups:
                            for u in g.units:
                                unit = db.unit_type_from_name(u.type)
                                if unit in UNITS_WITH_RADAR:
                                    has_radar = True
                                if unit.threat_range > max_range:
                                    max_range = unit.threat_range
                    if has_radar:
                        scene.addEllipse(go_pos[0] - max_range/300.0 + 8, go_pos[1] - max_range/300.0 + 8, max_range/150.0, max_range/150.0, CONST.COLORS["white_transparent"], CONST.COLORS["grey_transparent"])
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

    def draw_flight_plans(self, scene) -> None:
        for item in self.flight_path_items:
            try:
                scene.removeItem(item)
            except RuntimeError:
                # Something may have caused those items to already be removed.
                pass
        self.flight_path_items.clear()
        if not DisplayOptions.flight_paths:
            return
        for package in self.game_model.ato_model.packages:
            for flight in package.flights:
                self.draw_flight_plan(scene, flight)

    def draw_flight_plan(self, scene: QGraphicsScene, flight: Flight) -> None:
        is_player = flight.from_cp.captured
        pos = self._transform_point(flight.from_cp.position)

        self.draw_waypoint(scene, pos, is_player)
        prev_pos = tuple(pos)
        for point in flight.points:
            new_pos = self._transform_point(Point(point.x, point.y))
            self.draw_flight_path(scene, prev_pos, new_pos, is_player)
            self.draw_waypoint(scene, new_pos, is_player)
            prev_pos = tuple(new_pos)
        self.draw_flight_path(scene, prev_pos, pos, is_player)

    def draw_waypoint(self, scene: QGraphicsScene, position: Tuple[int, int],
                      player: bool) -> None:
        waypoint_pen = self.waypoint_pen(player)
        waypoint_brush = self.waypoint_brush(player)
        self.flight_path_items.append(scene.addEllipse(
            position[0], position[1], self.WAYPOINT_SIZE,
            self.WAYPOINT_SIZE, waypoint_pen, waypoint_brush
        ))

    def draw_flight_path(self, scene: QGraphicsScene, pos0: Tuple[int, int],
                         pos1: Tuple[int, int], player: bool):
        flight_path_pen = self.flight_path_pen(player)
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
            if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):
                if not cp.captured:
                    scene.addLine(pos[0], pos[1], pos2[0], pos2[1], pen=pen)
                else:
                    posx, h = Conflict.frontline_position(self.game.theater, cp, connected_cp)
                    pos2 = self._transform_point(posx)
                    scene.addLine(pos[0], pos[1], pos2[0], pos2[1], pen=pen)

                    p1 = point_from_heading(pos2[0], pos2[1], h+180, 25)
                    p2 = point_from_heading(pos2[0], pos2[1], h, 25)
                    scene.addItem(QFrontLine(p1[0], p1[1], p2[0], p2[1],
                                             FrontLine(cp, connected_cp)))

            else:
                scene.addLine(pos[0], pos[1], pos2[0], pos2[1], pen=pen)

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

    def base_faction_color_name(self, player: bool) -> str:
        if player:
            return self.game.get_player_color()
        else:
            return self.game.get_enemy_color()

    def waypoint_pen(self, player: bool) -> QPen:
        name = self.base_faction_color_name(player)
        return QPen(brush=CONST.COLORS[name])

    def waypoint_brush(self, player: bool) -> QColor:
        name = self.base_faction_color_name(player)
        return CONST.COLORS[f"{name}_transparent"]

    def flight_path_pen(self, player: bool) -> QPen:
        name = self.base_faction_color_name(player)
        color = CONST.COLORS[name]
        pen = QPen(brush=color)
        pen.setColor(color)
        pen.setWidth(1)
        pen.setStyle(Qt.DashDotLine)
        return pen

    def addBackground(self):
        scene = self.scene()

        bg = QPixmap("./resources/" + self.game.theater.overview_image)
        scene.addPixmap(bg)

        # Apply graphical effects to simulate current daytime
        if self.game.current_turn_daytime == "day":
            pass
        elif self.game.current_turn_daytime == "night":
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
