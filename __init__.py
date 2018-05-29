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

op = game.mission.InterceptOperation(
    mission=m,
    attacker=m.country("USA"),
    defender=m.country("Russia"),
    destination=theater.batumi,
    destination_port=m.terrain.batumi(),
    escort={Su_27: 2},
    transport={An_26B: 2},
    interceptors={M_2000C: 2}
)

op = game.mission.GroundInterceptOperation(
    mission=m,
    attacker=m.country("USA"),
    defender=m.country("Russia"),
    position=m.terrain.batumi().position,
    target={Unarmed.Transport_ZIL_4331: 10},
    strikegroup={A_10C: 2}
)

op = game.mission.CaptureOperation(
    mission=m,
    attacker=m.country("USA"),
    defender=m.country("Russia"),
    from_cp=theater.senaki,
    to_cp=theater.batumi,
    cas={A_10C: 2},
    escort={F_15C: 2},
    attack={Armor.MBT_M1A2_Abrams: 4},
    intercept={Su_27: 4},
    defense={Armor.MBT_T_55: 4},
    aa={AirDefence.AAA_ZU_23_Insurgent_on_Ural_375: 3})
op.generate()

if not os.path.exists("./build"):
    os.mkdir("./build")

m.save("build/output.miz")
