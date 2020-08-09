from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGraphicsScene

import qt_ui.uiconstants as CONST


class QLiberationScene(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)
        item = self.addText("Go to \"File/New Game\" to setup a new campaign or go to \"File/Open\" to load an existing save game.",
                            CONST.FONT_PRIMARY)
        item.setDefaultTextColor(CONST.COLORS["white"])
