from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QGraphicsWidget, QGraphicsView

from qt_ui.windows.QLiberationScene import QLiberationScene


class QLiberationMap(QGraphicsView):

    def __init__(self):
        super(QLiberationMap, self).__init__()
        self.setMinimumSize(800,600)
        self.init_scene()

    def init_scene(self):
        scene = QLiberationScene(self)
        scene.addText("Hello World")
        scene.addPixmap(QPixmap("../resources/caumap.gif"))
        self.setScene(scene)
