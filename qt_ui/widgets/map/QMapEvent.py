from PySide2.QtGui import QPen
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent

import qt_ui.uiconstants as CONST
from game.event import Event
from qt_ui.windows.QBriefingWindow import QBriefingWindow
from theater import TheaterGroundObject, ControlPoint


class QMapEvent(QGraphicsRectItem):

    def __init__(self, parent, x: float, y: float, w: float, h: float, gameEvent: Event):
        super(QMapEvent, self).__init__(x, y, w, h)
        self.gameEvent = gameEvent
        self.parent = parent
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        print(x,y,w,h)
        self.setToolTip(str(self.gameEvent))

    def paint(self, painter, option, widget=None):

        if self.parent.get_display_rule("events"):
            painter.save()

            if self.gameEvent.is_player_attacking:
                painter.setPen(QPen(brush=CONST.COLORS["blue"]))
                painter.setBrush(CONST.COLORS["blue"])
            else:
                painter.setPen(QPen(brush=CONST.COLORS["red"]))
                painter.setBrush(CONST.COLORS["red"])

            painter.drawRect(option.rect)
            print(option.rect)
            painter.drawPixmap(option.rect, CONST.EVENT_ICONS[self.gameEvent.__class__])
            painter.restore()

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        self.openBriefing()

    def openBriefing(self):
        self.briefing = QBriefingWindow(self.window(), self.gameEvent)
        self.briefing.show()