import datetime

from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QVBoxLayout

from game.weather import Conditions, TimeOfDay
import qt_ui.uiconstants as CONST


class QTurnCounter(QGroupBox):
    """
    UI Component to display current turn and time info
    """

    def __init__(self):
        super(QTurnCounter, self).__init__("Turn")

        self.icons = {
            TimeOfDay.Dawn: CONST.ICONS["Dawn"],
            TimeOfDay.Day: CONST.ICONS["Day"],
            TimeOfDay.Dusk: CONST.ICONS["Dusk"],
            TimeOfDay.Night: CONST.ICONS["Night"],
        }

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.daytime_icon = QLabel()
        self.daytime_icon.setPixmap(self.icons[TimeOfDay.Dawn])
        self.layout.addWidget(self.daytime_icon)

        self.time_column = QVBoxLayout()
        self.layout.addLayout(self.time_column)

        self.date_display = QLabel()
        self.time_column.addWidget(self.date_display)

        self.time_display = QLabel()
        self.time_column.addWidget(self.time_display)

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        """
        self.daytime_icon.setPixmap(self.icons[conditions.time_of_day])
        self.date_display.setText(conditions.start_time.strftime("%d %b %Y"))
        self.time_display.setText(
            conditions.start_time.strftime("%H:%M:%S Local"))
        self.setTitle("Turn " + str(turn + 1))
