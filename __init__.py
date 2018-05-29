#!/usr/bin/env python3

import dcs
import os

import gen
import theater.caucasus
import game.mission

from dcs.planes import *
from dcs.vehicles import *

m = dcs.Mission()

theater = theater.caucasus.CaucasusTheater()

theater.kutaisi.base.aircraft = {
    A_10C: 4,
    F_15C: 4,
}

theater.kutaisi.base.armor = {
    Armor.MBT_M1A2_Abrams: 4,
}

theater.senaki.base.aircraft = {
    MiG_21Bis: 8,
}

theater.senaki.base.armor = {
    Armor.MBT_T_55: 6,
}

theater.senaki.base.aa = {
    AirDefence.AAA_ZU_23_on_Ural_375: 2,
}

"""
op = game.mission.CaptureOperation(m, m.country("USA"), m.country("Russia"), theater.senaki, theater.batumi, {A_10C: 2}, {F_15C: 2}, {Armor.MBT_M1A2_Abrams: 4}, {Su_27: 4}, {Armor.MBT_T_55: 4}, {})
op.generate()
"""

op = game.mission.InterceptOperation(m,
                                     m.country("USA"),
                                     m.country("Russia"),
                                     theater.batumi,
                                     m.terrain.batumi(),
                                     escort={Su_27: 2},
                                     transport={An_26B: 2},
                                     interceptors={M_2000C: 2})
op.generate()

if not os.path.exists("./build"):
    os.mkdir("./build")

m.save("build/output.miz")
