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

op = game.mission.CaptureOperation.playerless(m, theater.kutaisi, theater.senaki)
op.generate()

m.save("build/output.miz")
