from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QFrame, QSizePolicy

from game.game import Game
from game.weather import Conditions, TimeOfDay, Weather

import qt_ui.uiconstants as CONST

class QWeatherInfoWindow(QDialog):

    def __init__(self, turn: int, conditions: Conditions):
        super(QWeatherInfoWindow, self).__init__()

        self.setModal(True)
        self.setWindowTitle("Weather Forecast Report")
        self.setWindowIcon(CONST.ICONS["Money"])
        self.setMinimumSize(450, 200)