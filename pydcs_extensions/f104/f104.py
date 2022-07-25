from typing import Set

from dcs import task
from dcs.liveries_scanner import Liveries
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF104:
    LAU_115C_2_AIM_9L = {
        "clsid": "{VSN_F104_LAU115C_AIM9L}",
        "name": "LAU-115C 2*AIM-9L",
        "weight": 332,
    }
    LAU_115C_2_AIM_9P = {
        "clsid": "{VSN_F104_LAU115C_AIM9P}",
        "name": "LAU-115C 2*AIM-9P",
        "weight": 332,
    }
    VSN_F104G_L_PTB = {"clsid": "VSN_F104G_L_PTB", "name": "500L Tank L", "weight": 632}
    VSN_F104G_L_PTB_ = {
        "clsid": "VSN_F104G_L_PTB",
        "name": "500L Tank L",
        "weight": 632,
    }
    VSN_F104G_L_PTB__ = {
        "clsid": "VSN_F104G_L_PTB",
        "name": "500L Tank L",
        "weight": 632,
    }
    VSN_F104G_PTB = {"clsid": "VSN_F104G_PTB", "name": "500L Tank", "weight": 632}
    VSN_F104G_PTB_ = {"clsid": "VSN_F104G_PTB", "name": "500L Tank", "weight": 632}
    VSN_F104G_PTB__ = {"clsid": "VSN_F104G_PTB", "name": "500L Tank", "weight": 632}
    VSN_F104G_R_PTB = {"clsid": "VSN_F104G_R_PTB", "name": "500L Tank R", "weight": 632}
    VSN_F104G_R_PTB_ = {
        "clsid": "VSN_F104G_R_PTB",
        "name": "500L Tank R",
        "weight": 632,
    }
    VSN_F104G_R_PTB__ = {
        "clsid": "VSN_F104G_R_PTB",
        "name": "500L Tank R",
        "weight": 632,
    }


inject_weapons(WeaponsF104)


@planemod
class VSN_F104C(PlaneType):
    id = "VSN_F104C"
    flyable = True
    height = 4.09
    width = 6.36
    length = 16.66
    fuel_max = 2641
    max_speed = 2336.4
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F104C"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        LAU_138_AIM_9L = (2, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (2, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        VSN_F104G_L_PTB = (2, WeaponsF104.VSN_F104G_L_PTB)

    class Pylon4:
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            4,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            4,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            4,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (4, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            4,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (4, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD,
        )
        _2_Mk_81___ = (4, Weapons._2_Mk_81___)
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        Kormoran___ASM = (4, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (4, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB = (4, WeaponsF104.VSN_F104G_PTB)

    class Pylon6:
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            6,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_105_2_AIM_9P5 = (6, Weapons.LAU_105_2_AIM_9P5)
        LAU_115C_2_AIM_9L = (6, WeaponsF104.LAU_115C_2_AIM_9L)
        LAU_115C_2_AIM_9P = (6, WeaponsF104.LAU_115C_2_AIM_9P)

    class Pylon8:
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            8,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            8,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            8,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (8, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            8,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (8, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (8, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            8,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            8,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD = (
            8,
            Weapons.BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD,
        )
        _2_Mk_81 = (8, Weapons._2_Mk_81)
        Mk_81___250lb_GP_Bomb_LD = (8, Weapons.Mk_81___250lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        Kormoran___ASM = (8, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (8, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB = (8, WeaponsF104.VSN_F104G_PTB)

    class Pylon10:
        LAU_138_AIM_9L = (10, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (10, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (10, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        VSN_F104G_R_PTB = (10, WeaponsF104.VSN_F104G_R_PTB)

    class Pylon11:
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons: Set[int] = {1, 2, 4, 6, 8, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep


@planemod
class VSN_F104G(PlaneType):
    id = "VSN_F104G"
    flyable = True
    height = 4.09
    width = 6.36
    length = 16.66
    fuel_max = 2644
    max_speed = 2336.4
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F104G"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        LAU_138_AIM_9L = (2, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (2, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        VSN_F104G_L_PTB = (2, WeaponsF104.VSN_F104G_L_PTB)

    class Pylon4:
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            4,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            4,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            4,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (4, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            4,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (4, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD,
        )
        _2_Mk_81___ = (4, Weapons._2_Mk_81___)
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        Kormoran___ASM = (4, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (4, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB = (4, WeaponsF104.VSN_F104G_PTB)

    class Pylon5:
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (5, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (5, Weapons.AIM_9P5_Sidewinder_IR_AAM)

    class Pylon6:
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            6,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )

    class Pylon7:
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (7, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (7, Weapons.AIM_9P5_Sidewinder_IR_AAM)

    class Pylon8:
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            8,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            8,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            8,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (8, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            8,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (8, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (8, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            8,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            8,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD = (
            8,
            Weapons.BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD,
        )
        _2_Mk_81 = (8, Weapons._2_Mk_81)
        Mk_81___250lb_GP_Bomb_LD = (8, Weapons.Mk_81___250lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        Kormoran___ASM = (8, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (8, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB = (8, WeaponsF104.VSN_F104G_PTB)

    class Pylon10:
        LAU_138_AIM_9L = (10, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (10, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (10, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        VSN_F104G_R_PTB = (10, WeaponsF104.VSN_F104G_R_PTB)

    class Pylon11:
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons: Set[int] = {1, 2, 4, 5, 6, 7, 8, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep


@planemod
class VSN_F104S(PlaneType):
    id = "VSN_F104S"
    flyable = True
    height = 4.09
    width = 6.36
    length = 16.66
    fuel_max = 2641
    max_speed = 2336.4
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F104S"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (2, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (2, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        VSN_F104G_L_PTB = (2, WeaponsF104.VSN_F104G_L_PTB)

    class Pylon3:
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (3, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        AIM_7E_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (4, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        VSN_F104G_PTB = (4, WeaponsF104.VSN_F104G_PTB)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (5, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (5, Weapons.AIM_9P5_Sidewinder_IR_AAM)

    class Pylon6:
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (6, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (6, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (6, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (6, Weapons.AIM_9P5_Sidewinder_IR_AAM)

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (7, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (7, Weapons.AIM_9P5_Sidewinder_IR_AAM)

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (8, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (8, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        VSN_F104G_PTB = (8, WeaponsF104.VSN_F104G_PTB)

    class Pylon9:
        AIM_9B_Sidewinder_IR_AAM = (9, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (9, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        AIM_7E_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (10, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (10, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (10, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        VSN_F104G_R_PTB = (10, WeaponsF104.VSN_F104G_R_PTB)

    class Pylon11:
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep


@planemod
class VSN_F104S_AG(PlaneType):
    id = "VSN_F104S_AG"
    flyable = True
    height = 4.09
    width = 6.36
    length = 16.66
    fuel_max = 2644
    max_speed = 2336.4
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F104S_AG"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        LAU_138_AIM_9L = (2, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (2, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        VSN_F104G_L_PTB = (2, WeaponsF104.VSN_F104G_L_PTB)

    class Pylon3:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            3,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            3,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            3,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (3, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            3,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (3, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (3, Weapons.AGM_119B_Penguin_ASM)

    class Pylon4:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            4,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            4,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            4,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            4,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (4, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            4,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (4, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD,
        )
        _2_Mk_81 = (4, Weapons._2_Mk_81)
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (4, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (4, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB = (4, WeaponsF104.VSN_F104G_PTB)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (5, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (5, Weapons.AIM_9P5_Sidewinder_IR_AAM)

    class Pylon6:
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (7, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (7, Weapons.AIM_9P5_Sidewinder_IR_AAM)

    class Pylon8:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            8,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            8,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            8,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            8,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (8, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            8,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (8, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (8, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            8,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            8,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD = (
            8,
            Weapons.BRU_42_with_3_x_Mk_81___250lb_GP_Bombs_LD,
        )
        _2_Mk_81 = (8, Weapons._2_Mk_81)
        Mk_81___250lb_GP_Bomb_LD = (8, Weapons.Mk_81___250lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (8, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (8, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB = (8, WeaponsF104.VSN_F104G_PTB)

    class Pylon9:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            9,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            9,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            9,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (9, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            9,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (9, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (9, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (9, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (9, Weapons.AGM_119B_Penguin_ASM)

    class Pylon10:
        LAU_138_AIM_9L = (10, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (10, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9P5_Sidewinder_IR_AAM = (10, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        VSN_F104G_R_PTB = (10, WeaponsF104.VSN_F104G_R_PTB)

    class Pylon11:
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep
