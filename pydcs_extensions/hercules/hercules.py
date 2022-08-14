from typing import Set

from dcs import task
from dcs.liveries_scanner import Liveries
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


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
    Herc_AAA_Vulcan_M163_Air = {
        "clsid": "Herc_AAA_Vulcan_M163_Air",
        "name": "AAA Vulcan M163 Air [21666lb]",
        "weight": 9848,
    }
    Herc_AAA_Vulcan_M163_Skid = {
        "clsid": "Herc_AAA_Vulcan_M163_Skid",
        "name": "AAA Vulcan M163 Skid [21577lb]",
        "weight": 9808,
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
    Herc_Ammo_TOW_missiles = {
        "clsid": "Herc_Ammo_TOW_missiles",
        "name": "Ammo TOW*30 [4125lb]",
        "weight": 1980,
    }
    Herc_Ammo_Vikhr_missiles = {
        "clsid": "Herc_Ammo_Vikhr_missiles",
        "name": "Ammo Vikhr*48 [5808lb]",
        "weight": 2760,
    }
    Herc_APC_BTR_80_Air = {
        "clsid": "Herc_APC_BTR_80_Air",
        "name": "APC BTR-80 Air [23936lb]",
        "weight": 10880,
    }
    Herc_APC_BTR_80_Skid = {
        "clsid": "Herc_APC_BTR_80_Skid",
        "name": "APC BTR-80 Skid [23826lb]",
        "weight": 10830,
    }
    Herc_APC_BTR_82A_Air = {
        "clsid": "Herc_APC_BTR_82A_Air",
        "name": "APC BTR-82A Air [24998lb]",
        "weight": 11363,
    }
    Herc_APC_BTR_82A_Skid = {
        "clsid": "Herc_APC_BTR_82A_Skid",
        "name": "APC BTR-82A Skid [24888lb]",
        "weight": 11313,
    }
    Herc_APC_COBRA_Air = {
        "clsid": "Herc_APC_COBRA_Air",
        "name": "APC Cobra Air [10912lb]",
        "weight": 4960,
    }
    Herc_APC_COBRA_Skid = {
        "clsid": "Herc_APC_COBRA_Skid",
        "name": "APC Cobra Skid [10802lb]",
        "weight": 4910,
    }
    Herc_APC_LAV_25_Air = {
        "clsid": "Herc_APC_LAV_25_Air",
        "name": "APC LAV-25 Air [22520lb]",
        "weight": 10254,
    }
    Herc_APC_LAV_25_Skid = {
        "clsid": "Herc_APC_LAV_25_Skid",
        "name": "APC LAV-25 Skid [22514lb]",
        "weight": 10234,
    }
    Herc_APC_M1025_HMMWV_Air = {
        "clsid": "Herc_APC_M1025_HMMWV_Air",
        "name": "M1025 HMMWV Air [6160lb]",
        "weight": 2800,
    }
    Herc_APC_M1025_HMMWV_Skid = {
        "clsid": "Herc_APC_M1025_HMMWV_Skid",
        "name": "M1025 HMMWV Skid [6050lb]",
        "weight": 2750,
    }
    Herc_APC_M1043_HMMWV_Armament_Air = {
        "clsid": "Herc_APC_M1043_HMMWV_Armament_Air",
        "name": "APC M1043 HMMWV Armament Air [7023lb]",
        "weight": 3192,
    }
    Herc_APC_M1043_HMMWV_Armament_Skid = {
        "clsid": "Herc_APC_M1043_HMMWV_Armament_Skid",
        "name": "APC M1043 HMMWV Armament Skid [6912lb]",
        "weight": 3142,
    }
    Herc_APC_M113_Air = {
        "clsid": "Herc_APC_M113_Air",
        "name": "APC M113 Air [21624lb]",
        "weight": 9830,
    }
    Herc_APC_M113_Skid = {
        "clsid": "Herc_APC_M113_Skid",
        "name": "APC M113 Skid [21494lb]",
        "weight": 9770,
    }
    Herc_APC_MTLB_Air = {
        "clsid": "Herc_APC_MTLB_Air",
        "name": "APC MTLB Air [26400lb]",
        "weight": 12000,
    }
    Herc_APC_MTLB_Skid = {
        "clsid": "Herc_APC_MTLB_Skid",
        "name": "APC MTLB Skid [26290lb]",
        "weight": 11950,
    }
    Herc_ART_GVOZDIKA = {
        "clsid": "Herc_ART_GVOZDIKA",
        "name": "ART GVOZDIKA [34720lb]",
        "weight": 15782,
    }
    Herc_ART_NONA_Air = {
        "clsid": "Herc_ART_NONA_Air",
        "name": "ART 2S9 NONA Air [19140lb]",
        "weight": 8700,
    }
    Herc_ART_NONA_Skid = {
        "clsid": "Herc_ART_NONA_Skid",
        "name": "ART 2S9 NONA Skid [19030lb]",
        "weight": 8650,
    }
    Herc_ARV_BRDM_2_Air = {
        "clsid": "Herc_ARV_BRDM_2_Air",
        "name": "ARV BRDM-2 Air [12320lb]",
        "weight": 5600,
    }
    Herc_ARV_BRDM_2_Skid = {
        "clsid": "Herc_ARV_BRDM_2_Skid",
        "name": "ARV BRDM-2 Skid [12210lb]",
        "weight": 5550,
    }
    Herc_ATGM_M1045_HMMWV_TOW_Air = {
        "clsid": "Herc_ATGM_M1045_HMMWV_TOW_Air",
        "name": "ATGM M1045 HMMWV TOW Air [7183lb]",
        "weight": 3265,
    }
    Herc_ATGM_M1045_HMMWV_TOW_Skid = {
        "clsid": "Herc_ATGM_M1045_HMMWV_TOW_Skid",
        "name": "ATGM M1045 HMMWV TOW Skid [7073lb]",
        "weight": 3215,
    }
    Herc_ATGM_M1134_Stryker = {
        "clsid": "Herc_ATGM_M1134_Stryker",
        "name": "ATGM M1134 Stryker [30337lb]",
        "weight": 13790,
    }
    Herc_BattleStation = {
        "clsid": "Herc_BattleStation",
        "name": "Battle Station",
        "weight": 1160,
    }
    Herc_BattleStation_TGP = {
        "clsid": "Herc_BattleStation_TGP",
        "name": "Battle Station with TGP",
        "weight": 1160,
    }
    Herc_EWR_SBORKA_Air = {
        "clsid": "Herc_EWR_SBORKA_Air",
        "name": "EWR SBORKA Air [21624lb]",
        "weight": 9829,
    }
    Herc_EWR_SBORKA_Skid = {
        "clsid": "Herc_EWR_SBORKA_Skid",
        "name": "EWR SBORKA Skid [21624lb]",
        "weight": 9829,
    }
    Herc_Ext_Fuel_Tank = {
        "clsid": "Herc_Ext_Fuel_Tank",
        "name": "External Fuel Tank",
        "weight": 4131,
    }
    Herc_GBU_43_B_MOAB_ = {
        "clsid": "Herc_GBU-43/B(MOAB)",
        "name": "GBU-43/B(MOAB)",
        "weight": 9800,
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
    Herc_IFV_BMD1_Air = {
        "clsid": "Herc_IFV_BMD1_Air",
        "name": "IFV BMD-1 Air [18040lb]",
        "weight": 8200,
    }
    Herc_IFV_BMD1_Skid = {
        "clsid": "Herc_IFV_BMD1_Skid",
        "name": "IFV BMD-1 Skid [17930lb]",
        "weight": 8150,
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
    Herc_IFV_BTRD_Air = {
        "clsid": "Herc_IFV_BTRD_Air",
        "name": "IFV BTR-D Air [18040lb]",
        "weight": 8200,
    }
    Herc_IFV_BTRD_Skid = {
        "clsid": "Herc_IFV_BTRD_Skid",
        "name": "IFV BTR-D Skid [17930lb]",
        "weight": 8150,
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
    Herc_JATO = {"clsid": "Herc_JATO", "name": "JATO", "weight": 200}
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
    Herc_SAM_CHAPARRAL_Air = {
        "clsid": "Herc_SAM_CHAPARRAL_Air",
        "name": "SAM CHAPARRAL Air [21624lb]",
        "weight": 9830,
    }
    Herc_SAM_CHAPARRAL_Skid = {
        "clsid": "Herc_SAM_CHAPARRAL_Skid",
        "name": "SAM CHAPARRAL Skid [21516lb]",
        "weight": 9780,
    }
    Herc_SAM_LINEBACKER = {
        "clsid": "Herc_SAM_LINEBACKER",
        "name": "SAM LINEBACKER [34720lb]",
        "weight": 15782,
    }
    Herc_SAM_M1097_HMMWV_Air = {
        "clsid": "Herc_SAM_M1097_HMMWV_Air",
        "name": "SAM Avenger M1097 Air [7200lb]",
        "weight": 3273,
    }
    Herc_SAM_M1097_HMMWV_Skid = {
        "clsid": "Herc_SAM_M1097_HMMWV_Skid",
        "name": "SAM Avenger M1097 Skid [7090lb]",
        "weight": 3223,
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
    Herc_TIGR_233036_Air = {
        "clsid": "Herc_TIGR_233036_Air",
        "name": "Transport Tigr Air [15900lb]",
        "weight": 7200,
    }
    Herc_TIGR_233036_Skid = {
        "clsid": "Herc_TIGR_233036_Skid",
        "name": "Transport Tigr Skid [15730lb]",
        "weight": 7150,
    }
    Herc_UAZ_469_Air = {
        "clsid": "Herc_UAZ_469_Air",
        "name": "Transport UAZ-469 Air [3747lb]",
        "weight": 1700,
    }
    Herc_UAZ_469_Skid = {
        "clsid": "Herc_UAZ_469_Skid",
        "name": "Transport UAZ-469 Skid [3630lb]",
        "weight": 1650,
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


inject_weapons(HerculesWeapons)


@planemod
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
                12: 252,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    livery_name = "HERCULES"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        Herc_JATO = (1, HerculesWeapons.Herc_JATO)

    class Pylon2:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (2, Weapons.Smokewinder___orange)
        MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Herc_Ext_Fuel_Tank = (2, HerculesWeapons.Herc_Ext_Fuel_Tank)

    class Pylon3:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        Smokewinder___red = (3, Weapons.Smokewinder___red)
        Smokewinder___green = (3, Weapons.Smokewinder___green)
        Smokewinder___blue = (3, Weapons.Smokewinder___blue)
        Smokewinder___white = (3, Weapons.Smokewinder___white)
        Smokewinder___yellow = (3, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (3, Weapons.Smokewinder___orange)
        MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Herc_Ext_Fuel_Tank = (3, HerculesWeapons.Herc_Ext_Fuel_Tank)

    class Pylon4:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        Smokewinder___red = (4, Weapons.Smokewinder___red)
        Smokewinder___green = (4, Weapons.Smokewinder___green)
        Smokewinder___blue = (4, Weapons.Smokewinder___blue)
        Smokewinder___white = (4, Weapons.Smokewinder___white)
        Smokewinder___yellow = (4, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (4, Weapons.Smokewinder___orange)
        MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Herc_Ext_Fuel_Tank = (4, HerculesWeapons.Herc_Ext_Fuel_Tank)

    class Pylon5:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        Smokewinder___red = (5, Weapons.Smokewinder___red)
        Smokewinder___green = (5, Weapons.Smokewinder___green)
        Smokewinder___blue = (5, Weapons.Smokewinder___blue)
        Smokewinder___white = (5, Weapons.Smokewinder___white)
        Smokewinder___yellow = (5, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (5, Weapons.Smokewinder___orange)
        MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD = (
            5,
            Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD,
        )
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
        Herc_BattleStation_TGP = (9, HerculesWeapons.Herc_BattleStation_TGP)

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
        Herc_Ammo_TOW_missiles = (10, HerculesWeapons.Herc_Ammo_TOW_missiles)
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
        Herc_APC_M1043_HMMWV_Armament_Air = (
            10,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament_Air,
        )
        Herc_ATGM_M1045_HMMWV_TOW_Air = (
            10,
            HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW_Air,
        )
        Herc_APC_M1025_HMMWV_Air = (10, HerculesWeapons.Herc_APC_M1025_HMMWV_Air)
        Herc_SAM_M1097_HMMWV_Air = (10, HerculesWeapons.Herc_SAM_M1097_HMMWV_Air)
        Herc_APC_COBRA_Air = (10, HerculesWeapons.Herc_APC_COBRA_Air)
        Herc_APC_COBRA_Skid = (10, HerculesWeapons.Herc_APC_COBRA_Skid)
        Herc_ARV_BRDM_2_Air = (10, HerculesWeapons.Herc_ARV_BRDM_2_Air)
        Herc_TIGR_233036_Air = (10, HerculesWeapons.Herc_TIGR_233036_Air)
        Herc_IFV_BMD1_Air = (10, HerculesWeapons.Herc_IFV_BMD1_Air)
        Herc_IFV_BTRD_Air = (10, HerculesWeapons.Herc_IFV_BTRD_Air)
        Herc_ART_NONA_Air = (10, HerculesWeapons.Herc_ART_NONA_Air)
        Herc_APC_M1043_HMMWV_Armament_Skid = (
            10,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament_Skid,
        )
        Herc_ATGM_M1045_HMMWV_TOW_Skid = (
            10,
            HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW_Skid,
        )
        Herc_APC_M1025_HMMWV_Skid = (10, HerculesWeapons.Herc_APC_M1025_HMMWV_Skid)
        Herc_SAM_M1097_HMMWV_Skid = (10, HerculesWeapons.Herc_SAM_M1097_HMMWV_Skid)
        Herc_ARV_BRDM_2_Skid = (10, HerculesWeapons.Herc_ARV_BRDM_2_Skid)
        Herc_TIGR_233036_Skid = (10, HerculesWeapons.Herc_TIGR_233036_Skid)
        Herc_IFV_BMD1_Skid = (10, HerculesWeapons.Herc_IFV_BMD1_Skid)
        Herc_IFV_BTRD_Skid = (10, HerculesWeapons.Herc_IFV_BTRD_Skid)
        Herc_ART_NONA_Skid = (10, HerculesWeapons.Herc_ART_NONA_Skid)
        Herc_GEN_CRATE = (10, HerculesWeapons.Herc_GEN_CRATE)
        Herc_UAZ_469_Air = (10, HerculesWeapons.Herc_UAZ_469_Air)
        Herc_UAZ_469_Skid = (10, HerculesWeapons.Herc_UAZ_469_Skid)

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
        Herc_Ammo_TOW_missiles = (11, HerculesWeapons.Herc_Ammo_TOW_missiles)
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
        Herc_APC_M1043_HMMWV_Armament_Air = (
            11,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament_Air,
        )
        Herc_APC_M1043_HMMWV_Armament_Skid = (
            11,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament_Skid,
        )
        Herc_ATGM_M1045_HMMWV_TOW_Air = (
            11,
            HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW_Air,
        )
        Herc_ATGM_M1045_HMMWV_TOW_Skid = (
            11,
            HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW_Skid,
        )
        Herc_AAA_Vulcan_M163_Air = (11, HerculesWeapons.Herc_AAA_Vulcan_M163_Air)
        Herc_AAA_Vulcan_M163_Skid = (11, HerculesWeapons.Herc_AAA_Vulcan_M163_Skid)
        Herc_SPG_M1126_Stryker_ICV = (11, HerculesWeapons.Herc_SPG_M1126_Stryker_ICV)
        Herc_SPG_M1128_Stryker_MGS = (11, HerculesWeapons.Herc_SPG_M1128_Stryker_MGS)
        Herc_ATGM_M1134_Stryker = (11, HerculesWeapons.Herc_ATGM_M1134_Stryker)
        Herc_APC_LAV_25_Air = (11, HerculesWeapons.Herc_APC_LAV_25_Air)
        Herc_APC_LAV_25_Skid = (11, HerculesWeapons.Herc_APC_LAV_25_Skid)
        Herc_SAM_M1097_HMMWV_Air = (11, HerculesWeapons.Herc_SAM_M1097_HMMWV_Air)
        Herc_SAM_M1097_HMMWV_Skid = (11, HerculesWeapons.Herc_SAM_M1097_HMMWV_Skid)
        Herc_APC_COBRA_Air = (11, HerculesWeapons.Herc_APC_COBRA_Air)
        Herc_APC_COBRA_Skid = (11, HerculesWeapons.Herc_APC_COBRA_Skid)
        Herc_APC_M113_Air = (11, HerculesWeapons.Herc_APC_M113_Air)
        Herc_APC_M113_Skid = (11, HerculesWeapons.Herc_APC_M113_Skid)
        Herc_Tanker_HEMTT = (11, HerculesWeapons.Herc_Tanker_HEMTT)
        Herc_HEMTT_TFFT = (11, HerculesWeapons.Herc_HEMTT_TFFT)
        Herc_IFV_M2A2_Bradley = (11, HerculesWeapons.Herc_IFV_M2A2_Bradley)
        Herc_IFV_MCV80_Warrior = (11, HerculesWeapons.Herc_IFV_MCV80_Warrior)
        Herc_IFV_BMP_1 = (11, HerculesWeapons.Herc_IFV_BMP_1)
        Herc_IFV_BMP_2 = (11, HerculesWeapons.Herc_IFV_BMP_2)
        Herc_IFV_BMP_3 = (11, HerculesWeapons.Herc_IFV_BMP_3)
        Herc_ARV_BRDM_2_Air = (11, HerculesWeapons.Herc_ARV_BRDM_2_Air)
        Herc_ARV_BRDM_2_Skid = (11, HerculesWeapons.Herc_ARV_BRDM_2_Skid)
        Herc_APC_BTR_80_Air = (11, HerculesWeapons.Herc_APC_BTR_80_Air)
        Herc_APC_BTR_80_Skid = (11, HerculesWeapons.Herc_APC_BTR_80_Skid)
        Herc_SAM_ROLAND_ADS = (11, HerculesWeapons.Herc_SAM_ROLAND_ADS)
        Herc_SAM_ROLAND_LN = (11, HerculesWeapons.Herc_SAM_ROLAND_LN)
        Herc_SAM_13 = (11, HerculesWeapons.Herc_SAM_13)
        Herc_ZSU_23_4 = (11, HerculesWeapons.Herc_ZSU_23_4)
        Herc_SAM_19 = (11, HerculesWeapons.Herc_SAM_19)
        Herc_URAL_375 = (11, HerculesWeapons.Herc_URAL_375)
        Herc_M_818 = (11, HerculesWeapons.Herc_M_818)
        Herc_SAM_CHAPARRAL_Air = (11, HerculesWeapons.Herc_SAM_CHAPARRAL_Air)
        Herc_SAM_CHAPARRAL_Skid = (11, HerculesWeapons.Herc_SAM_CHAPARRAL_Skid)
        Herc_SAM_LINEBACKER = (11, HerculesWeapons.Herc_SAM_LINEBACKER)
        Herc_IFV_MARDER = (11, HerculesWeapons.Herc_IFV_MARDER)
        Herc_IFV_TPZ = (11, HerculesWeapons.Herc_IFV_TPZ)
        Herc_IFV_BMD1_Air = (11, HerculesWeapons.Herc_IFV_BMD1_Air)
        Herc_IFV_BMD1_Skid = (11, HerculesWeapons.Herc_IFV_BMD1_Skid)
        Herc_IFV_BTRD_Air = (11, HerculesWeapons.Herc_IFV_BTRD_Air)
        Herc_IFV_BTRD_Skid = (11, HerculesWeapons.Herc_IFV_BTRD_Skid)
        Herc_ART_GVOZDIKA = (11, HerculesWeapons.Herc_ART_GVOZDIKA)
        Herc_ART_NONA_Air = (11, HerculesWeapons.Herc_ART_NONA_Air)
        Herc_ART_NONA_Skid = (11, HerculesWeapons.Herc_ART_NONA_Skid)
        Herc_APC_MTLB_Air = (11, HerculesWeapons.Herc_APC_MTLB_Air)
        Herc_APC_MTLB_Skid = (11, HerculesWeapons.Herc_APC_MTLB_Skid)
        Herc_GEN_CRATE = (11, HerculesWeapons.Herc_GEN_CRATE)
        Herc_EWR_SBORKA_Air = (11, HerculesWeapons.Herc_EWR_SBORKA_Air)
        Herc_EWR_SBORKA_Skid = (11, HerculesWeapons.Herc_EWR_SBORKA_Skid)
        Herc_APC_BTR_82A_Air = (11, HerculesWeapons.Herc_APC_BTR_82A_Air)
        Herc_APC_BTR_82A_Skid = (11, HerculesWeapons.Herc_APC_BTR_82A_Skid)

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
        Herc_Ammo_TOW_missiles = (12, HerculesWeapons.Herc_Ammo_TOW_missiles)
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
        Herc_APC_M1043_HMMWV_Armament_Air = (
            12,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament_Air,
        )
        Herc_APC_M1043_HMMWV_Armament_Skid = (
            12,
            HerculesWeapons.Herc_APC_M1043_HMMWV_Armament_Skid,
        )
        Herc_ATGM_M1045_HMMWV_TOW_Air = (
            12,
            HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW_Air,
        )
        Herc_ATGM_M1045_HMMWV_TOW_Skid = (
            12,
            HerculesWeapons.Herc_ATGM_M1045_HMMWV_TOW_Skid,
        )
        Herc_AAA_Vulcan_M163_Air = (12, HerculesWeapons.Herc_AAA_Vulcan_M163_Air)
        Herc_AAA_Vulcan_M163_Skid = (12, HerculesWeapons.Herc_AAA_Vulcan_M163_Skid)
        Herc_APC_LAV_25_Air = (12, HerculesWeapons.Herc_APC_LAV_25_Air)
        Herc_APC_LAV_25_Skid = (12, HerculesWeapons.Herc_APC_LAV_25_Skid)
        Herc_APC_M1025_HMMWV_Air = (12, HerculesWeapons.Herc_APC_M1025_HMMWV_Air)
        Herc_APC_M1025_HMMWV_Skid = (12, HerculesWeapons.Herc_APC_M1025_HMMWV_Skid)
        Herc_SAM_M1097_HMMWV_Air = (12, HerculesWeapons.Herc_SAM_M1097_HMMWV_Air)
        Herc_SAM_M1097_HMMWV_Skid = (12, HerculesWeapons.Herc_SAM_M1097_HMMWV_Skid)
        Herc_APC_COBRA_Air = (12, HerculesWeapons.Herc_APC_COBRA_Air)
        Herc_APC_COBRA_Skid = (12, HerculesWeapons.Herc_APC_COBRA_Skid)
        Herc_APC_M113_Air = (12, HerculesWeapons.Herc_APC_M113_Air)
        Herc_APC_M113_Skid = (12, HerculesWeapons.Herc_APC_M113_Skid)
        Herc_IFV_BMP_1 = (12, HerculesWeapons.Herc_IFV_BMP_1)
        Herc_ARV_BRDM_2_Air = (12, HerculesWeapons.Herc_ARV_BRDM_2_Air)
        Herc_ARV_BRDM_2_Skid = (12, HerculesWeapons.Herc_ARV_BRDM_2_Skid)
        Herc_APC_BTR_80_Air = (12, HerculesWeapons.Herc_APC_BTR_80_Air)
        Herc_APC_BTR_80_Skid = (12, HerculesWeapons.Herc_APC_BTR_80_Skid)
        Herc_SAM_13 = (12, HerculesWeapons.Herc_SAM_13)
        Herc_UAZ_469_Air = (12, HerculesWeapons.Herc_UAZ_469_Air)
        Herc_UAZ_469_Skid = (12, HerculesWeapons.Herc_UAZ_469_Skid)
        Herc_M_818 = (12, HerculesWeapons.Herc_M_818)
        Herc_TIGR_233036_Air = (12, HerculesWeapons.Herc_TIGR_233036_Air)
        Herc_TIGR_233036_Skid = (12, HerculesWeapons.Herc_TIGR_233036_Skid)
        Herc_SAM_CHAPARRAL_Air = (12, HerculesWeapons.Herc_SAM_CHAPARRAL_Air)
        Herc_SAM_CHAPARRAL_Skid = (12, HerculesWeapons.Herc_SAM_CHAPARRAL_Skid)
        Herc_IFV_BMD1_Air = (12, HerculesWeapons.Herc_IFV_BMD1_Air)
        Herc_IFV_BMD1_Skid = (12, HerculesWeapons.Herc_IFV_BMD1_Skid)
        Herc_IFV_BTRD_Air = (12, HerculesWeapons.Herc_IFV_BTRD_Air)
        Herc_IFV_BTRD_Skid = (12, HerculesWeapons.Herc_IFV_BTRD_Skid)
        Herc_ART_NONA_Air = (12, HerculesWeapons.Herc_ART_NONA_Air)
        Herc_ART_NONA_Skid = (12, HerculesWeapons.Herc_ART_NONA_Skid)
        Herc_GEN_CRATE = (12, HerculesWeapons.Herc_GEN_CRATE)
        Herc_EWR_SBORKA_Air = (12, HerculesWeapons.Herc_EWR_SBORKA_Air)
        Herc_EWR_SBORKA_Skid = (12, HerculesWeapons.Herc_EWR_SBORKA_Skid)
        Herc_APC_BTR_82A_Air = (12, HerculesWeapons.Herc_APC_BTR_82A_Air)
        Herc_APC_BTR_82A_Skid = (12, HerculesWeapons.Herc_APC_BTR_82A_Skid)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [task.Transport, task.CAS, task.GroundAttack]
    task_default = task.Transport
