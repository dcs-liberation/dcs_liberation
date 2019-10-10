from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGraphicsScene

from qt_ui.uiconstants import COLORS


class QLiberationScene(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)
        item = self.addText("No save file found. Go to \"File/New Game\" to setup a new campaign.",
                     QFont("Arial", 14, weight=5))
        item.setDefaultTextColor(COLORS["white"])
