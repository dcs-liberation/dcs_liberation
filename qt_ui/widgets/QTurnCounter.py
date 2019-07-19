import datetime

from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox

import qt_ui.uiconstants as CONST


class QTurnCounter(QGroupBox):
    """
    UI Component to display current turn and time info
    """

    def __init__(self):
        super(QTurnCounter, self).__init__("Turn")

        self.icons = [CONST.ICONS["Dawn"], CONST.ICONS["Day"], CONST.ICONS["Dusk"], CONST.ICONS["Night"]]

        self.daytime_icon = QLabel()
        self.daytime_icon.setPixmap(self.icons[0])
        self.turn_info = QLabel()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.daytime_icon)
        self.layout.addWidget(self.turn_info)
        self.setLayout(self.layout)

    def setCurrentTurn(self, turn: int, current_day: datetime):
        """
        Set the money amount to display
        :arg turn Current turn number
        :arg current_day Current day
        """
        self.daytime_icon.setPixmap(self.icons[turn % 4])
        self.turn_info.setText(current_day.strftime("%d %b %Y"))
        self.setTitle("Turn " + str(turn + 1))
