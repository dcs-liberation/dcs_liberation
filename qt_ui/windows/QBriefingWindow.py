from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QDialog


class QBriefingWindow(QDialog):

    def __init__(self, parent, event):
        super(QBriefingWindow, self).__init__(parent)
        self.gameEvent = event
        self.setWindowTitle("Briefing : " + str(event))
        self.setMinimumSize(200,200)
        self.setModal(True)
        self.initUi()

    def initUi(self):

        layout = QHBoxLayout()
        layout.addWidget(QLabel("TODO : This will be the briefing window"))

        self.setLayout(layout)