import typing
import dcs

import globals

from dcs.vehicles import *
from dcs.unitgroup import *
from dcs.planes import *
from dcs.task import *
from dcs.unittype import *

PRICES = {
    # planes

    Su_25T: 10,
    A_10A: 15,
    A_10C: 20,

    Su_27: 20,
    Su_33: 23,
    F_15C: 25,
    M_2000C: 17,

    MiG_15bis: 10,
    MiG_21Bis: 13,

    # armor

    Armor.MBT_T_55: 18,
    Armor.MBT_T_80U: 20,
    Armor.MBT_T_90: 22,

    Armor.MBT_M60A3_Patton: 15,
    Armor.MBT_M1A2_Abrams: 20,

    Armor.ATGM_M1134_Stryker: 12,
    Armor.APC_BTR_80: 10,
}

UNIT_BY_TASK = {
    FighterSweep: [Su_27, Su_33, Su_25, F_15C, MiG_15bis, MiG_21Bis, MiG_29A, ],
    CAS: [Su_25T, A_10A, A_10C, ],
    CAP: [Armor.MBT_T_90, Armor.MBT_T_80U, Armor.MBT_T_55, Armor.MBT_M1A2_Abrams, Armor.MBT_M60A3_Patton, Armor.ATGM_M1134_Stryker, Armor.APC_BTR_80, ]
}
