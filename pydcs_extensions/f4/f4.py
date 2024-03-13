from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF4:
    F4B_Gunpod_w_SAPHEI_T = {
        "clsid": "{VSN_F4B_Equalizer}",
        "name": "F4B Gunpod w/SAPHEI-T",
        "weight": 244.46,
    }
    F4B_SUU_23_Gun_Pod = {
        "clsid": "{VSN_F4B_Gunpod}",
        "name": "F4B SUU-23 Gun Pod",
        "weight": 112.35,
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


inject_weapons(WeaponsF4)


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
    radio_frequency = 127.5

    livery_name = "VSN_F4B"  # from type

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            2,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BIN_200 = (2, Weapons.BIN_200)
        VSN_F4EL_PTB = (2, Weapons.VSN_F4EL_PTB)

    class Pylon3:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_105_2_AIM_9L = (3, Weapons.LAU_105_2_AIM_9L)
        LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (3, Weapons.LAU_105_2_AIM_9P5)
        LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (3, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (3, Weapons.LAU_105_2_AIM_9JULI)
        AIM_7F_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
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
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon5:
        AIM_7F_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            6,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            6,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        ALQ_131___ECM_Pod = (6, Weapons.ALQ_131___ECM_Pod)
        F4B_Gunpod_w_SAPHEI_T = (6, Weapons.F4B_Gunpod_w_SAPHEI_T)
        VSN_F4EC_PTB = (6, Weapons.VSN_F4EC_PTB)
        VSN_F4B_C2_PTB = (6, Weapons.VSN_F4B_C2_PTB)

    class Pylon7:
        AIM_7F_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon8:
        AIM_7F_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon9:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            9,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            9,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_105_2_AIM_9L = (9, Weapons.LAU_105_2_AIM_9L)
        LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (9, Weapons.LAU_105_2_AIM_9P5)
        LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (9, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (9, Weapons.LAU_105_2_AIM_9JULI)
        AIM_7F_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            9,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            9,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
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
        GBU_10___2000lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            10,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            10,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            10,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            10,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BIN_200 = (10, Weapons.BIN_200)
        VSN_F4ER_PTB = (10, Weapons.VSN_F4ER_PTB)

    class Pylon11:
        # all added manually - did not pull using database export
        BRU42A_M117_3_LAU105_AIM9J_2 = (11, Weapons.BRU_42A_M117_3_LAU105_AIM9J_2)
        BRU42A_MK82_3_LAU105_AIM9J_2 = (11, Weapons.BRU_42A_MK82_3_LAU105_AIM9J_2)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            11,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            11,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )

    class Pylon12:
        # all added manually - did not pull using database export
        BRU42A_M117_3_LAU105_AIM9J_2 = (12, Weapons.BRU_42A_M117_3_LAU105_AIM9J_2)
        BRU42A_MK82_3_LAU105_AIM9J_2 = (12, Weapons.BRU_42A_MK82_3_LAU105_AIM9J_2)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            12,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            12,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )

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
    radio_frequency = 127.5

    livery_name = "VSN_F4C"  # from type

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            2,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BIN_200 = (2, Weapons.BIN_200)
        VSN_F4EL_PTB = (2, Weapons.VSN_F4EL_PTB)

    class Pylon3:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_45B_Shrike_ARM__Imp_ = (3, Weapons.AGM_45B_Shrike_ARM__Imp_)
        AGM_45A_Shrike_ARM = (3, Weapons.AGM_45A_Shrike_ARM)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_105_2_AIM_9L = (3, Weapons.LAU_105_2_AIM_9L)
        LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (3, Weapons.LAU_105_2_AIM_9P5)
        LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (3, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (3, Weapons.LAU_105_2_AIM_9JULI)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BIN_200 = (3, Weapons.BIN_200)

    class Pylon4:
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon5:
        AIM_7F_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            6,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            6,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        ALQ_131___ECM_Pod = (6, Weapons.ALQ_131___ECM_Pod)
        F4B_Gunpod_w_SAPHEI_T = (6, Weapons.F4B_Gunpod_w_SAPHEI_T)
        VSN_F4EC_PTB = (6, Weapons.VSN_F4EC_PTB)
        VSN_F4B_C2_PTB = (6, Weapons.VSN_F4B_C2_PTB)

    class Pylon7:
        AIM_7F_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon8:
        AIM_7F_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )

    class Pylon9:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_45B_Shrike_ARM__Imp_ = (9, Weapons.AGM_45B_Shrike_ARM__Imp_)
        AGM_45A_Shrike_ARM = (9, Weapons.AGM_45A_Shrike_ARM)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            9,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            9,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_105_2_AIM_9L = (9, Weapons.LAU_105_2_AIM_9L)
        LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9P5 = (9, Weapons.LAU_105_2_AIM_9P5)
        LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_7_with_2_x_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9J = (9, Weapons.LAU_105_2_AIM_9J)
        LAU_105_2_AIM_9JULI = (9, Weapons.LAU_105_2_AIM_9JULI)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            9,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            9,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BIN_200 = (9, Weapons.BIN_200)

    class Pylon10:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            10,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            10,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            10,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            10,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BIN_200 = (10, Weapons.BIN_200)
        VSN_F4ER_PTB = (10, Weapons.VSN_F4ER_PTB)

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
    ]
    task_default = task.CAP
