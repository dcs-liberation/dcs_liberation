from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QBrush, QColor, QWheelEvent, QPen, QFont
from PySide2.QtWidgets import QWidget, QGraphicsWidget, QGraphicsView, QFrame, QGraphicsTextItem

from qt_ui.widgets.QMapControlPoint import QMapControlPoint
from qt_ui.windows.QLiberationScene import QLiberationScene
from dcs import Point
from userdata import persistency
from game import Game
import qt_ui.uiconstants as CONST


class QLiberationMap(QGraphicsView):

    def __init__(self):
        super(QLiberationMap, self).__init__()
        self.setMinimumSize(800,600)
        self._zoom = 0

        self.init_scene()

        game = persistency.restore_game()
        self.loadGame(game)



    def init_scene(self):
        scene = QLiberationScene(self)
        scene.addText("Hello World")

        self.setScene(scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def loadGame(self, game: Game):
        self.game = game
        scene = self.scene()
        scene.clear()
        scene.addPixmap(QPixmap("../resources/" + self.game.theater.overview_image))
        for cp in self.game.theater.controlpoints:

            pos = self._transform_point(cp.position)
            scene.addItem(QMapControlPoint(self, pos[0]-CONST.CP_SIZE/2, pos[1]-CONST.CP_SIZE/2, CONST.CP_SIZE, CONST.CP_SIZE, cp))

            #e = scene.addEllipse(pos[0]-CONST.CP_SIZE/2, pos[1]-CONST.CP_SIZE/2, CONST.CP_SIZE, CONST.CP_SIZE, QPen(brush=QBrush(color=color), width=5), brush=color)

            text = scene.addText(cp.name, font=QFont("Trebuchet MS", 10, weight=5, italic=False))
            text.setPos(pos[0]+CONST.CP_SIZE, pos[1]-CONST.CP_SIZE/2)

            for go in cp.ground_objects:
                pos = self._transform_point(go.position)
                e = scene.addEllipse(pos[0] - CONST.CP_SIZE / 2, pos[1] - CONST.CP_SIZE / 2, CONST.CP_SIZE,
                                     CONST.CP_SIZE, QPen(brush=QBrush(color=CONST.COLORS["green"]), width=5), brush=CONST.COLORS["green"])




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
