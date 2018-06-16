#!/usr/bin/env python3
import os
import dcs

import theater.caucasus
import theater.persiangulf
import theater.nevada

import ui.window
import ui.mainmenu
import ui.newgamemenu

from game.game import Game
from theater import start_generator
from userdata import persistency

dcs.planes.FlyingType.payload_dirs.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources\\payloads"))


def proceed_to_main_menu(game: Game):
    m = ui.mainmenu.MainMenu(w, None, game)
    m.display()


w = ui.window.Window()
game = persistency.restore_game()
if not game:
    new_game_menu = None  # type: NewGameMenu

    def start_new_game(player_name: str, enemy_name: str, terrain: str, sams: bool):
        if terrain == "persiangulf":
            conflicttheater = theater.persiangulf.PersianGulfTheater()
        elif terrain == "nevada":
            conflicttheater = theater.nevada.NevadaTheater()
        else:
            conflicttheater = theater.caucasus.CaucasusTheater()

        start_generator.generate_initial(conflicttheater, enemy_name, sams)
        proceed_to_main_menu(Game(player_name=player_name,
                                  enemy_name=enemy_name,
                                  theater=conflicttheater))

    new_game_menu = ui.newgamemenu.NewGameMenu(w, start_new_game)
    new_game_menu.display()
else:
    proceed_to_main_menu(game)

w.run()

