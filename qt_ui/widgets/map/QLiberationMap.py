import typing
from typing import Dict

from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QPixmap, QBrush, QColor, QWheelEvent, QPen, QFont
from PySide2.QtWidgets import QGraphicsView, QFrame, QGraphicsOpacityEffect
from dcs import Point

import qt_ui.uiconstants as CONST
from game import Game
from game.event import InfantryTransportEvent, StrikeEvent, BaseAttackEvent, UnitsDeliveryEvent, Event, \
    FrontlineAttackEvent, FrontlinePatrolEvent, ConvoyStrikeEvent
from gen import Conflict
from qt_ui.widgets.map.QLiberationScene import QLiberationScene
from qt_ui.widgets.map.QMapControlPoint import QMapControlPoint
from qt_ui.widgets.map.QMapEvent import QMapEvent
from qt_ui.widgets.map.QMapGroundObject import QMapGroundObject
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from theater import ControlPoint


class QLiberationMap(QGraphicsView):

    instance = None
    display_rules: Dict[str, bool] = {
        "cp": True,
        "go": True,
        "lines": True,
        "events": True,
        "ennemy_sam_ranges": True,
        "ally_sam_ranges": True
    }

    def __init__(self, game: Game):
        super(QLiberationMap, self).__init__()
        QLiberationMap.instance = self

        self.frontline_vector_cache = {}

        self.setMinimumSize(800,600)
        self.setMaximumHeight(2160)
        self._zoom = 0
        self.init_scene()
        self.connectSignals()
        self.setGame(game)

    def init_scene(self):
        scene = QLiberationScene(self)
        scene.addText("Hello World")

        self.setScene(scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def connectSignals(self):
        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)

    def setGame(self, game: Game):
        self.game = game
        print("Reloading Map Canvas")
        if self.game is not None:
            self.reload_scene()

    def reload_scene(self):
        scene = self.scene()
        scene.clear()

        self.addBackground()

        self.add_game_events()

        for cp in self.game.theater.controlpoints:

            pos = self._transform_point(cp.position)
            scene.addItem(QMapControlPoint(self, pos[0] - CONST.CP_SIZE / 2, pos[1] - CONST.CP_SIZE / 2, CONST.CP_SIZE,
                                           CONST.CP_SIZE, cp, self.game))

            # e = scene.addEllipse(pos[0]-CONST.CP_SIZE/2, pos[1]-CONST.CP_SIZE/2, CONST.CP_SIZE, CONST.CP_SIZE, QPen(brush=QBrush(color=color), width=5), brush=color)

            text = scene.addText(cp.name, font=QFont("Trebuchet MS", 10, weight=5, italic=False))
            text.setPos(pos[0] + CONST.CP_SIZE, pos[1] - CONST.CP_SIZE / 2)

            text = scene.addText(cp.name, font=QFont("Trebuchet MS", 10, weight=5, italic=False))
            text.setDefaultTextColor(Qt.white)
            text.setPos(pos[0] + CONST.CP_SIZE + 1, pos[1] - CONST.CP_SIZE / 2 + 1)

            for ground_object in cp.ground_objects:
                go_pos = self._transform_point(ground_object.position)
                scene.addItem(QMapGroundObject(self, go_pos[0], go_pos[1], 16, 16, cp, ground_object))

            if self.get_display_rule("lines"):
                self.scene_create_lines_for_cp(cp)

    def scene_create_lines_for_cp(self, cp: ControlPoint):
        scene = self.scene()
        pos = self._transform_point(cp.position)
        for connected_cp in cp.connected_points:
            pos2 = self._transform_point(connected_cp.position)
            if connected_cp.captured != cp.captured:
                color = CONST.COLORS["red"]
            elif connected_cp.captured and cp.captured:
                color = CONST.COLORS["blue"]
            else:
                color = CONST.COLORS["black_transparent"]

            pen = QPen(brush=color)
            pen.setColor(color)
            pen.setWidth(4)
            scene.addLine(pos[0], pos[1], pos2[0], pos2[1], pen=pen)

            if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):
                frontline = self._frontline_vector(cp, connected_cp)
                if not frontline:
                    continue

                frontline_pos, heading, distance = frontline

                if distance < 10000:
                    frontline_pos = frontline_pos.point_from_heading(heading + 180, 5000)
                    distance = 10000

                start_coords = self._transform_point(frontline_pos, treshold=10)
                end_coords = self._transform_point(frontline_pos.point_from_heading(heading, distance),
                                                   treshold=60)

                frontline_pen = QPen(brush=CONST.COLORS["bright_red"])
                frontline_pen.setColor(CONST.COLORS["bright_red"])
                frontline_pen.setWidth(4)
                frontline_pen.setStyle(Qt.DashDotLine)
                scene.addLine(start_coords[0], start_coords[1], end_coords[0], end_coords[1], pen=frontline_pen)

    def _frontline_vector(self, from_cp: ControlPoint, to_cp: ControlPoint):
        # Cache mechanism to avoid performing frontline vector computation on every frame
        key = str(from_cp.id) + "_" + str(to_cp.id)
        if key in self.frontline_vector_cache:
            return self.frontline_vector_cache[key]
        else:
            frontline = Conflict.frontline_vector(from_cp, to_cp, self.game.theater)
            self.frontline_vector_cache[key] = frontline
            return frontline

    def _frontline_center(self, from_cp: ControlPoint, to_cp: ControlPoint) -> typing.Optional[Point]:
        frontline_vector = self._frontline_vector(from_cp, to_cp)
        if frontline_vector:
            return frontline_vector[0].point_from_heading(frontline_vector[1], frontline_vector[2]/2)
        else:
            return None

    def wheelEvent(self, event: QWheelEvent):

        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1

        if self._zoom > -5:
            self.scale(factor, factor)
        else:
            self._zoom = -5

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

    def add_game_events(self):

        occupied_rects = []

        for cp in self.game.theater.controlpoints:
            point = self._transform_point(cp.position)
            occupied_rects.append(QRect(point[0] - 16, point[1] - 16, 32, 48))

        def _location_to_rect(location: Point) -> QRect:
            nonlocal occupied_rects
            point = self._transform_point(location)
            rect = QRect(point[0] - 16, point[1] - 16, 32, 32)

            i = 0
            while True:
                result = True
                for occupied_rect in occupied_rects:
                    if rect.intersects(occupied_rect):
                        i += 1
                        if i % 2:
                            rect.setY(rect.y() + occupied_rect.height())
                        else:
                            rect.setX(rect.x() + occupied_rect.width())
                        result = False
                        break
                if result:
                    break
            occupied_rects.append(rect)
            return rect

        def _events_priority_key(event: Event) -> int:
            priority_list = [InfantryTransportEvent, StrikeEvent, BaseAttackEvent, UnitsDeliveryEvent]
            if type(event) not in priority_list:
                return 0
            else:
                return priority_list.index(type(event)) + 1

        scene = self.scene()
        events = self.game.events
        events.sort(key=_events_priority_key, reverse=True)

        for event in events:

            location = event.location
            if type(event) in [FrontlineAttackEvent, FrontlinePatrolEvent, ConvoyStrikeEvent]:
                location = self._frontline_center(event.from_cp, event.to_cp)

            rect = _location_to_rect(location)
            scene.addItem(QMapEvent(self, rect.x(), rect.y(), 32, 32, event))

    def addBackground(self):
        scene = self.scene()

        bg = QPixmap("./resources/" + self.game.theater.overview_image)
        scene.addPixmap(bg)

        # Apply graphical effects to simulate current daytime
        if self.game.current_turn_daytime == "day":
            pass
        elif self.game.current_turn_daytime == "night":
            ov = QPixmap(bg.width(), bg.height())
            ov.fill(QColor(40, 40, 150))
            overlay = scene.addPixmap(ov)
            effect = QGraphicsOpacityEffect();
            effect.setOpacity(0.7)
            overlay.setGraphicsEffect(effect)
        else:
            ov = QPixmap(bg.width(), bg.height())
            ov.fill(QColor(165, 100, 100))
            overlay = scene.addPixmap(ov)
            effect = QGraphicsOpacityEffect();
            effect.setOpacity(0.3)
            overlay.setGraphicsEffect(effect)











    @staticmethod
    def set_display_rule(rule: str, value: bool):
        QLiberationMap.display_rules[rule] = value
        QLiberationMap.instance.reload_scene()
        QLiberationMap.instance.update()

    @staticmethod
    def get_display_rules() -> Dict[str, bool]:
        return QLiberationMap.display_rules

    @staticmethod
    def get_display_rule(rule) -> bool:
        return QLiberationMap.display_rules[rule]
