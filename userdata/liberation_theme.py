import json
import os
from shutil import copyfile

import dcs
import qt_ui.uiconstants as CONST
from userdata import persistency

global __theme_index
global __theme_name
global __theme_file
global __theme_icons

THEME_PREFERENCES_FILE_PATH = "liberation_theme.json"

DEFAULT_THEME_INDEX = 0


def init():
    global __theme_index

    __theme_index = DEFAULT_THEME_INDEX
    print("init setting theme index to " + str(__theme_index))

    if os.path.isfile(THEME_PREFERENCES_FILE_PATH):
        try:
            with(open(THEME_PREFERENCES_FILE_PATH)) as prefs:
                pref_data = json.loads(prefs.read())
                __theme_index = pref_data["theme_index"]
                print(__theme_index)
                set_theme_index(__theme_index)
                set_theme_file()
                print("file setting theme index to " + str(__theme_index))
        except:
            set_theme_index(DEFAULT_THEME_INDEX)
            print("except setting theme index to " + str(__theme_index))
    else:
        set_theme_index(DEFAULT_THEME_INDEX)
        print("else setting theme index to " + str(__theme_index))


def set_theme_index(x):
    global __theme_index
    __theme_index = x


def get_theme_index():
    global __theme_index
    return __theme_index


# get or set current theme index number
def set_theme_name(x):
    global __theme_name
    __theme_name = str(x)


def get_theme_name():
    global __theme_name
    return __theme_name


# get or set current theme icons based on the theme name
def set_theme_icons():
    global __theme_icons
    __theme_icons = CONST.THEMES[get_theme_name()]["themeIcons"]


def get_theme_icons():
    theme_icons = CONST.THEMES[get_theme_index()]['themeIcons']
    return str(theme_icons)


# get or set theme from json file
def set_theme_file():
    theme_file = CONST.THEMES[get_theme_index()]['themeFile']
    global __theme_file
    __theme_file = theme_file

    pref_data = {
        "theme_index": get_theme_index()
    }
    with(open(THEME_PREFERENCES_FILE_PATH, "w")) as prefs:
        prefs.write(json.dumps(pref_data))


def get_theme_file():
    global __theme_file
    return str(__theme_file)
