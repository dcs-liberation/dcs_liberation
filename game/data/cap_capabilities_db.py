from dcs.planes import *
from pydcs_extensions.a4ec.a4ec import A_4E_C

"""
This list contains the aircraft that do not use the guns as the last resort weapons, but as a main weapon
They'll RTB when they don't have gun ammo left
"""
GUNFIGHTERS = [

    # Cold War
    MiG_15bis,
    MiG_19P,
    MiG_21Bis,
    F_86F_Sabre,
    A_4E_C,
    F_5E_3,

    # Trainers
    C_101CC,
    L_39ZA,

    # WW2
    P_51D_30_NA,
    P_51D,
    P_47D_30,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
    I_16,

]