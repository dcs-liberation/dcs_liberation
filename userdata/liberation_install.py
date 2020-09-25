import json
import os
from shutil import copyfile

import dcs

from userdata import persistency

global __dcs_saved_game_directory
global __dcs_installation_directory

PREFERENCES_FILE_PATH = "liberation_preferences.json"

def init():
    global __dcs_saved_game_directory
    global __dcs_installation_directory

    if os.path.isfile(PREFERENCES_FILE_PATH):
        try:
            with(open(PREFERENCES_FILE_PATH)) as prefs:
                pref_data = json.loads(prefs.read())
                __dcs_saved_game_directory = pref_data["saved_game_dir"]
                __dcs_installation_directory = pref_data["dcs_install_dir"]
            is_first_start = False
        except:
            __dcs_saved_game_directory = ""
            __dcs_installation_directory = ""
            is_first_start = True
    else:
        try:
            __dcs_saved_game_directory = dcs.installation.get_dcs_saved_games_directory()
            if os.path.exists(__dcs_saved_game_directory + ".openbeta"):
                __dcs_saved_game_directory = dcs.installation.get_dcs_saved_games_directory() + ".openbeta"
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


def save_config():
    global __dcs_saved_game_directory
    global __dcs_installation_directory
    pref_data = {"saved_game_dir": __dcs_saved_game_directory,
                 "dcs_install_dir": __dcs_installation_directory}
    with(open(PREFERENCES_FILE_PATH, "w")) as prefs:
        prefs.write(json.dumps(pref_data))


def get_dcs_install_directory():
    global __dcs_installation_directory
    return __dcs_installation_directory


def get_saved_game_dir():
    global __dcs_saved_game_directory
    return __dcs_saved_game_directory


def replace_mission_scripting_file():
    install_dir = get_dcs_install_directory()
    mission_scripting_path = os.path.join(install_dir, "Scripts", "MissionScripting.lua")
    liberation_scripting_path = "./resources/scripts/MissionScripting.lua"
    backup_scripting_path = "./resources/scripts/MissionScripting.original.lua"
    if os.path.isfile(mission_scripting_path):
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
    mission_scripting_path = os.path.join(install_dir, "Scripts", "MissionScripting.lua")
    backup_scripting_path = "./resources/scripts/MissionScripting.original.lua"

    if os.path.isfile(backup_scripting_path) and os.path.isfile(mission_scripting_path):
        copyfile(backup_scripting_path, mission_scripting_path)

