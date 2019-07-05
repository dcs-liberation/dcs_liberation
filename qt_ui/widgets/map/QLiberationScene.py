from PySide2.QtWidgets import QWidget, QGraphicsScene


class QLiberationScene(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)
        self.addText("Hello Liberation Map")
