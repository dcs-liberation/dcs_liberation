"""Common base for objects drawn on the game map."""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
)


class QMapObject(QGraphicsRectItem):
    """Base class for objects drawn on the game map.

    Game map objects have an on_click behavior that triggers on left click, and
    change the mouse cursor on hover.
    """
    def __init__(self, x: float, y: float, w: float, h: float):
        super().__init__(x, y, w, h)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            self.on_click()

    def on_click(self) -> None:
        raise NotImplementedError
