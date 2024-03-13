from typing import Dict, List, Set, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons
from dcs.unitpropertydescription import UnitPropertyDescription


from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsFA18EFG:
    AA42R_Buddy_Pod = {"clsid": "{AA42R}", "name": "AA42R Buddy Pod", "weight": 1520}
    ALQ_99Center = {"clsid": "{ALQ-99Center}", "name": "ALQ-99Center", "weight": 0}
    ALQ_99Wing = {"clsid": "{ALQ-99Wing}", "name": "ALQ-99Wing", "weight": 0}
    FLIR = {"clsid": "{FLIR}", "name": "FLIR", "weight": 0}
    FPU_12_Fuel_Tank_480_gallons = {
        "clsid": "{FPU_12_FUEL_TANK}",
        "name": "FPU-12 Fuel Tank 480 gallons",
        "weight": 1550,
    }
    FPU_12_Fuel_Tank_480_gallons_High_Vis = {
        "clsid": "{FPU_12_FUEL_TANKHighVis}",
        "name": "FPU-12 Fuel Tank 480 gallons High Vis",
        "weight": 1550,
    }
    TLAU_127 = {"clsid": "{TLAU_127}", "name": "TLAU_127", "weight": 0}
    USAFlag = {"clsid": "{USAFlag}", "name": "USAFlag", "weight": 0}
    AIM_120D_AMRAAM___Active_Rdr_AAM = {
        "clsid": "{C8E06185-7CD6-4C90-959F-044679E90751}",
        "name": "AIM-120D AMRAAM - Active Rdr AAM",
        "weight": 162.4,
    }
    LAU_115_2_LAU_127_AIM_120B = {
        "clsid": "LAU-115_2*LAU-127_AIM-120B",
        "name": "LAU-115 with 2 x LAU-127 AIM-120D AMRAAM - Active Rdr AAM",
        "weight": 469.8,
    }
    LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM = {
        "clsid": "{LAU-115 - AIM-120B}",
        "name": "LAU-115 with 1 x LAU-127 AIM-120D AMRAAM - Active Rdr AAM",
        "weight": 307.4,
    }
    LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM_ = {
        "clsid": "{LAU-115 - AIM-120B_R}",
        "name": "LAU-115 with 1 x LAU-127 AIM-120D AMRAAM - Active Rdr AAM",
        "weight": 307.4,
    }


inject_weapons(WeaponsFA18EFG)


@planemod
class FA_18E(PlaneType):
    id = "FA-18E"
    flyable = True
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 4900
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "OuterBoard": 0,
        "InnerBoard": 0,
        "HelmetMountedDevice": 1,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
    }

    class Properties:
        class OuterBoard:
            id = "OuterBoard"

            class Values:
                Single = 0
                Ripple = 1

        class InnerBoard:
            id = "InnerBoard"

            class Values:
                Single = 0
                Ripple = 1

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

    properties = {
        "OuterBoard": UnitPropertyDescription(
            identifier="OuterBoard",
            control="comboList",
            label="Outerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "InnerBoard": UnitPropertyDescription(
            identifier="InnerBoard",
            control="comboList",
            label="Innerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "FA-18E"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        CATM_9M = (1, Weapons.CATM_9M)
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        TLAU_127 = (2, Weapons.TLAU_127)
        AIM_120D_AMRAAM___Active_Rdr_AAM = (2, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        # ERRR {CATM-120C}
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR <CLEAN>
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_2_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (2, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon3:
        LAU_115_2_LAU_127_AIM_9M = (3, Weapons.LAU_115_2_LAU_127_AIM_9M)
        LAU_115_2_LAU_127_CATM_9M = (3, Weapons.LAU_115_2_LAU_127_CATM_9M)
        LAU_115_2_LAU_127_AIM_9L = (3, Weapons.LAU_115_2_LAU_127_AIM_9L)
        LAU_115_2_LAU_127_AIM_9X = (3, Weapons.LAU_115_2_LAU_127_AIM_9X)
        LAU_115_LAU_127_AIM_9X = (3, Weapons.LAU_115_LAU_127_AIM_9X)
        LAU_115_LAU_127_CATM_9M = (3, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (3, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (3, Weapons.LAU_115_LAU_127_AIM_9M)
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (3, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            3,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        AIM_120D_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (3, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (3, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
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
        BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb = (
            3,
            Weapons.BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb = (
            3,
            Weapons.BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_3_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (3, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon4:
        AIM_120D_AMRAAM___Active_Rdr_AAM = (4, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )

    class Pylon5:
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (5, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            5,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM = (
            5,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM,
        )
        LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (5, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (5, Weapons.LAU_115_2_LAU_127_AIM_120C)
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            5,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (5, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (5, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (5, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            5,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            5,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            5,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            5,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (5, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            5,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (5, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            5,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (5, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            5,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            5,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            5,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            5,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            5,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            5,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (5, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            5,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )

    class Pylon6:
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (6, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            6,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM = (
            6,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM,
        )
        LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (6, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (6, Weapons.LAU_115_2_LAU_127_AIM_120C)
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            6,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (6, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (6, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            6,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (6, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (6, Weapons.BDU_45B___500lb_Practice_Bomb)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            6,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            6,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb = (
            6,
            Weapons.BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb = (
            6,
            Weapons.BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            6,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            6,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            6,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (6, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            6,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (6, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            6,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            6,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            6,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            6,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            6,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            6,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (6, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            6,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )

    class Pylon7:
        LAU_115_2_LAU_127_AIM_9M = (7, Weapons.LAU_115_2_LAU_127_AIM_9M)
        LAU_115_2_LAU_127_CATM_9M = (7, Weapons.LAU_115_2_LAU_127_CATM_9M)
        LAU_115_2_LAU_127_AIM_9L = (7, Weapons.LAU_115_2_LAU_127_AIM_9L)
        LAU_115_2_LAU_127_AIM_9X = (7, Weapons.LAU_115_2_LAU_127_AIM_9X)
        LAU_115_LAU_127_AIM_9X = (7, Weapons.LAU_115_LAU_127_AIM_9X)
        LAU_115_LAU_127_CATM_9M = (7, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (7, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (7, Weapons.LAU_115_LAU_127_AIM_9M)
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (7, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            7,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        AIM_120D_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (7, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (7, Weapons.LAU_115_2_LAU_127_AIM_120C)
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (7, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb = (
            7,
            Weapons.BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb = (
            7,
            Weapons.BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            7,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            7,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (7, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_3_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (7, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon8:
        TLAU_127 = (8, Weapons.TLAU_127)
        AIM_120D_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        # ERRR {CATM-120C}
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR <CLEAN>
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_2_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (8, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        CATM_9M = (9, Weapons.CATM_9M)
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon10:
        AA42R_Buddy_Pod = (10, Weapons.AA42R_Buddy_Pod)
        FPU_12_Fuel_Tank_480_gallons = (10, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            10,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        USAFlag = (10, Weapons.USAFlag)
        Smoke_Generator___red_ = (10, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (10, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (10, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (10, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (10, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (10, Weapons.Smoke_Generator___orange_)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


from typing import Dict, List, Any


@planemod
class FA_18F(PlaneType):
    id = "FA-18F"
    flyable = True
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 4900
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "OuterBoard": 0,
        "InnerBoard": 0,
        "HelmetMountedDevice": 1,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
    }

    class Properties:
        class OuterBoard:
            id = "OuterBoard"

            class Values:
                Single = 0
                Ripple = 1

        class InnerBoard:
            id = "InnerBoard"

            class Values:
                Single = 0
                Ripple = 1

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

    properties = {
        "OuterBoard": UnitPropertyDescription(
            identifier="OuterBoard",
            control="comboList",
            label="Outerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "InnerBoard": UnitPropertyDescription(
            identifier="InnerBoard",
            control="comboList",
            label="Innerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "FA-18F"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        CATM_9M = (1, Weapons.CATM_9M)
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        TLAU_127 = (2, Weapons.TLAU_127)
        AIM_120D_AMRAAM___Active_Rdr_AAM = (2, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        # ERRR {CATM-120C}
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR <CLEAN>
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_2_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (2, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon3:
        LAU_115_2_LAU_127_AIM_9M = (3, Weapons.LAU_115_2_LAU_127_AIM_9M)
        LAU_115_2_LAU_127_CATM_9M = (3, Weapons.LAU_115_2_LAU_127_CATM_9M)
        LAU_115_2_LAU_127_AIM_9L = (3, Weapons.LAU_115_2_LAU_127_AIM_9L)
        LAU_115_2_LAU_127_AIM_9X = (3, Weapons.LAU_115_2_LAU_127_AIM_9X)
        LAU_115_LAU_127_AIM_9X = (3, Weapons.LAU_115_LAU_127_AIM_9X)
        LAU_115_LAU_127_CATM_9M = (3, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (3, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (3, Weapons.LAU_115_LAU_127_AIM_9M)
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (3, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            3,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        AIM_120D_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (3, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (3, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
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
        BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb = (
            3,
            Weapons.BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb = (
            3,
            Weapons.BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_3_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (3, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon4:
        AIM_120D_AMRAAM___Active_Rdr_AAM = (4, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )

    class Pylon5:
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (5, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            5,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM = (
            5,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM,
        )
        LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (5, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (5, Weapons.LAU_115_2_LAU_127_AIM_120C)
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            5,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (5, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (5, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (5, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            5,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            5,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            5,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            5,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (5, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            5,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (5, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            5,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (5, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            5,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            5,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            5,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            5,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            5,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            5,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (5, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            5,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )

    class Pylon6:
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (6, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            6,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM = (
            6,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120D_AMRAAM___Active_Rdr_AAM,
        )
        LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.LAU_115_with_1_x_LAU_127_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (6, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (6, Weapons.LAU_115_2_LAU_127_AIM_120C)
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            6,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (6, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (6, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            6,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (6, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (6, Weapons.BDU_45B___500lb_Practice_Bomb)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            6,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            6,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb = (
            6,
            Weapons.BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb = (
            6,
            Weapons.BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            6,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            6,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            6,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (6, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            6,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (6, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            6,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            6,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            6,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            6,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            6,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            6,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (6, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            6,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )

    class Pylon7:
        LAU_115_2_LAU_127_AIM_9M = (7, Weapons.LAU_115_2_LAU_127_AIM_9M)
        LAU_115_2_LAU_127_CATM_9M = (7, Weapons.LAU_115_2_LAU_127_CATM_9M)
        LAU_115_2_LAU_127_AIM_9L = (7, Weapons.LAU_115_2_LAU_127_AIM_9L)
        LAU_115_2_LAU_127_AIM_9X = (7, Weapons.LAU_115_2_LAU_127_AIM_9X)
        LAU_115_LAU_127_AIM_9X = (7, Weapons.LAU_115_LAU_127_AIM_9X)
        LAU_115_LAU_127_CATM_9M = (7, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (7, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (7, Weapons.LAU_115_LAU_127_AIM_9M)
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        FPU_12_Fuel_Tank_480_gallons = (7, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            7,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        AIM_120D_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120B = (7, Weapons.LAU_115_2_LAU_127_AIM_120B)
        LAU_115_2_LAU_127_AIM_120C = (7, Weapons.LAU_115_2_LAU_127_AIM_120C)
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_CATM_65K = (7, Weapons.LAU_117_CATM_65K)
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb = (
            7,
            Weapons.BRU_33_with_2_x_BDU_45___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb = (
            7,
            Weapons.BRU_33_with_2_x_BDU_45B___500lb_Practice_Bomb,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            7,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            7,
            Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        # ERRR <CLEAN>
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (7, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_3_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (7, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon8:
        TLAU_127 = (8, Weapons.TLAU_127)
        AIM_120D_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        # ERRR {CATM-120C}
        LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR <CLEAN>
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        BRU_42_with_2_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_ADM_141A_TALD = (8, Weapons.BRU_42_with_ADM_141A_TALD)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        CATM_9M = (9, Weapons.CATM_9M)
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon10:
        AA42R_Buddy_Pod = (10, Weapons.AA42R_Buddy_Pod)
        FPU_12_Fuel_Tank_480_gallons = (10, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            10,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        USAFlag = (10, Weapons.USAFlag)
        Smoke_Generator___red_ = (10, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (10, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (10, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (10, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (10, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (10, Weapons.Smoke_Generator___orange_)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class EA_18G(PlaneType):
    id = "EA-18G"
    flyable = True
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 4900
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "OuterBoard": 0,
        "InnerBoard": 0,
        "HelmetMountedDevice": 1,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
    }

    class Properties:
        class OuterBoard:
            id = "OuterBoard"

            class Values:
                Single = 0
                Ripple = 1

        class InnerBoard:
            id = "InnerBoard"

            class Values:
                Single = 0
                Ripple = 1

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

    properties = {
        "OuterBoard": UnitPropertyDescription(
            identifier="OuterBoard",
            control="comboList",
            label="Outerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "InnerBoard": UnitPropertyDescription(
            identifier="InnerBoard",
            control="comboList",
            label="Innerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "EA-18G"  # from type

    class Pylon1:
        FPU_12_Fuel_Tank_480_gallons = (1, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            1,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        ALQ_99Wing = (1, Weapons.ALQ_99Wing)

    # ERRR <CLEAN>

    class Pylon2:
        FPU_12_Fuel_Tank_480_gallons = (2, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            2,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        ALQ_99Wing = (2, Weapons.ALQ_99Wing)
        AGM_154A___JSOW_CEB__CBU_type_ = (2, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (2, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )

    # ERRR <CLEAN>

    class Pylon3:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        TLAU_127 = (3, Weapons.TLAU_127)

    class Pylon4:
        AIM_120D_AMRAAM___Active_Rdr_AAM = (4, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon5:
        FPU_12_Fuel_Tank_480_gallons = (5, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            5,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        ALQ_99Center = (5, Weapons.ALQ_99Center)

    # ERRR <CLEAN>

    class Pylon6:
        AIM_120D_AMRAAM___Active_Rdr_AAM = (6, Weapons.AIM_120D_AMRAAM___Active_Rdr_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon7:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        TLAU_127 = (7, Weapons.TLAU_127)

    class Pylon8:
        FPU_12_Fuel_Tank_480_gallons = (8, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            8,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        ALQ_99Wing = (8, Weapons.ALQ_99Wing)
        AGM_154A___JSOW_CEB__CBU_type_ = (8, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            8,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        AGM_154C___JSOW_Unitary_BROACH = (8, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH = (
            8,
            Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )

    # ERRR <CLEAN>

    class Pylon9:
        FPU_12_Fuel_Tank_480_gallons = (9, Weapons.FPU_12_Fuel_Tank_480_gallons)
        FPU_12_Fuel_Tank_480_gallons_High_Vis = (
            9,
            Weapons.FPU_12_Fuel_Tank_480_gallons_High_Vis,
        )
        ALQ_99Wing = (9, Weapons.ALQ_99Wing)

    # ERRR <CLEAN>

    class Pylon10:
        USAFlag = (10, Weapons.USAFlag)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP
