from PySide2.QtCore import QLine
from PySide2.QtGui import QColor, QPainter, QCursor, QTextItem, QPen
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsSceneHoverEvent, QGraphicsSceneContextMenuEvent, QMenu, \
    QAction

from qt_ui.windows.QBaseMenu import QBaseMenu
from theater import ControlPoint
from game import Game
import qt_ui.uiconstants as CONST


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

            if self.isUnderMouse():
                painter.setBrush(CONST.COLORS["green"])
                painter.setPen(self.pen_color)

            painter.drawEllipse(option.rect)

            r = option.rect
            painter.setPen(QPen(CONST.COLORS["white"], CONST.CP_SIZE/5))
            painter.setBrush(CONST.COLORS["white"])
            painter.drawLine(QLine(r.x()+CONST.CP_SIZE/5, r.y()+CONST.CP_SIZE/5,
                                   r.x()+r.width()-CONST.CP_SIZE/5,
                                   r.y()+r.height()-CONST.CP_SIZE/5))

            painter.restore()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
        # TODO : improve this and add contextual actions (just a placholder for now)

        openBaseMenu = QAction("Open base menu")
        openBaseMenu.triggered.connect(self.openBaseMenu)

        menu = QMenu("Menu", self.parent)
        menu.addAction("Plan a strike on " + self.model.name + " airbase")
        menu.addAction("See available intel")
        menu.addAction(openBaseMenu)
        menu.exec_(event.screenPos())


    @property
    def brush_color(self)->QColor:
        if self.parent.game.player_country == "USA":
            return self.model.captured and CONST.COLORS["blue"] or CONST.COLORS["red"]
        else:
            return self.model.captured and CONST.COLORS["red"] or CONST.COLORS["blue"]

    @property
    def pen_color(self) -> QColor:
        if self.parent.game.player_country == "USA":
            return self.model.captured and CONST.COLORS["dark_blue"] or CONST.COLORS["bright_red"]
        else:
            return self.model.captured and CONST.COLORS["bright_red"] or CONST.COLORS["dark_blue"]

    def openBaseMenu(self):
        self.baseMenu = QBaseMenu(self.window(), self.model, self.game)
        self.baseMenu.show()