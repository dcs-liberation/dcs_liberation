#!/usr/bin/env python3
import os
import re
import sys
import dcs
import logging

import theater.caucasus
import theater.persiangulf
import theater.nevada

import ui.window
import ui.mainmenu
import ui.newgamemenu
import ui.corruptedsavemenu

from game.game import Game
from theater import start_generator
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

        def start_new_game(player_name: str, enemy_name: str, terrain: str, sams: bool, midgame: bool, multiplier: float):
            if terrain == "persiangulf":
                conflicttheater = theater.persiangulf.PersianGulfTheater()
            elif terrain == "nevada":
                conflicttheater = theater.nevada.NevadaTheater()
            else:
                conflicttheater = theater.caucasus.CaucasusTheater()

            if midgame:
                for i in range(0, int(len(conflicttheater.controlpoints) / 2)):
                    conflicttheater.controlpoints[i].captured = True

            start_generator.generate_inital_units(conflicttheater, enemy_name, sams, multiplier)
            start_generator.generate_groundobjects(conflicttheater)
            game = Game(player_name=player_name,
                        enemy_name=enemy_name,
                        theater=conflicttheater)
            game.budget = int(game.budget * multiplier)
            game.settings.multiplier = multiplier
            game.settings.sams = sams
            game.settings.version = VERSION_STRING

            if midgame:
                game.budget = game.budget * 4 * len(list(conflicttheater.conflicts()))

            proceed_to_main_menu(game)

        new_game_menu = ui.newgamemenu.NewGameMenu(w, start_new_game)
        new_game_menu.display()
    else:
        game.settings.version = VERSION_STRING
        proceed_to_main_menu(game)
except Exception as e:
    logging.exception(e)
    ui.corruptedsavemenu.CorruptedSaveMenu(w).display()

w.run()

