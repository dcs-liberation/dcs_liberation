#!/usr/bin/env python3

import dcs
import os

import gen
import theater.caucasus
import game.operation
import ui.window
import ui.mainmenu

from game.game import Game
from theater.controlpoint import *

from dcs.planes import *
from dcs.vehicles import *

m = dcs.Mission()
theater = theater.caucasus.CaucasusTheater()
theater.kutaisi.base.aircraft = {
    F_15C: 4,
    A_10C: 2,
}

g = Game(theater=theater)

w = ui.window.Window()
m = ui.mainmenu.MainMenu(g, w)

w.run()


"""
selected_cp = None  # type: ControlPoint
while True:
    ptr = 0

    print("Budget: {}m".format(g.budget))

    if selected_cp is None:
        print("Events:")
        for event in g.events:
            ptr += 1
            print("{}. {} {}".format(ptr, event.attacker != g.side and "!" or " ", event))

        print("Control Points:")
        controlpoints = g.theater.controlpoints
        controlpoints.sort(key=lambda x: x.captured)
        for cp in g.theater.controlpoints:
            ptr += 1
            print("{}. [{}{}] {}{}{}{}".format(
                ptr,
                cp.captured and "x" or " ",
                int(cp.base.readiness * 10),
                cp.name,
                "^" * cp.base.total_planes,
                "." * cp.base.total_armor,
                "*" * cp.base.total_aa))

        events_boundary = len(g.events)
        try:
            selected_idx = int(input(">").strip()) - 1
        except:
            continue

        if selected_idx == -1:
            g.pass_turn()
            continue
        if selected_idx < events_boundary:
            event = g.events[selected_idx]
        else:
            selected_cp = controlpoints[selected_idx - events_boundary]
    else:
        print("Units on the base: ")
        for unit, count in selected_cp.base.all_units:
            print("{} ({}) ".format(unit.name and unit.name or unit.id, count), end="")
        print("")

        try:
            selected_idx = int(input(">").strip()) - 1
        except:
            continue
        if selected_idx == -1:
            selected_cp = None

if not os.path.exists("./build"):
    os.mkdir("./build")

m.save("build/output.miz")
"""

