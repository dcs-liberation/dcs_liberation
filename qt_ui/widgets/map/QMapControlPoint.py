from PySide2.QtCore import QRect, Qt
from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsSceneHoverEvent, QGraphicsSceneContextMenuEvent, QMenu, \
    QAction, QGraphicsSceneMouseEvent

import qt_ui.uiconstants as CONST
from game import Game
from qt_ui.windows.basemenu.QBaseMenu import QBaseMenu
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from theater import ControlPoint, db


class QMapControlPoint(QGraphicsRectItem):

    def __init__(self, parent, x: float, y: float, w: float, h: float, model: ControlPoint, game: Game):
        super(QMapControlPoint, self).__init__(x, y, w, h)
        self.model = model
        self.game = game
        self.parent = parent
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        self.setToolTip(self.model.name)


    def paint(self, painter, option, widget=None):
        #super(QMapControlPoint, self).paint(painter, option, widget)

        if self.parent.get_display_rule("cp"):
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(self.brush_color)
            painter.setPen(self.pen_color)

            if self.model.has_runway():
                if self.isUnderMouse():
                    painter.setBrush(CONST.COLORS["white"])
                    painter.setPen(self.pen_color)

                r = option.rect
                painter.drawEllipse(r.x(), r.y(), r.width(), r.height())

                #gauge = QRect(r.x(),
                #              r.y()+CONST.CP_SIZE/2 + 2,
                #              r.width(),
                #              CONST.CP_SIZE / 4)

                #painter.setBrush(CONST.COLORS["bright_red"])
                #painter.setPen(CONST.COLORS["black"])
                #painter.drawRect(gauge)

                #gauge2 = QRect(r.x(),
                #               r.y() + CONST.CP_SIZE / 2 + 2,
                #               r.width()*self.model.base.strength,
                #               CONST.CP_SIZE / 4)

                #painter.setBrush(CONST.COLORS["green"])
                #painter.drawRect(gauge2)
            else:
                # TODO : not drawing sunk carriers. Can be improved to display sunk carrier.
                pass
            painter.restore()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()
        self.setCursor(Qt.PointingHandCursor)

    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent):
        self.update()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        self.contextMenuEvent(event)

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):

        if self.model.captured:
            openBaseMenu = QAction("Open base menu")
        else:
            openBaseMenu = QAction("Open intel menu")

        openBaseMenu.triggered.connect(self.openBaseMenu)

        menu = QMenu("Menu", self.parent)
        menu.addAction(openBaseMenu)
        menu.exec_(event.screenPos())


    @property
    def brush_color(self)->QColor:
        if self.parent.game.player_country in db.BLUEFOR_FACTIONS:
            return self.model.captured and CONST.COLORS["blue"] or CONST.COLORS["super_red"]
        else:
            return self.model.captured and CONST.COLORS["super_red"] or CONST.COLORS["blue"]

    @property
    def pen_color(self) -> QColor:
        if self.parent.game.player_country in db.BLUEFOR_FACTIONS:
            return self.model.captured and CONST.COLORS["dark_blue"] or CONST.COLORS["bright_red"]
        else:
            return self.model.captured and CONST.COLORS["bright_red"] or CONST.COLORS["dark_blue"]

    def openBaseMenu(self):
        self.baseMenu = QBaseMenu2(self.window(), self.model, self.game)
        self.baseMenu.show()