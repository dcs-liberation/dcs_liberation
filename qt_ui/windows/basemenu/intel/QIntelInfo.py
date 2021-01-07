from PySide2.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QWidget,
)
from PySide2.QtCore import Qt
from dcs.task import CAP, CAS, Embarking, PinpointStrike

from game import Game, db
from game.theater import ControlPoint


class QIntelInfo(QFrame):

    def __init__(self, cp:ControlPoint, game:Game):
        super(QIntelInfo, self).__init__()
        self.cp = cp
        self.game = game
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        scroll_content = QWidget()
        intelLayout = QVBoxLayout()



        units = {
            CAP: db.find_unittype(CAP, self.game.enemy_name),
            Embarking: db.find_unittype(Embarking, self.game.enemy_name),
            CAS: db.find_unittype(CAS, self.game.enemy_name),
            PinpointStrike: db.find_unittype(PinpointStrike, self.game.enemy_name),
        }

        for task_type in units.keys():
            units_column = list(set(units[task_type]))

            if sum([self.cp.base.total_units_of_type(u) for u in units_column]) > 0:

                group = QGroupBox(db.task_name(task_type))
                groupLayout = QGridLayout()
                group.setLayout(groupLayout)

                row = 0
                for unit_type in units_column:
                    existing_units = self.cp.base.total_units_of_type(unit_type)
                    if existing_units == 0:
                        continue
                    groupLayout.addWidget(QLabel("<b>" + db.unit_pretty_name(self.game.enemy_country, unit_type) + "</b>"), row, 0)
                    groupLayout.addWidget(QLabel(str(existing_units)), row, 1)
                    row += 1

                intelLayout.addWidget(group)

        scroll_content.setLayout(intelLayout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)
        
        self.setLayout(layout)