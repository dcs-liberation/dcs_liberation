import json
import logging
import os
from pathlib import Path
from shutil import copyfile

import dcs

from game import persistency

global __dcs_saved_game_directory
global __dcs_installation_directory
global __last_save_file


USER_PATH = Path(os.environ["LOCALAPPDATA"]) / "DCSLiberation"

PREFERENCES_PATH = USER_PATH / "liberation_preferences.json"


def init():
    global __dcs_saved_game_directory
    global __dcs_installation_directory
    global __last_save_file
    global __ignore_empty_install_directory

    if PREFERENCES_PATH.exists():
        try:
            logging.debug("Loading Liberation preferences from %s", PREFERENCES_PATH)
            with PREFERENCES_PATH.open() as prefs:
                pref_data = json.load(prefs)
            __dcs_saved_game_directory = pref_data["saved_game_dir"]
            __dcs_installation_directory = pref_data["dcs_install_dir"]
            __last_save_file = pref_data.get("last_save_file", "")
            __ignore_empty_install_directory = pref_data.get(
                "ignore_empty_install_directory", False
            )
            is_first_start = False
        except KeyError:
            __dcs_saved_game_directory = ""
            __dcs_installation_directory = ""
            __last_save_file = ""
            __ignore_empty_install_directory = False
            is_first_start = True
    else:
        __last_save_file = ""
        __ignore_empty_install_directory = False
        try:
            __dcs_saved_game_directory = (
                dcs.installation.get_dcs_saved_games_directory()
            )
            if os.path.exists(__dcs_saved_game_directory + ".openbeta"):
                __dcs_saved_game_directory = (
                    dcs.installation.get_dcs_saved_games_directory() + ".openbeta"
                )
        except:
            __dcs_saved_game_directory = ""
        try:
            __dcs_installation_directory = dcs.installation.get_dcs_install_directory()
        except:
            __dcs_installation_directory = ""

        is_first_start = True
    persistency.setup(__dcs_saved_game_directory)
    return is_first_start


def setup(saved_game_dir, install_dir):
    global __dcs_saved_game_directory
    global __dcs_installation_directory
    __dcs_saved_game_directory = saved_game_dir
    __dcs_installation_directory = install_dir
    persistency.setup(__dcs_saved_game_directory)


def setup_last_save_file(last_save_file):
    global __last_save_file
    __last_save_file = last_save_file


def save_config():
    global __dcs_saved_game_directory
    global __dcs_installation_directory
    global __last_save_file
    global __ignore_empty_install_directory
    pref_data = {
        "saved_game_dir": __dcs_saved_game_directory,
        "dcs_install_dir": __dcs_installation_directory,
        "last_save_file": __last_save_file,
        "ignore_empty_install_directory": __ignore_empty_install_directory,
    }
    PREFERENCES_PATH.parent.mkdir(exist_ok=True, parents=True)
    with PREFERENCES_PATH.open("w") as prefs:
        json.dump(pref_data, prefs, indent="  ")


def get_dcs_install_directory():
    global __dcs_installation_directory
    return __dcs_installation_directory


def get_saved_game_dir():
    global __dcs_saved_game_directory
    return __dcs_saved_game_directory


def ignore_empty_install_directory():
    global __ignore_empty_install_directory
    return __ignore_empty_install_directory


def set_ignore_empty_install_directory(value: bool):
    global __ignore_empty_install_directory
    __ignore_empty_install_directory = value


def get_last_save_file():
    global __last_save_file
    print(__last_save_file)
    if os.path.exists(__last_save_file):
        return __last_save_file
    else:
        return None


def replace_mission_scripting_file():
    install_dir = get_dcs_install_directory()
    mission_scripting_path = os.path.join(
        install_dir, "Scripts", "MissionScripting.lua"
    )
    liberation_scripting_path = "./resources/scripts/MissionScripting.lua"
    backup_scripting_path = "./resources/scripts/MissionScripting.original.lua"
    if install_dir != "" and os.path.isfile(mission_scripting_path):
        with open(mission_scripting_path, "r") as ms:
            current_file_content = ms.read()
        with open(liberation_scripting_path, "r") as libe_ms:
            liberation_file_content = libe_ms.read()

        # Save original file
        if current_file_content != liberation_file_content:
            copyfile(mission_scripting_path, backup_scripting_path)

        # Replace DCS file
        copyfile(liberation_scripting_path, mission_scripting_path)


def restore_original_mission_scripting():
    install_dir = get_dcs_install_directory()
    mission_scripting_path = os.path.join(
        install_dir, "Scripts", "MissionScripting.lua"
    )
    backup_scripting_path = "./resources/scripts/MissionScripting.original.lua"

    if (
        install_dir != ""
        and os.path.isfile(backup_scripting_path)
        and os.path.isfile(mission_scripting_path)
    ):
        copyfile(backup_scripting_path, mission_scripting_path)
