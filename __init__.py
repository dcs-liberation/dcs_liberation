#!/usr/bin/env python3
import sys

import theater.caucasus
import ui.window
import ui.mainmenu

from game.game import Game
from theater import start_generator
from userdata import persistency

from dcs.lua.parse import loads

with open("/Users/sp/Downloads/won_cap.log", "r") as f:
    s = f.read()
    print(loads(s))

#sys.exit(0)

game = persistency.restore_game()
if not game:
    theater = theater.caucasus.CaucasusTheater()
    start_generator.generate_initial(theater, "Russia")

    game = Game(theater=theater)

w = ui.window.Window()
m = ui.mainmenu.MainMenu(w, None, game)
m.display()

w.run()

