from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class JAS39GripenWeapons:
    JAS_ARAKM70BAP = {
        "clsid": "JAS_ARAKM70BAP",
        "name": "ARAK M70B AP",
        "weight": 372.2,
    }
    JAS_ARAKM70BHE = {
        "clsid": "JAS_ARAKM70BHE",
        "name": "ARAK M70B HE",
        "weight": 372.2,
    }
    JAS_BK90 = {
        "clsid": "JAS_BK90",
        "name": "BK-90 Unguided Cluster Munition",
        "weight": 605,
    }
    JAS_BRIMSTONE = {
        "clsid": "JAS_BRIMSTONE",
        "name": "Brimstone Laser Guided Missile",
        "weight": 195.5,
    }
    JAS_GBU10_TV = {
        "clsid": "JAS_GBU10_TV",
        "name": "GBU-10 2000 lb TV-guided Bomb",
        "weight": 934,
    }
    JAS_GBU12 = {
        "clsid": "JAS_GBU12",
        "name": "GBU-12 500 lb Laser-guided Bomb",
        "weight": 275,
    }
    JAS_GBU16_TV = {
        "clsid": "JAS_GBU16_TV",
        "name": "GBU-16 1000lb TV Guided Bomb",
        "weight": 934,
    }
    JAS_GBU31 = {
        "clsid": "JAS_GBU31",
        "name": "GBU-31 2000lb TV Guided Glide-Bomb",
        "weight": 934,
    }
    JAS_GBU49_TV = {
        "clsid": "JAS_GBU49_TV",
        "name": "GBU-49 500lb TV Guided Bomb",
        "weight": 275,
    }
    JAS_IRIS_T = {
        "clsid": "JAS_IRIS-T",
        "name": "Rb98 IRIS-T Sidewinder IR AAM",
        "weight": 88.4,
    }
    JAS_Litening = {
        "clsid": "JAS_Litening",
        "name": "Litening III POD (LLTV)",
        "weight": 295,
    }
    JAS_MAR_1 = {
        "clsid": "JAS_MAR-1",
        "name": "MAR-1 High Speed Anti-Radiation Missile",
        "weight": 350,
    }
    JAS_Meteor = {
        "clsid": "JAS_Meteor",
        "name": "Rb101 Meteor BVRAAM Active Rdr AAM",
        "weight": 191,
    }
    JAS_RB15F = {
        "clsid": "JAS_RB15F",
        "name": "RBS-15 Mk. IV Gungnir Radiation Seeking Anti-ship Missile ",
        "weight": None,
    }
    JAS_RB75T = {
        "clsid": "JAS_RB75T",
        "name": "Rb-75T (AGM-65E Maverick) (Laser ASM Lg Whd)",
        "weight": 210,
    }
    JAS_Rb74 = {
        "clsid": "JAS_Rb74",
        "name": "Rb74 AIM-9L Sidewinder IR AAM",
        "weight": 90,
    }
    JAS_Rb99 = {
        "clsid": "JAS_Rb99",
        "name": "Rb99 AIM-120B AMRAAM Active Rdr AAM",
        "weight": 157,
    }
    JAS_Rb99_DUAL = {
        "clsid": "JAS_Rb99_DUAL",
        "name": "Rb99 AIM-120B AMRAAM Active Rdr AAM x 2",
        "weight": 313,
    }
    JAS_Stormshadow = {
        "clsid": "JAS_Stormshadow",
        "name": "Storm Shadow Long Range Anti-Radiation Cruise-missile",
        "weight": None,
    }
    JAS_TANK1100 = {
        "clsid": "JAS_TANK1100",
        "name": "External drop tank 1100 litre",
        "weight": 1019,
    }
    JAS_TANK1700 = {
        "clsid": "JAS_TANK1700",
        "name": "External drop tank 1700 litre",
        "weight": 1533,
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
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Pylon1:
        JAS_IRIS_T = (1, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (1, JAS39GripenWeapons.JAS_Rb74)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        JAS_IRIS_T = (2, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (2, JAS39GripenWeapons.JAS_Rb74)
        JAS_Meteor = (2, JAS39GripenWeapons.JAS_Meteor)
        JAS_Rb99 = (2, JAS39GripenWeapons.JAS_Rb99)
        JAS_Rb99_DUAL = (2, JAS39GripenWeapons.JAS_Rb99_DUAL)
        LAU_115_2_LAU_127_AIM_120C = (2, Weapons.LAU_115_2_LAU_127_AIM_120C)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            2,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )

    # ERRR <CLEAN>

    class Pylon3:
        JAS_Meteor = (3, JAS39GripenWeapons.JAS_Meteor)
        JAS_Rb99 = (3, JAS39GripenWeapons.JAS_Rb99)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            3,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        JAS_TANK1100 = (3, JAS39GripenWeapons.JAS_TANK1100)
        JAS_TANK1700 = (3, JAS39GripenWeapons.JAS_TANK1700)

    # ERRR <CLEAN>

    class Pylon4:
        L_081_Fantasmagoria_ELINT_pod = (4, Weapons.L_081_Fantasmagoria_ELINT_pod)

    class Pylon5:
        JAS_TANK1100 = (5, JAS39GripenWeapons.JAS_TANK1100)
        JAS_Meteor = (5, JAS39GripenWeapons.JAS_Meteor)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            5,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        JAS_Rb99 = (5, JAS39GripenWeapons.JAS_Rb99)
        JAS_Rb99_DUAL = (5, JAS39GripenWeapons.JAS_Rb99_DUAL)

    # ERRR <CLEAN>

    class Pylon6:
        L005_Sorbtsiya_ECM_pod__left_ = (6, Weapons.L005_Sorbtsiya_ECM_pod__left_)

    class Pylon7:
        JAS_Litening = (7, JAS39GripenWeapons.JAS_Litening)

    # ERRR <CLEAN>

    class Pylon8:
        JAS_Meteor = (8, JAS39GripenWeapons.JAS_Meteor)
        JAS_Rb99 = (8, JAS39GripenWeapons.JAS_Rb99)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            8,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        JAS_TANK1100 = (8, JAS39GripenWeapons.JAS_TANK1100)
        JAS_TANK1700 = (8, JAS39GripenWeapons.JAS_TANK1700)

    # ERRR <CLEAN>

    class Pylon9:
        JAS_IRIS_T = (9, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (9, JAS39GripenWeapons.JAS_Rb74)
        JAS_Meteor = (9, JAS39GripenWeapons.JAS_Meteor)
        JAS_Rb99 = (9, JAS39GripenWeapons.JAS_Rb99)
        JAS_Rb99_DUAL = (9, JAS39GripenWeapons.JAS_Rb99_DUAL)
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            9,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )

    # ERRR <CLEAN>

    class Pylon10:
        JAS_IRIS_T = (10, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (10, JAS39GripenWeapons.JAS_Rb74)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (10, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

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
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Pylon1:
        JAS_IRIS_T = (1, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (1, JAS39GripenWeapons.JAS_Rb74)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        JAS_IRIS_T = (2, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (2, JAS39GripenWeapons.JAS_Rb74)
        JAS_RB75T = (2, JAS39GripenWeapons.JAS_RB75T)
        AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        JAS_BK90 = (2, JAS39GripenWeapons.JAS_BK90)
        JAS_RB15F = (2, JAS39GripenWeapons.JAS_RB15F)
        JAS_MAR_1 = (2, JAS39GripenWeapons.JAS_MAR_1)
        JAS_GBU12 = (2, JAS39GripenWeapons.JAS_GBU12)
        JAS_GBU49_TV = (2, JAS39GripenWeapons.JAS_GBU49_TV)
        # ERRR JAS_GBU16
        JAS_GBU16_TV = (2, JAS39GripenWeapons.JAS_GBU16_TV)
        # ERRR GBU12_TEST
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            2,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        JAS_ARAKM70BHE = (2, JAS39GripenWeapons.JAS_ARAKM70BHE)
        JAS_ARAKM70BAP = (2, JAS39GripenWeapons.JAS_ARAKM70BAP)
        JAS_BRIMSTONE = (2, JAS39GripenWeapons.JAS_BRIMSTONE)

    # ERRR <CLEAN>

    class Pylon3:
        JAS_RB75T = (3, JAS39GripenWeapons.JAS_RB75T)
        AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        JAS_Stormshadow = (3, JAS39GripenWeapons.JAS_Stormshadow)
        JAS_BK90 = (3, JAS39GripenWeapons.JAS_BK90)
        JAS_GBU31 = (3, JAS39GripenWeapons.JAS_GBU31)
        JAS_RB15F = (3, JAS39GripenWeapons.JAS_RB15F)
        JAS_MAR_1 = (3, JAS39GripenWeapons.JAS_MAR_1)
        JAS_GBU12 = (3, JAS39GripenWeapons.JAS_GBU12)
        JAS_GBU49_TV = (3, JAS39GripenWeapons.JAS_GBU49_TV)
        # ERRR JAS_GBU16
        JAS_GBU16_TV = (3, JAS39GripenWeapons.JAS_GBU16_TV)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            3,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        JAS_TANK1100 = (3, JAS39GripenWeapons.JAS_TANK1100)
        JAS_TANK1700 = (3, JAS39GripenWeapons.JAS_TANK1700)
        JAS_ARAKM70BHE = (3, JAS39GripenWeapons.JAS_ARAKM70BHE)
        JAS_ARAKM70BAP = (3, JAS39GripenWeapons.JAS_ARAKM70BAP)
        JAS_BRIMSTONE = (3, JAS39GripenWeapons.JAS_BRIMSTONE)

    # ERRR <CLEAN>

    class Pylon4:
        L_081_Fantasmagoria_ELINT_pod = (4, Weapons.L_081_Fantasmagoria_ELINT_pod)

    class Pylon5:
        JAS_Stormshadow = (5, JAS39GripenWeapons.JAS_Stormshadow)
        JAS_GBU12 = (5, JAS39GripenWeapons.JAS_GBU12)
        JAS_GBU49_TV = (5, JAS39GripenWeapons.JAS_GBU49_TV)
        # ERRR JAS_GBU16
        JAS_GBU16_TV = (5, JAS39GripenWeapons.JAS_GBU16_TV)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            5,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            5,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        JAS_TANK1100 = (5, JAS39GripenWeapons.JAS_TANK1100)
        # ERRR JAS_WMD7
        JAS_BRIMSTONE = (5, JAS39GripenWeapons.JAS_BRIMSTONE)

    # ERRR {INV-SMOKE-RED}
    # ERRR {INV-SMOKE-GREEN}
    # ERRR {INV-SMOKE-BLUE}
    # ERRR {INV-SMOKE-WHITE}
    # ERRR {INV-SMOKE-YELLOW}
    # ERRR {INV-SMOKE-ORANGE}
    # ERRR <CLEAN>

    class Pylon6:
        L005_Sorbtsiya_ECM_pod__left_ = (6, Weapons.L005_Sorbtsiya_ECM_pod__left_)

    class Pylon7:
        JAS_Litening = (7, JAS39GripenWeapons.JAS_Litening)

    # ERRR <CLEAN>

    class Pylon8:
        JAS_RB75T = (8, JAS39GripenWeapons.JAS_RB75T)
        AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            8,
            Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        JAS_Stormshadow = (8, JAS39GripenWeapons.JAS_Stormshadow)
        JAS_BK90 = (8, JAS39GripenWeapons.JAS_BK90)
        JAS_GBU31 = (8, JAS39GripenWeapons.JAS_GBU31)
        JAS_RB15F = (8, JAS39GripenWeapons.JAS_RB15F)
        JAS_MAR_1 = (8, JAS39GripenWeapons.JAS_MAR_1)
        JAS_GBU12 = (8, JAS39GripenWeapons.JAS_GBU12)
        JAS_GBU49_TV = (8, JAS39GripenWeapons.JAS_GBU49_TV)
        # ERRR JAS_GBU16
        JAS_GBU16_TV = (8, JAS39GripenWeapons.JAS_GBU16_TV)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            8,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        JAS_TANK1100 = (8, JAS39GripenWeapons.JAS_TANK1100)
        JAS_TANK1700 = (8, JAS39GripenWeapons.JAS_TANK1700)
        JAS_ARAKM70BHE = (8, JAS39GripenWeapons.JAS_ARAKM70BHE)
        JAS_ARAKM70BAP = (8, JAS39GripenWeapons.JAS_ARAKM70BAP)
        JAS_BRIMSTONE = (8, JAS39GripenWeapons.JAS_BRIMSTONE)

    # ERRR <CLEAN>

    class Pylon9:
        JAS_IRIS_T = (9, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (9, JAS39GripenWeapons.JAS_Rb74)
        JAS_RB75T = (9, JAS39GripenWeapons.JAS_RB75T)
        AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        JAS_BK90 = (9, JAS39GripenWeapons.JAS_BK90)
        JAS_RB15F = (9, JAS39GripenWeapons.JAS_RB15F)
        JAS_MAR_1 = (9, JAS39GripenWeapons.JAS_MAR_1)
        JAS_GBU12 = (9, JAS39GripenWeapons.JAS_GBU12)
        JAS_GBU49_TV = (9, JAS39GripenWeapons.JAS_GBU49_TV)
        # ERRR JAS_GBU16
        JAS_GBU16_TV = (9, JAS39GripenWeapons.JAS_GBU16_TV)
        # ERRR GBU12_TEST
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            9,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            9,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        JAS_ARAKM70BHE = (9, JAS39GripenWeapons.JAS_ARAKM70BHE)
        JAS_ARAKM70BAP = (9, JAS39GripenWeapons.JAS_ARAKM70BAP)
        JAS_BRIMSTONE = (9, JAS39GripenWeapons.JAS_BRIMSTONE)

    # ERRR <CLEAN>

    class Pylon10:
        JAS_IRIS_T = (10, JAS39GripenWeapons.JAS_IRIS_T)
        JAS_Rb74 = (10, JAS39GripenWeapons.JAS_Rb74)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (10, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.SEAD,
        task.AntishipStrike,
        task.CAS,
        task.GroundAttack,
        task.PinpointStrike,
        task.RunwayAttack,
    ]
    task_default = task.CAS
