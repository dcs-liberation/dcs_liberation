from PySide2.QtGui import QPen, Qt
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent

import qt_ui.uiconstants as CONST
from game.event import Event, UnitsDeliveryEvent
from qt_ui.windows.QBriefingWindow import QBriefingWindow


class QMapEvent(QGraphicsRectItem):

    def __init__(self, parent, x: float, y: float, w: float, h: float, gameEvent: Event):
        super(QMapEvent, self).__init__(x, y, w, h)
        self.gameEvent = gameEvent
        self.parent = parent
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.setToolTip(str(self.gameEvent))
        self.playable = not isinstance(self.gameEvent, UnitsDeliveryEvent)

    def paint(self, painter, option, widget=None):

        if self.parent.get_display_rule("events"):
            painter.save()

            if self.gameEvent.is_player_attacking:
                painter.setPen(QPen(brush=CONST.COLORS["blue"]))
                painter.setBrush(CONST.COLORS["blue"])
            else:
                painter.setPen(QPen(brush=CONST.COLORS["red"]))
                painter.setBrush(CONST.COLORS["red"])

            if self.isUnderMouse() and self.playable:
                painter.setBrush(CONST.COLORS["white"])

            painter.drawRect(option.rect)
            painter.drawPixmap(option.rect, CONST.EVENT_ICONS[self.gameEvent.__class__])
            painter.restore()

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        if self.parent.get_display_rule("events"):
            self.openBriefing()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()
        if self.playable:
            self.setCursor(Qt.PointingHandCursor)

    def openBriefing(self):
        if self.playable:
            self.briefing = QBriefingWindow(self.gameEvent)
            self.briefing.show()