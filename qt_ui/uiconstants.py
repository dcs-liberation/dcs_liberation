import os
from typing import Dict

from PySide2.QtGui import QColor, QFont, QPixmap

from game.theater.theatergroundobject import CATEGORY_MAP
from .liberation_theme import get_theme_icons


URLS : Dict[str, str] = {
    "Manual": "https://github.com/khopa/dcs_liberation/wiki",
    "Repository": "https://github.com/khopa/dcs_liberation",
    "ForumThread": "https://forums.eagle.ru/showthread.php?t=214834",
    "Issues": "https://github.com/khopa/dcs_liberation/issues"
}

LABELS_OPTIONS = ["Full", "Abbreviated", "Dot Only", "Off"]
SKILL_OPTIONS = ["Average", "Good", "High", "Excellent"]

FONT_SIZE = 8
FONT_NAME = "Arial"
# FONT = QFont("Arial", 12, weight=5, italic=True)
FONT_PRIMARY = QFont(FONT_NAME, FONT_SIZE, weight=5, italic=False)
FONT_PRIMARY_I = QFont(FONT_NAME, FONT_SIZE, weight=5, italic=True)
FONT_PRIMARY_B = QFont(FONT_NAME, FONT_SIZE, weight=75, italic=False)
FONT_MAP = QFont(FONT_NAME, 10, weight=75, italic=False)

COLORS: Dict[str, QColor] = {
    "white": QColor(255, 255, 255),
    "white_transparent": QColor(255, 255, 255, 35),

    "light_red": QColor(231, 92, 83, 90),
    "red": QColor(200, 80, 80),
    "dark_red": QColor(140, 20, 20),
    "red_transparent": QColor(227, 32, 0, 20),
    "transparent": QColor(255, 255, 255, 0),

    "light_blue": QColor(105, 182, 240, 90),
    "blue": QColor(0, 132, 255),
    "dark_blue": QColor(45, 62, 80),
    "sea_blue": QColor(52, 68, 85),
    "sea_blue_transparent": QColor(52, 68, 85, 150),
    "blue_transparent": QColor(0, 132, 255, 20),

    "purple": QColor(187, 137, 255),
    "yellow": QColor(238, 225, 123),

    "bright_red": QColor(150, 80, 80),
    "super_red": QColor(227, 32, 0),

    "green": QColor(128, 186, 128),
    "light_green": QColor(223, 255, 173),
    "light_green_transparent": QColor(180, 255, 140, 50),
    "bright_green": QColor(64, 200, 64),

    "black": QColor(0, 0, 0),
    "black_transparent": QColor(0, 0, 0, 5),

    "orange": QColor(254, 125, 10),

    "night_overlay": QColor(12, 20, 69),
    "dawn_dust_overlay": QColor(46, 38, 85),

    "grey": QColor(150, 150, 150),
    "grey_transparent": QColor(150, 150, 150, 150),
    "dark_grey": QColor(75, 75, 75),
    "dark_grey_transparent": QColor(75, 75, 75, 150),
    "dark_dark_grey": QColor(48, 48, 48),
    "dark_dark_grey_transparent": QColor(48, 48, 48, 150),

}

CP_SIZE = 12

AIRCRAFT_ICONS: Dict[str, QPixmap] = {}
VEHICLES_ICONS: Dict[str, QPixmap] = {}
ICONS: Dict[str, QPixmap] = {}

def load_icons():

    ICONS["New"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/new.png")
    ICONS["Open"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/open.png")
    ICONS["Save"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/save.png")
    ICONS["Discord"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/discord.png")
    ICONS["Github"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/github.png")


    ICONS["Control Points"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/circle.png")
    ICONS["Ground Objects"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/industry.png")
    ICONS["Lines"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/arrows-h.png")
    ICONS["Waypoint Information"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/info.png")
    ICONS["Map Polygon Debug Mode"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/map.png")
    ICONS["Ally SAM Threat Range"] = QPixmap("./resources/ui/misc/blue-sam.png")
    ICONS["Enemy SAM Threat Range"] = QPixmap("./resources/ui/misc/red-sam.png")
    ICONS["SAM Detection Range"] = QPixmap("./resources/ui/misc/detection-sam.png")
    ICONS["Display Culling Zones"] = QPixmap("./resources/ui/misc/" + get_theme_icons() + "/eraser.png")
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

    ICONS["Money"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/money_icon.png")
    ICONS["PassTurn"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/hourglass.png")
    ICONS["Proceed"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/proceed.png")
    ICONS["Settings"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/settings.png")
    ICONS["Statistics"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/statistics.png")
    ICONS["Ordnance"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/ordnance_icon.png")

    ICONS["target"] = QPixmap("./resources/ui/ground_assets/target.png")
    ICONS["cleared"] = QPixmap("./resources/ui/ground_assets/cleared.png")
    for category in CATEGORY_MAP.keys():
        ICONS[category] = QPixmap("./resources/ui/ground_assets/" + category + ".png")
        ICONS[category + "_blue"] = QPixmap("./resources/ui/ground_assets/" + category + "_blue.png")
    ICONS["destroyed"] = QPixmap("./resources/ui/ground_assets/destroyed.png")
    ICONS["ship"] = QPixmap("./resources/ui/ground_assets/ship.png")
    ICONS["ship_blue"] = QPixmap("./resources/ui/ground_assets/ship_blue.png")
    ICONS["missile"] = QPixmap("./resources/ui/ground_assets/missile.png")
    ICONS["missile_blue"] = QPixmap("./resources/ui/ground_assets/missile_blue.png")

    ICONS["Generator"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/generator.png")
    ICONS["Missile"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/missile.png")
    ICONS["Cheat"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/cheat.png")
    ICONS["Plugins"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/plugins.png")
    ICONS["PluginsOptions"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/pluginsoptions.png")

    ICONS["TaskCAS"] = QPixmap("./resources/ui/tasks/cas.png")
    ICONS["TaskCAP"] = QPixmap("./resources/ui/tasks/cap.png")
    ICONS["TaskSEAD"] = QPixmap("./resources/ui/tasks/sead.png")
    ICONS["TaskEmpty"] = QPixmap("./resources/ui/tasks/empty.png")

    """
    Weather Icons
    """
    ICONS["Weather_winds"] = QPixmap("./resources/ui/conditions/weather/winds.png")
    ICONS["Weather_day-clear"] = QPixmap("./resources/ui/conditions/weather/day-clear.png")
    ICONS["Weather_day-cloudy-fog"] = QPixmap("./resources/ui/conditions/weather/day-cloudy-fog.png")
    ICONS["Weather_day-fog"] = QPixmap("./resources/ui/conditions/weather/day-fog.png")
    ICONS["Weather_day-partly-cloudy"] = QPixmap("./resources/ui/conditions/weather/day-partly-cloudy.png")
    ICONS["Weather_day-rain"] = QPixmap("./resources/ui/conditions/weather/day-rain.png")
    ICONS["Weather_day-thunderstorm"] = QPixmap("./resources/ui/conditions/weather/day-thunderstorm.png")
    ICONS["Weather_day-totally-cloud"] = QPixmap("./resources/ui/conditions/weather/day-totally-cloud.png")
    ICONS["Weather_night-clear"] = QPixmap("./resources/ui/conditions/weather/night-clear.png")
    ICONS["Weather_night-cloudy-fog"] = QPixmap("./resources/ui/conditions/weather/night-cloudy-fog.png")
    ICONS["Weather_night-fog"] = QPixmap("./resources/ui/conditions/weather/night-fog.png")
    ICONS["Weather_night-partly-cloudy"] = QPixmap("./resources/ui/conditions/weather/night-partly-cloudy.png")
    ICONS["Weather_night-rain"] = QPixmap("./resources/ui/conditions/weather/night-rain.png")
    ICONS["Weather_night-thunderstorm"] = QPixmap("./resources/ui/conditions/weather/night-thunderstorm.png")
    ICONS["Weather_night-totally-cloud"] = QPixmap("./resources/ui/conditions/weather/night-totally-cloud.png")


EVENT_ICONS: Dict[str, QPixmap] = {}


def load_event_icons():
    for image in os.listdir("./resources/ui/events/"):
        if image.endswith(".PNG"):
            EVENT_ICONS[image[:-4]] = QPixmap(os.path.join("./resources/ui/events/", image))

def load_aircraft_icons():
    for aircraft in os.listdir("./resources/ui/units/aircrafts/"):
        if aircraft.endswith(".jpg"):
            AIRCRAFT_ICONS[aircraft[:-7]] = QPixmap(os.path.join("./resources/ui/units/aircrafts/", aircraft))
    AIRCRAFT_ICONS["F-16C_50"] = AIRCRAFT_ICONS["F-16C"]
    AIRCRAFT_ICONS["FA-18C_hornet"] = AIRCRAFT_ICONS["FA-18C"]
    AIRCRAFT_ICONS["A-10C_2"] = AIRCRAFT_ICONS["A-10C"]


def load_vehicle_icons():
    for vehicle in os.listdir("./resources/ui/units/vehicles/"):
        if vehicle.endswith(".jpg"):
            VEHICLES_ICONS[vehicle[:-7]] = QPixmap(os.path.join("./resources/ui/units/vehicles/", vehicle))
