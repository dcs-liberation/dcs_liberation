from typing import Dict, List, Set, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.unitpropertydescription import UnitPropertyDescription
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsFA18EFG:
    STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_1X_AIM-9}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 85.72,
    }
    STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 84.46,
    }
    STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 84.46,
    }
    STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_1X_AIM-9X}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 84.46,
    }
    STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_01_PD_1X_ais-pod-t50}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 62.6,
    }
    STA_01_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_1X_CATM-9M}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 85.73,
    }
    STA_01_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_MOD_1X_CATM-9X}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x CATM-9X Sidewinder - Captive ACM",
        "weight": 84.46,
    }
    STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_BDU-45B}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_BDU-45}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_CBU-99}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-12}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-16}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-32}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-38}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU_54V}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_ROCKEYE}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-82Y}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-82}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-83AIR}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-83}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_02_SUU80_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_02_EMPTY}",
        "name": " [ STA 02	  | SUU80 | EMPTY ]",
        "weight": 0,
    }
    STA_02_SUU80_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7F}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7H}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7M}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7P}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MV_1X_AGM-65E}",
        "name": " [ STA 02	  | SUU80 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MV_1X_AGM-65F}",
        "name": " [ STA 02	  | SUU80 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MV_1X_CATM-65K}",
        "name": " [ STA 02	  | SUU80 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_AR_1X_AGM-88}",
        "name": " [ STA 02	  | SUU80 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_AM_1X_AIM-120}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 209.95,
    }
    STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_AM_1X_AIM-120C}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 213.58,
    }
    STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 214.5,
    }
    STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 214.5,
    }
    STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_SW_1X_AIM-9}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 137.82,
    }
    STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 136.56,
    }
    STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 136.56,
    }
    STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_SW_1X_AIM-9X}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 136.56,
    }
    STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_02_PD_1X_ais-pod-t50}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 114.7,
    }
    STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_AM_MOD_1X_CATM-120C}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x CATM-120C AMRAAM - Captive ACM",
        "weight": 206.321,
    }
    STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_SW_1X_CATM-9M}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 137.83,
    }
    STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_SW_MOD_1X_CATM-9X}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x CATM-9X Sidewinder - Captive ACM",
        "weight": 136.56,
    }
    STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_02_LAU127}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_AM_2X_AIM-120}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_AM_2X_AIM-120C}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_2X_AIM-9}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_2X_AIM-9X}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_02_03_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_2X_CATM-9M}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 1x/1x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_02_03_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_AM_3X_AIM-120}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 2x/1x AIM-120B AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 653.05,
    }
    STA_02_03_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_AM_3X_AIM-120C}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 2x/1x AIM-120C AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 663.94,
    }
    STA_02_03_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_AM_MOD_3X_AIM-120D_AI}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 2x/1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 666.7,
    }
    STA_02_03_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_3X_AIM-9}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 2x/1x AIM-9M Sidewinder - IR AAM, (AI Only)",
        "weight": 436.66,
    }
    STA_02_03_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_MOD_3X_AIM-9X2_AI}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_02_03_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_3X_AIM-9X}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_02_03_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MO_SW_3X_CATM-9M}",
        "name": " [ STA 02/03 | 79 / 80 | LAU127 ] - 2x/1x CATM-9M Sidewinder - Captive ACM, (AI Only)",
        "weight": 436.69,
    }
    STA_02_04_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IO_AM_3X_AIM-120}",
        "name": " [ STA 02/04 | 79 / 80 | LAU127 ] - 2x/1x AIM-120B AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 653.05,
    }
    STA_02_04_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IO_AM_3X_AIM-120C}",
        "name": " [ STA 02/04 | 79 / 80 | LAU127 ] - 2x/1x AIM-120C AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 663.94,
    }
    STA_02_04_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IO_AM_MOD_3X_AIM-120D_AI}",
        "name": " [ STA 02/04 | 79 / 80 | LAU127 ] - 2x/1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 666.7,
    }
    STA_02_04_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IO_SW_3X_AIM-9}",
        "name": " [ STA 02/04 | 79 / 80 | LAU127 ] - 2x/1x AIM-9M Sidewinder - IR AAM, (AI Only)",
        "weight": 436.66,
    }
    STA_02_04_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IO_SW_MOD_3X_AIM-9X2_AI}",
        "name": " [ STA 02/04 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_02_04_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IO_SW_3X_AIM-9X}",
        "name": " [ STA 02/04 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_02_04_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IO_SW_3X_CATM-9M}",
        "name": " [ STA 02/04 | 79 / 80 | LAU127 ] - 2x/1x CATM-9M Sidewinder - Captive ACM, (AI Only)",
        "weight": 436.69,
    }
    STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_1X_BRU32_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__ = {
        "clsid": "{SUPERHORNET_PYLON_03_BRU32AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_1X_BRU32_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_03_BRU32AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SM_1X_AGM-84E}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_174_1X_AIM-120_AI}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (AI Only)",
        "weight": 195.95,
    }
    STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_174_1X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (Current Hill's AIM-174B Mod Required)",
        "weight": 195.95,
    }
    STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_PD_1X_ALQ-167}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x ALQ-167 Countermeasures System",
        "weight": 141.518,
    }
    STA_03_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Jamming_Pod = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_ALQ_249_MID_BAND}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AN/ALQ-249 Mid-Band Jamming Pod",
        "weight": 534.47,
    }
    STA_03_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_Hi_Band_Jamming_Pod = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_ALQ_99_HI_BAND}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AN/ALQ-99 ICAP III Hi-Band Jamming Pod",
        "weight": 465.383,
    }
    STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_PD_1X_AWW-13}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_BDU-45B}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_BDU-45}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_CBU-99}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_FT_1X_FPU-12A_HV}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL) (High Vis), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_FT_1X_FPU-12A}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-10}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-10}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-16}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-16}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-24}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-24}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-31}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-31}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-31V}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU_54V}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-82Y}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-82Y}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-83AIR}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_03_SUU79_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-83AIR}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-84}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-84}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_BDU-45B}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_BDU-45}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-82Y}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_MK-83AIR}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1077.7885,
    }
    STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-83AIR}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1077.7885,
    }
    STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_BD_BRU41_6X_BDU-33}",
        "name": " [ STA 03	  | SUU79 | BRU41   ] - 6x BDU-33 - 25lb Practice Bomb LD",
        "weight": 195.713,
    }
    STA_03_SUU79_BRU42_1x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_03_SUU79_BRU42_2x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_03_SUU79_BRU42_3x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_1X_BRU55_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_1X_BRU55_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_1X_BRU55_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_1X_BRU55_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_2X_BRU55_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_2X_BRU55_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_2X_BRU55_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_2X_BRU55_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7F}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7F}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7H}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7H}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7M}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7M}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7P}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7P}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MV_1X_AGM-65E}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MV_1X_AGM-65E}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MV_1X_AGM-65F}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MV_1X_AGM-65F}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SM_1X_AGM-84D}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SM_1X_AGM-84E}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SM_1X_AGM-84H}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MV_1X_CATM-65K}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MV_1X_CATM-65K}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AR_1X_AGM-88}",
        "name": " [ STA 03	  | SUU79 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_1X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_1X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_1X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_1X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 341.9,
    }
    STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 341.9,
    }
    STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 341.9,
    }
    STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 341.9,
    }
    STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_1X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 265.22,
    }
    STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_1X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 265.22,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_1X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_1X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_1X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 265.23,
    }
    STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_1X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 265.23,
    }
    STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_2X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_2X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_2X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_2X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_2X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_2X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_2X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_2X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_2X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_2X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_03_02_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-10}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-12}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-16}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-24}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-31}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-31V}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-38}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_ROCKEYE}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-82Y}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-82}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-83AIR}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1021.54,
    }
    STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-83}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-84}",
        "name": " [ STA 03/02 | 79 / 80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_174_2X_AIM-120_AI}",
        "name": " [ STA 03/04 | SUU79 | BRU32   ] - 2x AIM-174B Gunslinger - Active Radar AAM, (AI Only)",
        "weight": 391.9,
    }
    STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_174_2X_AIM-120}",
        "name": " [ STA 03/04 | SUU79 | BRU32   ] - 2x AIM-174B Gunslinger - Active Radar AAM, (Current Hill's AIM-174B Mod Required)",
        "weight": 391.9,
    }
    STA_04_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_BRU32AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_BRU32AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SM_1X_AGM-84D}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SM_1X_AGM-84E}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SM_1X_AGM-84H}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_174_1X_AIM-120_AI}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (AI Only)",
        "weight": 195.95,
    }
    STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_174_1X_AIM-120}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (Current Hill's AIM-174B Mod Required)",
        "weight": 195.95,
    }
    STA_04_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_PD_1X_AWW-13}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_FT_1X_FPU-12A_HV}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL) (High Vis), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = {
        "clsid": "{SUPERHORNET_PYLON_04_IB_FT_1X_FPU-12A_HV}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL) (High Vis), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_FT_1X_FPU-12A}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = {
        "clsid": "{SUPERHORNET_PYLON_04_IB_FT_1X_FPU-12A}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_04_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_BDU-45B}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_04_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_BDU-45}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_GBU-12}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-82Y}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-82}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-83AIR}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1077.7885,
    }
    STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-83}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_04_SUU79_BRU42_1x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 04	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_04_SUU79_BRU42_2x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 04	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_04_SUU79_BRU42_3x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 04	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_BRU55_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_BRU55_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_2X_BRU55_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_2X_BRU55_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7F}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7H}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7M}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7P}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MV_1X_AGM-65E}",
        "name": " [ STA 04	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_04_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MV_1X_AGM-65F}",
        "name": " [ STA 04	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MV_1X_CATM-65K}",
        "name": " [ STA 04	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_04_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AR_1X_AGM-88}",
        "name": " [ STA 04	  | SUU79 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_1X_AIM-120}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_1X_AIM-120C}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 341.9,
    }
    STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 341.9,
    }
    STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_1X_AIM-9}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 265.22,
    }
    STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 263.96,
    }
    STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 263.96,
    }
    STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_1X_AIM-9X}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 263.96,
    }
    STA_04_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_1X_CATM-9M}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 265.23,
    }
    STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_2X_AIM-120}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_2X_AIM-120C}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_2X_AIM-9}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_2X_AIM-9X}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_04_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_2X_CATM-9M}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_04_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_BDU-45B}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_04_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_BDU-45}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_04_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_CBU-99}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-10}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-12}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-16}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-24}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31V}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-38}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU_54V}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_ROCKEYE}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-82Y}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-82}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-83AIR}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-83}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-84}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_04_02_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-10}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-12}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-16}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-24}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-31}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-31V}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-38}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_ROCKEYE}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-82Y}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-82}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-83AIR}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1021.54,
    }
    STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-83}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-84}",
        "name": " [ STA 04/02 | 79 / 80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_04_03_79_80_BRU32_1x_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_JS_2X_BRU_AGM-154A}",
        "name": " [ STA 04/03 | 79 / 80 | BRU32   ] - 1x/1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1038.94,
    }
    STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 04/03 | 79 / 80 | BRU32   ] - 1x/1x AGM-154C - JSOW Unitary BROACH",
        "weight": 1036.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_BDU-45B}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x BDU-45B - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_BDU-45}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x BDU-45 - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_CBU-99}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 112.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-10}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-12}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-16}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-24}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31_V_2B}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31V}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31_V_4B}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 2008.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-38}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU_54V}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 574.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_ROCKEYE}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-82Y}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-82_Snakeye}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-82}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-83AIR}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1021.54,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-83}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-84}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_1X_AIM-120}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 157.85,
    }
    STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_1X_AIM-120C}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 161.48,
    }
    STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 162.4,
    }
    STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 162.4,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7F}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7H}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7M}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7P}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_MOD_1X_CATM-120C}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x CATM-120C AMRAAM - Captive ACM",
        "weight": 154.221,
    }
    STA_05_CHEEK__TGPMNT_Empty_Weapon_Replacable_Assembly__WRA__Adapter = {
        "clsid": "{SUPERHORNET_PYLON_05_FS_TGP_MOUNT}",
        "name": " [ STA 05	  | CHEEK  | TGPMNT ] Empty Weapon Replacable Assembly (WRA) Adapter",
        "weight": 25,
    }
    STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = {
        "clsid": "{SUPERHORNET_PYLON_05_TP_ASQ228}",
        "name": " [ STA 05	  | CHEEK  | TGPMNT ] - 1x AN/ASQ-228 ATFLIR - Targeting Pod",
        "weight": 215.5,
    }
    STA_05_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_04_IB_PD_1X_AWW-13}",
        "name": " [ STA 05	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING_Targeting_Pod = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_TP_AAQ28}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x AN/AAQ-28 LITENING Targeting Pod",
        "weight": 242.47,
    }
    STA_06_SUU78_BRU32_1x_AN_ALQ_99_ICAP_III_Lo_Band_Jamming_Pod = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_ANALQ_99_LO_BAND}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x AN/ALQ-99 ICAP III Lo-Band Jamming Pod",
        "weight": 465.383,
    }
    STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_PD_1X_AWW-13}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_06_SUU78_BRU32_1x_A_A_42R_1__300_GAL__Aerial_Refueling_System___Player_limited_to_Fuel_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_06_FT_1X_AA-42R}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x A/A-42R-1 (300 GAL) Aerial Refueling System, (Player limited to Fuel Only)",
        "weight": 1332.47,
    }
    STA_06_SUU78_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_BDU-45B}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_06_SUU78_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_BDU-45}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_06_SUU78_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_CBU-99}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_06_FT_1X_FPU-12A_HV}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x FPU-12/A (480 GAL) (High Vis), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_06_FT_1X_FPU-12A}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x FPU-12/A (480 GAL), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_06_SUU78_BRU32_1x_FPU_13_A__340_GAL__w__ASG_34A_V_1_IRST___Player_limited_to_330_Gallons_and_Fuel_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_06_FT_1X_ASG-34A}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x FPU-13/A (340 GAL) w/ ASG-34A(V)1 IRST, (Player limited to 330 Gallons and Fuel Only)",
        "weight": 1310.57,
    }
    STA_06_SUU78_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_ROCKEYE}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_06_SUU78_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_MK-82Y}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_06_SUU78_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_06_SUU78_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_MK-82}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_06_SUU78_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_MK-83AIR}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_06_SUU78_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_MK-83}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_06_SUU78_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_1X_MK-84}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_06_SUU78_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_BDU-45B}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_06_SUU78_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_BDU-45}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_06_SUU78_BRU33_2x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_CBU-99}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 169.1885,
    }
    STA_06_SUU78_BRU33_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_ROCKEYE}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 569.1885,
    }
    STA_06_SUU78_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_MK-82Y}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_06_SUU78_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_06_SUU78_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_MK-82}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_06_SUU78_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_MK-83AIR}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1077.7885,
    }
    STA_06_SUU78_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_MK-83}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_06_SUU78_BRU33_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_MK_2X_MK-84}",
        "name": " [ STA 06	  | SUU78 | BRU33   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1949.1885,
    }
    STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_1X_AIM-120}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 157.85,
    }
    STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_1X_AIM-120C}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 161.48,
    }
    STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 162.4,
    }
    STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 162.4,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7F}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7H}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7M}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7P}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 231,
    }
    STA_07_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_MOD_1X_CATM-120C}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x CATM-120C AMRAAM - Captive ACM",
        "weight": 154.221,
    }
    STA_08_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_BRU32AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_BRU32AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SM_1X_AGM-84D}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SM_1X_AGM-84E}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SM_1X_AGM-84H}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_174_1X_AIM-120_AI}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (AI Only)",
        "weight": 195.95,
    }
    STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_174_1X_AIM-120}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (Current Hill's AIM-174B Mod Required)",
        "weight": 195.95,
    }
    STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_08_IB_PD_1X_AWW-13}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_PD_1X_AWW-13}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_08_IB_FT_1X_FPU-12A_HV}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL) (High Vis), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_FT_1X_FPU-12A_HV}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL) (High Vis), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_08_IB_FT_1X_FPU-12A}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_FT_1X_FPU-12A}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_08_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_BDU-45B}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_08_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_BDU-45}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_GBU-12}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-82Y}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-82}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-83AIR}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1077.7885,
    }
    STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-83}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_08_SUU79_BRU42_1x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 08	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_08_SUU79_BRU42_2x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 08	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_08_SUU79_BRU42_3x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 08	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_BRU55_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_BRU55_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_2X_BRU55_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_2X_BRU55_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7F}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7H}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7M}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7P}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MV_1X_AGM-65E}",
        "name": " [ STA 08	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_08_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MV_1X_AGM-65F}",
        "name": " [ STA 08	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MV_1X_CATM-65K}",
        "name": " [ STA 08	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_08_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AR_1X_AGM-88}",
        "name": " [ STA 08	  | SUU79 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_1X_AIM-120}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_1X_AIM-120C}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 341.9,
    }
    STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 341.9,
    }
    STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_1X_AIM-9}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 265.22,
    }
    STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 263.96,
    }
    STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 263.96,
    }
    STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_1X_AIM-9X}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 263.96,
    }
    STA_08_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_1X_CATM-9M}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 265.23,
    }
    STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_2X_AIM-120}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_2X_AIM-120C}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_2X_AIM-9}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_2X_AIM-9X}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_08_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_2X_CATM-9M}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_08_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_BDU-45B}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_08_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_BDU-45}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_08_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_CBU-99}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-10}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-12}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-16}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-24}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31V}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-32}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-38}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU_54V}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_ROCKEYE}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-82Y}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-82}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-83AIR}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-83}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-84}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 08/09 | SUU79 | BRU32   ] - 1x/1x AGM-154C - JSOW Unitary BROACH",
        "weight": 1036.94,
    }
    STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_174_2X_AIM-120_AI}",
        "name": " [ STA 08/09 | SUU79 | BRU32   ] - 2x AIM-174B Gunslinger - Active Radar AAM, (AI Only)",
        "weight": 391.9,
    }
    STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_174_2X_AIM-120}",
        "name": " [ STA 08/09 | SUU79 | BRU32   ] - 2x AIM-174B Gunslinger - Active Radar AAM, (Current Hill's AIM-174B Mod Required)",
        "weight": 391.9,
    }
    STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_BRU32AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_1X_BRU32_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_BRU32AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_1X_BRU32_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_174_1X_AIM-120_AI}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (AI Only)",
        "weight": 195.95,
    }
    STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_174_1X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AIM-174B Gunslinger - Active Radar AAM, (Current Hill's AIM-174B Mod Required)",
        "weight": 195.95,
    }
    STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_PD_1X_ALQ-167}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x ALQ-167 Countermeasures System",
        "weight": 141.518,
    }
    STA_09_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Jamming_Pod = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_ALQ_249_MID_BAND}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AN/ALQ-249 Mid-Band Jamming Pod",
        "weight": 534.47,
    }
    STA_09_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_Hi_Band_Jamming_Pod = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_ALQ_99_HI_BAND}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AN/ALQ-99 ICAP III Hi-Band Jamming Pod",
        "weight": 465.383,
    }
    STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_PD_1X_AWW-13}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_FT_1X_FPU-12A_HV}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL) (High Vis), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_FT_1X_FPU-12A}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x FPU-12/A (480 GAL), (Player limited to 330 Gallons)",
        "weight": 1656.97,
    }
    STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-10}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-12}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-16}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-24}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-31}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-31V}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-38}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-82Y}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-82}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-83AIR}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-83}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-84}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_BDU-45B}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_BDU-45}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_GBU-12}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_GBU-12}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-82Y}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-82}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_MK-82}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-83AIR}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1077.7885,
    }
    STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_MK-83AIR}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1077.7885,
    }
    STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-83}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_MK-83}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_BD_BRU41_6X_BDU-33}",
        "name": " [ STA 09	  | SUU79 | BRU41   ] - 6x BDU-33 - 25lb Practice Bomb LD",
        "weight": 195.713,
    }
    STA_09_SUU79_BRU42_1x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_09_SUU79_BRU42_2x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_09_SUU79_BRU42_3x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_BRU55_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_1X_BRU55_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_BRU55_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_1X_BRU55_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_2X_BRU55_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_2X_BRU55_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_2X_BRU55_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_2X_BRU55_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7F}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7F}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7H}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7H}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7M}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7M}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7P}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7P}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MV_1X_AGM-65E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MV_1X_AGM-65E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MV_1X_AGM-65F}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SM_1X_AGM-84D}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SM_1X_AGM-84E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SM_1X_AGM-84E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SM_1X_AGM-84H}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MV_1X_CATM-65K}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MV_1X_CATM-65K}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AR_1X_AGM-88}",
        "name": " [ STA 09	  | SUU79 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_1X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_1X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_1X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_1X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 341.9,
    }
    STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 341.9,
    }
    STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 341.9,
    }
    STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 341.9,
    }
    STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_1X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 265.22,
    }
    STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_1X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 265.22,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_1X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_1X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_1X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 265.23,
    }
    STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_1X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 265.23,
    }
    STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_2X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_2X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_2X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_2X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_2X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_2X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_2X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_2X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_2X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_2X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_BDU-45B}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_BDU-45}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_09_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_CBU-99}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-10}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-12}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-16}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-24}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-31}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-32}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-38}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU_54V}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-82Y}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-82}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-83AIR}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-83}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-84}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_09_08_SUU79_BRU32_1x_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_BDU-45B}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x BDU-45B - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_BDU-45}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x BDU-45 - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_CBU-99}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 112.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-10}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-12}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-16}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-24}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31_V_2B}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31V}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31_V_4B}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 2008.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-38}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU_54V}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 574.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_ROCKEYE}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-82Y}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-82_Snakeye}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-82}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-83AIR}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1021.54,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-83}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-84}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-10}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-12}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-16}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-24}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-31}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-31V}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-38}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_ROCKEYE}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-82Y}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-82}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-83AIR}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1021.54,
    }
    STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-83}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-84}",
        "name": " [ STA 09/10 | 79 / 80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_AM_2X_AIM-120}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_AM_2X_AIM-120C}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_AM_MOD_2X_AIM-120D_AI}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 504.3,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_AM_MOD_2X_AIM-120D}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 504.3,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_2X_AIM-9}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-9M Sidewinder - IR AAM",
        "weight": 350.94,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_MOD_2X_AIM-9X2_AI}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 348.42,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_MOD_2X_AIM-9X2}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 348.42,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_2X_AIM-9X}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x AIM-9X Sidewinder - IR AAM",
        "weight": 348.42,
    }
    STA_09_10_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_2X_CATM-9M}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 1x/1x CATM-9M Sidewinder - Captive ACM",
        "weight": 350.96,
    }
    STA_09_10_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_AM_3X_AIM-120}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 2x/1x AIM-120B AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 653.05,
    }
    STA_09_10_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_AM_3X_AIM-120C}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 2x/1x AIM-120C AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 663.94,
    }
    STA_09_10_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_AM_MOD_3X_AIM-120D_AI}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 2x/1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 666.7,
    }
    STA_09_10_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_3X_AIM-9}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 2x/1x AIM-9M Sidewinder - IR AAM, (AI Only)",
        "weight": 436.66,
    }
    STA_09_10_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_MOD_3X_AIM-9X2_AI}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_09_10_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_3X_AIM-9X}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_09_10_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MO_SW_3X_CATM-9M}",
        "name": " [ STA 09/10 | 79 / 80 | LAU127 ] - 2x/1x CATM-9M Sidewinder - Captive ACM, (AI Only)",
        "weight": 436.69,
    }
    STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_BDU-45B}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_BDU-45}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_CBU-99}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-12}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-16}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-32}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-38}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU_54V}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_ROCKEYE}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-82Y}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-82}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-83AIR}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 510.77,
    }
    STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-83}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_10_SUU80_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7F}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7F Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7H}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7MH Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7M}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7M Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7P}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7P Sparrow - Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MV_1X_AGM-65E}",
        "name": " [ STA 10	  | SUU80 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MV_1X_AGM-65F}",
        "name": " [ STA 10	  | SUU80 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MV_1X_CATM-65K}",
        "name": " [ STA 10	  | SUU80 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_AR_1X_AGM-88}",
        "name": " [ STA 10	  | SUU80 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_AM_1X_AIM-120}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 209.95,
    }
    STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_AM_1X_AIM-120C}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 213.58,
    }
    STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_AM_MOD_1X_AIM-120D_AI}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 214.5,
    }
    STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_AM_MOD_1X_AIM-120D}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM, (Modern Missiles Mod Required)",
        "weight": 214.5,
    }
    STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_SW_1X_AIM-9}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 137.82,
    }
    STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 136.56,
    }
    STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 136.56,
    }
    STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_SW_1X_AIM-9X}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 136.56,
    }
    STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_10_PD_1X_ais-pod-t50}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 114.7,
    }
    STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_AM_MOD_1X_CATM-120C}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x CATM-120C AMRAAM - Captive ACM",
        "weight": 206.321,
    }
    STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_10_SW_1X_CATM-9M}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 137.83,
    }
    STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_SW_MOD_1X_CATM-9X}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x CATM-9X Sidewinder - Captive ACM",
        "weight": 136.56,
    }
    STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_10_LAU127}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_10_08_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-10}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-12}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-16}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-24}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-31}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-31V}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-38}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_ROCKEYE}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-82Y}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-82}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-83AIR}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x Mk-83 AIR (BSU-85) - 1000 lb GP Chute Retarded Bomb HD",
        "weight": 1021.54,
    }
    STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-83}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-84}",
        "name": " [ STA 10/08 | 79 / 80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_10_08_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IO_AM_3X_AIM-120}",
        "name": " [ STA 10/08 | 79 / 80 | LAU127 ] - 2x/1x AIM-120B AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 653.05,
    }
    STA_10_08_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IO_AM_3X_AIM-120C}",
        "name": " [ STA 10/08 | 79 / 80 | LAU127 ] - 2x/1x AIM-120C AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 663.94,
    }
    STA_10_08_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IO_AM_MOD_3X_AIM-120D_AI}",
        "name": " [ STA 10/08 | 79 / 80 | LAU127 ] - 2x/1x AIM-120D AMRAAM - Active Radar AAM, (AI Only)",
        "weight": 666.7,
    }
    STA_10_08_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IO_SW_3X_AIM-9}",
        "name": " [ STA 10/08 | 79 / 80 | LAU127 ] - 2x/1x AIM-9M Sidewinder - IR AAM, (AI Only)",
        "weight": 436.66,
    }
    STA_10_08_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IO_SW_MOD_3X_AIM-9X2_AI}",
        "name": " [ STA 10/08 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_10_08_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IO_SW_3X_AIM-9X}",
        "name": " [ STA 10/08 | 79 / 80 | LAU127 ] - 2x/1x AIM-9X Sidewinder - IR AAM, (AI Only)",
        "weight": 432.88,
    }
    STA_10_08_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IO_SW_3X_CATM-9M}",
        "name": " [ STA 10/08 | 79 / 80 | LAU127 ] - 2x/1x CATM-9M Sidewinder - Captive ACM, (AI Only)",
        "weight": 436.69,
    }
    STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_1X_AIM-9}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AIM-9M Sidewinder - IR AAM",
        "weight": 85.72,
    }
    STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_MOD_1X_AIM-9X2_AI}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (AI Only)",
        "weight": 84.46,
    }
    STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_MOD_1X_AIM-9X2}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AIM-9X II Sidewinder - IR AAM, (Modern Missiles Mod Required)",
        "weight": 84.46,
    }
    STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_1X_AIM-9X}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AIM-9X Sidewinder - IR AAM",
        "weight": 84.46,
    }
    STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_11_PD_1X_ais-pod-t50}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 62.6,
    }
    STA_11_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_1X_CATM-9M}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x CATM-9M Sidewinder - Captive ACM",
        "weight": 85.73,
    }
    STA_11_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_MOD_1X_CATM-9X}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x CATM-9X Sidewinder - Captive ACM",
        "weight": 84.46,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_BLUE}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Blue",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_GREEN}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Green",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_ORANGE}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Orange",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_RED}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Red",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_WHITE}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - White",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_YELLOW}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Yellow",
        "weight": 15,
    }
    STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells__570_GAL_AI__330_GAL_PLAYER = {
        "clsid": "{SUPERHORNET_PYLON_IN_FT_AUX_CELLS}",
        "name": " [ STA AX	  | FUEL	 | CELLS ] - 1x Internal Auxillary Fuel Cells (570 GAL AI, 330 GAL PLAYER)",
        "weight": 1670,
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
    networked_datalink = True
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
            "Brutal",
            "Buckshot",
            "Cannon",
            "Carbine",
            "Carnage",
            "Colt",
            "Demon",
            "Falcon",
            "Pistol",
            "Ramrod",
            "Ruthless",
            "Sabre",
            "Savage",
            "Sonic",
            "Sword",
            "Wolf",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": 0,
        "AIRCRAFT_ID_SEQ": 0,
        "CJS_PARAM_BLOCK": 1,
        "CJS_PARAM_DEMO": 0,
        "CJS_PARAM_USAFLAG": 0,
        "HelmetMountedDevice": 1,
        "STA02_SUU80AA_MOUNT": 0,
        "STA03_SUU79AA_MOUNT": 0,
        "STA04_SUU79AA_MOUNT": 0,
        "STA05_LAU116B_MOUNT": 0,
        "STA06_SUU78AA_MOUNT": 0,
        "STA07_LAU116B_MOUNT": 0,
        "STA08_SUU79AA_MOUNT": 0,
        "STA09_SUU79AA_MOUNT": 0,
        "STA10_SUU80AA_MOUNT": 0,
        "OuterBoard": 0,
        "InnerBoard": 0,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS_MODE": 0,
        "DYNAMIC_BUNO_01": 0,
        "DYNAMIC_BUNO_02": 5,
        "DYNAMIC_BUNO_03": 4,
        "DYNAMIC_BUNO_04": 8,
        "DYNAMIC_BUNO_05": 9,
        "DYNAMIC_BUNO_06": 8,
        "NetCrewControlPriority": 0,
        "AIDisabled": 0,
        "HumanOrchestra": 0,
        "CJS_DEBUG_MSGS": 0,
        "CJS_SYSTEM_MSGS": 0,
    }

    class Properties:

        class SoloFlight:
            id = "SoloFlight"

            class Values:
                Pilot_Only = 0

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Pattern_Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class CJS_PARAM_BLOCK:
            id = "CJS_PARAM_BLOCK"

            class Values:
                Block_III___Cosmetic = 0
                Block_II____Cosmetic = 1

        class CJS_PARAM_DEMO:
            id = "CJS_PARAM_DEMO"

            class Values:
                None_ = 0
                Installed = 1

        class CJS_PARAM_USAFLAG:
            id = "CJS_PARAM_USAFLAG"

            class Values:
                None_ = 0
                Displayed___Left_Side = 1
                Displayed___Right_Side = 2

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class STA02_SUU80AA_MOUNT:
            id = "STA02_SUU80AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA03_SUU79AA_MOUNT:
            id = "STA03_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA04_SUU79AA_MOUNT:
            id = "STA04_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA05_LAU116B_MOUNT:
            id = "STA05_LAU116B_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA06_SUU78AA_MOUNT:
            id = "STA06_SUU78AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA07_LAU116B_MOUNT:
            id = "STA07_LAU116B_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA08_SUU79AA_MOUNT:
            id = "STA08_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA09_SUU79AA_MOUNT:
            id = "STA09_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA10_SUU80AA_MOUNT:
            id = "STA10_SUU80AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

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

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS_MODE:
            id = "DYNAMIC_BUNOS_MODE"

            class Values:
                DISABLED___NONE = 0
                BOEING_STANDARD = 1

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0

        class AIDisabled:
            id = "AIDisabled"

            class Values:
                Disabled = 0

        class HumanOrchestra:
            id = "HumanOrchestra"

            class Values:
                Disabled = 0

        class CJS_DEBUG_MSGS:
            id = "CJS_DEBUG_MSGS"

            class Values:
                Disabled = 0
                Enabled = 1

        class CJS_SYSTEM_MSGS:
            id = "CJS_SYSTEM_MSGS"

            class Values:
                Disabled = 0
                Enabled = 1

    properties = {
        "CJS_LABEL_CORE_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_CORE_VER",
            control="label",
            label="CJS PKG Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_ECHO_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_ECHO_VER",
            control="label",
            label="F/A-18E Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_CREW": UnitPropertyDescription(
            identifier="CJS_LABEL_CREW",
            control="label",
            label="-> Aircraft Crew Settings",
            player_only=False,
            x_lbl=0,
        ),
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="comboList",
            label="Aircraft Crew",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot Only",
            },
        ),
        "CJS_LABEL_EQUIP": UnitPropertyDescription(
            identifier="CJS_LABEL_EQUIP",
            control="label",
            label="-> Aircraft / Pilot Equipment Settings",
            player_only=False,
            x_lbl=0,
        ),
        "AIRCRAFT_ID_SEQ": UnitPropertyDescription(
            identifier="AIRCRAFT_ID_SEQ",
            control="comboList",
            label="Aircraft Strobe Sequence",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pattern Norm",
                1: "Pattern 0A",
                2: "Pattern 1B",
                3: "Pattern 2C",
                4: "Pattern 3D",
                5: "Pattern 4E",
                6: "Pattern 5F",
            },
        ),
        "CJS_PARAM_BLOCK": UnitPropertyDescription(
            identifier="CJS_PARAM_BLOCK",
            control="comboList",
            label="Aircraft Block (Visual Only)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Block III - Cosmetic",
                1: "Block II  - Cosmetic",
            },
        ),
        "CJS_PARAM_DEMO": UnitPropertyDescription(
            identifier="CJS_PARAM_DEMO",
            control="comboList",
            label="Aircraft Demo Team Equipment",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Installed",
            },
        ),
        "CJS_PARAM_USAFLAG": UnitPropertyDescription(
            identifier="CJS_PARAM_USAFLAG",
            control="comboList",
            label="Hood Displayed Folded Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Displayed - Left Side",
                2: "Displayed - Right Side",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Pilot Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "CJS_LABEL_PYLONS": UnitPropertyDescription(
            identifier="CJS_LABEL_PYLONS",
            control="label",
            label="-> Pylon Control (User req. to remove stores)",
            player_only=False,
            x_lbl=0,
        ),
        "STA02_SUU80AA_MOUNT": UnitPropertyDescription(
            identifier="STA02_SUU80AA_MOUNT",
            control="comboList",
            label="STA 2 SUU-80A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA03_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA03_SUU79AA_MOUNT",
            control="comboList",
            label="STA 3 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA04_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA04_SUU79AA_MOUNT",
            control="comboList",
            label="STA 4 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA05_LAU116B_MOUNT": UnitPropertyDescription(
            identifier="STA05_LAU116B_MOUNT",
            control="comboList",
            label="STA 5 LAU-116B/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA06_SUU78AA_MOUNT": UnitPropertyDescription(
            identifier="STA06_SUU78AA_MOUNT",
            control="comboList",
            label="STA 6 SUU-78A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA07_LAU116B_MOUNT": UnitPropertyDescription(
            identifier="STA07_LAU116B_MOUNT",
            control="comboList",
            label="STA 7 LAU-116B/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA08_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA08_SUU79AA_MOUNT",
            control="comboList",
            label="STA 8 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA09_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA09_SUU79AA_MOUNT",
            control="comboList",
            label="STA 9 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA10_SUU80AA_MOUNT": UnitPropertyDescription(
            identifier="STA10_SUU80AA_MOUNT",
            control="comboList",
            label="STA 10 SUU-80A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "ED_LABEL_ROCKETS": UnitPropertyDescription(
            identifier="ED_LABEL_ROCKETS",
            control="label",
            label="-> Aircraft Rocket Settings",
            player_only=True,
            x_lbl=0,
        ),
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
        "ED_LABEL_DATALINK": UnitPropertyDescription(
            identifier="ED_LABEL_DATALINK",
            control="label",
            label="-> Aircraft Datalink Settings",
            player_only=False,
            x_lbl=0,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
            w_ctrl=150,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
            w_ctrl=150,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
            w_ctrl=150,
        ),
        "DYNAMIC_BORTS": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS",
            control="label",
            label="-> Aircraft Identification Stencils",
            player_only=False,
            x_lbl=0,
        ),
        "DYNAMIC_BORTS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS_MODE",
            control="comboList",
            label="Aircraft Bort Identification Type",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "USN STANDARD",
                2: "RAAF FIGHTER",
                3: "RAAF GROWLER",
                4: "KAF LEGACY",
                5: "KAF SUPER HORNET",
            },
        ),
        "DYNAMIC_BUNOS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BUNOS_MODE",
            control="comboList",
            label="Aircraft Bureau Number",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "BOEING STANDARD",
            },
        ),
        "DYNAMIC_BUNO_01": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_01",
            control="comboList",
            label="Aircraft BUNO Digit #1",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_02": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_02",
            control="comboList",
            label="Aircraft BUNO Digit #2",
            player_only=False,
            default=5,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_03": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_03",
            control="comboList",
            label="Aircraft BUNO Digit #3",
            player_only=False,
            default=4,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_04": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_04",
            control="comboList",
            label="Aircraft BUNO Digit #4",
            player_only=False,
            default=8,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_05": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_05",
            control="comboList",
            label="Aircraft BUNO Digit #5",
            player_only=False,
            default=9,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_06": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_06",
            control="comboList",
            label="Aircraft BUNO Digit #6",
            player_only=False,
            default=8,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "ED_LABEL_MULTIPLAYER": UnitPropertyDescription(
            identifier="ED_LABEL_MULTIPLAYER",
            control="label",
            label="-> Multi-Player / Crew Settings, Not Integrated Yet",
            player_only=True,
            x_lbl=0,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
            },
        ),
        "AIDisabled": UnitPropertyDescription(
            identifier="AIDisabled",
            control="comboList",
            label="AI Crew Members",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="comboList",
            label="Multicrew Player Slots",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
            },
        ),
        "CJS_LABEL_DEBUG": UnitPropertyDescription(
            identifier="CJS_LABEL_DEBUG",
            control="label",
            label="-> Trouble Shooting / Debug Messages",
            player_only=True,
            x_lbl=0,
        ),
        "CJS_DEBUG_MSGS": UnitPropertyDescription(
            identifier="CJS_DEBUG_MSGS",
            control="comboList",
            label="Display Debug Msgs At MSN Start",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
                1: "Enabled",
            },
        ),
        "CJS_SYSTEM_MSGS": UnitPropertyDescription(
            identifier="CJS_SYSTEM_MSGS",
            control="comboList",
            label="Display Addon System Msgs",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
                1: "Enabled",
            },
        ),
    }

    livery_name = "FA-18E"  # from livery_entry

    class Pylon1:
        STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_01_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )

    class Pylon2:
        STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-38}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-32V}
        STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR2_MK-8Y}
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_03_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        BRU_42___1_x_ADM_141A_TALD = (2, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (2, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (2, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (2, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )

    class Pylon3:
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_JS_1X_BRU32_AGM-154C}
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32V}
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_,
        )
        STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_BR2_ROCKEYE}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_04_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_04_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_04_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_04_SUU79_BRU42_1x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_04_SUU79_BRU42_2x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_04_SUU79_BRU42_3x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_JS_1X_BRU32_AGM-154A}
        STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_JS_BRU32_AGM-154C}
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_MK_BR2_ROCKEYE}
        STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_PD_1X_ALQ-167}
        STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42___1_x_ADM_141A_TALD = (3, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (3, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (3, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
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
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)

    class Pylon4:
        STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__,
        )
        STA_05_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            4,
            WeaponsFA18EFG.STA_05_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_05_CHEEK__TGPMNT_Empty_Weapon_Replacable_Assembly__WRA__Adapter = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_Empty_Weapon_Replacable_Assembly__WRA__Adapter,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_05_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        AWW_13_DATALINK_POD = (4, Weapons.AWW_13_DATALINK_POD)

    class Pylon5:
        STA_06_SUU78_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_84___2000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU33_2x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_06_SUU78_BRU32_1x_FPU_13_A__340_GAL__w__ASG_34A_V_1_IRST___Player_limited_to_330_Gallons_and_Fuel_Only_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_13_A__340_GAL__w__ASG_34A_V_1_IRST___Player_limited_to_330_Gallons_and_Fuel_Only_,
        )
        STA_06_SUU78_BRU32_1x_A_A_42R_1__300_GAL__Aerial_Refueling_System___Player_limited_to_Fuel_Only_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_A_A_42R_1__300_GAL__Aerial_Refueling_System___Player_limited_to_Fuel_Only_,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING_Targeting_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING_Targeting_Pod,
        )
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    class Pylon6:
        STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_07_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)

    class Pylon7:
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_JS_1X_BRU32_AGM-154C}
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_MK_BR2_ROCKEYE}
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_08_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_10_08_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_08_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_JS_1X_BRU32_AGM-154A}
        STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_JS_1X_BRU32_AGM-154C}
        STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU42_1x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_2x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_3x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_MK_BR2_ROCKEYE}
        STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42___1_x_ADM_141A_TALD = (7, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (7, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (7, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
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
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)

    class Pylon8:
        STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_3x_ADM_141A_TALD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_10_MB_MK_BR55_1X_GBU-32V}
        STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        # ERRR {SUPERHORNET_PYLON_10_MB_MK_BR2_MK-82Y}
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_10_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        BRU_42___1_x_ADM_141A_TALD = (8, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (8, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (8, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (8, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            8,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )

    class Pylon9:
        STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_11_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells__570_GAL_AI__330_GAL_PLAYER = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells__570_GAL_AI__330_GAL_PLAYER,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange,
        )

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
class FA_18F(PlaneType):
    id = "FA-18F"
    flyable = True
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 4482
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    networked_datalink = True
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
            "Brutal",
            "Buckshot",
            "Cannon",
            "Carbine",
            "Carnage",
            "Colt",
            "Demon",
            "Falcon",
            "Pistol",
            "Ramrod",
            "Ruthless",
            "Sabre",
            "Savage",
            "Sonic",
            "Sword",
            "Wolf",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": 0,
        "AIRCRAFT_ID_SEQ": 0,
        "CJS_PARAM_BLOCK": 1,
        "CJS_PARAM_DEMO": 0,
        "CJS_PARAM_USAFLAG": 0,
        "HelmetMountedDevice": 1,
        "HelmetMountedDeviceWSO": 1,
        "STA02_SUU80AA_MOUNT": 0,
        "STA03_SUU79AA_MOUNT": 0,
        "STA04_SUU79AA_MOUNT": 0,
        "STA05_LAU116B_MOUNT": 0,
        "STA06_SUU78AA_MOUNT": 0,
        "STA07_LAU116B_MOUNT": 0,
        "STA08_SUU79AA_MOUNT": 0,
        "STA09_SUU79AA_MOUNT": 0,
        "STA10_SUU80AA_MOUNT": 0,
        "OuterBoard": 0,
        "InnerBoard": 0,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS_MODE": 0,
        "DYNAMIC_BUNO_01": 0,
        "DYNAMIC_BUNO_02": 5,
        "DYNAMIC_BUNO_03": 4,
        "DYNAMIC_BUNO_04": 8,
        "DYNAMIC_BUNO_05": 1,
        "DYNAMIC_BUNO_06": 6,
        "NetCrewControlPriority": 0,
        "AIDisabled": 0,
        "HumanOrchestra": 0,
        "CJS_DEBUG_MSGS": 0,
        "CJS_SYSTEM_MSGS": 0,
    }

    class Properties:

        class SoloFlight:
            id = "SoloFlight"

            class Values:
                Pilot_And_WSO = 0
                Pilot_Only = 1

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Pattern_Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class CJS_PARAM_BLOCK:
            id = "CJS_PARAM_BLOCK"

            class Values:
                Block_III___Cosmetic = 0
                Block_II____Cosmetic = 1

        class CJS_PARAM_DEMO:
            id = "CJS_PARAM_DEMO"

            class Values:
                None_ = 0
                Installed = 1

        class CJS_PARAM_USAFLAG:
            id = "CJS_PARAM_USAFLAG"

            class Values:
                None_ = 0
                Displayed___Left_Side = 1
                Displayed___Right_Side = 2

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class HelmetMountedDeviceWSO:
            id = "HelmetMountedDeviceWSO"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class STA02_SUU80AA_MOUNT:
            id = "STA02_SUU80AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA03_SUU79AA_MOUNT:
            id = "STA03_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA04_SUU79AA_MOUNT:
            id = "STA04_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA05_LAU116B_MOUNT:
            id = "STA05_LAU116B_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA06_SUU78AA_MOUNT:
            id = "STA06_SUU78AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA07_LAU116B_MOUNT:
            id = "STA07_LAU116B_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA08_SUU79AA_MOUNT:
            id = "STA08_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA09_SUU79AA_MOUNT:
            id = "STA09_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA10_SUU80AA_MOUNT:
            id = "STA10_SUU80AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

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

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS_MODE:
            id = "DYNAMIC_BUNOS_MODE"

            class Values:
                DISABLED___NONE = 0
                BOEING_STANDARD = 1

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0

        class AIDisabled:
            id = "AIDisabled"

            class Values:
                Disabled = 0

        class HumanOrchestra:
            id = "HumanOrchestra"

            class Values:
                Disabled = 0

        class CJS_DEBUG_MSGS:
            id = "CJS_DEBUG_MSGS"

            class Values:
                Disabled = 0
                Enabled = 1

        class CJS_SYSTEM_MSGS:
            id = "CJS_SYSTEM_MSGS"

            class Values:
                Disabled = 0
                Enabled = 1

    properties = {
        "CJS_LABEL_CORE_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_CORE_VER",
            control="label",
            label="CJS PKG Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_FOXT_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_FOXT_VER",
            control="label",
            label="F/A-18F Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_CREW": UnitPropertyDescription(
            identifier="CJS_LABEL_CREW",
            control="label",
            label="-> Aircraft Crew Settings",
            player_only=False,
            x_lbl=0,
        ),
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="comboList",
            label="Aircraft Crew",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot And WSO",
                1: "Pilot Only",
            },
        ),
        "CJS_LABEL_EQUIP": UnitPropertyDescription(
            identifier="CJS_LABEL_EQUIP",
            control="label",
            label="-> Aircraft / Pilot Equipment Settings",
            player_only=False,
            x_lbl=0,
        ),
        "AIRCRAFT_ID_SEQ": UnitPropertyDescription(
            identifier="AIRCRAFT_ID_SEQ",
            control="comboList",
            label="Aircraft Strobe Sequence",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pattern Norm",
                1: "Pattern 0A",
                2: "Pattern 1B",
                3: "Pattern 2C",
                4: "Pattern 3D",
                5: "Pattern 4E",
                6: "Pattern 5F",
            },
        ),
        "CJS_PARAM_BLOCK": UnitPropertyDescription(
            identifier="CJS_PARAM_BLOCK",
            control="comboList",
            label="Aircraft Block (Visual Only)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Block III - Cosmetic",
                1: "Block II  - Cosmetic",
            },
        ),
        "CJS_PARAM_DEMO": UnitPropertyDescription(
            identifier="CJS_PARAM_DEMO",
            control="comboList",
            label="Aircraft Demo Team Equipment",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Installed",
            },
        ),
        "CJS_PARAM_USAFLAG": UnitPropertyDescription(
            identifier="CJS_PARAM_USAFLAG",
            control="comboList",
            label="Hood Displayed Folded Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Displayed - Left Side",
                2: "Displayed - Right Side",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Pilot Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "HelmetMountedDeviceWSO": UnitPropertyDescription(
            identifier="HelmetMountedDeviceWSO",
            control="comboList",
            label="WSO Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "CJS_LABEL_PYLONS": UnitPropertyDescription(
            identifier="CJS_LABEL_PYLONS",
            control="label",
            label="-> Pylon Control (User req. to remove stores)",
            player_only=False,
            x_lbl=0,
        ),
        "STA02_SUU80AA_MOUNT": UnitPropertyDescription(
            identifier="STA02_SUU80AA_MOUNT",
            control="comboList",
            label="STA 2 SUU-80A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA03_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA03_SUU79AA_MOUNT",
            control="comboList",
            label="STA 3 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA04_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA04_SUU79AA_MOUNT",
            control="comboList",
            label="STA 4 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA05_LAU116B_MOUNT": UnitPropertyDescription(
            identifier="STA05_LAU116B_MOUNT",
            control="comboList",
            label="STA 5 LAU-116B/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA06_SUU78AA_MOUNT": UnitPropertyDescription(
            identifier="STA06_SUU78AA_MOUNT",
            control="comboList",
            label="STA 6 SUU-78A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA07_LAU116B_MOUNT": UnitPropertyDescription(
            identifier="STA07_LAU116B_MOUNT",
            control="comboList",
            label="STA 7 LAU-116B/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA08_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA08_SUU79AA_MOUNT",
            control="comboList",
            label="STA 8 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA09_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA09_SUU79AA_MOUNT",
            control="comboList",
            label="STA 9 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA10_SUU80AA_MOUNT": UnitPropertyDescription(
            identifier="STA10_SUU80AA_MOUNT",
            control="comboList",
            label="STA 10 SUU-80A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "ED_LABEL_ROCKETS": UnitPropertyDescription(
            identifier="ED_LABEL_ROCKETS",
            control="label",
            label="-> Aircraft Rocket Settings",
            player_only=True,
            x_lbl=0,
        ),
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
        "ED_LABEL_DATALINK": UnitPropertyDescription(
            identifier="ED_LABEL_DATALINK",
            control="label",
            label="-> Aircraft Datalink Settings",
            player_only=False,
            x_lbl=0,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
            w_ctrl=150,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
            w_ctrl=150,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
            w_ctrl=150,
        ),
        "DYNAMIC_BORTS": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS",
            control="label",
            label="-> Aircraft Identification Stencils",
            player_only=False,
            x_lbl=0,
        ),
        "DYNAMIC_BORTS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS_MODE",
            control="comboList",
            label="Aircraft Bort Identification Type",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "USN STANDARD",
                2: "RAAF FIGHTER",
                3: "RAAF GROWLER",
                4: "KAF LEGACY",
                5: "KAF SUPER HORNET",
            },
        ),
        "DYNAMIC_BUNOS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BUNOS_MODE",
            control="comboList",
            label="Aircraft Bureau Number",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "BOEING STANDARD",
            },
        ),
        "DYNAMIC_BUNO_01": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_01",
            control="comboList",
            label="Aircraft BUNO Digit #1",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_02": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_02",
            control="comboList",
            label="Aircraft BUNO Digit #2",
            player_only=False,
            default=5,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_03": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_03",
            control="comboList",
            label="Aircraft BUNO Digit #3",
            player_only=False,
            default=4,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_04": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_04",
            control="comboList",
            label="Aircraft BUNO Digit #4",
            player_only=False,
            default=8,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_05": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_05",
            control="comboList",
            label="Aircraft BUNO Digit #5",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_06": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_06",
            control="comboList",
            label="Aircraft BUNO Digit #6",
            player_only=False,
            default=6,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "ED_LABEL_MULTIPLAYER": UnitPropertyDescription(
            identifier="ED_LABEL_MULTIPLAYER",
            control="label",
            label="-> Multi-Player / Crew Settings, Not Integrated Yet",
            player_only=True,
            x_lbl=0,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
            },
        ),
        "AIDisabled": UnitPropertyDescription(
            identifier="AIDisabled",
            control="comboList",
            label="AI Crew Members",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="comboList",
            label="Multicrew Player Slots",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
            },
        ),
        "CJS_LABEL_DEBUG": UnitPropertyDescription(
            identifier="CJS_LABEL_DEBUG",
            control="label",
            label="-> Trouble Shooting / Debug Messages",
            player_only=True,
            x_lbl=0,
        ),
        "CJS_DEBUG_MSGS": UnitPropertyDescription(
            identifier="CJS_DEBUG_MSGS",
            control="comboList",
            label="Display Debug Msgs At MSN Start",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
                1: "Enabled",
            },
        ),
        "CJS_SYSTEM_MSGS": UnitPropertyDescription(
            identifier="CJS_SYSTEM_MSGS",
            control="comboList",
            label="Display Addon System Msgs",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
                1: "Enabled",
            },
        ),
    }

    livery_name = "FA-18F"  # from livery_entry

    class Pylon1:
        STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_01_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )

    class Pylon2:
        STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-38}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-32V}
        STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR2_MK-8Y}
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_03_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        BRU_42___1_x_ADM_141A_TALD = (2, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (2, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (2, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (2, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )

    class Pylon3:
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_JS_1X_BRU32_AGM-154C}
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32V}
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_,
        )
        STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_BR2_ROCKEYE}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_04_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_04_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_04_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_04_SUU79_BRU42_1x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_04_SUU79_BRU42_2x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_04_SUU79_BRU42_3x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_JS_1X_BRU32_AGM-154A}
        STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_JS_BRU32_AGM-154C}
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_MK_BR2_ROCKEYE}
        STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_PD_1X_ALQ-167}
        STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42___1_x_ADM_141A_TALD = (3, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (3, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (3, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
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
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)

    class Pylon4:
        STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__,
        )
        STA_05_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            4,
            WeaponsFA18EFG.STA_05_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_05_CHEEK__TGPMNT_Empty_Weapon_Replacable_Assembly__WRA__Adapter = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_Empty_Weapon_Replacable_Assembly__WRA__Adapter,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_05_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        AWW_13_DATALINK_POD = (4, Weapons.AWW_13_DATALINK_POD)

    class Pylon5:
        STA_06_SUU78_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_84___2000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU33_2x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_06_SUU78_BRU32_1x_FPU_13_A__340_GAL__w__ASG_34A_V_1_IRST___Player_limited_to_330_Gallons_and_Fuel_Only_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_13_A__340_GAL__w__ASG_34A_V_1_IRST___Player_limited_to_330_Gallons_and_Fuel_Only_,
        )
        STA_06_SUU78_BRU32_1x_A_A_42R_1__300_GAL__Aerial_Refueling_System___Player_limited_to_Fuel_Only_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_A_A_42R_1__300_GAL__Aerial_Refueling_System___Player_limited_to_Fuel_Only_,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING_Targeting_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING_Targeting_Pod,
        )
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    class Pylon6:
        STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_07_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)

    class Pylon7:
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_JS_1X_BRU32_AGM-154C}
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_MK_BR2_ROCKEYE}
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_08_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_10_08_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_08_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_JS_1X_BRU32_AGM-154A}
        STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_JS_1X_BRU32_AGM-154C}
        STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU42_1x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_2x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_3x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_MK_BR2_ROCKEYE}
        STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42___1_x_ADM_141A_TALD = (7, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (7, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (7, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
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
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)

    class Pylon8:
        STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_3x_ADM_141A_TALD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_10_MB_MK_BR55_1X_GBU-32V}
        STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        # ERRR {SUPERHORNET_PYLON_10_MB_MK_BR2_MK-82Y}
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_10_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        BRU_42___1_x_ADM_141A_TALD = (8, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (8, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (8, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (8, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            8,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )

    class Pylon9:
        STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_11_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells__570_GAL_AI__330_GAL_PLAYER = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells__570_GAL_AI__330_GAL_PLAYER,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange,
        )

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
    fuel_max = 4482
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    networked_datalink = True
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
            "Brutal",
            "Buckshot",
            "Cannon",
            "Carbine",
            "Carnage",
            "Colt",
            "Demon",
            "Falcon",
            "Pistol",
            "Ramrod",
            "Ruthless",
            "Sabre",
            "Savage",
            "Sonic",
            "Sword",
            "Wolf",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": 0,
        "AIRCRAFT_ID_SEQ": 0,
        "CJS_PARAM_BLOCK": 1,
        "CJS_PARAM_DEMO": 0,
        "CJS_PARAM_USAFLAG": 0,
        "HelmetMountedDevice": 1,
        "HelmetMountedDeviceWSO": 1,
        "STA02_SUU80AA_MOUNT": 0,
        "STA03_SUU79AA_MOUNT": 0,
        "STA04_SUU79AA_MOUNT": 0,
        "STA05_LAU116B_MOUNT": 0,
        "STA06_SUU78AA_MOUNT": 0,
        "STA07_LAU116B_MOUNT": 0,
        "STA08_SUU79AA_MOUNT": 0,
        "STA09_SUU79AA_MOUNT": 0,
        "STA10_SUU80AA_MOUNT": 0,
        "OuterBoard": 0,
        "InnerBoard": 0,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS_MODE": 0,
        "DYNAMIC_BUNO_01": 0,
        "DYNAMIC_BUNO_02": 5,
        "DYNAMIC_BUNO_03": 7,
        "DYNAMIC_BUNO_04": 2,
        "DYNAMIC_BUNO_05": 6,
        "DYNAMIC_BUNO_06": 8,
        "NetCrewControlPriority": 0,
        "AIDisabled": 0,
        "HumanOrchestra": 0,
        "CJS_DEBUG_MSGS": 0,
        "CJS_SYSTEM_MSGS": 0,
    }

    class Properties:

        class SoloFlight:
            id = "SoloFlight"

            class Values:
                Pilot_And_WSO = 0
                Pilot_Only = 1

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Pattern_Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class CJS_PARAM_BLOCK:
            id = "CJS_PARAM_BLOCK"

            class Values:
                Block_III___Cosmetic = 0
                Block_II____Cosmetic = 1

        class CJS_PARAM_DEMO:
            id = "CJS_PARAM_DEMO"

            class Values:
                None_ = 0
                Installed = 1

        class CJS_PARAM_USAFLAG:
            id = "CJS_PARAM_USAFLAG"

            class Values:
                None_ = 0
                Displayed___Left_Side = 1
                Displayed___Right_Side = 2

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class HelmetMountedDeviceWSO:
            id = "HelmetMountedDeviceWSO"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class STA02_SUU80AA_MOUNT:
            id = "STA02_SUU80AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA03_SUU79AA_MOUNT:
            id = "STA03_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA04_SUU79AA_MOUNT:
            id = "STA04_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA05_LAU116B_MOUNT:
            id = "STA05_LAU116B_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA06_SUU78AA_MOUNT:
            id = "STA06_SUU78AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA07_LAU116B_MOUNT:
            id = "STA07_LAU116B_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA08_SUU79AA_MOUNT:
            id = "STA08_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA09_SUU79AA_MOUNT:
            id = "STA09_SUU79AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

        class STA10_SUU80AA_MOUNT:
            id = "STA10_SUU80AA_MOUNT"

            class Values:
                Mounted = 0
                Removed = 1

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

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS_MODE:
            id = "DYNAMIC_BUNOS_MODE"

            class Values:
                DISABLED___NONE = 0
                BOEING_STANDARD = 1

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0

        class AIDisabled:
            id = "AIDisabled"

            class Values:
                Disabled = 0

        class HumanOrchestra:
            id = "HumanOrchestra"

            class Values:
                Disabled = 0

        class CJS_DEBUG_MSGS:
            id = "CJS_DEBUG_MSGS"

            class Values:
                Disabled = 0
                Enabled = 1

        class CJS_SYSTEM_MSGS:
            id = "CJS_SYSTEM_MSGS"

            class Values:
                Disabled = 0
                Enabled = 1

    properties = {
        "CJS_LABEL_CORE_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_CORE_VER",
            control="label",
            label="CJS PKG Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_GAMM_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_GAMM_VER",
            control="label",
            label="E/A-18G Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_CREW": UnitPropertyDescription(
            identifier="CJS_LABEL_CREW",
            control="label",
            label="-> Aircraft Crew Settings",
            player_only=False,
            x_lbl=0,
        ),
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="comboList",
            label="Aircraft Crew",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot And WSO",
                1: "Pilot Only",
            },
        ),
        "CJS_LABEL_EQUIP": UnitPropertyDescription(
            identifier="CJS_LABEL_EQUIP",
            control="label",
            label="-> Aircraft / Pilot Equipment Settings",
            player_only=False,
            x_lbl=0,
        ),
        "AIRCRAFT_ID_SEQ": UnitPropertyDescription(
            identifier="AIRCRAFT_ID_SEQ",
            control="comboList",
            label="Aircraft Strobe Sequence",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pattern Norm",
                1: "Pattern 0A",
                2: "Pattern 1B",
                3: "Pattern 2C",
                4: "Pattern 3D",
                5: "Pattern 4E",
                6: "Pattern 5F",
            },
        ),
        "CJS_PARAM_BLOCK": UnitPropertyDescription(
            identifier="CJS_PARAM_BLOCK",
            control="comboList",
            label="Aircraft Block (Visual Only)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Block III - Cosmetic",
                1: "Block II  - Cosmetic",
            },
        ),
        "CJS_PARAM_DEMO": UnitPropertyDescription(
            identifier="CJS_PARAM_DEMO",
            control="comboList",
            label="Aircraft Demo Team Equipment",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Installed",
            },
        ),
        "CJS_PARAM_USAFLAG": UnitPropertyDescription(
            identifier="CJS_PARAM_USAFLAG",
            control="comboList",
            label="Hood Displayed Folded Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Displayed - Left Side",
                2: "Displayed - Right Side",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Pilot Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "HelmetMountedDeviceWSO": UnitPropertyDescription(
            identifier="HelmetMountedDeviceWSO",
            control="comboList",
            label="WSO Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "CJS_LABEL_PYLONS": UnitPropertyDescription(
            identifier="CJS_LABEL_PYLONS",
            control="label",
            label="-> Pylon Control (User req. to remove stores)",
            player_only=False,
            x_lbl=0,
        ),
        "STA02_SUU80AA_MOUNT": UnitPropertyDescription(
            identifier="STA02_SUU80AA_MOUNT",
            control="comboList",
            label="STA 2 SUU-80A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA03_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA03_SUU79AA_MOUNT",
            control="comboList",
            label="STA 3 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA04_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA04_SUU79AA_MOUNT",
            control="comboList",
            label="STA 4 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA05_LAU116B_MOUNT": UnitPropertyDescription(
            identifier="STA05_LAU116B_MOUNT",
            control="comboList",
            label="STA 5 LAU-116B/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA06_SUU78AA_MOUNT": UnitPropertyDescription(
            identifier="STA06_SUU78AA_MOUNT",
            control="comboList",
            label="STA 6 SUU-78A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA07_LAU116B_MOUNT": UnitPropertyDescription(
            identifier="STA07_LAU116B_MOUNT",
            control="comboList",
            label="STA 7 LAU-116B/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA08_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA08_SUU79AA_MOUNT",
            control="comboList",
            label="STA 8 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA09_SUU79AA_MOUNT": UnitPropertyDescription(
            identifier="STA09_SUU79AA_MOUNT",
            control="comboList",
            label="STA 9 SUU-79A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "STA10_SUU80AA_MOUNT": UnitPropertyDescription(
            identifier="STA10_SUU80AA_MOUNT",
            control="comboList",
            label="STA 10 SUU-80A/A Pylon",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Mounted",
                1: "Removed",
            },
        ),
        "ED_LABEL_ROCKETS": UnitPropertyDescription(
            identifier="ED_LABEL_ROCKETS",
            control="label",
            label="-> Aircraft Rocket Settings",
            player_only=True,
            x_lbl=0,
        ),
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
        "ED_LABEL_DATALINK": UnitPropertyDescription(
            identifier="ED_LABEL_DATALINK",
            control="label",
            label="-> Aircraft Datalink Settings",
            player_only=False,
            x_lbl=0,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
            w_ctrl=150,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
            w_ctrl=150,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
            w_ctrl=150,
        ),
        "DYNAMIC_BORTS": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS",
            control="label",
            label="-> Aircraft Identification Stencils",
            player_only=False,
            x_lbl=0,
        ),
        "DYNAMIC_BORTS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS_MODE",
            control="comboList",
            label="Aircraft Bort Identification Type",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "USN STANDARD",
                2: "RAAF FIGHTER",
                3: "RAAF GROWLER",
                4: "KAF LEGACY",
                5: "KAF SUPER HORNET",
            },
        ),
        "DYNAMIC_BUNOS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BUNOS_MODE",
            control="comboList",
            label="Aircraft Bureau Number",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "BOEING STANDARD",
            },
        ),
        "DYNAMIC_BUNO_01": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_01",
            control="comboList",
            label="Aircraft BUNO Digit #1",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_02": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_02",
            control="comboList",
            label="Aircraft BUNO Digit #2",
            player_only=False,
            default=5,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_03": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_03",
            control="comboList",
            label="Aircraft BUNO Digit #3",
            player_only=False,
            default=7,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_04": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_04",
            control="comboList",
            label="Aircraft BUNO Digit #4",
            player_only=False,
            default=2,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_05": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_05",
            control="comboList",
            label="Aircraft BUNO Digit #5",
            player_only=False,
            default=6,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_06": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_06",
            control="comboList",
            label="Aircraft BUNO Digit #6",
            player_only=False,
            default=8,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "ED_LABEL_MULTIPLAYER": UnitPropertyDescription(
            identifier="ED_LABEL_MULTIPLAYER",
            control="label",
            label="-> Multi-Player / Crew Settings, Not Integrated Yet",
            player_only=True,
            x_lbl=0,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
            },
        ),
        "AIDisabled": UnitPropertyDescription(
            identifier="AIDisabled",
            control="comboList",
            label="AI Crew Members",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="comboList",
            label="Multicrew Player Slots",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
            },
        ),
        "CJS_LABEL_DEBUG": UnitPropertyDescription(
            identifier="CJS_LABEL_DEBUG",
            control="label",
            label="-> Trouble Shooting / Debug Messages",
            player_only=True,
            x_lbl=0,
        ),
        "CJS_DEBUG_MSGS": UnitPropertyDescription(
            identifier="CJS_DEBUG_MSGS",
            control="comboList",
            label="Display Debug Msgs At MSN Start",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
                1: "Enabled",
            },
        ),
        "CJS_SYSTEM_MSGS": UnitPropertyDescription(
            identifier="CJS_SYSTEM_MSGS",
            control="comboList",
            label="Display Addon System Msgs",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Disabled",
                1: "Enabled",
            },
        ),
    }

    livery_name = "EA-18G"  # from livery_entry

    class Pylon1:
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        STA_03_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_Hi_Band_Jamming_Pod = (
            1,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_Hi_Band_Jamming_Pod,
        )
        STA_03_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Jamming_Pod = (
            1,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Jamming_Pod,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            1,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            1,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )

    class Pylon2:
        STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-38}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-32V}
        STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR2_MK-8Y}
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_03_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        BRU_42___1_x_ADM_141A_TALD = (2, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (2, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (2, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (2, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            2,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            2,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )

    class Pylon3:
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_JS_1X_BRU32_AGM-154C}
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32V}
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_,
        )
        STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_BR2_ROCKEYE}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_04_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_02_04_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_04_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_04_SUU79_BRU42_1x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_04_SUU79_BRU42_2x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_04_SUU79_BRU42_3x_ADM_141A_TALD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_JS_1X_BRU32_AGM-154A}
        STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_JS_BRU32_AGM-154C}
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_MK_BR2_ROCKEYE}
        STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_PD_1X_ALQ-167}
        STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_02_04_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_02_04_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            3,
            WeaponsFA18EFG.STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_04_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42___1_x_ADM_141A_TALD = (3, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (3, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (3, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
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
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)

    class Pylon4:
        STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__,
        )
        STA_05_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            4,
            WeaponsFA18EFG.STA_05_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_05_CHEEK__TGPMNT_Empty_Weapon_Replacable_Assembly__WRA__Adapter = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_Empty_Weapon_Replacable_Assembly__WRA__Adapter,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_05_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        AWW_13_DATALINK_POD = (4, Weapons.AWW_13_DATALINK_POD)

    class Pylon5:
        STA_06_SUU78_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_06_SUU78_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_06_SUU78_BRU33_2x_Mk_84___2000lb_GP_Bomb_LD = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_06_SUU78_BRU33_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_06_SUU78_BRU33_2x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU33_2x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_06_SUU78_BRU32_1x_FPU_13_A__340_GAL__w__ASG_34A_V_1_IRST___Player_limited_to_330_Gallons_and_Fuel_Only_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_13_A__340_GAL__w__ASG_34A_V_1_IRST___Player_limited_to_330_Gallons_and_Fuel_Only_,
        )
        STA_06_SUU78_BRU32_1x_A_A_42R_1__300_GAL__Aerial_Refueling_System___Player_limited_to_Fuel_Only_ = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_A_A_42R_1__300_GAL__Aerial_Refueling_System___Player_limited_to_Fuel_Only_,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING_Targeting_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING_Targeting_Pod,
        )
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )
        STA_06_SUU78_BRU32_1x_AN_ALQ_99_ICAP_III_Lo_Band_Jamming_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_ALQ_99_ICAP_III_Lo_Band_Jamming_Pod,
        )

    class Pylon6:
        STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_07_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)

    class Pylon7:
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_JS_1X_BRU32_AGM-154C}
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_MK_BR2_ROCKEYE}
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar,
        )
        STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_08_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_10_08_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_08_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_JS_1X_BRU32_AGM-154A}
        STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_JS_1X_BRU32_AGM-154C}
        STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU42_1x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_2x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_3x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_MK_BR2_ROCKEYE}
        STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons__,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons__,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_10_08_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_10_08_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_ = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___Current_Hill_s_AIM_174B_Mod_Required_,
        )
        STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_2x_AIM_174B_Gunslinger___Active_Radar_AAM___AI_Only_,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42___1_x_ADM_141A_TALD = (7, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (7, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (7, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
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
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)

    class Pylon8:
        STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar,
        )
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow___Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder___IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_CATM_9M_Sidewinder___Captive_ACM_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_3x_ADM_141A_TALD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_10_MB_MK_BR55_1X_GBU-32V}
        STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        # ERRR {SUPERHORNET_PYLON_10_MB_MK_BR2_MK-82Y}
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD_,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9M_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9X_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120B_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120C_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_09_10_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_CATM_9M_Sidewinder___Captive_ACM___AI_Only_,
        )
        STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only__,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only__,
        )
        STA_09_10_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_2x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required__,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C___AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        BRU_42___1_x_ADM_141A_TALD = (8, Weapons.BRU_42___1_x_ADM_141A_TALD)
        BRU_42___2_x_ADM_141A_TALD = (8, Weapons.BRU_42___2_x_ADM_141A_TALD)
        BRU_42___3_x_ADM_141A_TALD = (8, Weapons.BRU_42___3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (8, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            8,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.BRU_33_with_2_x_Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )

    class Pylon9:
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder___IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9M_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_9X_Sidewinder___Captive_ACM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_ = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___Modern_Missiles_Mod_Required_,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_ = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_II_Sidewinder___IR_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_ = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM___AI_Only_,
        )
        STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_CATM_120C_AMRAAM___Captive_ACM,
        )
        STA_09_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_Hi_Band_Jamming_Pod = (
            9,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_Hi_Band_Jamming_Pod,
        )
        STA_09_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Jamming_Pod = (
            9,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Jamming_Pod,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_ = (
            9,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL____Player_limited_to_330_Gallons_,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_ = (
            9,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A__480_GAL___High_Vis____Player_limited_to_330_Gallons_,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells__570_GAL_AI__330_GAL_PLAYER = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells__570_GAL_AI__330_GAL_PLAYER,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange,
        )

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
class FA_18ET(PlaneType):
    id = "FA-18ET"
    group_size_max = 1
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 13154
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    networked_datalink = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}
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
            "Brutal",
            "Buckshot",
            "Cannon",
            "Carbine",
            "Carnage",
            "Colt",
            "Demon",
            "Falcon",
            "Pistol",
            "Ramrod",
            "Ruthless",
            "Sabre",
            "Savage",
            "Sonic",
            "Sword",
            "Wolf",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": 0,
        "CJS_PARAM_BLOCK": 1,
        "CJS_PARAM_USAFLAG": 0,
        "HelmetMountedDevice": 1,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS_MODE": 0,
        "DYNAMIC_BUNO_01": 0,
        "DYNAMIC_BUNO_02": 5,
        "DYNAMIC_BUNO_03": 5,
        "DYNAMIC_BUNO_04": 8,
        "DYNAMIC_BUNO_05": 9,
        "DYNAMIC_BUNO_06": 3,
    }

    class Properties:

        class SoloFlight:
            id = "SoloFlight"

            class Values:
                Pilot_Only = 0

        class CJS_PARAM_BLOCK:
            id = "CJS_PARAM_BLOCK"

            class Values:
                Block_III___Cosmetic = 0
                Block_II____Cosmetic = 1

        class CJS_PARAM_USAFLAG:
            id = "CJS_PARAM_USAFLAG"

            class Values:
                None_ = 0
                Displayed___Left_Side = 1
                Displayed___Right_Side = 2

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS_MODE:
            id = "DYNAMIC_BUNOS_MODE"

            class Values:
                DISABLED___NONE = 0
                BOEING_STANDARD = 1

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

    properties = {
        "CJS_LABEL_CORE_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_CORE_VER",
            control="label",
            label="CJS PKG Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_TNKE_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_TNKE_VER",
            control="label",
            label="K/A-18E Revision: 11.21.2025",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_CREW": UnitPropertyDescription(
            identifier="CJS_LABEL_CREW",
            control="label",
            label="-> Aircraft Crew Settings",
            player_only=False,
            x_lbl=0,
        ),
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="comboList",
            label="Aircraft Crew",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot Only",
            },
        ),
        "CJS_LABEL_EQUIP": UnitPropertyDescription(
            identifier="CJS_LABEL_EQUIP",
            control="label",
            label="-> Aircraft / Pilot Equipment Settings",
            player_only=False,
            x_lbl=0,
        ),
        "CJS_PARAM_BLOCK": UnitPropertyDescription(
            identifier="CJS_PARAM_BLOCK",
            control="comboList",
            label="Aircraft Block (Visual Only)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Block III - Cosmetic",
                1: "Block II  - Cosmetic",
            },
        ),
        "CJS_PARAM_USAFLAG": UnitPropertyDescription(
            identifier="CJS_PARAM_USAFLAG",
            control="comboList",
            label="Hood Displayed Folded Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Displayed - Left Side",
                2: "Displayed - Right Side",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Pilot Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "ED_LABEL_DATALINK": UnitPropertyDescription(
            identifier="ED_LABEL_DATALINK",
            control="label",
            label="-> Aircraft Datalink Settings",
            player_only=False,
            x_lbl=0,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
            w_ctrl=150,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
            w_ctrl=150,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
            w_ctrl=150,
        ),
        "DYNAMIC_BORTS": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS",
            control="label",
            label="-> Aircraft Identification Stencils",
            player_only=False,
            x_lbl=0,
        ),
        "DYNAMIC_BORTS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS_MODE",
            control="comboList",
            label="Aircraft Bort Identification Type",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "USN STANDARD",
                2: "RAAF FIGHTER",
                3: "RAAF GROWLER",
                4: "KAF LEGACY",
                5: "KAF SUPER HORNET",
            },
        ),
        "DYNAMIC_BUNOS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BUNOS_MODE",
            control="comboList",
            label="Aircraft Bureau Number",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "BOEING STANDARD",
            },
        ),
        "DYNAMIC_BUNO_01": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_01",
            control="comboList",
            label="Aircraft BUNO Digit #1",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_02": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_02",
            control="comboList",
            label="Aircraft BUNO Digit #2",
            player_only=False,
            default=5,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_03": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_03",
            control="comboList",
            label="Aircraft BUNO Digit #3",
            player_only=False,
            default=5,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_04": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_04",
            control="comboList",
            label="Aircraft BUNO Digit #4",
            player_only=False,
            default=8,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_05": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_05",
            control="comboList",
            label="Aircraft BUNO Digit #5",
            player_only=False,
            default=9,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_06": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_06",
            control="comboList",
            label="Aircraft BUNO Digit #6",
            player_only=False,
            default=3,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
    }

    livery_name = "FA-18E"  # from livery_entry

    pylons: Set[int] = set()

    tasks = [task.Refueling]
    task_default = task.Refueling


@planemod
class FA_18FT(PlaneType):
    id = "FA-18FT"
    group_size_max = 1
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 12736
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    networked_datalink = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}
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
            "Brutal",
            "Buckshot",
            "Cannon",
            "Carbine",
            "Carnage",
            "Colt",
            "Demon",
            "Falcon",
            "Pistol",
            "Ramrod",
            "Ruthless",
            "Sabre",
            "Savage",
            "Sonic",
            "Sword",
            "Wolf",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": 0,
        "CJS_PARAM_BLOCK": 1,
        "CJS_PARAM_USAFLAG": 0,
        "HelmetMountedDevice": 1,
        "HelmetMountedDeviceWSO": 1,
        "VoiceCallsignLabel": None,
        "VoiceCallsignNumber": None,
        "STN_L16": None,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS_MODE": 0,
        "DYNAMIC_BUNO_01": 0,
        "DYNAMIC_BUNO_02": 5,
        "DYNAMIC_BUNO_03": 5,
        "DYNAMIC_BUNO_04": 8,
        "DYNAMIC_BUNO_05": 1,
        "DYNAMIC_BUNO_06": 6,
    }

    class Properties:

        class SoloFlight:
            id = "SoloFlight"

            class Values:
                Pilot_And_WSO = 0
                Pilot_Only = 1

        class CJS_PARAM_BLOCK:
            id = "CJS_PARAM_BLOCK"

            class Values:
                Block_III___Cosmetic = 0
                Block_II____Cosmetic = 1

        class CJS_PARAM_USAFLAG:
            id = "CJS_PARAM_USAFLAG"

            class Values:
                None_ = 0
                Displayed___Left_Side = 1
                Displayed___Right_Side = 2

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class HelmetMountedDeviceWSO:
            id = "HelmetMountedDeviceWSO"

            class Values:
                Visor_Only = 0
                JHMCS = 1
                NVG = 2
                Helmet_Only__No_Visor = 3

        class VoiceCallsignLabel:
            id = "VoiceCallsignLabel"

        class VoiceCallsignNumber:
            id = "VoiceCallsignNumber"

        class STN_L16:
            id = "STN_L16"

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS_MODE:
            id = "DYNAMIC_BUNOS_MODE"

            class Values:
                DISABLED___NONE = 0
                BOEING_STANDARD = 1

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

    properties = {
        "CJS_LABEL_CORE_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_CORE_VER",
            control="label",
            label="CJS PKG Revision: 04.19.2026",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_TNKF_VER": UnitPropertyDescription(
            identifier="CJS_LABEL_TNKF_VER",
            control="label",
            label="K/A-18F Revision: 11.21.2025",
            player_only=False,
            x_lbl=100,
        ),
        "CJS_LABEL_CREW": UnitPropertyDescription(
            identifier="CJS_LABEL_CREW",
            control="label",
            label="-> Aircraft Crew Settings",
            player_only=False,
            x_lbl=0,
        ),
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="comboList",
            label="Aircraft Crew",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot And WSO",
                1: "Pilot Only",
            },
        ),
        "CJS_LABEL_EQUIP": UnitPropertyDescription(
            identifier="CJS_LABEL_EQUIP",
            control="label",
            label="-> Aircraft / Pilot Equipment Settings",
            player_only=False,
            x_lbl=0,
        ),
        "CJS_PARAM_BLOCK": UnitPropertyDescription(
            identifier="CJS_PARAM_BLOCK",
            control="comboList",
            label="Aircraft Block (Visual Only)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Block III - Cosmetic",
                1: "Block II  - Cosmetic",
            },
        ),
        "CJS_PARAM_USAFLAG": UnitPropertyDescription(
            identifier="CJS_PARAM_USAFLAG",
            control="comboList",
            label="Hood Displayed Folded Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "None",
                1: "Displayed - Left Side",
                2: "Displayed - Right Side",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Pilot Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "HelmetMountedDeviceWSO": UnitPropertyDescription(
            identifier="HelmetMountedDeviceWSO",
            control="comboList",
            label="WSO Helmet Mounted Device",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "Visor Only",
                1: "JHMCS",
                2: "NVG",
                3: "Helmet Only, No Visor",
            },
        ),
        "ED_LABEL_DATALINK": UnitPropertyDescription(
            identifier="ED_LABEL_DATALINK",
            control="label",
            label="-> Aircraft Datalink Settings",
            player_only=False,
            x_lbl=0,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
            w_ctrl=150,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
            w_ctrl=150,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
            w_ctrl=150,
        ),
        "DYNAMIC_BORTS": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS",
            control="label",
            label="-> Aircraft Identification Stencils",
            player_only=False,
            x_lbl=0,
        ),
        "DYNAMIC_BORTS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BORTS_MODE",
            control="comboList",
            label="Aircraft Bort Identification Type",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "USN STANDARD",
                2: "RAAF FIGHTER",
                3: "RAAF GROWLER",
                4: "KAF LEGACY",
                5: "KAF SUPER HORNET",
            },
        ),
        "DYNAMIC_BUNOS_MODE": UnitPropertyDescription(
            identifier="DYNAMIC_BUNOS_MODE",
            control="comboList",
            label="Aircraft Bureau Number",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "DISABLED / NONE",
                1: "BOEING STANDARD",
            },
        ),
        "DYNAMIC_BUNO_01": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_01",
            control="comboList",
            label="Aircraft BUNO Digit #1",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_02": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_02",
            control="comboList",
            label="Aircraft BUNO Digit #2",
            player_only=False,
            default=5,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_03": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_03",
            control="comboList",
            label="Aircraft BUNO Digit #3",
            player_only=False,
            default=5,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_04": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_04",
            control="comboList",
            label="Aircraft BUNO Digit #4",
            player_only=False,
            default=8,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_05": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_05",
            control="comboList",
            label="Aircraft BUNO Digit #5",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
        "DYNAMIC_BUNO_06": UnitPropertyDescription(
            identifier="DYNAMIC_BUNO_06",
            control="comboList",
            label="Aircraft BUNO Digit #6",
            player_only=False,
            default=6,
            w_ctrl=150,
            values={
                0: "1",
                1: "2",
                2: "3",
                3: "4",
                4: "5",
                5: "6",
                6: "7",
                7: "8",
                8: "9",
                9: "0",
                10: "Blank",
            },
        ),
    }

    livery_name = "FA-18F"  # from livery_entry

    pylons: Set[int] = set()

    tasks = [task.Refueling]
    task_default = task.Refueling
