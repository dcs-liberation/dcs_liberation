#!/usr/bin/env python3
import os
import sys
import dcs

import theater.caucasus
import theater.persiangulf
import theater.nevada

import ui.window
import ui.mainmenu
import ui.newgamemenu
import ui.corruptedsavemenu

from game.game import Game
from theater import start_generator
from userdata import persistency


"""
from dcs.lua.parse import *
a = loads(open("build/mission", "r").read())
b = loads(open("build/mission_workin.lua", "r").read())


def get(a, k):
    b = a
    for x in k.strip().split(" "):
        if isinstance(a, dict):
            y = a
            a = a.get(x, None)
            if a is None:
                try:
                    a = y.get(int(x), None)
                except:
                    pass
        else:
            break
    if a is None:
        pass
    return a

def cycle(kk, ref, v):
    if isinstance(v, dict):
        for k, v in v.items():
            cycle(kk + " " + str(k), ref, v)
    elif isinstance(v, list):
        for i, v in enumerate(v):
            cycle(kk + " " + str(i), ref, v)
    else:
        if get(ref, kk) != v:
            print(kk, v)
            print(get(ref, kk))

cycle("", a, b)
sys.exit(0)
"""

persistency.setup(sys.argv[1])
dcs.planes.FlyingType.payload_dirs.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources\\payloads"))


def proceed_to_main_menu(game: Game):
    m = ui.mainmenu.MainMenu(w, None, game)
    m.display()


w = ui.window.Window()
try:
    game = persistency.restore_game()
    if not game:
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

            start_generator.generate_initial(conflicttheater, enemy_name, sams, multiplier)
            game = Game(player_name=player_name,
                        enemy_name=enemy_name,
                        theater=conflicttheater)
            game.budget = int(game.budget * multiplier)
            game.settings.multiplier = multiplier
            game.settings.sams = sams

            if midgame:
                game.budget = game.budget * 4 * len(list(conflicttheater.conflicts()))

            proceed_to_main_menu(game)

        new_game_menu = ui.newgamemenu.NewGameMenu(w, start_new_game)
        new_game_menu.display()
    else:
        proceed_to_main_menu(game)
except Exception as e:
    ui.corruptedsavemenu.CorruptedSaveMenu(w).display()

w.run()

