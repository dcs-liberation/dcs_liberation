from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF4BC:
    AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = {
        "clsid": "{AGM-45PJ}",
        "name": "AGM-45A-10 Shrike - Passive radar homing Anti-Radiation-Missile",
        "weight": None,
    }
    AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = {
        "clsid": "{AGM-45BPJ}",
        "name": "AGM-45B-10 Shrike - Passive radar homing Anti-Radiation-Missile",
        "weight": None,
    }
    BRU_42A_M117_3_LAU105_AIM9J_2 = {
        "clsid": "{F4B_BRU42A_M117_3_LAU105_AIM9J_2}",
        "name": "BRU 42A M117*3 LAU105 AIM9J*2",
        "weight": 1500,
    }
    BRU_42A_MK82_3_LAU105_AIM9J_2 = {
        "clsid": "{F4B_BRU42A_MK82_3_LAU105_AIM9J_2}",
        "name": "BRU 42A MK82*3 LAU105 AIM9J*2",
        "weight": 1500,
    }
    F4B_LAU105_AIM9J_2_BRU42A_M117_3 = {
        "clsid": "{F4B_LAU105_AIM9J_2_BRU42A_M117_3}",
        "name": "F4B_LAU105_AIM9J_2_BRU42A_M117_3",
        "weight": 332,
    }
    F4B_LAU105_AIM9J_2_BRU42A_MK82_3 = {
        "clsid": "{F4B_LAU105_AIM9J_2_BRU42A_MK82_3}",
        "name": "F4B_LAU105_AIM9J_2_BRU42A_MK82_3",
        "weight": 332,
    }
    F4B_LAU105_AIM9J_2_MER_MK20_3 = {
        "clsid": "{F4B_LAU105_AIM9J_2_MER_MK20_3}",
        "name": "F4B_LAU105_AIM9J_2_MER_MK20_3",
        "weight": 332,
    }
    F4B_LAU105_AIM9J_2_TER9A_MK82SE_3 = {
        "clsid": "{F4B_LAU105_AIM9J_2_TER9A_MK82SE_3}",
        "name": "F4B_LAU105_AIM9J_2_TER9A_MK82SE_3",
        "weight": 332,
    }
    LAU_105_2_AIM_9J = {
        "clsid": "{VSN_F4B_LAU105_AIM9J}",
        "name": "LAU-105 2*AIM-9J",
        "weight": 332,
    }
    LAU_105_2_AIM_9JULI = {
        "clsid": "{VSN_F4B_LAU105_AIM9JULI}",
        "name": "LAU-105 2*AIM-9JULI",
        "weight": 332,
    }
    LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = {
        "clsid": "{F4C_LAU118_AGM45A-10_PJ}",
        "name": "LAU-118a and AGM-45A-10 Shrike - Passive radar homing Anti-Radiation-Missile",
        "weight": 177,
    }
    LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile = {
        "clsid": "{F4C_LAU118_AGM45A}",
        "name": "LAU-118a and AGM-45A Shrike - Passive radar homing Anti-Radiation-Missile",
        "weight": 177,
    }
    LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = {
        "clsid": "{F4C_LAU118_AGM45B-10_PJ}",
        "name": "LAU-118a and AGM-45B-10 Shrike - Passive radar homing Anti-Radiation-Missile",
        "weight": 177,
    }
    SUU_23A_M61_Gunpod_HE_AP_HE_INV_ = {
        "clsid": "{VSN_F4B_Equalizer}",
        "name": "SUU-23A M61 Gunpod HE/AP/HE-INV.",
        "weight": 744.362,
    }
    VSN_F4B_C2_PTB = {
        "clsid": "VSN_F4B_C2_PTB",
        "name": "Fuel tank Center 370 Gal",
        "weight": 1240,
    }
    VSN_F4EC_PTB = {
        "clsid": "VSN_F4EC_PTB",
        "name": "Fuel tank Center 600 Gal",
        "weight": 1980,
    }
    VSN_F4EL_PTB = {
        "clsid": "VSN_F4EL_PTB",
        "name": "Fuel tank Wing L 370 Gal",
        "weight": 1240,
    }
    VSN_F4ER_PTB = {
        "clsid": "VSN_F4ER_PTB",
        "name": "Fuel tank Wing R 370 Gal",
        "weight": 1240,
    }


inject_weapons(WeaponsF4BC)


@planemod
class VSN_F4B(PlaneType):
    id = "VSN_F4B"
    flyable = True
    height = 5.02
    width = 11.71
    length = 19.2
    fuel_max = 6416
    max_speed = 2545.2
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 264

    panel_radio = {
        1: {
            "channels": {
                1: 264,
                2: 265,
                4: 254,
                8: 258,
                16: 267,
                17: 251,
                9: 262,
                18: 253,
                5: 250,
                10: 259,
                11: 268,
                3: 256,
                6: 270,
                12: 269,
                13: 260,
                7: 257,
                14: 263,
                15: 261,
            },
        },
    }

    livery_name = "VSN_F4B"  # from type

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            2,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            2,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__ = (
            2,
            Weapons._6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__,
        )
        _6x_Mk_81___250lb_GP_Bomb_LD__MER__ = (
            2,
            Weapons._6x_Mk_81___250lb_GP_Bomb_LD__MER__,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BIN_200 = (2, Weapons.BIN_200)
        VSN_F4EL_PTB = (2, Weapons.VSN_F4EL_PTB)

    class Pylon3:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            3,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            3,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_105_2_AIM_9L = (3, Weapons.LAU_105_2_AIM_9L)
        LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (3, Weapons.LAU_105_2_AIM_9P5)
        LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (3, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (3, Weapons.LAU_105_2_AIM_9JULI)
        AIM_7F_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BIN_200 = (3, Weapons.BIN_200)
        F4B_LAU105_AIM9J_2_BRU42A_M117_3 = (3, Weapons.F4B_LAU105_AIM9J_2_BRU42A_M117_3)
        F4B_LAU105_AIM9J_2_BRU42A_MK82_3 = (3, Weapons.F4B_LAU105_AIM9J_2_BRU42A_MK82_3)
        F4B_LAU105_AIM9J_2_TER9A_MK82SE_3 = (
            3,
            Weapons.F4B_LAU105_AIM9J_2_TER9A_MK82SE_3,
        )
        F4B_LAU105_AIM9J_2_MER_MK20_3 = (3, Weapons.F4B_LAU105_AIM9J_2_MER_MK20_3)

    class Pylon4:
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon5:
        AIM_7F_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)
        BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _6x_Mk_81___250lb_GP_Bomb_LD__MER__ = (
            6,
            Weapons._6x_Mk_81___250lb_GP_Bomb_LD__MER__,
        )
        _6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__ = (
            6,
            Weapons._6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__,
        )
        _6x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__MER__ = (
            6,
            Weapons._6x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__MER__,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            6,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        SUU_23A_M61_Gunpod_HE_AP_HE_INV_ = (6, Weapons.SUU_23A_M61_Gunpod_HE_AP_HE_INV_)
        VSN_F4EC_PTB = (6, Weapons.VSN_F4EC_PTB)
        VSN_F4B_C2_PTB = (6, Weapons.VSN_F4B_C2_PTB)

    class Pylon7:
        AIM_7F_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon8:
        AIM_7F_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon9:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            9,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            9,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            9,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            9,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            9,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_105_2_AIM_9L = (9, Weapons.LAU_105_2_AIM_9L)
        LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (9, Weapons.LAU_105_2_AIM_9P5)
        LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (9, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (9, Weapons.LAU_105_2_AIM_9JULI)
        AIM_7F_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            9,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            9,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            9,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BIN_200 = (9, Weapons.BIN_200)
        F4B_LAU105_AIM9J_2_BRU42A_M117_3 = (9, Weapons.F4B_LAU105_AIM9J_2_BRU42A_M117_3)
        F4B_LAU105_AIM9J_2_BRU42A_MK82_3 = (9, Weapons.F4B_LAU105_AIM9J_2_BRU42A_MK82_3)
        F4B_LAU105_AIM9J_2_TER9A_MK82SE_3 = (
            9,
            Weapons.F4B_LAU105_AIM9J_2_TER9A_MK82SE_3,
        )
        F4B_LAU105_AIM9J_2_MER_MK20_3 = (9, Weapons.F4B_LAU105_AIM9J_2_MER_MK20_3)

    class Pylon10:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            10,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            10,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            10,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            10,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            10,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__ = (
            10,
            Weapons._6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__,
        )
        _6x_Mk_81___250lb_GP_Bomb_LD__MER__ = (
            10,
            Weapons._6x_Mk_81___250lb_GP_Bomb_LD__MER__,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BIN_200 = (10, Weapons.BIN_200)
        VSN_F4ER_PTB = (10, Weapons.VSN_F4ER_PTB)

    # ERRR <CLEAN>
    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.PinpointStrike,
    ]
    task_default = task.CAP


@planemod
class VSN_F4C(PlaneType):
    id = "VSN_F4C"
    flyable = True
    height = 5.02
    width = 11.71
    length = 19.2
    fuel_max = 6416
    max_speed = 2545.2
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 264

    panel_radio = {
        1: {
            "channels": {
                1: 264,
                2: 265,
                4: 254,
                8: 258,
                16: 267,
                17: 251,
                9: 262,
                18: 253,
                5: 250,
                10: 259,
                11: 268,
                3: 256,
                6: 270,
                12: 269,
                13: 260,
                7: 257,
                14: 263,
                15: 261,
            },
        },
    }

    livery_name = "VSN_F4C"  # from type

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            2,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            2,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__ = (
            2,
            Weapons._6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__,
        )
        _6x_Mk_81___250lb_GP_Bomb_LD__MER__ = (
            2,
            Weapons._6x_Mk_81___250lb_GP_Bomb_LD__MER__,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BIN_200 = (2, Weapons.BIN_200)
        VSN_F4EL_PTB = (2, Weapons.VSN_F4EL_PTB)
        LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            2,
            Weapons.LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118A___AGM_45B_Shrike_ARM = (2, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            2,
            Weapons.LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            2,
            Weapons.LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )

    class Pylon3:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_118A___AGM_45B_Shrike_ARM = (3, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            3,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            3,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_105_2_AIM_9L = (3, Weapons.LAU_105_2_AIM_9L)
        LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (3, Weapons.LAU_105_2_AIM_9P5)
        LAU_105_2_AIM_9P3 = (3, Weapons.LAU_105_2_AIM_9P3)
        LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (3, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (3, Weapons.LAU_105_2_AIM_9JULI)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        _2x_M117___750lb_GP_Bomb_LD__TER____ = (
            3,
            Weapons._2x_M117___750lb_GP_Bomb_LD__TER____,
        )
        _3x_M117___750lb_GP_Bomb_LD__MER_ = (
            3,
            Weapons._3x_M117___750lb_GP_Bomb_LD__MER_,
        )
        BIN_200 = (3, Weapons.BIN_200)
        LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            3,
            Weapons.LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            3,
            Weapons.LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            3,
            Weapons.LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )

    class Pylon4:
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon5:
        AIM_7F_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)
        BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            6,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _6x_Mk_81___250lb_GP_Bomb_LD__MER__ = (
            6,
            Weapons._6x_Mk_81___250lb_GP_Bomb_LD__MER__,
        )
        _6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__ = (
            6,
            Weapons._6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__,
        )
        _6x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__MER__ = (
            6,
            Weapons._6x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__MER__,
        )
        SUU_23A_M61_Gunpod_HE_AP_HE_INV_ = (6, Weapons.SUU_23A_M61_Gunpod_HE_AP_HE_INV_)
        VSN_F4EC_PTB = (6, Weapons.VSN_F4EC_PTB)
        VSN_F4B_C2_PTB = (6, Weapons.VSN_F4B_C2_PTB)

    class Pylon7:
        AIM_7F_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon8:
        AIM_7F_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon9:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            9,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_118A___AGM_45B_Shrike_ARM = (9, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            9,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            9,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            9,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            9,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_105_2_AIM_9L = (9, Weapons.LAU_105_2_AIM_9L)
        LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_105___2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (9, Weapons.LAU_105_2_AIM_9P5)
        LAU_105_2_AIM_9P3 = (9, Weapons.LAU_105_2_AIM_9P3)
        LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_7___2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (9, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (9, Weapons.LAU_105_2_AIM_9JULI)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            9,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            9,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        _2x_M117___750lb_GP_Bomb_LD__TER_____ = (
            9,
            Weapons._2x_M117___750lb_GP_Bomb_LD__TER_____,
        )
        _3x_M117___750lb_GP_Bomb_LD__MER__ = (
            9,
            Weapons._3x_M117___750lb_GP_Bomb_LD__MER__,
        )
        BIN_200 = (9, Weapons.BIN_200)
        LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            9,
            Weapons.LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            9,
            Weapons.LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            9,
            Weapons.LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )

    class Pylon10:
        BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            10,
            Weapons.BRU_42___3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.TER_9_A___3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            10,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            10,
            Weapons.BRU_42_3_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            10,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            10,
            Weapons.BRU_33_2_x_LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_41A___6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__ = (
            10,
            Weapons._6x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER__,
        )
        _6x_Mk_81___250lb_GP_Bomb_LD__MER__ = (
            10,
            Weapons._6x_Mk_81___250lb_GP_Bomb_LD__MER__,
        )
        BIN_200 = (10, Weapons.BIN_200)
        VSN_F4ER_PTB = (10, Weapons.VSN_F4ER_PTB)
        LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            10,
            Weapons.LAU_118a_and_AGM_45A_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118A___AGM_45B_Shrike_ARM = (10, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            10,
            Weapons.LAU_118a_and_AGM_45A_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )
        LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile = (
            10,
            Weapons.LAU_118a_and_AGM_45B_10_Shrike___Passive_radar_homing_Anti_Radiation_Missile,
        )

    # ERRR <CLEAN>
    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.SEAD,
        task.PinpointStrike,
    ]
    task_default = task.CAP
