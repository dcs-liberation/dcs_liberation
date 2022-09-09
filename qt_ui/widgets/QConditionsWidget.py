from datetime import datetime

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)
from dcs.weather import CloudPreset, Weather as PydcsWeather

import qt_ui.uiconstants as CONST
from game.sim.gameupdateevents import GameUpdateEvents
from game.timeofday import TimeOfDay
from game.utils import mps
from game.weather import Conditions
from qt_ui.simcontroller import SimController


class QTimeTurnWidget(QGroupBox):
    """
    UI Component to display current turn and time info
    """

    def __init__(self, sim_controller: SimController) -> None:
        super(QTimeTurnWidget, self).__init__("Turn")
        self.sim_controller = sim_controller
        self.setStyleSheet(
            "padding: 0px; margin-left: 5px; margin-right: 0px; margin-top: 1ex; margin-bottom: 5px; border-right: 0px"
        )

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

        sim_controller.sim_update.connect(self.on_sim_update)

    def on_sim_update(self, _events: GameUpdateEvents) -> None:
        time = self.sim_controller.current_time_in_sim
        if time is None:
            self.date_display.setText("")
            self.time_display.setText("")
        else:
            self.set_date_and_time(time)

    def set_current_turn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        """
        self.daytime_icon.setPixmap(self.icons[conditions.time_of_day])
        self.set_date_and_time(conditions.start_time)
        self.setTitle(f"Turn {turn}")

    def set_date_and_time(self, time: datetime) -> None:
        self.date_display.setText(time.strftime("%d %b %Y"))
        self.time_display.setText(time.strftime("%H:%M:%S Local"))


class QWeatherWidget(QGroupBox):
    """
    UI Component to display current weather forecast
    """

    turn = None
    conditions = None

    def __init__(self):
        super(QWeatherWidget, self).__init__("")
        self.setProperty("style", "QWeatherWidget")

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
        """Makes the Weather Icon Widget"""
        self.weather_icon = QLabel()
        self.weather_icon.setPixmap(self.icons[TimeOfDay.Dawn])
        self.layout.addWidget(self.weather_icon)

    def makeCloudRainFogWidget(self):
        """Makes the Cloud, Rain, Fog Widget"""
        self.textLayout = QVBoxLayout()
        self.layout.addLayout(self.textLayout)

        self.forecastClouds = self.makeLabel()
        self.textLayout.addWidget(self.forecastClouds)

        self.forecastRain = self.makeLabel()
        self.textLayout.addWidget(self.forecastRain)

        self.forecastFog = self.makeLabel()
        self.textLayout.addWidget(self.forecastFog)

    def makeWindsWidget(self):
        """Factory for the winds widget."""
        windsLayout = QGridLayout()
        self.layout.addLayout(windsLayout)

        windsLayout.addWidget(self.makeIcon(CONST.ICONS["Weather_winds"]), 0, 0, 3, 1)

        windsLayout.addWidget(self.makeLabel("At GL"), 0, 1)
        windsLayout.addWidget(self.makeLabel("At FL08"), 1, 1)
        windsLayout.addWidget(self.makeLabel("At FL26"), 2, 1)

        self.windGLSpeedLabel = self.makeLabel("0kts")
        self.windGLDirLabel = self.makeLabel("0º")
        windsLayout.addWidget(self.windGLSpeedLabel, 0, 2)
        windsLayout.addWidget(self.windGLDirLabel, 0, 3)

        self.windFL08SpeedLabel = self.makeLabel("0kts")
        self.windFL08DirLabel = self.makeLabel("0º")
        windsLayout.addWidget(self.windFL08SpeedLabel, 1, 2)
        windsLayout.addWidget(self.windFL08DirLabel, 1, 3)

        self.windFL26SpeedLabel = self.makeLabel("0kts")
        self.windFL26DirLabel = self.makeLabel("0º")
        windsLayout.addWidget(self.windFL26SpeedLabel, 2, 2)
        windsLayout.addWidget(self.windFL26DirLabel, 2, 3)

    def makeLabel(self, text: str = "") -> QLabel:
        """Shorthand to generate a QLabel with widget standard style

        :arg pixmap QPixmap for the icon.
        """
        label = QLabel(text)
        label.setProperty("style", "text-sm")

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

        self.update_forecast()
        self.updateWinds()

    def updateWinds(self):
        """Updates the UI with the current conditions wind info."""
        windGlSpeed = mps(self.conditions.weather.wind.at_0m.speed or 0)
        windGlDir = str(self.conditions.weather.wind.at_0m.direction or 0).rjust(3, "0")
        self.windGLSpeedLabel.setText(f"{int(windGlSpeed.knots)}kts")
        self.windGLDirLabel.setText(f"{windGlDir}º")

        windFL08Speed = mps(self.conditions.weather.wind.at_2000m.speed or 0)
        windFL08Dir = str(self.conditions.weather.wind.at_2000m.direction or 0).rjust(
            3, "0"
        )
        self.windFL08SpeedLabel.setText(f"{int(windFL08Speed.knots)}kts")
        self.windFL08DirLabel.setText(f"{windFL08Dir}º")

        windFL26Speed = mps(self.conditions.weather.wind.at_8000m.speed or 0)
        windFL26Dir = str(self.conditions.weather.wind.at_8000m.direction or 0).rjust(
            3, "0"
        )
        self.windFL26SpeedLabel.setText(f"{int(windFL26Speed.knots)}kts")
        self.windFL26DirLabel.setText(f"{windFL26Dir}º")

    def update_forecast_from_preset(self, preset: CloudPreset) -> None:
        self.forecastFog.setText("No fog")
        if "Rain" in preset.name:
            self.forecastRain.setText("Rain")
            self.update_forecast_icons("rain")
        else:
            self.forecastRain.setText("No rain")
            self.update_forecast_icons("partly-cloudy")

        # We get a description like the following for the cloud preset.
        #
        # 09 ##Two Layer Broken/Scattered \nMETAR:BKN 7.5/10 SCT 20/22 FEW41
        #
        # The second line is probably interesting but doesn't fit into the widget
        # currently, so for now just extract the first line.
        self.forecastClouds.setText(preset.description.splitlines()[0].split("##")[1])

    def update_forecast(self):
        """Updates the Forecast Text and icon with the current conditions wind info."""
        if (
            self.conditions.weather.clouds
            and self.conditions.weather.clouds.preset is not None
        ):
            self.update_forecast_from_preset(self.conditions.weather.clouds.preset)
            return

        if self.conditions.weather.clouds is None:
            cloud_density = 0
            precipitation = None
        else:
            cloud_density = self.conditions.weather.clouds.density
            precipitation = self.conditions.weather.clouds.precipitation

        if not cloud_density:
            self.forecastClouds.setText("Clear")
            weather_type = "clear"
        elif cloud_density < 3:
            self.forecastClouds.setText("Partly Cloudy")
            weather_type = "partly-cloudy"
        elif cloud_density < 5:
            self.forecastClouds.setText("Mostly Cloudy")
            weather_type = "partly-cloudy"
        else:
            self.forecastClouds.setText("Totally Cloudy")
            weather_type = "partly-cloudy"

        if precipitation == PydcsWeather.Preceptions.Rain:
            self.forecastRain.setText("Rain")
            weather_type = "rain"
        elif precipitation == PydcsWeather.Preceptions.Thunderstorm:
            self.forecastRain.setText("Thunderstorm")
            weather_type = "thunderstorm"
        else:
            self.forecastRain.setText("No rain")

        if not self.conditions.weather.fog is not None:
            self.forecastFog.setText("No fog")
        else:
            visibility = round(self.conditions.weather.fog.visibility.nautical_miles, 1)
            self.forecastFog.setText(f"Fog vis: {visibility}nm")
            if cloud_density > 1:
                weather_type = "cloudy-fog"
            else:
                weather_type = "fog"

        self.update_forecast_icons(weather_type)

    def update_forecast_icons(self, weather_type: str) -> None:
        time = "night" if self.conditions.time_of_day == TimeOfDay.Night else "day"
        icon_key = f"Weather_{time}-{weather_type}"
        icon = CONST.ICONS.get(icon_key) or CONST.ICONS["Weather_night-partly-cloudy"]
        self.weather_icon.setPixmap(icon)


class QConditionsWidget(QFrame):
    """
    UI Component to display Turn Number, Day Time & Hour and weather combined.
    """

    def __init__(self, sim_controller: SimController) -> None:
        super(QConditionsWidget, self).__init__()
        self.setProperty("style", "QConditionsWidget")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        self.time_turn_widget = QTimeTurnWidget(sim_controller)
        self.time_turn_widget.setStyleSheet("QGroupBox { margin-right: 0px; }")
        self.layout.addWidget(self.time_turn_widget, 0, 0)

        self.weather_widget = QWeatherWidget()
        self.weather_widget.setStyleSheet(
            "QGroupBox { margin-top: 5px; margin-left: 0px; border-left: 0px; }"
        )
        self.weather_widget.hide()
        self.layout.addWidget(self.weather_widget, 0, 1)

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        """
        self.time_turn_widget.set_current_turn(turn, conditions)
        self.weather_widget.setCurrentTurn(turn, conditions)
        self.weather_widget.show()
