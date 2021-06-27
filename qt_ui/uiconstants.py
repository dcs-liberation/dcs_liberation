import os
from typing import Dict

from PySide2.QtGui import QPixmap

from game.theater.theatergroundobject import NAME_BY_CATEGORY
from .liberation_theme import get_theme_icons

URLS: Dict[str, str] = {
    "Manual": "https://github.com/dcs-liberation/dcs_liberation/wiki",
    "Repository": "https://github.com/dcs-liberation/dcs_liberation",
    "ForumThread": "https://forums.eagle.ru/showthread.php?t=214834",
    "Issues": "https://github.com/dcs-liberation/dcs_liberation/issues",
}

LABELS_OPTIONS = ["Full", "Abbreviated", "Dot Only", "Neutral Dot", "Off"]
SKILL_OPTIONS = ["Average", "Good", "High", "Excellent"]
SHORAD_IN_AG_PROBABILITY = ["None", "25%", "50%", "75%", "All"]

AIRCRAFT_BANNERS: Dict[str, QPixmap] = {}
AIRCRAFT_ICONS: Dict[str, QPixmap] = {}
VEHICLE_BANNERS: Dict[str, QPixmap] = {}
VEHICLES_ICONS: Dict[str, QPixmap] = {}
ICONS: Dict[str, QPixmap] = {}


def load_icons():

    ICONS["New"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/new.png")
    ICONS["Open"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/open.png")
    ICONS["Save"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/save.png")
    ICONS["Discord"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/discord.png"
    )
    ICONS["Github"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/github.png"
    )

    ICONS["Control Points"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/circle.png"
    )
    ICONS["Ground Objects"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/industry.png"
    )
    ICONS["Lines"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/arrows-h.png"
    )
    ICONS["Waypoint Information"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/info.png"
    )
    ICONS["Map Polygon Debug Mode"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/map.png"
    )
    ICONS["Ally SAM Threat Range"] = QPixmap("./resources/ui/misc/blue-sam.png")
    ICONS["Enemy SAM Threat Range"] = QPixmap("./resources/ui/misc/red-sam.png")
    ICONS["SAM Detection Range"] = QPixmap("./resources/ui/misc/detection-sam.png")
    ICONS["Display Culling Zones"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/eraser.png"
    )
    ICONS["Hide Flight Paths"] = QPixmap("./resources/ui/misc/hide-flight-path.png")
    ICONS["Show Selected Flight Path"] = QPixmap("./resources/ui/misc/flight-path.png")
    ICONS["Show All Flight Paths"] = QPixmap("./resources/ui/misc/all-flight-paths.png")

    ICONS["Hangar"] = QPixmap("./resources/ui/misc/hangar.png")

    ICONS["Terrain_Caucasus"] = QPixmap("./resources/ui/terrain_caucasus.gif")
    ICONS["Terrain_PersianGulf"] = QPixmap("./resources/ui/terrain_pg.gif")
    ICONS["Terrain_Nevada"] = QPixmap("./resources/ui/terrain_nevada.gif")
    ICONS["Terrain_Normandy"] = QPixmap("./resources/ui/terrain_normandy.gif")
    ICONS["Terrain_TheChannel"] = QPixmap("./resources/ui/terrain_channel.gif")
    ICONS["Terrain_Syria"] = QPixmap("./resources/ui/terrain_syria.gif")

    ICONS["Dawn"] = QPixmap("./resources/ui/conditions/timeofday/dawn.png")
    ICONS["Day"] = QPixmap("./resources/ui/conditions/timeofday/day.png")
    ICONS["Dusk"] = QPixmap("./resources/ui/conditions/timeofday/dusk.png")
    ICONS["Night"] = QPixmap("./resources/ui/conditions/timeofday/night.png")

    ICONS["Money"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/money_icon.png"
    )
    ICONS["PassTurn"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/hourglass.png"
    )
    ICONS["Proceed"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/proceed.png"
    )
    ICONS["Settings"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/settings.png"
    )
    ICONS["Statistics"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/statistics.png"
    )
    ICONS["Ordnance"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/ordnance_icon.png"
    )

    ICONS["Generator"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/generator.png"
    )
    ICONS["Missile"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/missile.png"
    )
    ICONS["Cheat"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/cheat.png")
    ICONS["Plugins"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/plugins.png"
    )
    ICONS["PluginsOptions"] = QPixmap(
        "./resources/ui/misc/" + get_theme_icons() + "/pluginsoptions.png"
    )

    ICONS["TaskCAS"] = QPixmap("./resources/ui/tasks/cas.png")
    ICONS["TaskCAP"] = QPixmap("./resources/ui/tasks/cap.png")
    ICONS["TaskSEAD"] = QPixmap("./resources/ui/tasks/sead.png")
    ICONS["TaskEmpty"] = QPixmap("./resources/ui/tasks/empty.png")

    """
    Weather Icons
    """
    ICONS["Weather_winds"] = QPixmap("./resources/ui/conditions/weather/winds.png")
    ICONS["Weather_day-clear"] = QPixmap(
        "./resources/ui/conditions/weather/day-clear.png"
    )
    ICONS["Weather_day-cloudy-fog"] = QPixmap(
        "./resources/ui/conditions/weather/day-cloudy-fog.png"
    )
    ICONS["Weather_day-fog"] = QPixmap("./resources/ui/conditions/weather/day-fog.png")
    ICONS["Weather_day-partly-cloudy"] = QPixmap(
        "./resources/ui/conditions/weather/day-partly-cloudy.png"
    )
    ICONS["Weather_day-rain"] = QPixmap(
        "./resources/ui/conditions/weather/day-rain.png"
    )
    ICONS["Weather_day-thunderstorm"] = QPixmap(
        "./resources/ui/conditions/weather/day-thunderstorm.png"
    )
    ICONS["Weather_day-totally-cloud"] = QPixmap(
        "./resources/ui/conditions/weather/day-totally-cloud.png"
    )
    ICONS["Weather_night-clear"] = QPixmap(
        "./resources/ui/conditions/weather/night-clear.png"
    )
    ICONS["Weather_night-cloudy-fog"] = QPixmap(
        "./resources/ui/conditions/weather/night-cloudy-fog.png"
    )
    ICONS["Weather_night-fog"] = QPixmap(
        "./resources/ui/conditions/weather/night-fog.png"
    )
    ICONS["Weather_night-partly-cloudy"] = QPixmap(
        "./resources/ui/conditions/weather/night-partly-cloudy.png"
    )
    ICONS["Weather_night-rain"] = QPixmap(
        "./resources/ui/conditions/weather/night-rain.png"
    )
    ICONS["Weather_night-thunderstorm"] = QPixmap(
        "./resources/ui/conditions/weather/night-thunderstorm.png"
    )
    ICONS["Weather_night-totally-cloud"] = QPixmap(
        "./resources/ui/conditions/weather/night-totally-cloud.png"
    )


EVENT_ICONS: Dict[str, QPixmap] = {}


def load_event_icons():
    for image in os.listdir("./resources/ui/events/"):
        if image.endswith(".PNG"):
            EVENT_ICONS[image[:-4]] = QPixmap(
                os.path.join("./resources/ui/events/", image)
            )


def load_aircraft_icons():
    for aircraft in os.listdir("./resources/ui/units/aircrafts/icons/"):
        if aircraft.endswith(".jpg"):
            AIRCRAFT_ICONS[aircraft[:-7]] = QPixmap(
                os.path.join("./resources/ui/units/aircrafts/icons/", aircraft)
            )
    AIRCRAFT_ICONS["F-16C_50"] = AIRCRAFT_ICONS["F-16C"]
    AIRCRAFT_ICONS["FA-18C_hornet"] = AIRCRAFT_ICONS["FA-18C"]
    AIRCRAFT_ICONS["A-10C_2"] = AIRCRAFT_ICONS["A-10C"]


def load_vehicle_icons():
    for vehicle in os.listdir("./resources/ui/units/vehicles/icons/"):
        if vehicle.endswith(".jpg"):
            VEHICLES_ICONS[vehicle[:-7]] = QPixmap(
                os.path.join("./resources/ui/units/vehicles/icons/", vehicle)
            )


def load_aircraft_banners():
    for aircraft in os.listdir("./resources/ui/units/aircrafts/banners/"):
        if aircraft.endswith(".jpg"):
            AIRCRAFT_BANNERS[aircraft[:-7]] = QPixmap(
                os.path.join("./resources/ui/units/aircrafts/banners/", aircraft)
            )


def load_vehicle_banners():
    for aircraft in os.listdir("./resources/ui/units/vehicles/banners/"):
        if aircraft.endswith(".jpg"):
            VEHICLE_BANNERS[aircraft[:-7]] = QPixmap(
                os.path.join("./resources/ui/units/vehicles/banners/", aircraft)
            )
