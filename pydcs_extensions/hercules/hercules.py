from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons


class HerculesWeapons:
    GAU_23A_Chain_Gun__30mm_ = {
        "clsid": "{Herc_GAU_23A_Chain_Gun}",
        "name": "GAU 23A Chain Gun (30mm)",
        "weight": 595.9426,
    }
    Herc_AAA_GEPARD = {
        "clsid": "Herc_AAA_GEPARD",
        "name": "AAA GEPARD [34720lb]",
        "weight": 15782,
    }
    Herc_AAA_Vulcan_M163 = {
        "clsid": "Herc_AAA_Vulcan_M163",
        "name": "AAA Vulcan M163 [21666lb]",
        "weight": 9848,
    }
    Herc_Ammo_AGM_154C_missiles = {
        "clsid": "Herc_Ammo_AGM_154C_missiles",
        "name": "Ammo AGM-154C*10 [10648lb]",
        "weight": 4960,
    }
    Herc_Ammo_AGM_65D_missiles = {
        "clsid": "Herc_Ammo_AGM_65D_missiles",
        "name": "Ammo AGM-65D*10 [4800lb]",
        "weight": 2300,
    }
    Herc_Ammo_AGM_65E_missiles = {
        "clsid": "Herc_Ammo_AGM_65E_missiles",
        "name": "Ammo AGM-65E*10 [6292lb]",
        "weight": 2980,
    }
    Herc_Ammo_AGM_65G_missiles = {
        "clsid": "Herc_Ammo_AGM_65G_missiles",
        "name": "Ammo AGM-65G*10 [6622lb]",
        "weight": 3130,
    }
    Herc_Ammo_AGM_65H_missiles = {
        "clsid": "Herc_Ammo_AGM_65H_missiles",
        "name": "Ammo AGM-65H*10 [4570lb]",
        "weight": 2200,
    }
    Herc_Ammo_AGM_65K_missiles = {
        "clsid": "Herc_Ammo_AGM_65K_missiles",
        "name": "Ammo AGM-65K*10 [7920lb]",
        "weight": 3720,
    }
    Herc_Ammo_AGM_84A_missiles = {
        "clsid": "Herc_Ammo_AGM_84A_missiles",
        "name": "Ammo AGM-84A*8 [11651lb]",
        "weight": 5408,
    }
    Herc_Ammo_AGM_84E_missiles = {
        "clsid": "Herc_Ammo_AGM_84E_missiles",
        "name": "Ammo AGM-84E*8 [11651lb]",
        "weight": 5408,
    }
    Herc_Ammo_AGM_88C_missiles = {
        "clsid": "Herc_Ammo_AGM_88C_missiles",
        "name": "Ammo AGM-88C*10 [7920lb]",
        "weight": 3730,
    }
    Herc_Ammo_AIM120B_missiles = {
        "clsid": "Herc_Ammo_AIM120B_missiles",
        "name": "Ammo AIM-120B*24 [11193lb]",
        "weight": 5208,
    }
    Herc_Ammo_AIM120C_missiles = {
        "clsid": "Herc_Ammo_AIM120C_missiles",
        "name": "Ammo AIM-120C*24 [10665lb]",
        "weight": 5208,
    }
    Herc_Ammo_AIM54C_missiles = {
        "clsid": "Herc_Ammo_AIM54C_missiles",
        "name": "Ammo AIM-54C*18 [18335lb]",
        "weight": 8454,
    }
    Herc_Ammo_AIM7M_missiles = {
        "clsid": "Herc_Ammo_AIM7M_missiles",
        "name": "Ammo AIM-7M*24 [14995lb]",
        "weight": 6936,
    }
    Herc_Ammo_AIM9M_missiles = {
        "clsid": "Herc_Ammo_AIM9M_missiles",
        "name": "Ammo AIM-9M*30 [7128lb]",
        "weight": 4860,
    }
    Herc_Ammo_AIM9P5_missiles = {
        "clsid": "Herc_Ammo_AIM9P5_missiles",
        "name": "Ammo AIM-9P5*30 [5676lb]",
        "weight": 2700,
    }
    Herc_Ammo_AIM9X_missiles = {
        "clsid": "Herc_Ammo_AIM9X_missiles",
        "name": "Ammo AIM-9X*30 [5676lb]",
        "weight": 2700,
    }
    Herc_Ammo_BETAB500SP_bombs = {
        "clsid": "Herc_Ammo_BETAB500SP_bombs",
        "name": "Ammo BetAB-500ShP*10 [9328lb]",
        "weight": 4360,
    }
    Herc_Ammo_BETAB500_bombs = {
        "clsid": "Herc_Ammo_BETAB500_bombs",
        "name": "Ammo BetAB-500*10 [9460lb]",
        "weight": 4420,
    }
    Herc_Ammo_CBU_103_bombs = {
        "clsid": "Herc_Ammo_CBU_103_bombs",
        "name": "Ammo CBU-103*10 [10142lb]",
        "weight": 4730,
    }
    Herc_Ammo_CBU_105_bombs = {
        "clsid": "Herc_Ammo_CBU_105_bombs",
        "name": "Ammo CBU-105*10 [11022lb]",
        "weight": 5130,
    }
    Herc_Ammo_CBU_87_bombs = {
        "clsid": "Herc_Ammo_CBU_87_bombs",
        "name": "Ammo CBU-87*10 [9460lb]",
        "weight": 4420,
    }
    Herc_Ammo_CBU_97_bombs = {
        "clsid": "Herc_Ammo_CBU_97_bombs",
        "name": "Ammo CBU-97*10 [10362lb]",
        "weight": 4830,
    }
    Herc_Ammo_FAB100_bombs = {
        "clsid": "Herc_Ammo_FAB100_bombs",
        "name": "Ammo FAB-100*20 [4400lb",
        "weight": 2120,
    }
    Herc_Ammo_FAB250_bombs = {
        "clsid": "Herc_Ammo_FAB250_bombs",
        "name": "Ammo FAB-250*20 [11000lb]",
        "weight": 5120,
    }
    Herc_Ammo_FAB500_bombs = {
        "clsid": "Herc_Ammo_FAB500_bombs",
        "name": "Ammo FAB-500*10 [11000lb]",
        "weight": 5120,
    }
    Herc_Ammo_GBU_10_bombs = {
        "clsid": "Herc_Ammo_GBU_10_bombs",
        "name": "Ammo GBU-10*6 [15340lb]",
        "weight": 7092,
    }
    Herc_Ammo_GBU_12_bombs = {
        "clsid": "Herc_Ammo_GBU_12_bombs",
        "name": "Ammo GBU-12*16 [9680lb]",
        "weight": 4520,
    }
    Herc_Ammo_GBU_16_bombs = {
        "clsid": "Herc_Ammo_GBU_16_bombs",
        "name": "Ammo GBU-16*10 [12408lb]",
        "weight": 5760,
    }
    Herc_Ammo_GBU_31_V3B_bombs = {
        "clsid": "Herc_Ammo_GBU_31_V3B_bombs",
        "name": "Ammo GBU-31V3B*6 [12949lb]",
        "weight": 6006,
    }
    Herc_Ammo_GBU_31_VB_bombs = {
        "clsid": "Herc_Ammo_GBU_31_VB_bombs",
        "name": "Ammo GBU-31V/B*6 [12328lb]",
        "weight": 5724,
    }
    Herc_Ammo_GBU_38_bombs = {
        "clsid": "Herc_Ammo_GBU_38_bombs",
        "name": "Ammo GBU-38*10 [6028lb]",
        "weight": 2860,
    }
    Herc_Ammo_hydra_HE_rockets = {
        "clsid": "Herc_Ammo_hydra_HE_rockets",
        "name": "Ammo M151 Hydra HE*80 [4752lb]",
        "weight": 2280,
    }
    Herc_Ammo_hydra_WP_rockets = {
        "clsid": "Herc_Ammo_hydra_WP_rockets",
        "name": "Ammo M156 Hydra WP*80 [4752lb]",
        "weight": 2280,
    }
    Herc_Ammo_KAB500KR_bombs = {
        "clsid": "Herc_Ammo_KAB500KR_bombs",
        "name": "Ammo KAB-500kr*10 [12320lb]",
        "weight": 5720,
    }
    Herc_Ammo_KH25ML_missiles = {
        "clsid": "Herc_Ammo_KH25ML_missiles",
        "name": "Ammo Kh-25ML*10 [7920lb]",
        "weight": 3720,
    }
    Herc_Ammo_KH25MPU_missiles = {
        "clsid": "Herc_Ammo_KH25MPU_missiles",
        "name": "Ammo Kh-25MPU*10 [8140lb]",
        "weight": 3820,
    }
    Herc_Ammo_KH29L_missiles = {
        "clsid": "Herc_Ammo_KH29L_missiles",
        "name": "Ammo Kh-29L*10 [16434lb]",
        "weight": 7590,
    }
    Herc_Ammo_KH29T_missiles = {
        "clsid": "Herc_Ammo_KH29T_missiles",
        "name": "Ammo Kh-29T*10 [16720lb]",
        "weight": 7720,
    }
    Herc_Ammo_KH58U_missiles = {
        "clsid": "Herc_Ammo_KH58U_missiles",
        "name": "Ammo Kh-58U*10 [16060lb]",
        "weight": 7420,
    }
    Herc_Ammo_KMGU296AO25KO_bombs = {
        "clsid": "Herc_Ammo_KMGU296AO25KO_bombs",
        "name": "Ammo KMGU-2 - 96 PTAB-2.5KO*10 [11440lb]",
        "weight": 5320,
    }
    Herc_Ammo_KMGU296AO25RT_bombs = {
        "clsid": "Herc_Ammo_KMGU296AO25RT_bombs",
        "name": "Ammo KMGU-2 - 96 AO-2.5RT*10 [11440lb]",
        "weight": 5320,
    }
    Herc_Ammo_M117_bombs = {
        "clsid": "Herc_Ammo_M117_bombs",
        "name": "Ammo M117*16 [11968lb]",
        "weight": 5560,
    }
    Herc_Ammo_MAGIC2_missiles = {
        "clsid": "Herc_Ammo_MAGIC2_missiles",
        "name": "Ammo Magic2*30 [5676lb]",
        "weight": 2700,
    }
    Herc_Ammo_MK20_bombs = {
        "clsid": "Herc_Ammo_MK20_bombs",
        "name": "Ammo MK20*20 [9768lb]",
        "weight": 4560,
    }
    Herc_Ammo_Mk_82AIR_bombs = {
        "clsid": "Herc_Ammo_Mk_82AIR_bombs",
        "name": "Ammo Mk-82AIR*20 [11044lb]",
        "weight": 4940,
    }
    Herc_Ammo_Mk_82Snake_bombs = {
        "clsid": "Herc_Ammo_Mk_82Snake_bombs",
        "name": "Ammo Mk-82Snakeye*20 [11880lb]",
        "weight": 4940,
    }
    Herc_Ammo_Mk_82_bombs = {
        "clsid": "Herc_Ammo_Mk_82_bombs",
        "name": "Ammo Mk-82*20 [10560lb]",
        "weight": 4940,
    }
    Herc_Ammo_Mk_83_bombs = {
        "clsid": "Herc_Ammo_Mk_83_bombs",
        "name": "Ammo Mk-83*10 [9834lb]",
        "weight": 4590,
    }
    Herc_Ammo_Mk_84_bombs = {
        "clsid": "Herc_Ammo_Mk_84_bombs",
        "name": "Ammo Mk-84*8 [15735b]",
        "weight": 7272,
    }
    Herc_Ammo_R27ER_missiles = {
        "clsid": "Herc_Ammo_R27ER_missiles",
        "name": "Ammo R-27ER*24 [18480lb]",
        "weight": 8520,
    }
    Herc_Ammo_R27ET_missiles = {
        "clsid": "Herc_Ammo_R27ET_missiles",
        "name": "Ammo R-27ET*24 [18480lb",
        "weight": 8496,
    }
    Herc_Ammo_R27R_missiles = {
        "clsid": "Herc_Ammo_R27R_missiles",
        "name": "Ammo R-27R*24 [13359lb]",
        "weight": 6192,
    }
    Herc_Ammo_R27T_missiles = {
        "clsid": "Herc_Ammo_R27T_missiles",
        "name": "Ammo R-27T*24 [13359lb]",
        "weight": 6192,
    }
    Herc_Ammo_R60M_missiles = {
        "clsid": "Herc_Ammo_R60M_missiles",
        "name": "Ammo R-60M*30 [2904lb]",
        "weight": 1440,
    }
    Herc_Ammo_R77_missiles = {
        "clsid": "Herc_Ammo_R77_missiles",
        "name": "Ammo R-77*24 [9240lb]",
        "weight": 4320,
    }
    Herc_Ammo_RBK250PTAB25M_bombs = {
        "clsid": "Herc_Ammo_RBK250PTAB25M_bombs",
        "name": "Ammo RBK-250 PTAB-2.5M*20 [12012lb]",
        "weight": 5580,
    }
    Herc_Ammo_RBK500255PTAB105_bombs = {
        "clsid": "Herc_Ammo_RBK500255PTAB105_bombs",
        "name": "Ammo RBK-500-255 PTAB-10-5*10 [9394lb]",
        "weight": 4390,
    }
    Herc_Ammo_RBK500PTAB1M_bombs = {
        "clsid": "Herc_Ammo_RBK500PTAB1M_bombs",
        "name": "Ammo RBK-500 PTAB-1M*10 [9394lb]",
        "weight": 4390,
    }
    Herc_Ammo_S24B_missiles = {
        "clsid": "Herc_Ammo_S24B_missiles",
        "name": "Ammo S-24B*20 [10340lb]",
        "weight": 4820,
    }
    Herc_Ammo_S25L_missiles = {
        "clsid": "Herc_Ammo_S25L_missiles",
        "name": "Ammo S-25L*10 [11000b]",
        "weight": 5120,
    }
    Herc_Ammo_S25OFM_missiles = {
        "clsid": "Herc_Ammo_S25OFM_missiles",
        "name": "Ammo S-25OFM*10 [10890lb]",
        "weight": 5070,
    }
    Herc_Ammo_S530D_missiles = {
        "clsid": "Herc_Ammo_S530D_missiles",
        "name": "Ammo Super 530D*24 [6480lb]",
        "weight": 6600,
    }
    Herc_Ammo_SAB100_bombs = {
        "clsid": "Herc_Ammo_SAB100_bombs",
        "name": "Ammo SAB-100*20 [11000lb]",
        "weight": 2120,
    }
    Herc_Ammo_Vikhr_missiles = {
        "clsid": "Herc_Ammo_Vikhr_missiles",
        "name": "Ammo Vikhr*48 [5808lb]",
        "weight": 2760,
    }
    Herc_APC_BTR_80 = {
        "clsid": "Herc_APC_BTR_80",
        "name": "APC BTR-80 [23936lb]",
        "weight": 10880,
    }
    Herc_APC_COBRA = {
        "clsid": "Herc_APC_COBRA",
        "name": "APC Cobra [10912lb]",
        "weight": 4960,
    }
    Herc_APC_LAV_25 = {
        "clsid": "Herc_APC_LAV_25",
        "name": "APC LAV-25 [22514lb]",
        "weight": 10234,
    }
    Herc_APC_M1025_HMMWV = {
        "clsid": "Herc_APC_M1025_HMMWV",
        "name": "M1025 HMMWV [6160lb]",
        "weight": 2800,
    }
    Herc_APC_M1043_HMMWV_Armament = {
        "clsid": "Herc_APC_M1043_HMMWV_Armament",
        "name": "APC M1043 HMMWV Armament [7023lb]",
        "weight": 3192,
    }
    Herc_APC_M113 = {
        "clsid": "Herc_APC_M113",
        "name": "APC M113 [21624lb]",
        "weight": 9830,
    }
    Herc_APC_MTLB = {
        "clsid": "Herc_APC_MTLB",
        "name": "APC MTLB [26000lb]",
        "weight": 12000,
    }
    Herc_ART_GVOZDIKA = {
        "clsid": "Herc_ART_GVOZDIKA",
        "name": "ART GVOZDIKA [34720lb]",
        "weight": 15782,
    }
    Herc_ART_NONA = {
        "clsid": "Herc_ART_NONA",
        "name": "ART 2S9 NONA [19140lb]",
        "weight": 8700,
    }
    Herc_ARV_BRDM_2 = {
        "clsid": "Herc_ARV_BRDM_2",
        "name": "ARV BRDM-2 [12320lb]",
        "weight": 5600,
    }
    Herc_ATGM_M1045_HMMWV_TOW = {
        "clsid": "Herc_ATGM_M1045_HMMWV_TOW",
        "name": "ATGM M1045 HMMWV TOW [7183lb]",
        "weight": 3265,
    }
    Herc_ATGM_M1134_Stryker = {
        "clsid": "Herc_ATGM_M1134_Stryker",
        "name": "ATGM M1134 Stryker [30337lb]",
        "weight": 13790,
    }
    Herc_BattleStation = {
        "clsid": "Herc_BattleStation",
        "name": "Battle Station",
        "weight": 0,
    }
    Herc_Ext_Fuel_Tank = {
        "clsid": "Herc_Ext_Fuel_Tank",
        "name": "External Fuel Tank",
        "weight": 4131,
    }
    Herc_GEN_CRATE = {
        "clsid": "Herc_GEN_CRATE",
        "name": "Generic Crate [20000lb]",
        "weight": 9071,
    }
    Herc_HEMTT_TFFT = {
        "clsid": "Herc_HEMTT_TFFT",
        "name": "HEMTT TFFT [34400lb]",
        "weight": 15634,
    }
    Herc_IFV_BMD1 = {
        "clsid": "Herc_IFV_BMD1",
        "name": "IFV BMD-1 [18040lb]",
        "weight": 8200,
    }
    Herc_IFV_BMP_1 = {
        "clsid": "Herc_IFV_BMP_1",
        "name": "IFV BMP-1 [23232lb]",
        "weight": 10560,
    }
    Herc_IFV_BMP_2 = {
        "clsid": "Herc_IFV_BMP_2",
        "name": "IFV BMP-2 [25168lb]",
        "weight": 11440,
    }
    Herc_IFV_BMP_3 = {
        "clsid": "Herc_IFV_BMP_3",
        "name": "IFV BMP-3 [32912lb]",
        "weight": 14960,
    }
    Herc_IFV_BTRD = {
        "clsid": "Herc_IFV_BTRD",
        "name": "IFV BTR-D [18040lb]",
        "weight": 8200,
    }
    Herc_IFV_M2A2_Bradley = {
        "clsid": "Herc_IFV_M2A2_Bradley",
        "name": "IFV M2A2 Bradley [34720lb]",
        "weight": 15782,
    }
    Herc_IFV_MARDER = {
        "clsid": "Herc_IFV_MARDER",
        "name": "IFV MARDER [34720lb]",
        "weight": 15782,
    }
    Herc_IFV_MCV80_Warrior = {
        "clsid": "Herc_IFV_MCV80_Warrior",
        "name": "IFV MCV-80 [34720lb]",
        "weight": 15782,
    }
    Herc_IFV_TPZ = {
        "clsid": "Herc_IFV_TPZ",
        "name": "IFV TPZ FUCH [33440lb]",
        "weight": 15200,
    }
    Herc_JATO = {"clsid": "Herc_JATO", "name": "JATO", "weight": 0}
    Herc_M_818 = {
        "clsid": "Herc_M_818",
        "name": "Transport M818 [16000lb]",
        "weight": 7272,
    }
    Herc_SAM_13 = {
        "clsid": "Herc_SAM_13",
        "name": "SAM SA-13 STRELA [21624lb]",
        "weight": 9830,
    }
    Herc_SAM_19 = {
        "clsid": "Herc_SAM_19",
        "name": "SAM SA-19 Tunguska 2S6 [34720lb]",
        "weight": 15782,
    }
    Herc_SAM_CHAPARRAL = {
        "clsid": "Herc_SAM_CHAPARRAL",
        "name": "SAM CHAPARRAL [21624lb]",
        "weight": 9830,
    }
    Herc_SAM_LINEBACKER = {
        "clsid": "Herc_SAM_LINEBACKER",
        "name": "SAM LINEBACKER [34720lb]",
        "weight": 15782,
    }
    Herc_SAM_M1097_HMMWV = {
        "clsid": "Herc_SAM_M1097_HMMWV",
        "name": "SAM Avenger M1097 [7200lb]",
        "weight": 3273,
    }
    Herc_SAM_ROLAND_ADS = {
        "clsid": "Herc_SAM_ROLAND_ADS",
        "name": "SAM ROLAND ADS [34720lb]",
        "weight": 15782,
    }
    Herc_SAM_ROLAND_LN = {
        "clsid": "Herc_SAM_ROLAND_LN",
        "name": "SAM ROLAND LN [34720b]",
        "weight": 15782,
    }
    Herc_Soldier_Squad = {
        "clsid": "Herc_Soldier_Squad",
        "name": "Squad 30 x Soldier [7950lb]",
        "weight": 120,
    }
    Herc_SPG_M1126_Stryker_ICV = {
        "clsid": "Herc_SPG_M1126_Stryker_ICV",
        "name": "APC M1126 Stryker ICV [29542lb]",
        "weight": 13429,
    }
    Herc_SPG_M1128_Stryker_MGS = {
        "clsid": "Herc_SPG_M1128_Stryker_MGS",
        "name": "SPG M1128 Stryker MGS [33036lb]",
        "weight": 15016,
    }
    Herc_Tanker_HEMTT = {
        "clsid": "Herc_Tanker_HEMTT",
        "name": "Tanker M978 HEMTT [34000lb]",
        "weight": 15455,
    }
    Herc_TIGR_233036 = {
        "clsid": "Herc_TIGR_233036",
        "name": "Transport Tigr [15900lb]",
        "weight": 7200,
    }
    Herc_UAZ_469 = {
        "clsid": "Herc_UAZ_469",
        "name": "Transport UAZ-469 [3747lb]",
        "weight": 1700,
    }
    Herc_URAL_375 = {
        "clsid": "Herc_URAL_375",
        "name": "Transport URAL-375 [14815lb]",
        "weight": 6734,
    }
    Herc_ZSU_23_4 = {
        "clsid": "Herc_ZSU_23_4",
        "name": "AAA ZSU-23-4 Shilka [32912lb]",
        "weight": 14960,
    }
    M61_Vulcan_Rotary_Cannon__20mm_ = {
        "clsid": "{Herc_M61_Vulcan_Rotary_Cannon}",
        "name": "M61 Vulcan Rotary Cannon (20mm)",
        "weight": 595.9426,
    }
    _105mm_Howitzer = {
        "clsid": "{Herc_105mm_Howitzer}",
        "name": "105mm Howitzer",
        "weight": 595.9426,
    }
    Herc_GBU_43_B_MOAB_ = {
        "clsid": "Herc_GBU-43/B(MOAB)",
        "name": "GBU-43/B(MOAB)",
        "weight": 9800,
    }


class Hercules(PlaneType):
    id = "Hercules"
    flyable = True
    height = 11.84
    width = 40.41
    length = 34.36
    fuel_max = 19759
    max_speed = 669.6
    chaff = 840
    flare = 840
    charge_total = 1680
    chaff_charge_size = 1
    flare_charge_size = 1
    radio_frequency = 118

    panel_radio = {
        1: {
            "channels": {
                1: 118,
                2: 119,
                4: 121,
                8: 125,
                16: 133,
                17: 134,
                9: 126,
                18: 135,
                5: 122,
                10: 127,
                20: 143,
                11: 128,
                3: 120,
                6: 123,
                12: 129,
                13: 130,
                7: 124,
                14: 131,
                19: 136,
                15: 132,
            },
        },
    }

    class Liveries:
        class USSR(Enum):
            default = "default"

        class Georgia(Enum):
            default = "default"

        class Venezuela(Enum):
            default = "default"

        class Australia(Enum):
            default = "default"

        class Israel(Enum):
            default = "default"

        class Combined_Joint_Task_Forces_Blue(Enum):
            default = "default"

        class Sudan(Enum):
            default = "default"

        class Norway(Enum):
            default = "default"

        class Romania(Enum):
            default = "default"

        class Iran(Enum):
            default = "default"

        class Ukraine(Enum):
            default = "default"

        class Libya(Enum):
            default = "default"

        class Belgium(Enum):
            default = "default"

        class Slovakia(Enum):
            default = "default"

        class Greece(Enum):
            default = "default"

        class UK(Enum):
            default = "default"

        class Third_Reich(Enum):
            default = "default"

        class Hungary(Enum):
            default = "default"

        class Abkhazia(Enum):
            default = "default"

        class Morocco(Enum):
            default = "default"

        class United_Nations_Peacekeepers(Enum):
            default = "default"

        class Switzerland(Enum):
            default = "default"

        class SouthOssetia(Enum):
            default = "default"

        class Vietnam(Enum):
            default = "default"

        class China(Enum):
            default = "default"

        class Yemen(Enum):
            default = "default"

        class Kuwait(Enum):
            default = "default"

        class Serbia(Enum):
            default = "default"

        class Oman(Enum):
            default = "default"

        class India(Enum):
            default = "default"

        class Egypt(Enum):
            default = "default"

        class TheNetherlands(Enum):
            default = "default"

        class Poland(Enum):
            default = "default"

        class Syria(Enum):
            default = "default"

        class Finland(Enum):
            default = "default"

        class Kazakhstan(Enum):
            default = "default"

        class Denmark(Enum):
            default = "default"

        class Sweden(Enum):
            default = "default"

        class Croatia(Enum):
            default = "default"

        class CzechRepublic(Enum):
            default = "default"

        class GDR(Enum):
            default = "default"

        class Yugoslavia(Enum):
            default = "default"

        class Bulgaria(Enum):
            default = "default"

        class SouthKorea(Enum):
            default = "default"

        class Tunisia(Enum):
            default = "default"

        class Combined_Joint_Task_Forces_Red(Enum):
            default = "default"

        class Lebanon(Enum):
            default = "default"

        class Portugal(Enum):
            default = "default"

        class Cuba(Enum):
            default = "default"

        class Insurgents(Enum):
            default = "default"

        class SaudiArabia(Enum):
            default = "default"

        class France(Enum):
            default = "default"

        class USA(Enum):
            default = "default"

        class Honduras(Enum):
            default = "default"

        class Qatar(Enum):
            default = "default"

        class Russia(Enum):
            default = "default"

        class United_Arab_Emirates(Enum):
            default = "default"

        class Italian_Social_Republi(Enum):
            default = "default"

        class Austria(Enum):
            default = "default"

        class Bahrain(Enum):
            default = "default"

        class Italy(Enum):
            default = "default"

        class Chile(Enum):
            default = "default"

        class Turkey(Enum):
            default = "default"

        class Philippines(Enum):
            default = "default"

        class Algeria(Enum):
            default = "default"

        class Pakistan(Enum):
            default = "default"

        class Malaysia(Enum):
            default = "default"

        class Indonesia(Enum):
            default = "default"

        class Iraq(Enum):
            default = "default"

        class Germany(Enum):
            default = "default"

        class South_Africa(Enum):
            default = "default"

        class Jordan(Enum):
            default = "default"

        class Mexico(Enum):
            default = "default"

        class USAFAggressors(Enum):
            default = "default"

        class Brazil(Enum):
            default = "default"

        class Spain(Enum):
            default = "default"

        class Belarus(Enum):
            default = "default"

        class Canada(Enum):
            default = "default"

        class NorthKorea(Enum):
            default = "default"

        class Ethiopia(Enum):
            default = "default"

        class Japan(Enum):
            default = "default"

        class Thailand(Enum):
            default = "default"

    class Pylon1:
        Herc_JATO = (1, HerculesWeapons.Herc_JATO)

    class Pylon2:
        LAU_68___7_2_75__rockets_M257__Parachute_illumination_ = (
            2,
            Weapons.LAU_68___7_2_75__rockets_M257__Parachute_illumination_,
        )
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (2, Weapons.Smokewinder___orange)
        Herc_Ext_Fuel_Tank = (2, HerculesWeapons.Herc_Ext_Fuel_Tank)

    class Pylon3:
        LAU_68___7_2_75__rockets_M257__Parachute_illumination_ = (
            3,
            Weapons.LAU_68___7_2_75__rockets_M257__Parachute_illumination_,
        )
        Smokewinder___red = (3, Weapons.Smokewinder___red)
        Smokewinder___green = (3, Weapons.Smokewinder___green)
        Smokewinder___blue = (3, Weapons.Smokewinder___blue)
        Smokewinder___white = (3, Weapons.Smokewinder___white)
        Smokewinder___yellow = (3, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (3, Weapons.Smokewinder___orange)
        Herc_Ext_Fuel_Tank = (3, HerculesWeapons.Herc_Ext_Fuel_Tank)

    class Pylon4:
        LAU_68___7_2_75__rockets_M257__Parachute_illumination_ = (
            4,
            Weapons.LAU_68___7_2_75__rockets_M257__Parachute_illumination_,
        )
        Smokewinder___red = (4, Weapons.Smokewinder___red)
        Smokewinder___green = (4, Weapons.Smokewinder___green)
        Smokewinder___blue = (4, Weapons.Smokewinder___blue)
        Smokewinder___white = (4, Weapons.Smokewinder___white)
        Smokewinder___yellow = (4, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (4, Weapons.Smokewinder___orange)
        Herc_Ext_Fuel_Tank = (4, HerculesWeapons.Herc_Ext_Fuel_Tank)

    class Pylon5:
        LAU_68___7_2_75__rockets_M257__Parachute_illumination_ = (
            5,
            Weapons.LAU_68___7_2_75__rockets_M257__Parachute_illumination_,
        )
        Smokewinder___red = (5, Weapons.Smokewinder___red)
        Smokewinder___green = (5, Weapons.Smokewinder___green)
        Smokewinder___blue = (5, Weapons.Smokewinder___blue)
        Smokewinder___white = (5, Weapons.Smokewinder___white)
        Smokewinder___yellow = (5, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (5, Weapons.Smokewinder___orange)
        Herc_Ext_Fuel_Tank = (5, HerculesWeapons.Herc_Ext_Fuel_Tank)

    class Pylon6:
        M61_Vulcan_Rotary_Cannon__20mm_ = (
            6,
            HerculesWeapons.M61_Vulcan_Rotary_Cannon__20mm_,
        )

    class Pylon7:
        GAU_23A_Chain_Gun__30mm_ = (7, HerculesWeapons.GAU_23A_Chain_Gun__30mm_)

    class Pylon8:
        _105mm_Howitzer = (8, HerculesWeapons._105mm_Howitzer)

    class Pylon9:
        Herc_BattleStation = (9, HerculesWeapons.Herc_BattleStation)

    class Pylon10:
        Herc_Ammo_AGM_65D_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_65D_missiles)
        Herc_Ammo_AGM_65H_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_65H_missiles)
        Herc_Ammo_AGM_65G_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_65G_missiles)
        Herc_Ammo_AGM_65E_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_65E_missiles)
        Herc_Ammo_AGM_88C_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_88C_missiles)
        Herc_Ammo_AGM_65K_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_65K_missiles)
        Herc_Ammo_Vikhr_missiles = (10, HerculesWeapons.Herc_Ammo_Vikhr_missiles)
        Herc_Ammo_AGM_84A_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_84A_missiles)
        Herc_Ammo_AGM_84E_missiles = (10, HerculesWeapons.Herc_Ammo_AGM_84E_missiles)
        Herc_Ammo_KH25ML_missiles = (10, HerculesWeapons.Herc_Ammo_KH25ML_missiles)
        Herc_Ammo_KH25MPU_missiles = (10, HerculesWeapons.Herc_Ammo_KH25MPU_missiles)
        Herc_Ammo_KH29T_missiles = (10, HerculesWeapons.Herc_Ammo_KH29T_missiles)
        Herc_Ammo_KH29L_missiles = (10, HerculesWeapons.Herc_Ammo_KH29L_missiles)
        Herc_Ammo_KH58U_missiles = (10, HerculesWeapons.Herc_Ammo_KH58U_missiles)
        Herc_Ammo_S24B_missiles = (10, HerculesWeapons.Herc_Ammo_S24B_missiles)
        Herc_Ammo_S25OFM_missiles = (10, HerculesWeapons.Herc_Ammo_S25OFM_missiles)
        Herc_Ammo_S25L_missiles = (10, HerculesWeapons.Herc_Ammo_S25L_missiles)
        # Herc_Ammo_TOW_missiles = (10, HerculesWeapons.Herc_Ammo_TOW_missiles)
        Herc_Ammo_GBU_10_bombs = (10, HerculesWeapons.Herc_Ammo_GBU_10_bombs)
        Herc_Ammo_GBU_12_bombs = (10, HerculesWeapons.Herc_Ammo_GBU_12_bombs)
        Herc_Ammo_GBU_16_bombs = (10, HerculesWeapons.Herc_Ammo_GBU_16_bombs)
        Herc_Ammo_GBU_31_VB_bombs = (10, HerculesWeapons.Herc_Ammo_GBU_31_VB_bombs)
        Herc_Ammo_GBU_31_V3B_bombs = (10, HerculesWeapons.Herc_Ammo_GBU_31_V3B_bombs)
        Herc_Ammo_GBU_38_bombs = (10, HerculesWeapons.Herc_Ammo_GBU_38_bombs)
        Herc_Ammo_CBU_87_bombs = (10, HerculesWeapons.Herc_Ammo_CBU_87_bombs)
        Herc_Ammo_CBU_97_bombs = (10, HerculesWeapons.Herc_Ammo_CBU_97_bombs)
        Herc_Ammo_CBU_103_bombs = (10, HerculesWeapons.Herc_Ammo_CBU_103_bombs)
        Herc_Ammo_CBU_105_bombs = (10, HerculesWeapons.Herc_Ammo_CBU_105_bombs)
        Herc_Ammo_Mk_82_bombs = (10, HerculesWeapons.Herc_Ammo_Mk_82_bombs)
        Herc_Ammo_Mk_82AIR_bombs = (10, HerculesWeapons.Herc_Ammo_Mk_82AIR_bombs)
        Herc_Ammo_Mk_82Snake_bombs = (10, HerculesWeapons.Herc_Ammo_Mk_82Snake_bombs)
        Herc_Ammo_Mk_83_bombs = (10, HerculesWeapons.Herc_Ammo_Mk_83_bombs)
        Herc_Ammo_Mk_84_bombs = (10, HerculesWeapons.Herc_Ammo_Mk_84_bombs)
        Herc_Ammo_FAB100_bombs = (10, HerculesWeapons.Herc_Ammo_FAB100_bombs)
        Herc_Ammo_FAB250_bombs = (10, HerculesWeapons.Herc_Ammo_FAB250_bombs)
        Herc_Ammo_FAB500_bombs = (10, HerculesWeapons.Herc_Ammo_FAB500_bombs)
        Herc_Ammo_BETAB500_bombs = (10, HerculesWeapons.Herc_Ammo_BETAB500_bombs)
        Herc_Ammo_BETAB500SP_bombs = (10, HerculesWeapons.Herc_Ammo_BETAB500SP_bombs)
        Herc_Ammo_KAB500KR_bombs = (10, HerculesWeapons.Herc_Ammo_KAB500KR_bombs)
        Herc_Ammo_RBK250PTAB25M_bombs = (
            10,
            HerculesWeapons.Herc_Ammo_RBK250PTAB25M_bombs,
        )
        Herc_Ammo_RBK500255PTAB105_bombs = (
            10,
            HerculesWeapons.Herc_Ammo_RBK500255PTAB105_bombs,
        )
        Herc_Ammo_RBK500PTAB1M_bombs = (
            10,
            HerculesWeapons.Herc_Ammo_RBK500PTAB1M_bombs,
        )
        # ERRR Herc_Ammo_Herc_Ammo_M117_bombs_bombs
        Herc_Ammo_KMGU296AO25RT_bombs = (
            10,
            HerculesWeapons.Herc_Ammo_KMGU296AO25RT_bombs,
        )
        Herc_Ammo_KMGU296AO25KO_bombs = (
            10,
            HerculesWeapons.Herc_Ammo_KMGU296AO25KO_bombs,
        )
        Herc_Ammo_MK20_bombs = (10, HerculesWeapons.Herc_Ammo_MK20_bombs)
        Herc_Ammo_SAB100_bombs = (10, HerculesWeapons.Herc_Ammo_SAB100_bombs)
        Herc_Ammo_hydra_HE_rockets = (10, HerculesWeapons.Herc_Ammo_hydra_HE_rockets)
        Herc_Ammo_hydra_WP_rockets = (10, HerculesWeapons.Herc_Ammo_hydra_WP_rockets)
        Herc_Ammo_AIM9M_missiles = (10, HerculesWeapons.Herc_Ammo_AIM9M_missiles)
        Herc_Ammo_AIM9P5_missiles = (10, HerculesWeapons.Herc_Ammo_AIM9P5_missiles)
        Herc_Ammo_AIM9X_missiles = (10, HerculesWeapons.Herc_Ammo_AIM9X_missiles)
        Herc_Ammo_AIM7M_missiles = (10, HerculesWeapons.Herc_Ammo_AIM7M_missiles)
        Herc_Ammo_AIM120B_missiles = (10, HerculesWeapons.Herc_Ammo_AIM120B_missiles)
        Herc_Ammo_AIM120C_missiles = (10, HerculesWeapons.Herc_Ammo_AIM120C_missiles)
        Herc_Ammo_R60M_missiles = (10, HerculesWeapons.Herc_Ammo_R60M_missiles)
        Herc_Ammo_MAGIC2_missiles = (10, HerculesWeapons.Herc_Ammo_MAGIC2_missiles)
        Herc_Ammo_R27R_missiles = (10, HerculesWeapons.Herc_Ammo_R27R_missiles)
        Herc_Ammo_R27ER_missiles = (10, HerculesWeapons.Herc_Ammo_R27ER_missiles)
        Herc_Ammo_R27T_missiles = (10, HerculesWeapons.Herc_Ammo_R27T_missiles)
        Herc_Ammo_R27ET_missiles = (10, HerculesWeapons.Herc_Ammo_R27ET_missiles)
        # ERRR Herc_Ammo_R27_missiles
        Herc_Ammo_S530D_missiles = (10, HerculesWeapons.Herc_Ammo_S530D_missiles)
        Herc_Ammo_AIM54C_missiles = (10, HerculesWeapons.Herc_Ammo_AIM54C_missiles)
        Herc_APC_M1043_HMMWV_Armament = (
            10,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament,
        )
        # Herc_ATGM_M1045_HMMWV_TOW = (10, HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW)
        Herc_APC_M1025_HMMWV = (10, HerculesWeapons.Herc_APC_M1025_HMMWV)
        Herc_SAM_M1097_HMMWV = (10, HerculesWeapons.Herc_SAM_M1097_HMMWV)
        Herc_APC_COBRA = (10, HerculesWeapons.Herc_APC_COBRA)
        Herc_ARV_BRDM_2 = (10, HerculesWeapons.Herc_ARV_BRDM_2)
        Herc_TIGR_233036 = (10, HerculesWeapons.Herc_TIGR_233036)
        Herc_IFV_BMD1 = (10, HerculesWeapons.Herc_IFV_BMD1)
        Herc_IFV_BTRD = (10, HerculesWeapons.Herc_IFV_BTRD)
        Herc_ART_NONA = (10, HerculesWeapons.Herc_ART_NONA)
        Herc_GEN_CRATE = (10, HerculesWeapons.Herc_GEN_CRATE)

    class Pylon11:
        Herc_Ammo_AGM_65D_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_65D_missiles)
        Herc_Ammo_AGM_65H_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_65H_missiles)
        Herc_Ammo_AGM_65G_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_65G_missiles)
        Herc_Ammo_AGM_65E_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_65E_missiles)
        Herc_Ammo_AGM_88C_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_88C_missiles)
        Herc_Ammo_AGM_65K_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_65K_missiles)
        Herc_Ammo_Vikhr_missiles = (11, HerculesWeapons.Herc_Ammo_Vikhr_missiles)
        Herc_Ammo_AGM_84A_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_84A_missiles)
        Herc_Ammo_AGM_84E_missiles = (11, HerculesWeapons.Herc_Ammo_AGM_84E_missiles)
        Herc_Ammo_KH25ML_missiles = (11, HerculesWeapons.Herc_Ammo_KH25ML_missiles)
        Herc_Ammo_KH25MPU_missiles = (11, HerculesWeapons.Herc_Ammo_KH25MPU_missiles)
        Herc_Ammo_KH29T_missiles = (11, HerculesWeapons.Herc_Ammo_KH29T_missiles)
        Herc_Ammo_KH29L_missiles = (11, HerculesWeapons.Herc_Ammo_KH29L_missiles)
        Herc_Ammo_KH58U_missiles = (11, HerculesWeapons.Herc_Ammo_KH58U_missiles)
        Herc_Ammo_S24B_missiles = (11, HerculesWeapons.Herc_Ammo_S24B_missiles)
        Herc_Ammo_S25OFM_missiles = (11, HerculesWeapons.Herc_Ammo_S25OFM_missiles)
        Herc_Ammo_S25L_missiles = (11, HerculesWeapons.Herc_Ammo_S25L_missiles)
        # Herc_Ammo_TOW_missiles = (11, HerculesWeapons.Herc_Ammo_TOW_missiles)
        Herc_GBU_43_B_MOAB_ = (11, HerculesWeapons.Herc_GBU_43_B_MOAB_)
        Herc_Ammo_GBU_10_bombs = (11, HerculesWeapons.Herc_Ammo_GBU_10_bombs)
        Herc_Ammo_GBU_12_bombs = (11, HerculesWeapons.Herc_Ammo_GBU_12_bombs)
        Herc_Ammo_GBU_16_bombs = (11, HerculesWeapons.Herc_Ammo_GBU_16_bombs)
        Herc_Ammo_GBU_31_VB_bombs = (11, HerculesWeapons.Herc_Ammo_GBU_31_VB_bombs)
        Herc_Ammo_GBU_31_V3B_bombs = (11, HerculesWeapons.Herc_Ammo_GBU_31_V3B_bombs)
        Herc_Ammo_GBU_38_bombs = (11, HerculesWeapons.Herc_Ammo_GBU_38_bombs)
        Herc_Ammo_CBU_87_bombs = (11, HerculesWeapons.Herc_Ammo_CBU_87_bombs)
        Herc_Ammo_CBU_97_bombs = (11, HerculesWeapons.Herc_Ammo_CBU_97_bombs)
        Herc_Ammo_CBU_103_bombs = (11, HerculesWeapons.Herc_Ammo_CBU_103_bombs)
        Herc_Ammo_CBU_105_bombs = (11, HerculesWeapons.Herc_Ammo_CBU_105_bombs)
        Herc_Ammo_Mk_82_bombs = (11, HerculesWeapons.Herc_Ammo_Mk_82_bombs)
        Herc_Ammo_Mk_82AIR_bombs = (11, HerculesWeapons.Herc_Ammo_Mk_82AIR_bombs)
        Herc_Ammo_Mk_82Snake_bombs = (11, HerculesWeapons.Herc_Ammo_Mk_82Snake_bombs)
        Herc_Ammo_Mk_83_bombs = (11, HerculesWeapons.Herc_Ammo_Mk_83_bombs)
        Herc_Ammo_Mk_84_bombs = (11, HerculesWeapons.Herc_Ammo_Mk_84_bombs)
        Herc_Ammo_FAB100_bombs = (11, HerculesWeapons.Herc_Ammo_FAB100_bombs)
        Herc_Ammo_FAB250_bombs = (11, HerculesWeapons.Herc_Ammo_FAB250_bombs)
        Herc_Ammo_FAB500_bombs = (11, HerculesWeapons.Herc_Ammo_FAB500_bombs)
        Herc_Ammo_BETAB500_bombs = (11, HerculesWeapons.Herc_Ammo_BETAB500_bombs)
        Herc_Ammo_BETAB500SP_bombs = (11, HerculesWeapons.Herc_Ammo_BETAB500SP_bombs)
        Herc_Ammo_KAB500KR_bombs = (11, HerculesWeapons.Herc_Ammo_KAB500KR_bombs)
        Herc_Ammo_RBK250PTAB25M_bombs = (
            11,
            HerculesWeapons.Herc_Ammo_RBK250PTAB25M_bombs,
        )
        Herc_Ammo_RBK500255PTAB105_bombs = (
            11,
            HerculesWeapons.Herc_Ammo_RBK500255PTAB105_bombs,
        )
        Herc_Ammo_RBK500PTAB1M_bombs = (
            11,
            HerculesWeapons.Herc_Ammo_RBK500PTAB1M_bombs,
        )
        # ERRR Herc_Ammo_Herc_Ammo_M117_bombs_bombs
        Herc_Ammo_KMGU296AO25RT_bombs = (
            11,
            HerculesWeapons.Herc_Ammo_KMGU296AO25RT_bombs,
        )
        Herc_Ammo_KMGU296AO25KO_bombs = (
            11,
            HerculesWeapons.Herc_Ammo_KMGU296AO25KO_bombs,
        )
        Herc_Ammo_MK20_bombs = (11, HerculesWeapons.Herc_Ammo_MK20_bombs)
        Herc_Ammo_SAB100_bombs = (11, HerculesWeapons.Herc_Ammo_SAB100_bombs)
        Herc_Ammo_hydra_HE_rockets = (11, HerculesWeapons.Herc_Ammo_hydra_HE_rockets)
        Herc_Ammo_hydra_WP_rockets = (11, HerculesWeapons.Herc_Ammo_hydra_WP_rockets)
        Herc_Ammo_AIM9M_missiles = (11, HerculesWeapons.Herc_Ammo_AIM9M_missiles)
        Herc_Ammo_AIM9P5_missiles = (11, HerculesWeapons.Herc_Ammo_AIM9P5_missiles)
        Herc_Ammo_AIM9X_missiles = (11, HerculesWeapons.Herc_Ammo_AIM9X_missiles)
        Herc_Ammo_AIM7M_missiles = (11, HerculesWeapons.Herc_Ammo_AIM7M_missiles)
        Herc_Ammo_AIM120B_missiles = (11, HerculesWeapons.Herc_Ammo_AIM120B_missiles)
        Herc_Ammo_AIM120C_missiles = (11, HerculesWeapons.Herc_Ammo_AIM120C_missiles)
        Herc_Ammo_R60M_missiles = (11, HerculesWeapons.Herc_Ammo_R60M_missiles)
        Herc_Ammo_MAGIC2_missiles = (11, HerculesWeapons.Herc_Ammo_MAGIC2_missiles)
        Herc_Ammo_R27R_missiles = (11, HerculesWeapons.Herc_Ammo_R27R_missiles)
        Herc_Ammo_R27ER_missiles = (11, HerculesWeapons.Herc_Ammo_R27ER_missiles)
        Herc_Ammo_R27T_missiles = (11, HerculesWeapons.Herc_Ammo_R27T_missiles)
        Herc_Ammo_R27ET_missiles = (11, HerculesWeapons.Herc_Ammo_R27ET_missiles)
        # ERRR Herc_Ammo_R27_missiles
        Herc_Ammo_S530D_missiles = (11, HerculesWeapons.Herc_Ammo_S530D_missiles)
        Herc_Ammo_AIM54C_missiles = (11, HerculesWeapons.Herc_Ammo_AIM54C_missiles)
        Herc_APC_M1043_HMMWV_Armament = (
            11,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament,
        )
        Herc_ATGM_M1045_HMMWV_TOW = (11, HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW)
        Herc_AAA_Vulcan_M163 = (11, HerculesWeapons.Herc_AAA_Vulcan_M163)
        Herc_SPG_M1126_Stryker_ICV = (11, HerculesWeapons.Herc_SPG_M1126_Stryker_ICV)
        Herc_SPG_M1128_Stryker_MGS = (11, HerculesWeapons.Herc_SPG_M1128_Stryker_MGS)
        Herc_ATGM_M1134_Stryker = (11, HerculesWeapons.Herc_ATGM_M1134_Stryker)
        Herc_APC_LAV_25 = (11, HerculesWeapons.Herc_APC_LAV_25)
        Herc_APC_M1025_HMMWV = (11, HerculesWeapons.Herc_APC_M1025_HMMWV)
        Herc_SAM_M1097_HMMWV = (11, HerculesWeapons.Herc_SAM_M1097_HMMWV)
        Herc_APC_COBRA = (11, HerculesWeapons.Herc_APC_COBRA)
        Herc_APC_M113 = (11, HerculesWeapons.Herc_APC_M113)
        Herc_Tanker_HEMTT = (11, HerculesWeapons.Herc_Tanker_HEMTT)
        Herc_HEMTT_TFFT = (11, HerculesWeapons.Herc_HEMTT_TFFT)
        Herc_IFV_M2A2_Bradley = (11, HerculesWeapons.Herc_IFV_M2A2_Bradley)
        Herc_IFV_MCV80_Warrior = (11, HerculesWeapons.Herc_IFV_MCV80_Warrior)
        Herc_IFV_BMP_1 = (11, HerculesWeapons.Herc_IFV_BMP_1)
        Herc_IFV_BMP_2 = (11, HerculesWeapons.Herc_IFV_BMP_2)
        Herc_IFV_BMP_3 = (11, HerculesWeapons.Herc_IFV_BMP_3)
        Herc_ARV_BRDM_2 = (11, HerculesWeapons.Herc_ARV_BRDM_2)
        Herc_APC_BTR_80 = (11, HerculesWeapons.Herc_APC_BTR_80)
        Herc_SAM_ROLAND_ADS = (11, HerculesWeapons.Herc_SAM_ROLAND_ADS)
        Herc_SAM_ROLAND_LN = (11, HerculesWeapons.Herc_SAM_ROLAND_LN)
        Herc_SAM_13 = (11, HerculesWeapons.Herc_SAM_13)
        Herc_ZSU_23_4 = (11, HerculesWeapons.Herc_ZSU_23_4)
        Herc_SAM_19 = (11, HerculesWeapons.Herc_SAM_19)
        Herc_UAZ_469 = (11, HerculesWeapons.Herc_UAZ_469)
        Herc_URAL_375 = (11, HerculesWeapons.Herc_URAL_375)
        Herc_M_818 = (11, HerculesWeapons.Herc_M_818)
        Herc_TIGR_233036 = (11, HerculesWeapons.Herc_TIGR_233036)
        Herc_AAA_GEPARD = (11, HerculesWeapons.Herc_AAA_GEPARD)
        Herc_SAM_CHAPARRAL = (11, HerculesWeapons.Herc_SAM_CHAPARRAL)
        Herc_SAM_LINEBACKER = (11, HerculesWeapons.Herc_SAM_LINEBACKER)
        Herc_IFV_MARDER = (11, HerculesWeapons.Herc_IFV_MARDER)
        Herc_IFV_TPZ = (11, HerculesWeapons.Herc_IFV_TPZ)
        Herc_IFV_BMD1 = (11, HerculesWeapons.Herc_IFV_BMD1)
        Herc_IFV_BTRD = (11, HerculesWeapons.Herc_IFV_BTRD)
        Herc_ART_NONA = (11, HerculesWeapons.Herc_ART_NONA)
        Herc_ART_GVOZDIKA = (11, HerculesWeapons.Herc_ART_GVOZDIKA)
        Herc_APC_MTLB = (11, HerculesWeapons.Herc_APC_MTLB)
        Herc_GEN_CRATE = (11, HerculesWeapons.Herc_GEN_CRATE)

    class Pylon12:
        Herc_Soldier_Squad = (12, HerculesWeapons.Herc_Soldier_Squad)
        Herc_Ammo_AGM_65D_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_65D_missiles)
        Herc_Ammo_AGM_65H_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_65H_missiles)
        Herc_Ammo_AGM_65G_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_65G_missiles)
        Herc_Ammo_AGM_65E_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_65E_missiles)
        Herc_Ammo_AGM_88C_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_88C_missiles)
        Herc_Ammo_AGM_65K_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_65K_missiles)
        Herc_Ammo_Vikhr_missiles = (12, HerculesWeapons.Herc_Ammo_Vikhr_missiles)
        Herc_Ammo_AGM_84A_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_84A_missiles)
        Herc_Ammo_AGM_84E_missiles = (12, HerculesWeapons.Herc_Ammo_AGM_84E_missiles)
        Herc_Ammo_KH25ML_missiles = (12, HerculesWeapons.Herc_Ammo_KH25ML_missiles)
        Herc_Ammo_KH25MPU_missiles = (12, HerculesWeapons.Herc_Ammo_KH25MPU_missiles)
        Herc_Ammo_KH29T_missiles = (12, HerculesWeapons.Herc_Ammo_KH29T_missiles)
        Herc_Ammo_KH29L_missiles = (12, HerculesWeapons.Herc_Ammo_KH29L_missiles)
        Herc_Ammo_KH58U_missiles = (12, HerculesWeapons.Herc_Ammo_KH58U_missiles)
        Herc_Ammo_S24B_missiles = (12, HerculesWeapons.Herc_Ammo_S24B_missiles)
        Herc_Ammo_S25OFM_missiles = (12, HerculesWeapons.Herc_Ammo_S25OFM_missiles)
        Herc_Ammo_S25L_missiles = (12, HerculesWeapons.Herc_Ammo_S25L_missiles)
        # Herc_Ammo_TOW_missiles = (12, HerculesWeapons.Herc_Ammo_TOW_missiles)
        Herc_Ammo_GBU_10_bombs = (12, HerculesWeapons.Herc_Ammo_GBU_10_bombs)
        Herc_Ammo_GBU_12_bombs = (12, HerculesWeapons.Herc_Ammo_GBU_12_bombs)
        Herc_Ammo_GBU_16_bombs = (12, HerculesWeapons.Herc_Ammo_GBU_16_bombs)
        Herc_Ammo_GBU_31_VB_bombs = (12, HerculesWeapons.Herc_Ammo_GBU_31_VB_bombs)
        Herc_Ammo_GBU_31_V3B_bombs = (12, HerculesWeapons.Herc_Ammo_GBU_31_V3B_bombs)
        Herc_Ammo_GBU_38_bombs = (12, HerculesWeapons.Herc_Ammo_GBU_38_bombs)
        Herc_Ammo_CBU_87_bombs = (12, HerculesWeapons.Herc_Ammo_CBU_87_bombs)
        Herc_Ammo_CBU_97_bombs = (12, HerculesWeapons.Herc_Ammo_CBU_97_bombs)
        Herc_Ammo_CBU_103_bombs = (12, HerculesWeapons.Herc_Ammo_CBU_103_bombs)
        Herc_Ammo_CBU_105_bombs = (12, HerculesWeapons.Herc_Ammo_CBU_105_bombs)
        Herc_Ammo_Mk_82_bombs = (12, HerculesWeapons.Herc_Ammo_Mk_82_bombs)
        Herc_Ammo_Mk_82AIR_bombs = (12, HerculesWeapons.Herc_Ammo_Mk_82AIR_bombs)
        Herc_Ammo_Mk_82Snake_bombs = (12, HerculesWeapons.Herc_Ammo_Mk_82Snake_bombs)
        Herc_Ammo_Mk_83_bombs = (12, HerculesWeapons.Herc_Ammo_Mk_83_bombs)
        Herc_Ammo_Mk_84_bombs = (12, HerculesWeapons.Herc_Ammo_Mk_84_bombs)
        Herc_Ammo_FAB100_bombs = (12, HerculesWeapons.Herc_Ammo_FAB100_bombs)
        Herc_Ammo_FAB250_bombs = (12, HerculesWeapons.Herc_Ammo_FAB250_bombs)
        Herc_Ammo_FAB500_bombs = (12, HerculesWeapons.Herc_Ammo_FAB500_bombs)
        Herc_Ammo_BETAB500_bombs = (12, HerculesWeapons.Herc_Ammo_BETAB500_bombs)
        Herc_Ammo_BETAB500SP_bombs = (12, HerculesWeapons.Herc_Ammo_BETAB500SP_bombs)
        Herc_Ammo_KAB500KR_bombs = (12, HerculesWeapons.Herc_Ammo_KAB500KR_bombs)
        Herc_Ammo_RBK250PTAB25M_bombs = (
            12,
            HerculesWeapons.Herc_Ammo_RBK250PTAB25M_bombs,
        )
        Herc_Ammo_RBK500255PTAB105_bombs = (
            12,
            HerculesWeapons.Herc_Ammo_RBK500255PTAB105_bombs,
        )
        Herc_Ammo_RBK500PTAB1M_bombs = (
            12,
            HerculesWeapons.Herc_Ammo_RBK500PTAB1M_bombs,
        )
        # ERRR Herc_Ammo_Herc_Ammo_M117_bombs_bombs
        Herc_Ammo_KMGU296AO25RT_bombs = (
            12,
            HerculesWeapons.Herc_Ammo_KMGU296AO25RT_bombs,
        )
        Herc_Ammo_KMGU296AO25KO_bombs = (
            12,
            HerculesWeapons.Herc_Ammo_KMGU296AO25KO_bombs,
        )
        Herc_Ammo_MK20_bombs = (12, HerculesWeapons.Herc_Ammo_MK20_bombs)
        Herc_Ammo_SAB100_bombs = (12, HerculesWeapons.Herc_Ammo_SAB100_bombs)
        Herc_Ammo_hydra_HE_rockets = (12, HerculesWeapons.Herc_Ammo_hydra_HE_rockets)
        Herc_Ammo_hydra_WP_rockets = (12, HerculesWeapons.Herc_Ammo_hydra_WP_rockets)
        Herc_Ammo_AIM9M_missiles = (12, HerculesWeapons.Herc_Ammo_AIM9M_missiles)
        Herc_Ammo_AIM9P5_missiles = (12, HerculesWeapons.Herc_Ammo_AIM9P5_missiles)
        Herc_Ammo_AIM9X_missiles = (12, HerculesWeapons.Herc_Ammo_AIM9X_missiles)
        Herc_Ammo_AIM7M_missiles = (12, HerculesWeapons.Herc_Ammo_AIM7M_missiles)
        Herc_Ammo_AIM120B_missiles = (12, HerculesWeapons.Herc_Ammo_AIM120B_missiles)
        Herc_Ammo_AIM120C_missiles = (12, HerculesWeapons.Herc_Ammo_AIM120C_missiles)
        Herc_Ammo_R60M_missiles = (12, HerculesWeapons.Herc_Ammo_R60M_missiles)
        Herc_Ammo_MAGIC2_missiles = (12, HerculesWeapons.Herc_Ammo_MAGIC2_missiles)
        Herc_Ammo_R27R_missiles = (12, HerculesWeapons.Herc_Ammo_R27R_missiles)
        Herc_Ammo_R27ER_missiles = (12, HerculesWeapons.Herc_Ammo_R27ER_missiles)
        Herc_Ammo_R27T_missiles = (12, HerculesWeapons.Herc_Ammo_R27T_missiles)
        Herc_Ammo_R27ET_missiles = (12, HerculesWeapons.Herc_Ammo_R27ET_missiles)
        # ERRR Herc_Ammo_R27_missiles
        Herc_Ammo_S530D_missiles = (12, HerculesWeapons.Herc_Ammo_S530D_missiles)
        Herc_Ammo_AIM54C_missiles = (12, HerculesWeapons.Herc_Ammo_AIM54C_missiles)
        Herc_APC_M1043_HMMWV_Armament = (
            12,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament,
        )
        Herc_ATGM_M1045_HMMWV_TOW = (12, HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW)
        Herc_AAA_Vulcan_M163 = (12, HerculesWeapons.Herc_AAA_Vulcan_M163)
        Herc_APC_LAV_25 = (12, HerculesWeapons.Herc_APC_LAV_25)
        Herc_APC_M1025_HMMWV = (12, HerculesWeapons.Herc_APC_M1025_HMMWV)
        Herc_SAM_M1097_HMMWV = (12, HerculesWeapons.Herc_SAM_M1097_HMMWV)
        Herc_APC_COBRA = (12, HerculesWeapons.Herc_APC_COBRA)
        Herc_APC_M113 = (12, HerculesWeapons.Herc_APC_M113)
        Herc_IFV_BMP_1 = (12, HerculesWeapons.Herc_IFV_BMP_1)
        Herc_ARV_BRDM_2 = (12, HerculesWeapons.Herc_ARV_BRDM_2)
        Herc_APC_BTR_80 = (12, HerculesWeapons.Herc_APC_BTR_80)
        Herc_SAM_13 = (12, HerculesWeapons.Herc_SAM_13)
        Herc_UAZ_469 = (12, HerculesWeapons.Herc_UAZ_469)
        Herc_URAL_375 = (12, HerculesWeapons.Herc_URAL_375)
        Herc_M_818 = (12, HerculesWeapons.Herc_M_818)
        Herc_TIGR_233036 = (12, HerculesWeapons.Herc_TIGR_233036)
        Herc_SAM_CHAPARRAL = (12, HerculesWeapons.Herc_SAM_CHAPARRAL)
        Herc_IFV_BMD1 = (12, HerculesWeapons.Herc_IFV_BMD1)
        Herc_IFV_BTRD = (12, HerculesWeapons.Herc_IFV_BTRD)
        Herc_ART_NONA = (12, HerculesWeapons.Herc_ART_NONA)
        Herc_GEN_CRATE = (12, HerculesWeapons.Herc_GEN_CRATE)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [task.Transport, task.CAS, task.GroundAttack]
    task_default = task.Transport
