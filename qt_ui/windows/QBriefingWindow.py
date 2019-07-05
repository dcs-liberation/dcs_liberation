from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget


class QBriefingWindow(QWindow):

    def __init__(self, parent):
        super(QBriefingWindow, self).__init__(parent)
        self.initUi()

    def initUi(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("TODO : This will be the briefing window"))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)