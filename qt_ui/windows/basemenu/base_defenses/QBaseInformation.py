from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QFrame,
    QGridLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from game.theater import Airport, ControlPoint
from qt_ui.windows.basemenu.base_defenses.QBaseDefenseGroupInfo import \
    QBaseDefenseGroupInfo


class QBaseInformation(QFrame):

    def __init__(self, cp:ControlPoint, airport:Airport, game):
        super(QBaseInformation, self).__init__()
        self.cp = cp
        self.airport = airport
        self.game = game
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        self.mainLayout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        scroll_content.setLayout(task_box_layout)

        for g in self.cp.ground_objects:
            if g.airbase_group:
                group_info = QBaseDefenseGroupInfo(self.cp, g, self.game)
                task_box_layout.addWidget(group_info)

        scroll_content.setLayout(task_box_layout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)

        self.mainLayout.addWidget(scroll)

        self.setLayout(self.mainLayout)