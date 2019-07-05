from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget


class QDebriefingWindow(QWindow):

    def __init__(self, parent):
        super(QDebriefingWindow, self).__init__(parent)
        self.initUi()

    def initUi(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("TODO : This will be the debriefing menu"))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)