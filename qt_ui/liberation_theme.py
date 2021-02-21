import json
import logging
import os
from typing import Dict

global __theme_index

THEME_PREFERENCES_FILE_PATH = "liberation_theme.json"

DEFAULT_THEME_INDEX = 1


# new themes can be added here
THEMES: Dict[int, Dict[str, str]] = {
    0: {
        "themeName": "Vanilla",
        "themeFile": "windows-style.css",
        "themeIcons": "medium",
    },
    1: {
        "themeName": "DCS World",
        "themeFile": "style-dcs.css",
        "themeIcons": "light",
    },
}


def init():
    global __theme_index

    __theme_index = DEFAULT_THEME_INDEX

    if os.path.isfile(THEME_PREFERENCES_FILE_PATH):
        try:
            with (open(THEME_PREFERENCES_FILE_PATH)) as prefs:
                pref_data = json.loads(prefs.read())
                __theme_index = pref_data["theme_index"]
                set_theme_index(__theme_index)
                save_theme_config()
        except:
            # is this necessary?
            set_theme_index(DEFAULT_THEME_INDEX)
            logging.exception("Unable to change theme")
    else:
        # is this necessary?
        set_theme_index(DEFAULT_THEME_INDEX)
        logging.error(
            f"Using default theme because {THEME_PREFERENCES_FILE_PATH} "
            "does not exist"
        )


# set theme index then use save_theme_config to save to file
def set_theme_index(x):
    global __theme_index
    __theme_index = x


# get theme index to reference other theme properties(themeName, themeFile, themeIcons)
def get_theme_index():
    global __theme_index
    return __theme_index


# get theme name based on current index
def get_theme_name():
    theme_name = THEMES[get_theme_index()]["themeName"]
    return theme_name


# get theme icon sub-folder name based on current index
def get_theme_icons():
    theme_icons = THEMES[get_theme_index()]["themeIcons"]
    return str(theme_icons)


# get theme stylesheet css based on current index
def get_theme_css_file():
    theme_file = THEMES[get_theme_index()]["themeFile"]
    return str(theme_file)


# save current theme index to json file
def save_theme_config():
    pref_data = {"theme_index": get_theme_index()}
    with (open(THEME_PREFERENCES_FILE_PATH, "w")) as prefs:
        prefs.write(json.dumps(pref_data))
