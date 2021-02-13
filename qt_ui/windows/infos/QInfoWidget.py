from PySide2.QtWidgets import QFrame, QLabel, QGridLayout

from game.infos.information import Information


class QInfoWidget(QFrame):
    def __init__(self, info: Information):
        super(QInfoWidget, self).__init__()
        self.info = info
        self.titleLabel = QLabel("<b>" + info.title + "</b>")
        self.textLabel = QLabel(info.text)
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(self.titleLabel, 0, 0)
        layout.addWidget(self.textLabel, 1, 0)
        self.setLayout(layout)
