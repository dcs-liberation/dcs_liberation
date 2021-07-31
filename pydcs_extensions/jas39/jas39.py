from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

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
    JAS39_AIM120B = {
        "clsid": "JAS39_AIM120B",
        "name": "AIM-120B AMRAAM Active Rdr AAM",
        "weight": 157,
    }
    JAS39_AIM120C5 = {
        "clsid": "JAS39_AIM120C5",
        "name": "AIM-120C-5 AMRAAM Active Rdr AAM",
        "weight": 162.5,
    }
    JAS39_AIM120C7 = {
        "clsid": "JAS39_AIM120C7",
        "name": "AIM-120C-7 AMRAAM Active Rdr AAM",
        "weight": 162.5,
    }
    JAS39_AIM_9L = {
        "clsid": "JAS39_AIM-9L",
        "name": "AIM-9L Sidewinder IR AAM",
        "weight": 86,
    }
    JAS39_AIM_9M = {
        "clsid": "JAS39_AIM-9M",
        "name": "AIM-9M Sidewinder IR AAM",
        "weight": 86,
    }
    JAS39_AIM_9X = {
        "clsid": "JAS39_AIM-9X",
        "name": "AIM-9X Sidewinder IR AAM",
        "weight": 86.5,
    }
    JAS39_ASRAAM = {
        "clsid": "JAS39_ASRAAM",
        "name": "AIM-132 ASRAAM IR AAM",
        "weight": 89,
    }
    JAS39_A_DARTER = {
        "clsid": "JAS39_A-DARTER",
        "name": "A-Darter IR AAM",
        "weight": 90,
    }
    JAS39_BRIMSTONE = {
        "clsid": "JAS39_BRIMSTONE",
        "name": "Brimstone Laser Guided Missile",
        "weight": 195.5,
    }
    JAS39_Derby = {
        "clsid": "JAS39_Derby",
        "name": "I-Derby ER BVRAAM Active Rdr AAM",
        "weight": 119,
    }
    JAS39_DWS39 = {
        "clsid": "JAS39_DWS39",
        "name": "DWS39 Unguided Cluster Munition",
        "weight": 605,
    }
    JAS39_GBU10 = {
        "clsid": "JAS39_GBU10",
        "name": "GBU-10 2000 lb Laser-guided Bomb",
        "weight": 934,
    }
    JAS39_GBU12 = {
        "clsid": "JAS39_GBU12",
        "name": "GBU-12 500 lb Laser-guided Bomb",
        "weight": 275,
    }
    JAS39_GBU16 = {
        "clsid": "JAS39_GBU16",
        "name": "GBU-16 1000 lb Laser-guided Bomb",
        "weight": 454,
    }
    JAS39_GBU31 = {
        "clsid": "JAS39_GBU31",
        "name": "GBU-31 2000lb TV Guided Glide-Bomb",
        "weight": 934,
    }
    JAS39_GBU32 = {
        "clsid": "JAS39_GBU32",
        "name": "GBU-32 1000lb TV Guided Glide-Bomb",
        "weight": 454,
    }
    JAS39_GBU38 = {
        "clsid": "JAS39_GBU38",
        "name": "GBU-38 500lb TV Guided Glide-Bomb",
        "weight": 241,
    }
    JAS39_GBU49 = {
        "clsid": "JAS39_GBU49",
        "name": "GBU-49 500lb TV Guided Bomb",
        "weight": 241,
    }
    JAS39_IRIS_T = {"clsid": "JAS39_IRIS-T", "name": "IRIS-T IR AAM", "weight": 88.4}
    JAS39_Litening = {
        "clsid": "JAS39_Litening",
        "name": "Litening III Targeting Pod",
        "weight": 208,
    }
    JAS39_M70BAP = {
        "clsid": "JAS39_M70BAP",
        "name": "M70B AP Unguided rocket",
        "weight": 372.2,
    }
    JAS39_M70BHE = {
        "clsid": "JAS39_M70BHE",
        "name": "M70B HE Unguided rocket",
        "weight": 372.2,
    }
    JAS39_M71LD = {
        "clsid": "JAS39_M71LD",
        "name": "4x M/71 120kg GP Bomb Low-drag",
        "weight": 605,
    }
    JAS39_MAR_1 = {
        "clsid": "JAS39_MAR-1",
        "name": "MAR-1 High Speed Anti-Radiation Missile",
        "weight": 350,
    }
    JAS39_Meteor = {
        "clsid": "JAS39_Meteor",
        "name": "Meteor BVRAAM Active Rdr AAM",
        "weight": 191,
    }
    JAS39_PYTHON_5 = {
        "clsid": "JAS39_PYTHON-5",
        "name": "Python-5 IR AAM",
        "weight": 106,
    }
    JAS39_RBS15 = {
        "clsid": "JAS39_RBS15",
        "name": "RBS-15 Mk4 Gungnir Anti-ship Missile",
        "weight": 650,
    }
    JAS39_RBS15AI = {
        "clsid": "JAS39_RBS15AI",
        "name": "RBS-15 Mk4 Gungnir Anti-ship Missile (AI)",
        "weight": 650,
    }
    JAS39_SDB = {
        "clsid": "JAS39_SDB",
        "name": "GBU-39 SDB 285lb TV Guided Glide-Bomb",
        "weight": 661,
    }
    JAS39_STORMSHADOW = {
        "clsid": "JAS39_STORMSHADOW",
        "name": "Storm Shadow Long Range Anti-Radiation Cruise-missile",
        "weight": 1300,
    }
    JAS39_TANK1100 = {
        "clsid": "JAS39_TANK1100",
        "name": "Drop tank 1100 litre",
        "weight": 1019,
    }
    JAS39_TANK1700 = {
        "clsid": "JAS39_TANK1700",
        "name": "Drop tank 1700 litre",
        "weight": 1533,
    }
    Litening_III_Targeting_Pod_FLIR = {
        "clsid": "{JAS39_FLIR}",
        "name": "Litening III Targeting Pod FLIR",
        "weight": 2,
    }


inject_weapons(JAS39GripenWeapons)


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
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Pylon1:
        JAS39_IRIS_T = (1, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (1, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (1, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (1, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (1, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (1, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (1, JAS39GripenWeapons.JAS39_ASRAAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        JAS39_IRIS_T = (2, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (2, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (2, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (2, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (2, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (2, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (2, JAS39GripenWeapons.JAS39_ASRAAM)
        JAS39_Meteor = (2, JAS39GripenWeapons.JAS39_Meteor)
        JAS39_AIM120B = (2, JAS39GripenWeapons.JAS39_AIM120B)
        JAS39_AIM120C5 = (2, JAS39GripenWeapons.JAS39_AIM120C5)
        JAS39_AIM120C7 = (2, JAS39GripenWeapons.JAS39_AIM120C7)
        JAS39_Derby = (2, JAS39GripenWeapons.JAS39_Derby)

    class Pylon3:
        JAS39_AIM_9L = (3, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_IRIS_T = (3, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_A_DARTER = (3, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (3, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (3, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (3, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (3, JAS39GripenWeapons.JAS39_ASRAAM)
        JAS39_Meteor = (3, JAS39GripenWeapons.JAS39_Meteor)
        JAS39_AIM120B = (3, JAS39GripenWeapons.JAS39_AIM120B)
        JAS39_AIM120C5 = (3, JAS39GripenWeapons.JAS39_AIM120C5)
        JAS39_AIM120C7 = (3, JAS39GripenWeapons.JAS39_AIM120C7)
        JAS39_Derby = (3, JAS39GripenWeapons.JAS39_Derby)
        JAS39_TANK1100 = (3, JAS39GripenWeapons.JAS39_TANK1100)
        JAS39_TANK1700 = (3, JAS39GripenWeapons.JAS39_TANK1700)

    class Pylon4:
        JAS39_TANK1100 = (4, JAS39GripenWeapons.JAS39_TANK1100)

    class Pylon5:
        JAS39_Litening = (5, JAS39GripenWeapons.JAS39_Litening)

    class Pylon6:
        JAS39_AIM_9L = (6, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_IRIS_T = (6, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_A_DARTER = (6, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (6, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (6, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (6, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (6, JAS39GripenWeapons.JAS39_ASRAAM)
        JAS39_Meteor = (6, JAS39GripenWeapons.JAS39_Meteor)
        JAS39_AIM120B = (6, JAS39GripenWeapons.JAS39_AIM120B)
        JAS39_AIM120C5 = (6, JAS39GripenWeapons.JAS39_AIM120C5)
        JAS39_AIM120C7 = (6, JAS39GripenWeapons.JAS39_AIM120C7)
        JAS39_Derby = (6, JAS39GripenWeapons.JAS39_Derby)
        JAS39_TANK1100 = (6, JAS39GripenWeapons.JAS39_TANK1100)
        JAS39_TANK1700 = (6, JAS39GripenWeapons.JAS39_TANK1700)

    class Pylon7:
        JAS39_IRIS_T = (7, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (7, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (7, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (7, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (7, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (7, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (7, JAS39GripenWeapons.JAS39_ASRAAM)
        JAS39_Meteor = (7, JAS39GripenWeapons.JAS39_Meteor)
        JAS39_AIM120B = (7, JAS39GripenWeapons.JAS39_AIM120B)
        JAS39_AIM120C5 = (7, JAS39GripenWeapons.JAS39_AIM120C5)
        JAS39_AIM120C7 = (7, JAS39GripenWeapons.JAS39_AIM120C7)
        JAS39_Derby = (7, JAS39GripenWeapons.JAS39_Derby)

    class Pylon8:
        JAS39_IRIS_T = (8, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (8, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (8, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (8, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (8, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (8, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (8, JAS39GripenWeapons.JAS39_ASRAAM)
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
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Pylon1:
        JAS39_IRIS_T = (1, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (1, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (1, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (1, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (1, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (1, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (1, JAS39GripenWeapons.JAS39_ASRAAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        JAS39_IRIS_T = (2, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (2, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (2, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (2, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (2, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (2, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (2, JAS39GripenWeapons.JAS39_ASRAAM)
        JAS39_RBS15 = (2, JAS39GripenWeapons.JAS39_RBS15)
        JAS39_RBS15AI = (2, JAS39GripenWeapons.JAS39_RBS15AI)
        JAS39_MAR_1 = (2, JAS39GripenWeapons.JAS39_MAR_1)
        JAS39_GBU49 = (2, JAS39GripenWeapons.JAS39_GBU49)
        JAS39_GBU32 = (2, JAS39GripenWeapons.JAS39_GBU32)
        JAS39_GBU38 = (2, JAS39GripenWeapons.JAS39_GBU38)
        JAS39_SDB = (2, JAS39GripenWeapons.JAS39_SDB)
        JAS39_GBU12 = (2, JAS39GripenWeapons.JAS39_GBU12)
        JAS39_GBU16 = (2, JAS39GripenWeapons.JAS39_GBU16)
        JAS39_DWS39 = (2, JAS39GripenWeapons.JAS39_DWS39)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        JAS39_M71LD = (2, JAS39GripenWeapons.JAS39_M71LD)
        JAS39_M70BHE = (2, JAS39GripenWeapons.JAS39_M70BHE)
        JAS39_M70BAP = (2, JAS39GripenWeapons.JAS39_M70BAP)
        JAS39_BRIMSTONE = (2, JAS39GripenWeapons.JAS39_BRIMSTONE)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (2, Weapons.LAU_117_AGM_65H)

    class Pylon3:
        JAS39_AIM_9L = (3, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_IRIS_T = (3, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_A_DARTER = (3, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (3, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (3, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (3, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (3, JAS39GripenWeapons.JAS39_ASRAAM)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        JAS39_BRIMSTONE = (3, JAS39GripenWeapons.JAS39_BRIMSTONE)
        JAS39_RBS15 = (3, JAS39GripenWeapons.JAS39_RBS15)
        JAS39_RBS15AI = (3, JAS39GripenWeapons.JAS39_RBS15AI)
        JAS39_MAR_1 = (3, JAS39GripenWeapons.JAS39_MAR_1)
        JAS39_GBU49 = (3, JAS39GripenWeapons.JAS39_GBU49)
        JAS39_GBU31 = (3, JAS39GripenWeapons.JAS39_GBU31)
        JAS39_GBU32 = (3, JAS39GripenWeapons.JAS39_GBU32)
        JAS39_GBU38 = (3, JAS39GripenWeapons.JAS39_GBU38)
        JAS39_SDB = (3, JAS39GripenWeapons.JAS39_SDB)
        JAS39_GBU12 = (3, JAS39GripenWeapons.JAS39_GBU12)
        JAS39_GBU10 = (3, JAS39GripenWeapons.JAS39_GBU10)
        JAS39_GBU16 = (3, JAS39GripenWeapons.JAS39_GBU16)
        JAS39_DWS39 = (3, JAS39GripenWeapons.JAS39_DWS39)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        JAS39_M71LD = (3, JAS39GripenWeapons.JAS39_M71LD)
        JAS39_TANK1100 = (3, JAS39GripenWeapons.JAS39_TANK1100)
        JAS39_TANK1700 = (3, JAS39GripenWeapons.JAS39_TANK1700)
        JAS39_M70BHE = (3, JAS39GripenWeapons.JAS39_M70BHE)
        JAS39_M70BAP = (3, JAS39GripenWeapons.JAS39_M70BAP)
        JAS39_STORMSHADOW = (3, JAS39GripenWeapons.JAS39_STORMSHADOW)

    class Pylon4:
        JAS39_BRIMSTONE = (4, JAS39GripenWeapons.JAS39_BRIMSTONE)
        JAS39_STORMSHADOW = (4, JAS39GripenWeapons.JAS39_STORMSHADOW)
        JAS39_GBU49 = (4, JAS39GripenWeapons.JAS39_GBU49)
        JAS39_GBU31 = (4, JAS39GripenWeapons.JAS39_GBU31)
        JAS39_GBU32 = (4, JAS39GripenWeapons.JAS39_GBU32)
        JAS39_GBU38 = (4, JAS39GripenWeapons.JAS39_GBU38)
        JAS39_SDB = (4, JAS39GripenWeapons.JAS39_SDB)
        JAS39_GBU10 = (4, JAS39GripenWeapons.JAS39_GBU10)
        JAS39_GBU12 = (4, JAS39GripenWeapons.JAS39_GBU12)
        JAS39_GBU16 = (4, JAS39GripenWeapons.JAS39_GBU16)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            4,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        JAS39_M71LD = (4, JAS39GripenWeapons.JAS39_M71LD)
        JAS39_TANK1100 = (4, JAS39GripenWeapons.JAS39_TANK1100)

    class Pylon5:
        JAS39_Litening = (5, JAS39GripenWeapons.JAS39_Litening)

    class Pylon6:
        JAS39_AIM_9L = (6, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_IRIS_T = (6, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_A_DARTER = (6, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (6, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (6, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (6, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (6, JAS39GripenWeapons.JAS39_ASRAAM)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            6,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (6, Weapons.LAU_117_AGM_65H)
        JAS39_BRIMSTONE = (6, JAS39GripenWeapons.JAS39_BRIMSTONE)
        JAS39_RBS15 = (6, JAS39GripenWeapons.JAS39_RBS15)
        JAS39_RBS15AI = (6, JAS39GripenWeapons.JAS39_RBS15AI)
        JAS39_MAR_1 = (6, JAS39GripenWeapons.JAS39_MAR_1)
        JAS39_GBU49 = (6, JAS39GripenWeapons.JAS39_GBU49)
        JAS39_GBU31 = (6, JAS39GripenWeapons.JAS39_GBU31)
        JAS39_GBU32 = (6, JAS39GripenWeapons.JAS39_GBU32)
        JAS39_GBU38 = (6, JAS39GripenWeapons.JAS39_GBU38)
        JAS39_SDB = (6, JAS39GripenWeapons.JAS39_SDB)
        JAS39_GBU12 = (6, JAS39GripenWeapons.JAS39_GBU12)
        JAS39_GBU10 = (6, JAS39GripenWeapons.JAS39_GBU10)
        JAS39_GBU16 = (6, JAS39GripenWeapons.JAS39_GBU16)
        JAS39_DWS39 = (6, JAS39GripenWeapons.JAS39_DWS39)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        JAS39_M71LD = (6, JAS39GripenWeapons.JAS39_M71LD)
        JAS39_TANK1100 = (6, JAS39GripenWeapons.JAS39_TANK1100)
        JAS39_TANK1700 = (6, JAS39GripenWeapons.JAS39_TANK1700)
        JAS39_M70BHE = (6, JAS39GripenWeapons.JAS39_M70BHE)
        JAS39_M70BAP = (6, JAS39GripenWeapons.JAS39_M70BAP)
        JAS39_STORMSHADOW = (6, JAS39GripenWeapons.JAS39_STORMSHADOW)

    class Pylon7:
        JAS39_IRIS_T = (7, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (7, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (7, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (7, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (7, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (7, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (7, JAS39GripenWeapons.JAS39_ASRAAM)
        JAS39_RBS15 = (7, JAS39GripenWeapons.JAS39_RBS15)
        JAS39_RBS15AI = (7, JAS39GripenWeapons.JAS39_RBS15AI)
        JAS39_MAR_1 = (7, JAS39GripenWeapons.JAS39_MAR_1)
        JAS39_GBU49 = (7, JAS39GripenWeapons.JAS39_GBU49)
        JAS39_GBU32 = (7, JAS39GripenWeapons.JAS39_GBU32)
        JAS39_GBU38 = (7, JAS39GripenWeapons.JAS39_GBU38)
        JAS39_SDB = (7, JAS39GripenWeapons.JAS39_SDB)
        JAS39_GBU12 = (7, JAS39GripenWeapons.JAS39_GBU12)
        JAS39_GBU16 = (7, JAS39GripenWeapons.JAS39_GBU16)
        JAS39_DWS39 = (7, JAS39GripenWeapons.JAS39_DWS39)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        JAS39_M71LD = (7, JAS39GripenWeapons.JAS39_M71LD)
        JAS39_M70BHE = (7, JAS39GripenWeapons.JAS39_M70BHE)
        JAS39_M70BAP = (7, JAS39GripenWeapons.JAS39_M70BAP)
        JAS39_BRIMSTONE = (7, JAS39GripenWeapons.JAS39_BRIMSTONE)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)

    class Pylon8:
        JAS39_IRIS_T = (8, JAS39GripenWeapons.JAS39_IRIS_T)
        JAS39_AIM_9L = (8, JAS39GripenWeapons.JAS39_AIM_9L)
        JAS39_A_DARTER = (8, JAS39GripenWeapons.JAS39_A_DARTER)
        JAS39_AIM_9M = (8, JAS39GripenWeapons.JAS39_AIM_9M)
        JAS39_AIM_9X = (8, JAS39GripenWeapons.JAS39_AIM_9X)
        JAS39_PYTHON_5 = (8, JAS39GripenWeapons.JAS39_PYTHON_5)
        JAS39_ASRAAM = (8, JAS39GripenWeapons.JAS39_ASRAAM)
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
