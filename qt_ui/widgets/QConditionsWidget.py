from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QVBoxLayout, QFrame, QGridLayout
from PySide2.QtGui import QPixmap

from game.weather import Conditions, TimeOfDay, Weather
from game.utils import meter_to_nm, mps_to_knots
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

        self.icons = {
            TimeOfDay.Dawn: CONST.ICONS["Dawn"],
            TimeOfDay.Day: CONST.ICONS["Day"],
            TimeOfDay.Dusk: CONST.ICONS["Dusk"],
            TimeOfDay.Night: CONST.ICONS["Night"],
        }

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.makeWeatherIcon()
        self.makeCloudRainFogWidget()
        self.makeWindsWidget()
   
    def makeWeatherIcon(self):
        """Makes the Weather Icon Widget
        """
        self.weather_icon = QLabel()
        self.weather_icon.setPixmap(self.icons[TimeOfDay.Dawn])
        self.layout.addWidget(self.weather_icon)

    def makeCloudRainFogWidget(self):
        """Makes the Cloud, Rain, Fog Widget
        """
        self.textLayout = QVBoxLayout()
        self.layout.addLayout(self.textLayout)

        self.forecastClouds = self.makeLabel()
        self.textLayout.addWidget(self.forecastClouds)

        self.forecastRain = self.makeLabel()
        self.textLayout.addWidget(self.forecastRain)

        self.forecastFog = self.makeLabel()
        self.textLayout.addWidget(self.forecastFog)

    def makeWindsWidget(self):
        """Factory for the winds widget.
        """
        windsLayout = QGridLayout()
        self.layout.addLayout(windsLayout)

        windsLayout.addWidget(self.makeIcon(CONST.ICONS['Weather_winds']), 0, 0, 3, 1)

        windsLayout.addWidget(self.makeLabel('At GL'), 0, 1)
        windsLayout.addWidget(self.makeLabel('At FL08'), 1, 1)
        windsLayout.addWidget(self.makeLabel('At FL26'), 2, 1)

        self.windGLSpeedLabel = self.makeLabel('0kts')
        self.windGLDirLabel = self.makeLabel('0º')
        windsLayout.addWidget(self.windGLSpeedLabel, 0, 2)
        windsLayout.addWidget(self.windGLDirLabel, 0, 3)

        
        self.windFL08SpeedLabel = self.makeLabel('0kts')
        self.windFL08DirLabel = self.makeLabel('0º')
        windsLayout.addWidget(self.windFL08SpeedLabel, 1, 2)
        windsLayout.addWidget(self.windFL08DirLabel, 1, 3)

        self.windFL26SpeedLabel = self.makeLabel('0kts')
        self.windFL26DirLabel = self.makeLabel('0º')
        windsLayout.addWidget(self.windFL26SpeedLabel, 2, 2)
        windsLayout.addWidget(self.windFL26DirLabel, 2, 3)

    def makeLabel(self, text: str = '') -> QLabel:
        """Shorthand to generate a QLabel with widget standard style

        :arg pixmap QPixmap for the icon.
        """
        label = QLabel(text)
        label.setProperty('style', 'text-sm')

        return label
    
    def makeIcon(self, pixmap: QPixmap) -> QLabel:
        """Shorthand to generate a QIcon with pixmap.

        :arg pixmap QPixmap for the icon.
        """
        icon = QLabel()
        icon.setPixmap(pixmap)

        return icon

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        """
        self.turn = turn
        self.conditions = conditions

        self.updateForecast()
        self.updateWinds()

    def updateWinds(self):
        """Updates the UI with the current conditions wind info.
        """
        windGlSpeed = mps_to_knots(self.conditions.weather.wind.at_0m.speed or 0)
        windGlDir = self.conditions.weather.wind.at_0m.direction or 0
        self.windGLSpeedLabel.setText('{}kts'.format(windGlSpeed))
        self.windGLDirLabel.setText('{}º'.format(windGlDir))

        windFL08Speed = mps_to_knots(self.conditions.weather.wind.at_2000m.speed or 0)
        windFL08Dir = self.conditions.weather.wind.at_2000m.direction or 0
        self.windFL08SpeedLabel.setText('{}kts'.format(windFL08Speed))
        self.windFL08DirLabel.setText('{}º'.format(windFL08Dir))

        windFL26Speed = mps_to_knots(self.conditions.weather.wind.at_8000m.speed or 0)
        windFL26Dir = self.conditions.weather.wind.at_8000m.direction or 0
        self.windFL26SpeedLabel.setText('{}kts'.format(windFL26Speed))
        self.windFL26DirLabel.setText('{}º'.format(windFL26Dir))

    def updateForecast(self):
        """Updates the Forecast Text and icon with the current conditions wind info.
        """
        icon = []
        cloudDensity = self.conditions.weather.clouds.density or 0
        precipitation = self.conditions.weather.clouds.precipitation or None
        fog = self.conditions.weather.fog or None
        is_night = self.conditions.time_of_day == TimeOfDay.Night
        time = 'night' if is_night else 'day'

        if cloudDensity <= 0:
            self.forecastClouds.setText('Sunny')
            icon = [time, 'clear']
        
        if cloudDensity > 0 and cloudDensity < 3:
            self.forecastClouds.setText('Partly Cloudy')
            icon = [time, 'partly-cloudy']

        if cloudDensity >= 3 and cloudDensity < 5:
            self.forecastClouds.setText('Mostly Cloudy')
            icon = [time, 'partly-cloudy']

        if cloudDensity >= 5:
            self.forecastClouds.setText('Totally Cloudy')
            icon = [time, 'partly-cloudy']

        if precipitation == PydcsWeather.Preceptions.Rain:
            self.forecastRain.setText('Rain')
            icon = [time, 'rain']

        elif precipitation == PydcsWeather.Preceptions.Thunderstorm:
            self.forecastRain.setText('Thunderstorm')
            icon = [time, 'thunderstorm']
            
        else:
            self.forecastRain.setText('No Rain')

        if not fog:
            self.forecastFog.setText('No fog')
        else:       
            visvibilityNm = round(meter_to_nm(fog.visibility), 1)
            self.forecastFog.setText('Fog vis: {}nm'.format(visvibilityNm))
            icon = [time, ('cloudy' if cloudDensity > 1 else None), 'fog']


        icon_key = "Weather_{}".format('-'.join(filter(None.__ne__, icon)))
        icon = CONST.ICONS.get(icon_key) or CONST.ICONS['Weather_night-partly-cloudy']        
        self.weather_icon.setPixmap(icon)


class QConditionsWidget(QFrame):
    """
    UI Component to display Turn Number, Day Time & Hour and weather combined.
    """

    def __init__(self):
        super(QConditionsWidget, self).__init__()
        self.setProperty('style', 'QConditionsWidget')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        self.time_turn_widget = QTimeTurnWidget()
        self.time_turn_widget.setStyleSheet('QGroupBox { margin-right: 0px; }')
        self.layout.addWidget(self.time_turn_widget, 0, 0)

        self.weather_widget = QWeatherWidget()
        self.weather_widget.setStyleSheet('QGroupBox { margin-top: 5px; margin-left: 0px; border-left: 0px; }')
        self.weather_widget.hide()
        self.layout.addWidget(self.weather_widget, 0, 1)

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        """
        self.time_turn_widget.setCurrentTurn(turn, conditions)
        self.weather_widget.setCurrentTurn(turn, conditions)
        self.weather_widget.show()

