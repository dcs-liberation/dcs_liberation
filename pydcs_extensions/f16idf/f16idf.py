from enum import Enum
from typing import Dict, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF16I:
    AIM_9M_ = {
        "clsid": "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}",
        "name": "AIM-9M ",
        "weight": 103
    }
    AIM_9P5_ = {
        "clsid": "{AIM-9P5}", "name": "AIM-9P5 ",
        "weight": 85.5
    }
    AIM_9P_ = {
        "clsid": "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
        "name": "AIM-9P ",
        "weight": 86.18
    }
    AIM_9X_ = {
        "clsid": "{5CE2FF2A-645A-4197-B48D-8720AC69394F}",
        "name": "AIM-9X ",
        "weight": 103
    }
    AN_AAQ_13 = {
        "clsid": "{ANAAQ-13}",
        "name": "AN/AAQ-13",
        "weight": 25
    }
    CATM_9M = {
        "clsid": "CATM-9M",
        "name": "CAP-9M",
        "weight": 85.5
    }
    CREW = {
        "clsid": "{CREW}",
        "name": "CREW",
        "weight": 0
    }
    Crew_Ladder = {
        "clsid": "{IDF Mods Project LDR}",
        "name": "Crew Ladder",
        "weight": 0
    }
    Delilah_cover_Pylon_3 = {
        "clsid": "{Delilah cover S 3}",
        "name": "Delilah cover Pylon 3",
        "weight": 0
    }
    Delilah_cover_Pylon_3_7 = {
        "clsid": "{Delilah cover S 3-7}",
        "name": "Delilah cover Pylon 3-7",
        "weight": 0
    }
    Delilah_cover_Pylon_7 = {
        "clsid": "{Delilah cover S 7}",
        "name": "Delilah cover Pylon 7",
        "weight": 0
    }
    Fuel_tank_300_gal_ = {
        "clsid": "{IDF Mods Project 300gal}",
        "name": "Fuel tank 300 gal",
        "weight": 971.4895155
    }
    Fuel_tank_300_gal__ = {
        "clsid": "{F14-300gal}",
        "name": "Fuel tank 300 gal",
        "weight": 958.4
    }
    Fuel_tank_600_gal = {
        "clsid": "{600gal}",
        "name": "Fuel tank 600 gal",
        "weight": 2015.806774925
    }
    Fuel_tank_600_gal__EMPTY_ = {
        "clsid": "{600gal_Empty}",
        "name": "Fuel tank 600 gal *EMPTY*",
        "weight": 180
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Left}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb",
        "weight": 680.0827540681
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Left + Fuel Tank 370}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb + 370Gal",
        "weight": 1789.8845750252
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Right}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb",
        "weight": 680.0827540681
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Right + Fuel Tank 370}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb + 370Gal",
        "weight": 1789.8845750252
    }
    LAU_105_1_AIM_9L_L = {
        "clsid": "LAU-105_1*AIM-9L_L",
        "name": "LAU-105 Python-5 ",
        "weight": 115.5
    }
    LAU_105_1_AIM_9L_R = {
        "clsid": "LAU-105_1*AIM-9L_R",
        "name": "LAU-105 Python-5 ",
        "weight": 115.5
    }
    LAU_105_1_AIM_9M_L = {
        "clsid": "LAU-105_1*AIM-9M_L",
        "name": "LAU-105 AIM-9M ",
        "weight": 133
    }
    LAU_105_1_AIM_9M_R = {
        "clsid": "LAU-105_1*AIM-9M_R",
        "name": "LAU-105 AIM-9M ",
        "weight": 133
    }
    LAU_105_1_CATM_9M_L = {
        "clsid": "LAU-105_1*CATM-9M_L",
        "name": "LAU-105 CAP-9M",
        "weight": 115.5
    }
    LAU_105_1_CATM_9M_R = {
        "clsid": "LAU-105_1*CATM-9M_R",
        "name": "LAU-105 CAP-9M",
        "weight": 115.5
    }
    LAU_105_2_AIM_9L = {
        "clsid": "LAU-105_2*AIM-9L",
        "name": "LAU-105 - 2 Python-5 ",
        "weight": 201
    }
    LAU_105_2_AIM_9P5 = {
        "clsid": "LAU-105_2*AIM-9P5",
        "name": "LAU-105 - 2 AIM-9P5 ",
        "weight": 201
    }
    LAU_105_2_CATM_9M = {
        "clsid": "LAU-105_2*CATM-9M",
        "name": "LAU-105 - 2 CAP-9M",
        "weight": 201
    }
    LAU_105_AIS_ASQ_T50_L = {
        "clsid": "LAU-105_AIS_ASQ_T50_L",
        "name": "LAU-105 Python-5 Training",
        "weight": 115.5
    }
    LAU_105_AIS_ASQ_T50_R = {
        "clsid": "LAU-105_AIS_ASQ_T50_R",
        "name": "LAU-105 Python-5 Training",
        "weight": 115.5
    }
    LAU_105___2_AIM_9M_ = {
        "clsid": "{DB434044-F5D0-4F1F-9BA9-B73027E18DD3}",
        "name": "LAU-105 - 2 AIM-9M ",
        "weight": 236
    }
    LAU_105___2_AIM_9P_ = {
        "clsid": "{3C0745ED-8B0B-42eb-B907-5BD5C1717447}",
        "name": "LAU-105 - 2 AIM-9P ",
        "weight": 202.36
    }
    LAU_115_2_LAU_127_AIM_9L = {
        "clsid": "LAU-115_2*LAU-127_AIM-9L",
        "name": "LAU-115 - 2 LAU-127 Python-5 ",
        "weight": 316
    }
    LAU_115_2_LAU_127_AIM_9M = {
        "clsid": "LAU-115_2*LAU-127_AIM-9M",
        "name": "LAU-115 - 2 LAU-127 AIM-9M ",
        "weight": 351
    }
    LAU_115_2_LAU_127_AIM_9X = {
        "clsid": "LAU-115_2*LAU-127_AIM-9X",
        "name": "LAU-115 - 2 LAU-127 AIM-9X ",
        "weight": 351
    }
    LAU_115_2_LAU_127_CATM_9M = {
        "clsid": "LAU-115_2*LAU-127_CATM-9M",
        "name": "LAU-115 - 2 LAU-127 CAP-9M",
        "weight": 316
    }
    LAU_115_LAU_127_AIM_9L = {
        "clsid": "LAU-115_LAU-127_AIM-9L",
        "name": "LAU-115C LAU-127 Python-5 ",
        "weight": 185.2
    }
    LAU_115_LAU_127_AIM_9M = {
        "clsid": "LAU-115_LAU-127_AIM-9M",
        "name": "LAU-115C LAU-127 AIM-9M ",
        "weight": 202.7
    }
    LAU_115_LAU_127_AIM_9X = {
        "clsid": "LAU-115_LAU-127_AIM-9X",
        "name": "LAU-115C LAU-127 AIM-9X ",
        "weight": 202.7
    }
    LAU_115_LAU_127_CATM_9M = {
        "clsid": "LAU-115_LAU-127_CATM-9M",
        "name": "LAU-115C LAU-127 CAP-9M",
        "weight": 185.2
    }
    LAU_127_AIM_9L = {
        "clsid": "LAU-127_AIM-9L",
        "name": "LAU-127 Python-5 ",
        "weight": 130.8
    }
    LAU_127_AIM_9M = {
        "clsid": "LAU-127_AIM-9M",
        "name": "LAU-127 AIM-9M ",
        "weight": 148.3
    }
    LAU_127_AIM_9X = {
        "clsid": "LAU-127_AIM-9X",
        "name": "LAU-127 AIM-9X ",
        "weight": 148.3
    }
    LAU_127_CATM_9M = {
        "clsid": "LAU-127_CATM-9M",
        "name": "LAU-127 CAP-9M",
        "weight": 130.8
    }
    LAU_7_AIM_9M_ = {
        "clsid": "{AIM-9M-ON-ADAPTER}",
        "name": "LAU-7 AIM-9M ",
        "weight": 118
    }
    LAU_7_AIM_9P5_ = {
        "clsid": "{AIM-9P5-ON-ADAPTER}",
        "name": "LAU-7 AIM-9P5 ",
        "weight": 100.5
    }
    LAU_7_AIM_9P_ = {
        "clsid": "{AIM-9P-ON-ADAPTER}",
        "name": "LAU-7 AIM-9P ",
        "weight": 101.18
    }
    LAU_7_AIM_9X_ = {
        "clsid": "{AIM-9X-ON-ADAPTER}",
        "name": "LAU-7 AIM-9X ",
        "weight": 118
    }
    LAU_7_GAR_8_ = {
        "clsid": "{GAR-8}",
        "name": "LAU-7 GAR-8 ",
        "weight": 100.5
    }
    LAU_7_Python_5_Training = {
        "clsid": "{LAU-7_AIS_ASQ_T50}",
        "name": "LAU-7 Python-5 Training",
        "weight": 115.5
    }
    LAU_7___2_AIM_9M_ = {
        "clsid": "{9DDF5297-94B9-42FC-A45E-6E316121CD85}",
        "name": "LAU-7 - 2 AIM-9M ",
        "weight": 236
    }
    LAU_7___2_AIM_9P5_ = {
        "clsid": "{F4-2-AIM9P5}",
        "name": "LAU-7 - 2 AIM-9P5 ",
        "weight": 201
    }
    LAU_7___2_AIM_9P_ = {
        "clsid": "{773675AB-7C29-422f-AFD8-32844A7B7F17}",
        "name": "LAU-7 - 2 AIM-9P ",
        "weight": 202.36
    }
    LAU_7___2_GAR_8_ = {
        "clsid": "{F4-2-AIM9B}",
        "name": "LAU-7 - 2 GAR-8 ",
        "weight": 201
    }
    LAU_7___2_Python_5_ = {
        "clsid": "{F4-2-AIM9L}",
        "name": "LAU-7 - 2 Python-5 ",
        "weight": 201
    }
    Python_5_ = {
        "clsid": "{AIM-9L}",
        "name": "Python-5 ",
        "weight": 85.5
    }
    Python_5_Cover_Pylon_2 = {
        "clsid": "{Python 5 cover S 2}",
        "name": "Python 5 Cover Pylon 2",
        "weight": 0
    }
    Python_5_Cover_Pylon_2_8 = {
        "clsid": "{Python 5 cover S 2-8}",
        "name": "Python 5 Cover Pylon 2-8",
        "weight": 0
    }
    Python_5_Cover_Pylon_8 = {
        "clsid": "{Python 5 cover S 8}",
        "name": "Python 5 Cover Pylon 8",
        "weight": 0
    }
    Python_5_Training = {
        "clsid": "{AIS_ASQ_T50}",
        "name": "Python-5 Training",
        "weight": 85.5
    }
    Remove_Before_Flight = {
        "clsid": "{IDF Mods Project RBF}",
        "name": "Remove Before Flight",
        "weight": 0
    }
    Remove_Before_Flight_without_Lantirn = {
        "clsid": "{IDF Mods Project Remove Before Flight without Lantirn}",
        "name": "Remove Before Flight without Lantirn",
        "weight": 0
    }
    Remove_Before_Flight_without_TGP_ = {
        "clsid": "{IDF Mods Project Remove Before Flight without TGP}",
        "name": "Remove Before Flight without TGP ",
        "weight": 0
    }
    Remove_Before_Flight_without_TGP_And_Lantirn = {
        "clsid": "{Remove Before Flight without TGP And Lantirn}",
        "name": "Remove Before Flight without TGP And Lantirn",
        "weight": 0
    }
    Spice_2000_Cover_Pylon_4 = {
        "clsid": "{Spice 2000 cov S 4}",
        "name": "Spice 2000 Cover Pylon 4",
        "weight": 0
    }
    Spice_2000_Cover_Pylon_4_6 = {
        "clsid": "{Spice 2000 cov S 4-6}",
        "name": "Spice 2000 Cover Pylon 4-6",
        "weight": 0
    }
    Spice_2000_Cover_Pylon_6 = {
        "clsid": "{Spice 2000 cov S 6}",
        "name": "Spice 2000 Cover Pylon 6",
        "weight": 0
    }


inject_weapons(WeaponsF16I)


@planemod
class F_16I(PlaneType):
    id = "F-16I"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 3249
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
                15: 263
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134
            },
        },
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    class Liveries:
        class Israel(Enum):
            IAF_101st_squadron = "IAF_101st_squadron"
            IAF_110th_Squadron = "IAF_110th_Squadron"
            IAF_115th_Aggressors_Squadron = "IAF_115th_Aggressors_Squadron"
            IAF_117th_Squadron = "IAF_117th_Squadron"

        class Combined_Joint_Task_Forces_Blue(Enum):
            default = "default"
            IAF_101st_squadron = "IAF_101st_squadron"
            IAF_110th_Squadron = "IAF_110th_Squadron"
            IAF_115th_Aggressors_Squadron = "IAF_115th_Aggressors_Squadron"
            IAF_117th_Squadron = "IAF_117th_Squadron"

        class Combined_Joint_Task_Forces_Red(Enum):
            default = "default"
            IAF_101st_squadron = "IAF_101st_squadron"
            IAF_110th_Squadron = "IAF_110th_Squadron"
            IAF_115th_Aggressors_Squadron = "IAF_115th_Aggressors_Squadron"
            IAF_117th_Squadron = "IAF_117th_Squadron"

        class USA(Enum):
            default = "default"

    class Pylon1:
        AIM_9M_ = (1, Weapons.AIM_9M_)
        Python_5_ = (1, Weapons.Python_5_)
        AIM_9X_ = (1, Weapons.AIM_9X_)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (1, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (1, Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM)
        CATM_9M = (1, Weapons.CATM_9M)
        Python_5_Training = (1, Weapons.Python_5_Training)

    class Pylon2:
        AIM_9M_ = (2, Weapons.AIM_9M_)
        Python_5_ = (2, Weapons.Python_5_)
        AIM_9X_ = (2, Weapons.AIM_9X_)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (2, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (2, Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM)
        CATM_9M = (2, Weapons.CATM_9M)
        Python_5_Training = (2, Weapons.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_ = (3, Weapons.AIM_9M_)
        Python_5_ = (3, Weapons.Python_5_)
        AIM_9X_ = (3, Weapons.AIM_9X_)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM)
        CATM_9M = (3, Weapons.CATM_9M)
        Python_5_Training = (3, Weapons.Python_5_Training)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (3, Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
        3, Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (3, Weapons.GBU_10___2000lb_Laser_Guided_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (3, Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (3, Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_)
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (3, Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_)
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (3, Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_)
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        3, Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_)
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (3, Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb)
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
        3, Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (3, Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb)
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
        3, Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_)
        CBU_105___10_x_SFW__CBU_with_WCMD = (3, Weapons.CBU_105___10_x_SFW__CBU_with_WCMD)
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
        3, Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (3, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD)
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
        3, Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb)
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb)
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (3, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_)
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (4, Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
        4, Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (4, Weapons.GBU_10___2000lb_Laser_Guided_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb)
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (4, Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD)
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        4, Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (4, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD)
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
        4, Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb)
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        MXU_648_TP = (5, Weapons.MXU_648_TP)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (6, Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
        6, Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (6, Weapons.GBU_10___2000lb_Laser_Guided_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb)
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (6, Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD)
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        6, Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (6, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_)
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
        6, Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_)
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
        6, Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_)
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (6, Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_)
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (6, Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_)

    class Pylon7:
        AIM_9M_ = (7, Weapons.AIM_9M_)
        Python_5_ = (7, Weapons.Python_5_)
        AIM_9X_ = (7, Weapons.AIM_9X_)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM)
        CATM_9M = (7, Weapons.CATM_9M)
        Python_5_Training = (7, Weapons.Python_5_Training)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (7, Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD)
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
        7, Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (7, Weapons.GBU_10___2000lb_Laser_Guided_Bomb)
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (7, Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (7, Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_)
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (7, Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_)
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (7, Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_)
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        7, Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_)
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (7, Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb)
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
        7, Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (7, Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb)
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
        7, Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_)
        CBU_105___10_x_SFW__CBU_with_WCMD = (7, Weapons.CBU_105___10_x_SFW__CBU_with_WCMD)
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
        7, Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (7, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_)
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
        7, Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_)
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
        7, Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_)
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
        7, Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_)
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (7, Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_)
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (7, Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_)
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (7, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__)
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)

    class Pylon8:
        AIM_9M_ = (8, Weapons.AIM_9M_)
        Python_5_ = (8, Weapons.Python_5_)
        AIM_9X_ = (8, Weapons.AIM_9X_)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM)
        CATM_9M = (8, Weapons.CATM_9M)
        Python_5_Training = (8, Weapons.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_ = (9, Weapons.AIM_9M_)
        Python_5_ = (9, Weapons.Python_5_)
        AIM_9X_ = (9, Weapons.AIM_9X_)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (9, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (9, Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM)
        CATM_9M = (9, Weapons.CATM_9M)
        Python_5_Training = (9, Weapons.Python_5_Training)

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (11, Weapons.AN_AAQ_28_LITENING___Targeting_Pod)

    pylons: = {1, 2, 3, 4, 5, 6, 7, 8, 9, 11}

    tasks = [task.CAP,
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
             task.Reconnaissance
             ]
    task_default = task.CAP
