from typing import Set

from dcs import task
from dcs.liveries_scanner import Liveries
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class JAS39GripenWeapons:
    EWS_39_Integrated_ECM = {
        "clsid": "{JAS39_EWS39}",
        "name": "EWS 39 Integrated ECM",
        "weight": 1,
    }
    Integrated_ELINT = {
        "clsid": "{JAS39_ELINT}",
        "name": "Integrated ELINT",
        "weight": 1,
    }
    AIM_120B_AMRAAM_Active_Rdr_AAM = {
        "clsid": "{JAS39_AIM120B}",
        "name": "AIM-120B AMRAAM Active Rdr AAM",
        "weight": 157,
    }
    AIM_120C_5_AMRAAM_Active_Rdr_AAM = {
        "clsid": "{JAS39_AIM120C5}",
        "name": "AIM-120C-5 AMRAAM Active Rdr AAM",
        "weight": 162.5,
    }
    AIM_120C_7_AMRAAM_Active_Rdr_AAM = {
        "clsid": "{JAS39_AIM120C7}",
        "name": "AIM-120C-7 AMRAAM Active Rdr AAM",
        "weight": 162.5,
    }
    AIM_9L_Sidewinder_IR_AAM_ = {
        "clsid": "{JAS39_AIM-9L}",
        "name": "AIM-9L Sidewinder IR AAM",
        "weight": 86,
    }
    AIM_9M_Sidewinder_IR_AAM_ = {
        "clsid": "{JAS39_AIM-9M}",
        "name": "AIM-9M Sidewinder IR AAM",
        "weight": 86,
    }
    AIM_9X_Sidewinder_IR_AAM_ = {
        "clsid": "{JAS39_AIM-9X}",
        "name": "AIM-9X Sidewinder IR AAM",
        "weight": 86.5,
    }
    AIM_132_ASRAAM_IR_AAM = {
        "clsid": "{JAS39_ASRAAM}",
        "name": "AIM-132 ASRAAM IR AAM",
        "weight": 89,
    }
    A_Darter_IR_AAM = {
        "clsid": "{JAS39_A-DARTER}",
        "name": "A-Darter IR AAM",
        "weight": 90,
    }
    _3_x_Brimstone_Laser_Guided_Missile = {
        "clsid": "{JAS39_BRIMSTONE}",
        "name": "3 x Brimstone Laser Guided Missile",
        "weight": 195.5,
    }
    I_Derby_ER_BVRAAM_Active_Rdr_AAM = {
        "clsid": "{JAS39_Derby}",
        "name": "I-Derby ER BVRAAM Active Rdr AAM",
        "weight": 119,
    }
    DWS_39_MJ2_Anti_radiation_Cluster_Bomb = {
        "clsid": "{JAS39_DWS39_ARM}",
        "name": "DWS 39 MJ2 Anti-radiation Cluster Bomb",
        "weight": 672,
    }
    DWS_39_MJ2_TV_Guided_Cluster_Bomb = {
        "clsid": "{JAS39_DWS39_TV}",
        "name": "DWS 39 MJ2 TV Guided Cluster Bomb",
        "weight": 672,
    }
    GBU_10_2000_lb_Laser_guided_Bomb = {
        "clsid": "{JAS39_GBU10}",
        "name": "GBU-10 2000 lb Laser-guided Bomb",
        "weight": 934,
    }
    GBU_12_500_lb_Laser_guided_Bomb = {
        "clsid": "{JAS39_GBU12}",
        "name": "GBU-12 500 lb Laser-guided Bomb",
        "weight": 275,
    }
    GBU_16_1000_lb_Laser_guided_Bomb = {
        "clsid": "{JAS39_GBU16}",
        "name": "GBU-16 1000 lb Laser-guided Bomb",
        "weight": 454,
    }
    GBU_31_2000_lb_TV_Guided_Glide_Bomb = {
        "clsid": "{JAS39_GBU31}",
        "name": "GBU-31 2000 lb TV Guided Glide-Bomb",
        "weight": 934,
    }
    GBU_31_2000_lb_Penetrator_TV_Guided_Glide_Bomb = {
        "clsid": "{JAS39_GBU31_BLU109}",
        "name": "GBU-31 2000 lb Penetrator TV Guided Glide-Bomb",
        "weight": 970,
    }
    GBU_32_1000_lb_TV_Guided_Glide_Bomb = {
        "clsid": "{JAS39_GBU32}",
        "name": "GBU-32 1000 lb TV Guided Glide-Bomb",
        "weight": 467,
    }
    GBU_38_500_lb_TV_Guided_Glide_Bomb = {
        "clsid": "{JAS39_GBU38}",
        "name": "GBU-38 500 lb TV Guided Glide-Bomb",
        "weight": 241,
    }
    GBU_49_500_lb_TV_Guided_Bomb = {
        "clsid": "{JAS39_GBU49}",
        "name": "GBU-49 500 lb TV Guided Bomb",
        "weight": 241,
    }
    IRIS_T_IR_AAM = {"clsid": "{JAS39_IRIS-T}", "name": "IRIS-T IR AAM", "weight": 88.4}
    Litening_III_Targeting_Pod = {
        "clsid": "{JAS39_Litening}",
        "name": "Litening III Targeting Pod",
        "weight": 208,
    }
    M70B_AP_Unguided_rocket = {
        "clsid": "{JAS39_M70BAP}",
        "name": "M70B AP Unguided rocket",
        "weight": 372.2,
    }
    M70B_HE_Unguided_rocket = {
        "clsid": "{JAS39_M70BHE}",
        "name": "M70B HE Unguided rocket",
        "weight": 372.2,
    }
    _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = {
        "clsid": "{JAS39_M71LD}",
        "name": "4 x M/71 120 kg GP Bomb Low-drag ",
        "weight": 605,
    }
    MAR_1_High_Speed_Anti_Radiation_Missile = {
        "clsid": "{JAS39_MAR-1}",
        "name": "MAR-1 High Speed Anti-Radiation Missile",
        "weight": 350,
    }
    Meteor_BVRAAM_Active_Rdr_AAM = {
        "clsid": "{JAS39_Meteor}",
        "name": "Meteor BVRAAM Active Rdr AAM",
        "weight": 191,
    }
    Python_5_IR_AAM = {
        "clsid": "{JAS39_PYTHON-5}",
        "name": "Python-5 IR AAM",
        "weight": 106,
    }
    RBS_15_Mk4_Gungnir_Anti_ship_Missile = {
        "clsid": "{JAS39_RBS15}",
        "name": "RBS-15 Mk4 Gungnir Anti-ship Missile",
        "weight": 650,
    }
    RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_ = {
        "clsid": "{JAS39_RBS15AI}",
        "name": "RBS-15 Mk4 Gungnir Anti-ship Missile (AI)",
        "weight": 650,
    }
    _4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb = {
        "clsid": "{JAS39_SDB}",
        "name": "4 x GBU-39 SDB 285 lb TV Guided Glide-Bomb",
        "weight": 661,
    }
    Storm_Shadow_Long_Range_Anti_Radiation_Cruise_missile = {
        "clsid": "{JAS39_STORMSHADOW_ARM}",
        "name": "Storm Shadow Long Range Anti-Radiation Cruise-missile",
        "weight": 1300,
    }
    Drop_tank_1100_litre = {
        "clsid": "{JAS39_TANK1100}",
        "name": "Drop tank 1100 litre",
        "weight": 946.06,
    }
    Litening_III_Targeting_Pod_FLIR = {
        "clsid": "{JAS39_FLIR}",
        "name": "Litening III Targeting Pod FLIR",
        "weight": 2,
    }
    Mk_82_500_lb_GP_Bomb = {
        "clsid": "{JAS39_MK82}",
        "name": "Mk-82 500 lb GP Bomb",
        "weight": 241,
    }
    Mk_83_1000_lb_GP_Bomb = {
        "clsid": "{JAS39_MK83}",
        "name": "Mk-83 1000 lb GP Bomb",
        "weight": 447,
    }
    Mk_84_2000_lb_GP_Bomb = {
        "clsid": "{JAS39_MK84}",
        "name": "Mk-84 2000 lb GP Bomb",
        "weight": 894,
    }
    _2_x_GBU_12_500_lb_Laser_guided_Bomb = {
        "clsid": "{JAS39_BRU33_GBU12}",
        "name": "2 x GBU-12 500 lb Laser-guided Bomb",
        "weight": 625,
    }
    _2_x_GBU_16_1000_lb_Laser_guided_Bomb = {
        "clsid": "{JAS39_BRU33_GBU16}",
        "name": "2 x GBU-16 1000 lb Laser-guided Bomb",
        "weight": 983,
    }
    _2_x_GBU_32_1000_lb_TV_Guided_Glide_Bomb = {
        "clsid": "{JAS39_BRU33_GBU32}",
        "name": "2 x GBU-32 1000 lb TV Guided Glide-Bomb",
        "weight": 1009,
    }
    _2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb = {
        "clsid": "{JAS39_BRU33_GBU38}",
        "name": "2 x GBU-38 500 lb TV Guided Glide-Bomb",
        "weight": 557,
    }
    _2_x_GBU_49_500_lb_TV_Guided_Bomb = {
        "clsid": "{JAS39_BRU33_GBU49}",
        "name": "2 x GBU-49 500 lb TV Guided Bomb",
        "weight": 557,
    }
    _2_x_Mk_82_500_lb_GP_Bomb = {
        "clsid": "{JAS39_BRU33_MK82}",
        "name": "2 x Mk-82 500 lb GP Bomb",
        "weight": 557,
    }
    _2_x_Mk_83_1000_lb_GP_Bomb = {
        "clsid": "{JAS39_BRU33_MK83}",
        "name": "2 x Mk-83 1000 lb GP Bomb",
        "weight": 969,
    }
    _3_x_SPEAR_3_Anti_Radiation_Missile = {
        "clsid": "{JAS39_SPEAR3}",
        "name": "3 x SPEAR-3 Anti-Radiation Missile",
        "weight": 360,
    }
    _3_x_SPEAR_EW_Decoy = {
        "clsid": "{JAS39_SPEAREW}",
        "name": "3 x SPEAR-EW Decoy",
        "weight": 360,
    }
    KEPD_350_Long_Range_Anti_Radiation_Cruise_missile = {
        "clsid": "{JAS39_KEPD350_ARM}",
        "name": "KEPD 350 Long Range Anti-Radiation Cruise-missile",
        "weight": 1400,
    }


inject_weapons(JAS39GripenWeapons)


@planemod
class JAS39Gripen(PlaneType):
    id = "JAS39Gripen"
    flyable = True
    height = 4.5
    width = 8.4
    length = 14.1
    fuel_max = 2550
    max_speed = 2649.996
    chaff = 80
    flare = 40
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "JAS39GRIPEN"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        IRIS_T_IR_AAM = (1, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (1, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (1, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (1, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (1, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (1, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (1, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        IRIS_T_IR_AAM = (2, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (2, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (2, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (2, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (2, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (2, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (2, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        Meteor_BVRAAM_Active_Rdr_AAM = (
            2,
            JAS39GripenWeapons.Meteor_BVRAAM_Active_Rdr_AAM,
        )
        AIM_120B_AMRAAM_Active_Rdr_AAM = (
            2,
            JAS39GripenWeapons.AIM_120B_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_5_AMRAAM_Active_Rdr_AAM = (
            2,
            JAS39GripenWeapons.AIM_120C_5_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_7_AMRAAM_Active_Rdr_AAM = (
            2,
            JAS39GripenWeapons.AIM_120C_7_AMRAAM_Active_Rdr_AAM,
        )
        I_Derby_ER_BVRAAM_Active_Rdr_AAM = (
            2,
            JAS39GripenWeapons.I_Derby_ER_BVRAAM_Active_Rdr_AAM,
        )
        Mk_82_500_lb_GP_Bomb = (2, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (2, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (2, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            2,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        M70B_HE_Unguided_rocket = (2, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (2, JAS39GripenWeapons.M70B_AP_Unguided_rocket)

    class Pylon3:
        AIM_9L_Sidewinder_IR_AAM_ = (3, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        IRIS_T_IR_AAM = (3, JAS39GripenWeapons.IRIS_T_IR_AAM)
        A_Darter_IR_AAM = (3, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (3, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (3, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (3, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (3, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        Meteor_BVRAAM_Active_Rdr_AAM = (
            3,
            JAS39GripenWeapons.Meteor_BVRAAM_Active_Rdr_AAM,
        )
        AIM_120B_AMRAAM_Active_Rdr_AAM = (
            3,
            JAS39GripenWeapons.AIM_120B_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_5_AMRAAM_Active_Rdr_AAM = (
            3,
            JAS39GripenWeapons.AIM_120C_5_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_7_AMRAAM_Active_Rdr_AAM = (
            3,
            JAS39GripenWeapons.AIM_120C_7_AMRAAM_Active_Rdr_AAM,
        )
        I_Derby_ER_BVRAAM_Active_Rdr_AAM = (
            3,
            JAS39GripenWeapons.I_Derby_ER_BVRAAM_Active_Rdr_AAM,
        )
        Mk_82_500_lb_GP_Bomb = (3, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (3, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        Mk_84_2000_lb_GP_Bomb = (3, JAS39GripenWeapons.Mk_84_2000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (3, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _2_x_Mk_83_1000_lb_GP_Bomb = (3, JAS39GripenWeapons._2_x_Mk_83_1000_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            3,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        M70B_HE_Unguided_rocket = (3, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (3, JAS39GripenWeapons.M70B_AP_Unguided_rocket)
        Drop_tank_1100_litre = (3, JAS39GripenWeapons.Drop_tank_1100_litre)

    class Pylon4:
        Drop_tank_1100_litre = (4, JAS39GripenWeapons.Drop_tank_1100_litre)

    class Pylon5:
        Litening_III_Targeting_Pod = (5, JAS39GripenWeapons.Litening_III_Targeting_Pod)

    class Pylon6:
        AIM_9L_Sidewinder_IR_AAM_ = (6, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        IRIS_T_IR_AAM = (6, JAS39GripenWeapons.IRIS_T_IR_AAM)
        A_Darter_IR_AAM = (6, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (6, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (6, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (6, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (6, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        Meteor_BVRAAM_Active_Rdr_AAM = (
            6,
            JAS39GripenWeapons.Meteor_BVRAAM_Active_Rdr_AAM,
        )
        AIM_120B_AMRAAM_Active_Rdr_AAM = (
            6,
            JAS39GripenWeapons.AIM_120B_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_5_AMRAAM_Active_Rdr_AAM = (
            6,
            JAS39GripenWeapons.AIM_120C_5_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_7_AMRAAM_Active_Rdr_AAM = (
            6,
            JAS39GripenWeapons.AIM_120C_7_AMRAAM_Active_Rdr_AAM,
        )
        I_Derby_ER_BVRAAM_Active_Rdr_AAM = (
            6,
            JAS39GripenWeapons.I_Derby_ER_BVRAAM_Active_Rdr_AAM,
        )
        Mk_82_500_lb_GP_Bomb = (6, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (6, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        Mk_84_2000_lb_GP_Bomb = (6, JAS39GripenWeapons.Mk_84_2000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (6, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _2_x_Mk_83_1000_lb_GP_Bomb = (6, JAS39GripenWeapons._2_x_Mk_83_1000_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            6,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        M70B_HE_Unguided_rocket = (6, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (6, JAS39GripenWeapons.M70B_AP_Unguided_rocket)
        Drop_tank_1100_litre = (6, JAS39GripenWeapons.Drop_tank_1100_litre)

    class Pylon7:
        IRIS_T_IR_AAM = (7, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (7, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (7, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (7, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (7, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (7, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (7, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        Meteor_BVRAAM_Active_Rdr_AAM = (
            7,
            JAS39GripenWeapons.Meteor_BVRAAM_Active_Rdr_AAM,
        )
        AIM_120B_AMRAAM_Active_Rdr_AAM = (
            7,
            JAS39GripenWeapons.AIM_120B_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_5_AMRAAM_Active_Rdr_AAM = (
            7,
            JAS39GripenWeapons.AIM_120C_5_AMRAAM_Active_Rdr_AAM,
        )
        AIM_120C_7_AMRAAM_Active_Rdr_AAM = (
            7,
            JAS39GripenWeapons.AIM_120C_7_AMRAAM_Active_Rdr_AAM,
        )
        I_Derby_ER_BVRAAM_Active_Rdr_AAM = (
            7,
            JAS39GripenWeapons.I_Derby_ER_BVRAAM_Active_Rdr_AAM,
        )
        Mk_82_500_lb_GP_Bomb = (7, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (7, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (7, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            7,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        M70B_HE_Unguided_rocket = (7, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (7, JAS39GripenWeapons.M70B_AP_Unguided_rocket)

    class Pylon8:
        IRIS_T_IR_AAM = (8, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (8, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (8, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (8, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (8, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (8, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (8, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (8, Weapons.Smokewinder___red)
        Smokewinder___green = (8, Weapons.Smokewinder___green)
        Smokewinder___blue = (8, Weapons.Smokewinder___blue)
        Smokewinder___white = (8, Weapons.Smokewinder___white)
        Smokewinder___yellow = (8, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (8, Weapons.Smokewinder___orange)

    class Pylon9:
        Litening_III_Targeting_Pod_FLIR = (
            9,
            JAS39GripenWeapons.Litening_III_Targeting_Pod_FLIR,
        )

    class Pylon10:
        Integrated_ELINT = (10, JAS39GripenWeapons.Integrated_ELINT)

    class Pylon11:
        EWS_39_Integrated_ECM = (11, JAS39GripenWeapons.EWS_39_Integrated_ECM)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.Intercept,
        task.CAP,
        task.Reconnaissance,
        task.Escort,
        task.FighterSweep,
    ]
    task_default = task.FighterSweep


@planemod
class JAS39Gripen_AG(PlaneType):
    id = "JAS39Gripen_AG"
    flyable = True
    height = 4.5
    width = 8.4
    length = 14.1
    fuel_max = 2550
    max_speed = 2649.996
    chaff = 80
    flare = 40
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "JAS39GRIPEN_AG"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        IRIS_T_IR_AAM = (1, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (1, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (1, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (1, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (1, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (1, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (1, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        IRIS_T_IR_AAM = (2, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (2, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (2, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (2, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (2, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (2, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (2, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        RBS_15_Mk4_Gungnir_Anti_ship_Missile = (
            2,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile,
        )
        RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_ = (
            2,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_,
        )
        MAR_1_High_Speed_Anti_Radiation_Missile = (
            2,
            JAS39GripenWeapons.MAR_1_High_Speed_Anti_Radiation_Missile,
        )
        GBU_49_500_lb_TV_Guided_Bomb = (
            2,
            JAS39GripenWeapons.GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_32_1000_lb_TV_Guided_Glide_Bomb = (
            2,
            JAS39GripenWeapons.GBU_32_1000_lb_TV_Guided_Glide_Bomb,
        )
        GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            2,
            JAS39GripenWeapons.GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb = (
            2,
            JAS39GripenWeapons._4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb,
        )
        GBU_12_500_lb_Laser_guided_Bomb = (
            2,
            JAS39GripenWeapons.GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_12_500_lb_Laser_guided_Bomb = (
            2,
            JAS39GripenWeapons._2_x_GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            2,
            JAS39GripenWeapons._2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _2_x_GBU_49_500_lb_TV_Guided_Bomb = (
            2,
            JAS39GripenWeapons._2_x_GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_16_1000_lb_Laser_guided_Bomb = (
            2,
            JAS39GripenWeapons.GBU_16_1000_lb_Laser_guided_Bomb,
        )
        DWS_39_MJ2_TV_Guided_Cluster_Bomb = (
            2,
            JAS39GripenWeapons.DWS_39_MJ2_TV_Guided_Cluster_Bomb,
        )
        DWS_39_MJ2_Anti_radiation_Cluster_Bomb = (
            2,
            JAS39GripenWeapons.DWS_39_MJ2_Anti_radiation_Cluster_Bomb,
        )
        Mk_82_500_lb_GP_Bomb = (2, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (2, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (2, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            2,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        M70B_HE_Unguided_rocket = (2, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (2, JAS39GripenWeapons.M70B_AP_Unguided_rocket)
        _3_x_Brimstone_Laser_Guided_Missile = (
            2,
            JAS39GripenWeapons._3_x_Brimstone_Laser_Guided_Missile,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (2, Weapons.LAU_117_AGM_65H)
        _3_x_SPEAR_3_Anti_Radiation_Missile = (
            2,
            JAS39GripenWeapons._3_x_SPEAR_3_Anti_Radiation_Missile,
        )
        _3_x_SPEAR_EW_Decoy = (2, JAS39GripenWeapons._3_x_SPEAR_EW_Decoy)

    class Pylon3:
        AIM_9L_Sidewinder_IR_AAM_ = (3, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        IRIS_T_IR_AAM = (3, JAS39GripenWeapons.IRIS_T_IR_AAM)
        A_Darter_IR_AAM = (3, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (3, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (3, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (3, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (3, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        _3_x_Brimstone_Laser_Guided_Missile = (
            3,
            JAS39GripenWeapons._3_x_Brimstone_Laser_Guided_Missile,
        )
        _3_x_SPEAR_3_Anti_Radiation_Missile = (
            3,
            JAS39GripenWeapons._3_x_SPEAR_3_Anti_Radiation_Missile,
        )
        _3_x_SPEAR_EW_Decoy = (3, JAS39GripenWeapons._3_x_SPEAR_EW_Decoy)
        RBS_15_Mk4_Gungnir_Anti_ship_Missile = (
            3,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile,
        )
        RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_ = (
            3,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_,
        )
        MAR_1_High_Speed_Anti_Radiation_Missile = (
            3,
            JAS39GripenWeapons.MAR_1_High_Speed_Anti_Radiation_Missile,
        )
        GBU_49_500_lb_TV_Guided_Bomb = (
            3,
            JAS39GripenWeapons.GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_31_2000_lb_TV_Guided_Glide_Bomb = (
            3,
            JAS39GripenWeapons.GBU_31_2000_lb_TV_Guided_Glide_Bomb,
        )
        GBU_31_2000_lb_Penetrator_TV_Guided_Glide_Bomb = (
            3,
            JAS39GripenWeapons.GBU_31_2000_lb_Penetrator_TV_Guided_Glide_Bomb,
        )
        GBU_32_1000_lb_TV_Guided_Glide_Bomb = (
            3,
            JAS39GripenWeapons.GBU_32_1000_lb_TV_Guided_Glide_Bomb,
        )
        GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            3,
            JAS39GripenWeapons.GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb = (
            3,
            JAS39GripenWeapons._4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb,
        )
        GBU_12_500_lb_Laser_guided_Bomb = (
            3,
            JAS39GripenWeapons.GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_12_500_lb_Laser_guided_Bomb = (
            3,
            JAS39GripenWeapons._2_x_GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            3,
            JAS39GripenWeapons._2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _2_x_GBU_49_500_lb_TV_Guided_Bomb = (
            3,
            JAS39GripenWeapons._2_x_GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_10_2000_lb_Laser_guided_Bomb = (
            3,
            JAS39GripenWeapons.GBU_10_2000_lb_Laser_guided_Bomb,
        )
        GBU_16_1000_lb_Laser_guided_Bomb = (
            3,
            JAS39GripenWeapons.GBU_16_1000_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_16_1000_lb_Laser_guided_Bomb = (
            3,
            JAS39GripenWeapons._2_x_GBU_16_1000_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_32_1000_lb_TV_Guided_Glide_Bomb = (
            3,
            JAS39GripenWeapons._2_x_GBU_32_1000_lb_TV_Guided_Glide_Bomb,
        )
        DWS_39_MJ2_TV_Guided_Cluster_Bomb = (
            3,
            JAS39GripenWeapons.DWS_39_MJ2_TV_Guided_Cluster_Bomb,
        )
        DWS_39_MJ2_Anti_radiation_Cluster_Bomb = (
            3,
            JAS39GripenWeapons.DWS_39_MJ2_Anti_radiation_Cluster_Bomb,
        )
        Mk_82_500_lb_GP_Bomb = (3, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (3, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        Mk_84_2000_lb_GP_Bomb = (3, JAS39GripenWeapons.Mk_84_2000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (3, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _2_x_Mk_83_1000_lb_GP_Bomb = (3, JAS39GripenWeapons._2_x_Mk_83_1000_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            3,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        Drop_tank_1100_litre = (3, JAS39GripenWeapons.Drop_tank_1100_litre)
        M70B_HE_Unguided_rocket = (3, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (3, JAS39GripenWeapons.M70B_AP_Unguided_rocket)
        Storm_Shadow_Long_Range_Anti_Radiation_Cruise_missile = (
            3,
            JAS39GripenWeapons.Storm_Shadow_Long_Range_Anti_Radiation_Cruise_missile,
        )
        KEPD_350_Long_Range_Anti_Radiation_Cruise_missile = (
            3,
            JAS39GripenWeapons.KEPD_350_Long_Range_Anti_Radiation_Cruise_missile,
        )

    class Pylon4:
        Drop_tank_1100_litre = (4, JAS39GripenWeapons.Drop_tank_1100_litre)

    # ERRR {INV-SMOKE-RED}
    # ERRR {INV-SMOKE-GREEN}
    # ERRR {INV-SMOKE-BLUE}
    # ERRR {INV-SMOKE-WHITE}
    # ERRR {INV-SMOKE-YELLOW}
    # ERRR {INV-SMOKE-ORANGE}

    class Pylon5:
        Litening_III_Targeting_Pod = (5, JAS39GripenWeapons.Litening_III_Targeting_Pod)

    class Pylon6:
        AIM_9L_Sidewinder_IR_AAM_ = (6, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        IRIS_T_IR_AAM = (6, JAS39GripenWeapons.IRIS_T_IR_AAM)
        A_Darter_IR_AAM = (6, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (6, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (6, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (6, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (6, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            6,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (6, Weapons.LAU_117_AGM_65H)
        _3_x_Brimstone_Laser_Guided_Missile = (
            6,
            JAS39GripenWeapons._3_x_Brimstone_Laser_Guided_Missile,
        )
        _3_x_SPEAR_3_Anti_Radiation_Missile = (
            6,
            JAS39GripenWeapons._3_x_SPEAR_3_Anti_Radiation_Missile,
        )
        _3_x_SPEAR_EW_Decoy = (6, JAS39GripenWeapons._3_x_SPEAR_EW_Decoy)
        RBS_15_Mk4_Gungnir_Anti_ship_Missile = (
            6,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile,
        )
        RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_ = (
            6,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_,
        )
        MAR_1_High_Speed_Anti_Radiation_Missile = (
            6,
            JAS39GripenWeapons.MAR_1_High_Speed_Anti_Radiation_Missile,
        )
        GBU_49_500_lb_TV_Guided_Bomb = (
            6,
            JAS39GripenWeapons.GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_31_2000_lb_TV_Guided_Glide_Bomb = (
            6,
            JAS39GripenWeapons.GBU_31_2000_lb_TV_Guided_Glide_Bomb,
        )
        GBU_31_2000_lb_Penetrator_TV_Guided_Glide_Bomb = (
            6,
            JAS39GripenWeapons.GBU_31_2000_lb_Penetrator_TV_Guided_Glide_Bomb,
        )
        GBU_32_1000_lb_TV_Guided_Glide_Bomb = (
            6,
            JAS39GripenWeapons.GBU_32_1000_lb_TV_Guided_Glide_Bomb,
        )
        GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            6,
            JAS39GripenWeapons.GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb = (
            6,
            JAS39GripenWeapons._4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb,
        )
        GBU_12_500_lb_Laser_guided_Bomb = (
            6,
            JAS39GripenWeapons.GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_12_500_lb_Laser_guided_Bomb = (
            6,
            JAS39GripenWeapons._2_x_GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            6,
            JAS39GripenWeapons._2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _2_x_GBU_49_500_lb_TV_Guided_Bomb = (
            6,
            JAS39GripenWeapons._2_x_GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_10_2000_lb_Laser_guided_Bomb = (
            6,
            JAS39GripenWeapons.GBU_10_2000_lb_Laser_guided_Bomb,
        )
        GBU_16_1000_lb_Laser_guided_Bomb = (
            6,
            JAS39GripenWeapons.GBU_16_1000_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_16_1000_lb_Laser_guided_Bomb = (
            6,
            JAS39GripenWeapons._2_x_GBU_16_1000_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_32_1000_lb_TV_Guided_Glide_Bomb = (
            6,
            JAS39GripenWeapons._2_x_GBU_32_1000_lb_TV_Guided_Glide_Bomb,
        )
        DWS_39_MJ2_TV_Guided_Cluster_Bomb = (
            6,
            JAS39GripenWeapons.DWS_39_MJ2_TV_Guided_Cluster_Bomb,
        )
        DWS_39_MJ2_Anti_radiation_Cluster_Bomb = (
            6,
            JAS39GripenWeapons.DWS_39_MJ2_Anti_radiation_Cluster_Bomb,
        )
        Mk_82_500_lb_GP_Bomb = (6, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (6, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        Mk_84_2000_lb_GP_Bomb = (6, JAS39GripenWeapons.Mk_84_2000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (6, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _2_x_Mk_83_1000_lb_GP_Bomb = (6, JAS39GripenWeapons._2_x_Mk_83_1000_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            6,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        Drop_tank_1100_litre = (6, JAS39GripenWeapons.Drop_tank_1100_litre)
        M70B_HE_Unguided_rocket = (6, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (6, JAS39GripenWeapons.M70B_AP_Unguided_rocket)
        Storm_Shadow_Long_Range_Anti_Radiation_Cruise_missile = (
            6,
            JAS39GripenWeapons.Storm_Shadow_Long_Range_Anti_Radiation_Cruise_missile,
        )
        KEPD_350_Long_Range_Anti_Radiation_Cruise_missile = (
            6,
            JAS39GripenWeapons.KEPD_350_Long_Range_Anti_Radiation_Cruise_missile,
        )

    class Pylon7:
        IRIS_T_IR_AAM = (7, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (7, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (7, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (7, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (7, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (7, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (7, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        RBS_15_Mk4_Gungnir_Anti_ship_Missile = (
            7,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile,
        )
        RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_ = (
            7,
            JAS39GripenWeapons.RBS_15_Mk4_Gungnir_Anti_ship_Missile__AI_,
        )
        MAR_1_High_Speed_Anti_Radiation_Missile = (
            7,
            JAS39GripenWeapons.MAR_1_High_Speed_Anti_Radiation_Missile,
        )
        GBU_49_500_lb_TV_Guided_Bomb = (
            7,
            JAS39GripenWeapons.GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_32_1000_lb_TV_Guided_Glide_Bomb = (
            7,
            JAS39GripenWeapons.GBU_32_1000_lb_TV_Guided_Glide_Bomb,
        )
        GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            7,
            JAS39GripenWeapons.GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb = (
            7,
            JAS39GripenWeapons._4_x_GBU_39_SDB_285_lb_TV_Guided_Glide_Bomb,
        )
        GBU_12_500_lb_Laser_guided_Bomb = (
            7,
            JAS39GripenWeapons.GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_12_500_lb_Laser_guided_Bomb = (
            7,
            JAS39GripenWeapons._2_x_GBU_12_500_lb_Laser_guided_Bomb,
        )
        _2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb = (
            7,
            JAS39GripenWeapons._2_x_GBU_38_500_lb_TV_Guided_Glide_Bomb,
        )
        _2_x_GBU_49_500_lb_TV_Guided_Bomb = (
            7,
            JAS39GripenWeapons._2_x_GBU_49_500_lb_TV_Guided_Bomb,
        )
        GBU_16_1000_lb_Laser_guided_Bomb = (
            7,
            JAS39GripenWeapons.GBU_16_1000_lb_Laser_guided_Bomb,
        )
        DWS_39_MJ2_TV_Guided_Cluster_Bomb = (
            7,
            JAS39GripenWeapons.DWS_39_MJ2_TV_Guided_Cluster_Bomb,
        )
        DWS_39_MJ2_Anti_radiation_Cluster_Bomb = (
            7,
            JAS39GripenWeapons.DWS_39_MJ2_Anti_radiation_Cluster_Bomb,
        )
        Mk_82_500_lb_GP_Bomb = (7, JAS39GripenWeapons.Mk_82_500_lb_GP_Bomb)
        Mk_83_1000_lb_GP_Bomb = (7, JAS39GripenWeapons.Mk_83_1000_lb_GP_Bomb)
        _2_x_Mk_82_500_lb_GP_Bomb = (7, JAS39GripenWeapons._2_x_Mk_82_500_lb_GP_Bomb)
        _4_x_M_71_120_kg_GP_Bomb_Low_drag_ = (
            7,
            JAS39GripenWeapons._4_x_M_71_120_kg_GP_Bomb_Low_drag_,
        )
        M70B_HE_Unguided_rocket = (7, JAS39GripenWeapons.M70B_HE_Unguided_rocket)
        M70B_AP_Unguided_rocket = (7, JAS39GripenWeapons.M70B_AP_Unguided_rocket)
        _3_x_Brimstone_Laser_Guided_Missile = (
            7,
            JAS39GripenWeapons._3_x_Brimstone_Laser_Guided_Missile,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        _3_x_SPEAR_3_Anti_Radiation_Missile = (
            7,
            JAS39GripenWeapons._3_x_SPEAR_3_Anti_Radiation_Missile,
        )
        _3_x_SPEAR_EW_Decoy = (7, JAS39GripenWeapons._3_x_SPEAR_EW_Decoy)

    class Pylon8:
        IRIS_T_IR_AAM = (8, JAS39GripenWeapons.IRIS_T_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM_ = (8, JAS39GripenWeapons.AIM_9L_Sidewinder_IR_AAM_)
        A_Darter_IR_AAM = (8, JAS39GripenWeapons.A_Darter_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM_ = (8, JAS39GripenWeapons.AIM_9M_Sidewinder_IR_AAM_)
        AIM_9X_Sidewinder_IR_AAM_ = (8, JAS39GripenWeapons.AIM_9X_Sidewinder_IR_AAM_)
        Python_5_IR_AAM = (8, JAS39GripenWeapons.Python_5_IR_AAM)
        AIM_132_ASRAAM_IR_AAM = (8, JAS39GripenWeapons.AIM_132_ASRAAM_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (8, Weapons.Smokewinder___red)
        Smokewinder___green = (8, Weapons.Smokewinder___green)
        Smokewinder___blue = (8, Weapons.Smokewinder___blue)
        Smokewinder___white = (8, Weapons.Smokewinder___white)
        Smokewinder___yellow = (8, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (8, Weapons.Smokewinder___orange)

    class Pylon9:
        Litening_III_Targeting_Pod_FLIR = (
            9,
            JAS39GripenWeapons.Litening_III_Targeting_Pod_FLIR,
        )

    class Pylon10:
        Integrated_ELINT = (10, JAS39GripenWeapons.Integrated_ELINT)

    class Pylon11:
        EWS_39_Integrated_ECM = (11, JAS39GripenWeapons.EWS_39_Integrated_ECM)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.SEAD,
        task.AntishipStrike,
        task.CAS,
        task.GroundAttack,
        task.PinpointStrike,
        task.RunwayAttack,
    ]
    task_default = task.CAS
