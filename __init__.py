#!/usr/bin/env python3
import logging
import os
import re
import sys

import dcs

import ui.corruptedsavemenu
import ui.mainmenu
import ui.newgamemenu
import ui.window
from game.game import Game
from userdata import persistency, logging as logging_module

assert len(sys.argv) >= 3, "__init__.py should be started with two mandatory arguments: %UserProfile% location and application version"

persistency.setup(sys.argv[1])
dcs.planes.FlyingType.payload_dirs = [os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources\\payloads")]

VERSION_STRING = sys.argv[2]
logging_module.setup_version_string(VERSION_STRING)
logging.info("Using {} as userdata folder".format(persistency.base_path()))


def proceed_to_main_menu(game: Game):
    m = ui.mainmenu.MainMenu(w, None, game)
    m.display()


def is_version_compatible(save_version):
    current_version_components = re.split(r"[\._]", VERSION_STRING)
    save_version_components = re.split(r"[\._]", save_version)

    if "--ignore-save" in sys.argv:
        return False

    if current_version_components == save_version_components:
        return True

    if save_version in ["1.4_rc1", "1.4_rc2", "1.4_rc3", "1.4_rc4", "1.4_rc5", "1.4_rc6"]:
        return False

    if current_version_components[:2] == save_version_components[:2]:
        return True

    return False


w = ui.window.Window()

try:
    game = persistency.restore_game()
    if not game or not is_version_compatible(game.settings.version):
        new_game_menu = None  # type: NewGameMenu
        new_game_menu = ui.newgamemenu.NewGameMenu(w, w.start_new_game)
        new_game_menu.display()
    else:
        game.settings.version = VERSION_STRING
        proceed_to_main_menu(game)
except Exception as e:
    logging.exception(e)
    ui.corruptedsavemenu.CorruptedSaveMenu(w).display()

w.run()

