import datetime

from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QVBoxLayout, QFrame, QSizePolicy, QStyle, QPushButton

from game.weather import Conditions, TimeOfDay
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

    def __init__(self):
        super(QWeatherWidget, self).__init__("")
        self.setProperty('style', 'QWeatherWidget')

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

        self.forecast = QLabel('')
        self.layout.addWidget(self.forecast)

        self.details = QPushButton("Weather")
        self.details.setProperty("style", "btn-primary")
        self.details.setDisabled(True)
        self.details.clicked.connect(self.openDetailWindow)
        self.layout.addWidget(self.details)

    def openDetailWindow(self):
        pass

    def setCurrentConditions(self, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg conditions Current time and weather conditions.
        """
        self.conditions = conditions

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

        pass

    def updateDetailsBtn(self):        
        if not self.conditions:
            self.details.setEnable(False)
        else:
            self.details.setEnable(True)
        

class QConditionsWidget(QFrame):
    def __init__(self):
        super(QConditionsWidget, self).__init__()
        self.layout = QHBoxLayout()        
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setProperty('style', 'QConditionsWidget')

        self.time_turn_widget = QTimeTurnWidget()
        self.layout.addWidget(self.time_turn_widget)

        self.weather_widget = QWeatherWidget()
        self.layout.addWidget(self.weather_widget)

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        self.time_turn_widget.setCurrentTurn(turn, conditions)
        self.weather_widget.setCurrentConditions(conditions)

