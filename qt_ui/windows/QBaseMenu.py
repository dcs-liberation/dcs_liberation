from PySide2.QtCore import Qt
from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget

from theater import ControlPoint


class QBaseMenu(QWidget):

    def __init__(self, parent, controlPoint: ControlPoint):
        super(QBaseMenu, self).__init__(parent)
        self.cp = controlPoint
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.initUi()

    def initUi(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("TODO : This will be the base menu"))
        layout.addWidget(QLabel(self.cp.name + " Base Info"))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setLayout(layout)