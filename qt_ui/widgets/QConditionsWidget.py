import datetime

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QVBoxLayout, QFrame, QSizePolicy, QStyle, QPushButton, QGridLayout
from PySide2.QtGui import QFont

from game.weather import Conditions, TimeOfDay, Weather
from dcs.weather import Weather as PydcsWeather

from qt_ui.windows.weather.QWeatherInfoWindow import QWeatherInfoWindow
import qt_ui.uiconstants as CONST



class QTimeTurnWidget(QGroupBox):
    """
    UI Component to display current turn and time info
    """
    
    def __init__(self):
        super(QTimeTurnWidget, self).__init__("Turn")
        self.setStyleSheet('padding: 0px; margin-left: 5px; margin-right: 0px; margin-top: 1ex; margin-bottom: 5px; border-right: 0px')

        self.icons = {
            TimeOfDay.Dawn: CONST.ICONS["Dawn"],
            TimeOfDay.Day: CONST.ICONS["Day"],
            TimeOfDay.Dusk: CONST.ICONS["Dusk"],
            TimeOfDay.Night: CONST.ICONS["Night"],
        }

        # self.setProperty('style', 'conditions__widget--turn')
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

class QWeatherWidget(QGroupBox):
    """
    UI Component to display current weather forecast
    """
    turn = None
    conditions = None

    def __init__(self):
        super(QWeatherWidget, self).__init__("")
        self.setProperty('style', 'QWeatherWidget')
        self.conditions = None
        

        self.icons = {
            TimeOfDay.Dawn: CONST.ICONS["Dawn"],
            TimeOfDay.Day: CONST.ICONS["Day"],
            TimeOfDay.Dusk: CONST.ICONS["Dusk"],
            TimeOfDay.Night: CONST.ICONS["Night"],
        }

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.weather_icon = QLabel()
        self.weather_icon.setPixmap(self.icons[TimeOfDay.Dawn])
        self.layout.addWidget(self.weather_icon)

        self.textLayout = QVBoxLayout()
        self.layout.addLayout(self.textLayout)

        self.forecastClouds = QLabel('')
        self.textLayout.addWidget(self.forecastClouds)

        self.forecastRain = QLabel('')
        self.textLayout.addWidget(self.forecastRain)

        self.forecastFog = QLabel('')
        self.textLayout.addWidget(self.forecastFog)

        self.details = QPushButton("Weather")
        self.details.setProperty("style", "btn-primary")
        self.details.setDisabled(True)
        self.details.clicked.connect(self.openDetailWindow)
        self.layout.addWidget(self.details)

    def openDetailWindow(self):
        self.subwindow = QWeatherInfoWindow(self.turn, self.conditions)
        self.subwindow.show()

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg conditions Current time and weather conditions.
        """
        self.turn
        self.conditions = conditions

        if conditions and turn > 0:
            self.details.setDisabled(True)
        else:
            self.details.setDisabled(False)

        self.updateIcon()
        self.updateText()

        pass

    def updateIcon(self):
        """
        Updates the Forecast Icon based on turn conditions
        """
        

        pass

    def updateText(self):
        """
        Updates the Forecast Text based on turn conditions
        """
        cloudDensity = self.conditions.weather.clouds.density
        precipitation = self.conditions.weather.clouds.precipitation

        if cloudDensity <= 0:
            self.forecastClouds.setText('Sunny')
        
        if cloudDensity > 0 and cloudDensity < 3:
            self.forecastClouds.setText('Partly Cloudy')

        if cloudDensity > 3 and cloudDensity < 6:
            self.forecastClouds.setText('Mostly Cloudy')

        if cloudDensity > 6:
            self.forecastClouds.setText('Totally Cloudy')
        

        if precipitation == PydcsWeather.Preceptions.Rain:
            self.forecastRain.setText('Rain')
        elif precipitation == PydcsWeather.Preceptions.Thunderstorm:
            self.forecastRain.setText('Thunderstorm')
        else:
            self.forecastRain.setText('No Rain')

        if not self.conditions.weather.fog:
            self.textLayout.removeWidget(self.forecastFog)


    def updateDetailsBtn(self):        
        if not self.conditions:
            self.details.setEnable(False)
        else:
            self.details.setEnable(True)


class QConditionsWidget(QFrame):
    def __init__(self):
        super(QConditionsWidget, self).__init__()
        self.setProperty('style', 'QConditionsWidget')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        self.time_turn_widget = QTimeTurnWidget()
        self.time_turn_widget.setStyleSheet('QGroupBox { margin-right: 0px; border-right: 0px; }')
        self.layout.addWidget(self.time_turn_widget, 0, 0)

        self.weather_widget = QWeatherWidget()
        self.weather_widget.setStyleSheet('QGroupBox { margin-top: 5px; margin-left: 0px; }')
        self.layout.addWidget(self.weather_widget, 0, 1)

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        self.time_turn_widget.setCurrentTurn(turn, conditions)
        self.weather_widget.setCurrentTurn(turn, conditions)

