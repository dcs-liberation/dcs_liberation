# URL for UI links
import os
from typing import Dict

from PySide2.QtGui import QColor, QFont, QPixmap

from game.event import UnitsDeliveryEvent, FrontlineAttackEvent
from theater.theatergroundobject import CATEGORY_MAP
from userdata.liberation_theme import get_theme_icons

VERSION_STRING = "2.1.3"

URLS : Dict[str, str] = {
    "Manual": "https://github.com/khopa/dcs_liberation/wiki",
    "Repository": "https://github.com/khopa/dcs_liberation",
    "ForumThread": "https://forums.eagle.ru/showthread.php?t=214834",
    "Issues": "https://github.com/khopa/dcs_liberation/issues",
    "VEAFForum": "https://community.veaf.org/",
    "VEAFScriptsDoc": "https://tinyurl.com/veaf-ot"
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

# new themes can be added here
THEMES: Dict[int, Dict[str, str]] = {
    0: {'themeName': 'Vanilla',
        'themeFile': 'windows-style.css',
        'themeIcons': 'medium',
        },

    1: {'themeName': 'DCS World',
        'themeFile': 'style-dcs.css',
        'themeIcons': 'light',
        },

}

COLORS: Dict[str, QColor] = {
    "white": QColor(255, 255, 255),
    "white_transparent": QColor(255, 255, 255, 35),
    "grey_transparent": QColor(150, 150, 150, 30),

    "red": QColor(200, 80, 80),
    "dark_red": QColor(140, 20, 20),
    "red_transparent": QColor(227, 32, 0, 20),

    "blue": QColor(0, 132, 255),
    "dark_blue": QColor(45, 62, 80),
    "blue_transparent": QColor(0, 132, 255, 20),

    "bright_red": QColor(150, 80, 80),
    "super_red": QColor(227, 32, 0),

    "green": QColor(128, 186, 128),
    "bright_green": QColor(64, 200, 64),

    "black": QColor(0, 0, 0),
    "black_transparent": QColor(0, 0, 0, 5),

    "orange": QColor(254, 125, 10),

    "night_overlay": QColor(12, 20, 69),
    "dawn_dust_overlay": QColor(46, 38, 85),

}

CP_SIZE = 12

AIRCRAFT_ICONS: Dict[str, QPixmap] = {}
VEHICLES_ICONS: Dict[str, QPixmap] = {}
ICONS: Dict[str, QPixmap] = {}

def load_icons():

    ICONS["New"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/new.png")
    ICONS["Open"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/open.png")
    ICONS["Save"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/save.png")
    ICONS["Hangar"] = QPixmap("./resources/ui/misc/hangar.png")

    ICONS["Terrain_Caucasus"] = QPixmap("./resources/ui/terrain_caucasus.gif")
    ICONS["Terrain_Persian_Gulf"] = QPixmap("./resources/ui/terrain_pg.gif")
    ICONS["Terrain_Nevada"] = QPixmap("./resources/ui/terrain_nevada.gif")
    ICONS["Terrain_Normandy"] = QPixmap("./resources/ui/terrain_normandy.gif")
    ICONS["Terrain_Channel"] = QPixmap("./resources/ui/terrain_channel.gif")
    ICONS["Terrain_Syria"] = QPixmap("./resources/ui/terrain_syria.gif")

    ICONS["Dawn"] = QPixmap("./resources/ui/daytime/dawn.png")
    ICONS["Day"] = QPixmap("./resources/ui/daytime/day.png")
    ICONS["Dusk"] = QPixmap("./resources/ui/daytime/dusk.png")
    ICONS["Night"] = QPixmap("./resources/ui/daytime/night.png")

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

    ICONS["Generator"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/generator.png")
    ICONS["Missile"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/missile.png")
    ICONS["Cheat"] = QPixmap("./resources/ui/misc/"+get_theme_icons()+"/cheat.png")

    ICONS["TaskCAS"] = QPixmap("./resources/ui/tasks/cas.png")
    ICONS["TaskCAP"] = QPixmap("./resources/ui/tasks/cap.png")
    ICONS["TaskSEAD"] = QPixmap("./resources/ui/tasks/sead.png")
    ICONS["TaskEmpty"] = QPixmap("./resources/ui/tasks/empty.png")


EVENT_ICONS: Dict[str, QPixmap] = {}


def load_event_icons():
    for image in os.listdir("./resources/ui/events/"):
        print(image)
        if image.endswith(".PNG"):
            EVENT_ICONS[image[:-4]] = QPixmap(os.path.join("./resources/ui/events/", image))

def load_aircraft_icons():
    for aircraft in os.listdir("./resources/ui/units/aircrafts/"):
        print(aircraft)
        if aircraft.endswith(".jpg"):
            print(aircraft[:-7] + " : " + os.path.join("./resources/ui/units/aircrafts/", aircraft) + " ")
            AIRCRAFT_ICONS[aircraft[:-7]] = QPixmap(os.path.join("./resources/ui/units/aircrafts/", aircraft))
    AIRCRAFT_ICONS["F-16C_50"] = AIRCRAFT_ICONS["F-16C"]
    AIRCRAFT_ICONS["FA-18C_hornet"] = AIRCRAFT_ICONS["FA-18C"]
    AIRCRAFT_ICONS["A-10C_2"] = AIRCRAFT_ICONS["A-10C"]


def load_vehicle_icons():
    for vehicle in os.listdir("./resources/ui/units/vehicles/"):
        print(vehicle)
        if vehicle.endswith(".jpg"):
            print(vehicle[:-7] + " : " + os.path.join("./resources/ui/units/vehicles/", vehicle) + " ")
            VEHICLES_ICONS[vehicle[:-7]] = QPixmap(os.path.join("./resources/ui/units/vehicles/", vehicle))
