from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class EurofighterWeapons:
    IRIS_T = {"clsid": "{irist}", "name": "Iris-T infrared-guided AAM", "weight": 85}
    AIM_132 = {"clsid": "{aim132}", "name": "AIM-132 infrared-guided AAM", "weight": 90}
    METEOR = {
        "clsid": "{Meteor}",
        "name": "Meteor active radar guided BVRAAM",
        "weight": 90,
    }
    EF_FuelTank_1000L = {
        "clsid": "{EF_FuelTank_1000L}",
        "name": "Central fuel tank (1000L)",
        "weight": 1190,
    }


inject_weapons(EurofighterWeapons)


class Eurofighter(PlaneType):
    id = "Eurofighter"
    flyable = True
    height = 5.29
    width = 10.94
    length = 15.96
    fuel_max = 4223
    max_speed = 2649.996
    chaff = 320
    flare = 32
    charge_total = 356
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Pylon1:
        IRIS_T = (1, EurofighterWeapons.IRIS_T)
        AIM_132 = (1, EurofighterWeapons.AIM_132)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_3_GBU_12 = (2, Weapons.BRU_42_3_GBU_12)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82_Snakeye = (2, Weapons._3_Mk_82_Snakeye)
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            2,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        ALARM = (2, Weapons.ALARM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            2,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        IRIS_T = (2, EurofighterWeapons.IRIS_T)
        AIM_132 = (2, EurofighterWeapons.AIM_132)
        METEOR = (2, EurofighterWeapons.METEOR)

    class Pylon3:
        EF_FuelTank_1000L = (3, EurofighterWeapons.EF_FuelTank_1000L)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_3_GBU_12 = (3, Weapons.BRU_42_3_GBU_12)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82_Snakeye = (3, Weapons._3_Mk_82_Snakeye)
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        ALARM = (3, Weapons.ALARM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            3,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        IRIS_T = (3, EurofighterWeapons.IRIS_T)
        AIM_132 = (3, EurofighterWeapons.AIM_132)
        METEOR = (3, EurofighterWeapons.METEOR)

    class Pylon4:
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            4,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_3_GBU_12 = (4, Weapons.BRU_42_3_GBU_12)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            4,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82_Snakeye = (4, Weapons._3_Mk_82_Snakeye)
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            4,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            4,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        ALARM = (4, Weapons.ALARM)

    class Pylon5:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            5,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_132 = (5, EurofighterWeapons.AIM_132)
        METEOR = (5, EurofighterWeapons.METEOR)

    class Pylon6:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            6,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_132 = (6, EurofighterWeapons.AIM_132)
        METEOR = (6, EurofighterWeapons.METEOR)

    class Pylon7:
        EF_FuelTank_1000L = (7, EurofighterWeapons.EF_FuelTank_1000L)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        _3_Mk_83 = (7, Weapons._3_Mk_83)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            7,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82_Snakeye = (7, Weapons._3_Mk_82_Snakeye)
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            7,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            7,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    class Pylon8:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            8,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_132 = (8, EurofighterWeapons.AIM_132)
        METEOR = (8, EurofighterWeapons.METEOR)

    class Pylon9:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            9,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_132 = (9, EurofighterWeapons.AIM_132)
        METEOR = (9, EurofighterWeapons.METEOR)

    class Pylon10:
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_3_GBU_12 = (10, Weapons.BRU_42_3_GBU_12)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            10,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82_Snakeye = (10, Weapons._3_Mk_82_Snakeye)
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            10,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            10,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            10,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            10,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        ALARM = (10, Weapons.ALARM)

    class Pylon11:
        EF_FuelTank_1000L = (11, EurofighterWeapons.EF_FuelTank_1000L)
        GBU_12___500lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            11,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_3_GBU_12 = (11, Weapons.BRU_42_3_GBU_12)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (11, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            11,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            11,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            11,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            11,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            11,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82_Snakeye = (11, Weapons._3_Mk_82_Snakeye)
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            11,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            11,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            11,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            11,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        ALARM = (11, Weapons.ALARM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            11,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        IRIS_T = (11, EurofighterWeapons.IRIS_T)
        AIM_132 = (11, EurofighterWeapons.AIM_132)
        METEOR = (11, EurofighterWeapons.METEOR)

    class Pylon12:
        GBU_12___500lb_Laser_Guided_Bomb = (
            12,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            12,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_3_GBU_12 = (12, Weapons.BRU_42_3_GBU_12)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            12,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            12,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            12,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (12, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            12,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            12,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            12,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            12,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            12,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82_Snakeye = (12, Weapons._3_Mk_82_Snakeye)
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            12,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            12,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            12,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            12,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        ALARM = (12, Weapons.ALARM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            12,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_9M_Sidewinder_IR_AAM = (12, Weapons.AIM_9M_Sidewinder_IR_AAM)
        IRIS_T = (12, EurofighterWeapons.IRIS_T)
        AIM_132 = (12, EurofighterWeapons.AIM_132)
        METEOR = (12, EurofighterWeapons.METEOR)

    class Pylon13:
        IRIS_T = (13, EurofighterWeapons.IRIS_T)
        AIM_132 = (13, EurofighterWeapons.AIM_132)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (13, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (13, Weapons.Smokewinder___red)
        Smokewinder___green = (13, Weapons.Smokewinder___green)
        Smokewinder___blue = (13, Weapons.Smokewinder___blue)
        Smokewinder___white = (13, Weapons.Smokewinder___white)
        Smokewinder___yellow = (13, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (13, Weapons.Smokewinder___orange)

    pylons = {1, 13, 12, 11, 2, 3, 4, 10, 5, 6, 9, 8, 7}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.SEAD,
    ]
    task_default = task.CAP
