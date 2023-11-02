from typing import Any, Dict, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsA4EC:
    AN_M66A2___2000lb_GP_Bomb_LD = {
        "clsid": "{AN-M66A2}",
        "name": "AN-M66A2 - 2000lb GP Bomb LD",
        "weight": 970.68688,
    }
    AN_M81___260lb_GP_Bomb_LD = {
        "clsid": "{AN-M81}",
        "name": "AN-M81 - 260lb GP Bomb LD",
        "weight": 117.93392,
    }
    AN_M88___220lb_GP_Bomb_LD = {
        "clsid": "{AN-M88}",
        "name": "AN-M88 - 220lb GP Bomb LD",
        "weight": 98.0665904,
    }
    Bomblets_BLU_3B_x_19__HE = {
        "clsid": "{BLU_3B_GROUP}",
        "name": "Bomblets BLU-3B x 19, HE",
        "weight": 0.793786,
    }
    Bomblets_BLU_4B_x_27__HE = {
        "clsid": "{BLU_4B_GROUP}",
        "name": "Bomblets BLU-4B x 27, HE",
        "weight": 0.5443104,
    }
    CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE = {
        "clsid": "{CBU-1/A}",
        "name": "CBU-1/A pod - 19 x tubes of Bomblets BLU-4B x 27, HE",
        "weight": 337.2910112,
    }
    CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE_ = {
        "clsid": "{CBU-1/A*2}",
        "name": "CBU-1/A pod - 19 x tubes of Bomblets BLU-4B x 27, HE",
        "weight": 616.5222464,
    }
    CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE = {
        "clsid": "{CBU-2B/A}",
        "name": "CBU-2B/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE",
        "weight": 344.616522,
    }
    CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE_ = {
        "clsid": "{CBU-2B/A*2}",
        "name": "CBU-2B/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE",
        "weight": 631.173268,
    }
    CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE = {
        "clsid": "{CBU-2/A}",
        "name": "CBU-2/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE",
        "weight": 344.616522,
    }
    CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE_ = {
        "clsid": "{CBU-2/A*2}",
        "name": "CBU-2/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE",
        "weight": 631.173268,
    }
    CBU_DUMMY_pod___0_x_tubes_of_Bomblets_BLU_4B_x_27__HE = {
        "clsid": "{CBU_DUMMY}",
        "name": "CBU_DUMMY pod - 0 x tubes of Bomblets BLU-4B x 27, HE",
        "weight": 58.059776,
    }
    Fuel_Tank_150_gallons = {
        "clsid": "{DFT-150gal}",
        "name": "Fuel Tank 150 gallons",
        "weight": 515.888512,
    }
    Fuel_Tank_150_gallons__EMPTY_ = {
        "clsid": "{DFT-150gal_EMPTY}",
        "name": "Fuel Tank 150 gallons (EMPTY)",
        "weight": 515.888512,
    }
    Fuel_Tank_300_gallons = {
        "clsid": "{DFT-300gal}",
        "name": "Fuel Tank 300 gallons",
        "weight": 991.407336,
    }
    Fuel_Tank_300_gallons_ = {
        "clsid": "{DFT-300gal_LR}",
        "name": "Fuel Tank 300 gallons",
        "weight": 998.664808,
    }
    Fuel_Tank_300_gallons__EMPTY_ = {
        "clsid": "{DFT-300gal_EMPTY}",
        "name": "Fuel Tank 300 gallons (EMPTY)",
        "weight": 991.407336,
    }
    Fuel_Tank_300_gallons__EMPTY__ = {
        "clsid": "{DFT-300gal_LR_EMPTY}",
        "name": "Fuel Tank 300 gallons (EMPTY)",
        "weight": 998.664808,
    }
    Fuel_Tank_400_gallons = {
        "clsid": "{DFT-400gal}",
        "name": "Fuel Tank 400 gallons",
        "weight": 1320.06208,
    }
    Fuel_Tank_400_gallons__EMPTY_ = {
        "clsid": "{DFT-400gal_EMPTY}",
        "name": "Fuel Tank 400 gallons (EMPTY)",
        "weight": 1320.06208,
    }
    LAU_7_with_AIM_9J_Sidewinder_IR_AAM = {
        "clsid": "{AIM-9J-ON-ADAPTER}",
        "name": "LAU-7 with AIM-9J Sidewinder IR AAM",
        "weight": 115.84,
    }
    LAU_7_with_AIM_9P3_Sidewinder_IR_AAM = {
        "clsid": "{A4E-AIM-9P3-ON-ADAPTER}",
        "name": "LAU-7 with AIM-9P3 Sidewinder IR AAM",
        "weight": 121.7,
    }
    LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_ = {
        "clsid": "{A4E-ASQ-T50-ON-ADAPTER}",
        "name": "LAU-7 with AN/ASQ-T50 TCTS Pod - ACMI Pod",
        "weight": 103.6,
    }
    Mk4_HIPEG___Gunpod = {
        "clsid": "{Mk4 HIPEG}",
        "name": "Mk4 HIPEG - Gunpod",
        "weight": 612.35,
    }
    Mk_77_mod_0___750lb_Fire_Bomb_LD = {
        "clsid": "{mk77mod0}",
        "name": "Mk-77 mod 0 - 750lb Fire Bomb LD",
        "weight": 340,
    }
    Mk_77_mod_1___500lb_Fire_Bomb_LD = {
        "clsid": "{mk77mod1}",
        "name": "Mk-77 mod 1 - 500lb Fire Bomb LD",
        "weight": 230,
    }
    Mk_81_Snakeye___250lb_GP_Bomb_HD = {
        "clsid": "{MK-81SE}",
        "name": "Mk-81 Snakeye - 250lb GP Bomb HD",
        "weight": 113.398,
    }
    _2_x_AN_M57___250lb_GP_Bomb_LD__TER_ = {
        "clsid": "{AN-M57_TER_2_L}",
        "name": "2 x AN-M57 - 250lb GP Bomb LD (TER)",
        "weight": 273.6,
    }
    _2_x_AN_M57___250lb_GP_Bomb_LD__TER__ = {
        "clsid": "{AN-M57_TER_2_R}",
        "name": "2 x AN-M57 - 250lb GP Bomb LD (TER)",
        "weight": 273.6,
    }
    _2_x_CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE__TER_ = {
        "clsid": "{CBU-1/A_TER_2_L}",
        "name": "2 x CBU-1/A pod - 19 x tubes of Bomblets BLU-4B x 27, HE (TER)",
        "weight": 722.1820224,
    }
    _2_x_CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE__TER__ = {
        "clsid": "{CBU-1/A_TER_2_R}",
        "name": "2 x CBU-1/A pod - 19 x tubes of Bomblets BLU-4B x 27, HE (TER)",
        "weight": 722.1820224,
    }
    _2_x_CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER_ = {
        "clsid": "{CBU-2B/A_TER_2_L}",
        "name": "2 x CBU-2B/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE (TER)",
        "weight": 827.324648,
    }
    _2_x_CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER__ = {
        "clsid": "{CBU-2B/A_TER_2_R}",
        "name": "2 x CBU-2B/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE (TER)",
        "weight": 827.324648,
    }
    _2_x_CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER_ = {
        "clsid": "{CBU-2/A_TER_2_L}",
        "name": "2 x CBU-2/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE (TER)",
        "weight": 736.833044,
    }
    _2_x_CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER__ = {
        "clsid": "{CBU-2/A_TER_2_R}",
        "name": "2 x CBU-2/A pod - 19 x tubes of Bomblets BLU-3B x 19, HE (TER)",
        "weight": 736.833044,
    }
    _2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER_ = {
        "clsid": "{LAU-10 ZUNI_TER_2_C}",
        "name": "2 x LAU-10 pod - 4 x 127mm ZUNI, UnGd Rkts MK 71, HE/FRAG (TER)",
        "weight": 596.392,
    }
    _2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER__ = {
        "clsid": "{LAU-10 ZUNI_TER_2_L}",
        "name": "2 x LAU-10 pod - 4 x 127mm ZUNI, UnGd Rkts MK 71, HE/FRAG (TER)",
        "weight": 596.392,
    }
    _2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER___ = {
        "clsid": "{LAU-10 ZUNI_TER_2_R}",
        "name": "2 x LAU-10 pod - 4 x 127mm ZUNI, UnGd Rkts MK 71, HE/FRAG (TER)",
        "weight": 596.392,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = {
        "clsid": "{LAU-3 FFAR WP156_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 542.3414512,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER__ = {
        "clsid": "{LAU-3 FFAR WP156_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 542.3414512,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER___ = {
        "clsid": "{LAU-3 FFAR WP156_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 542.3414512,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 487.184664,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER__ = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 487.184664,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER___ = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 487.184664,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER_ = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk5, HEAT (TER)',
        "weight": 488.9083136,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER__ = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk5, HEAT (TER)',
        "weight": 488.9083136,
    }
    _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER___ = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk5, HEAT (TER)',
        "weight": 488.9083136,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = {
        "clsid": "{LAU3_HE151_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 515.98,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER__ = {
        "clsid": "{LAU3_HE151_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 515.98,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER___ = {
        "clsid": "{LAU3_HE151_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 515.98,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = {
        "clsid": "{LAU3_WP156_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 359.42,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER__ = {
        "clsid": "{LAU3_WP156_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 359.42,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER___ = {
        "clsid": "{LAU3_WP156_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 359.42,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = {
        "clsid": "{LAU3_HE5_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 451.38,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER__ = {
        "clsid": "{LAU3_HE5_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 451.38,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER___ = {
        "clsid": "{LAU3_HE5_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 451.38,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = {
        "clsid": "{LAU3_WP1B_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 462.78,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER__ = {
        "clsid": "{LAU3_WP1B_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 462.78,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER___ = {
        "clsid": "{LAU3_WP1B_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 462.78,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = {
        "clsid": "{LAU3_WP61_TER_2_C}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 462.78,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER__ = {
        "clsid": "{LAU3_WP61_TER_2_L}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 462.78,
    }
    _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER___ = {
        "clsid": "{LAU3_WP61_TER_2_R}",
        "name": '2 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 462.78,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER_ = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 268.2262208,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER__ = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 268.2262208,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER___ = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 268.2262208,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = {
        "clsid": "{LAU-68 FFAR WP156_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 287.9121136,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER__ = {
        "clsid": "{LAU-68 FFAR WP156_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 287.9121136,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER___ = {
        "clsid": "{LAU-68 FFAR WP156_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 287.9121136,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 267.591192,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER__ = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 267.591192,
    }
    _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER___ = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 267.591192,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = {
        "clsid": "{LAU-68 Hydra M151 HE_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER__ = {
        "clsid": "{LAU-68 Hydra M151 HE_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER___ = {
        "clsid": "{LAU-68 Hydra M151 HE_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = {
        "clsid": "{LAU-68 Hydra WP156_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 276.52,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER__ = {
        "clsid": "{LAU-68 Hydra WP156_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 276.52,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER___ = {
        "clsid": "{LAU-68 Hydra WP156_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 276.52,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER_ = {
        "clsid": "{LAU-68 Hydra M257 PI_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M257, Para Illum (TER)',
        "weight": 285.2,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER__ = {
        "clsid": "{LAU-68 Hydra M257 PI_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M257, Para Illum (TER)',
        "weight": 285.2,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER___ = {
        "clsid": "{LAU-68 Hydra M257 PI_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M257, Para Illum (TER)',
        "weight": 285.2,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER_ = {
        "clsid": "{LAU-68 Hydra M274 PS_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M274, Practice Smk (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER__ = {
        "clsid": "{LAU-68 Hydra M274 PS_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M274, Practice Smk (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER___ = {
        "clsid": "{LAU-68 Hydra M274 PS_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M274, Practice Smk (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER_ = {
        "clsid": "{LAU-68 Hydra Mk1 Practice_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk1, Practice (TER)',
        "weight": 255.94,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER__ = {
        "clsid": "{LAU-68 Hydra Mk1 Practice_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk1, Practice (TER)',
        "weight": 255.94,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER___ = {
        "clsid": "{LAU-68 Hydra Mk1 Practice_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk1, Practice (TER)',
        "weight": 255.94,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = {
        "clsid": "{LAU-68 Hydra Mk5 HEAT_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 251.74,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER__ = {
        "clsid": "{LAU-68 Hydra Mk5 HEAT_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 251.74,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER___ = {
        "clsid": "{LAU-68 Hydra Mk5 HEAT_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 251.74,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = {
        "clsid": "{LAU-68 Hydra Mk61 Practice_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 255.94,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER__ = {
        "clsid": "{LAU-68 Hydra Mk61 Practice_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 255.94,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER___ = {
        "clsid": "{LAU-68 Hydra Mk61 Practice_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 255.94,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = {
        "clsid": "{LAU-68 Hydra WTU1B Practice_TER_2_C}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER__ = {
        "clsid": "{LAU-68 Hydra WTU1B Practice_TER_2_L}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 274,
    }
    _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER___ = {
        "clsid": "{LAU-68 Hydra WTU1B Practice_TER_2_R}",
        "name": '2 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 274,
    }
    _2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER_ = {
        "clsid": "{Mk-20_TER_2_L}",
        "name": "2 x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets (TER)",
        "weight": 491.6,
    }
    _2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER__ = {
        "clsid": "{Mk-20_TER_2_R}",
        "name": "2 x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets (TER)",
        "weight": 491.6,
    }
    _2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER___ = {
        "clsid": "{Mk-20_TER_2_C}",
        "name": "2 x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets (TER)",
        "weight": 491.6,
    }
    _2_x_Mk_77_mod_1___500lb_Fire_Bomb_LD__TER_ = {
        "clsid": "{Mk-77 mod 1_TER_2_L}",
        "name": "2 x Mk-77 mod 1 - 500lb Fire Bomb LD (TER)",
        "weight": 507.6,
    }
    _2_x_Mk_77_mod_1___500lb_Fire_Bomb_LD__TER__ = {
        "clsid": "{Mk-77 mod 1_TER_2_R}",
        "name": "2 x Mk-77 mod 1 - 500lb Fire Bomb LD (TER)",
        "weight": 507.6,
    }
    _2_x_Mk_77_mod_1___500lb_Fire_Bomb_LD__TER___ = {
        "clsid": "{Mk-77 mod 1_TER_2_C}",
        "name": "2 x Mk-77 mod 1 - 500lb Fire Bomb LD (TER)",
        "weight": 507.6,
    }
    _2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER_ = {
        "clsid": "{Mk-82 Snakeye_TER_2_L}",
        "name": "2 x Mk-82 Snakeye - 500lb GP Bomb HD (TER)",
        "weight": 529.6,
    }
    _2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER__ = {
        "clsid": "{Mk-82 Snakeye_TER_2_R}",
        "name": "2 x Mk-82 Snakeye - 500lb GP Bomb HD (TER)",
        "weight": 529.6,
    }
    _2_x_Mk_82___500lb_GP_Bomb_LD__TER_ = {
        "clsid": "{Mk-82_TER_2_L}",
        "name": "2 x Mk-82 - 500lb GP Bomb LD (TER)",
        "weight": 529.6,
    }
    _2_x_Mk_82___500lb_GP_Bomb_LD__TER__ = {
        "clsid": "{Mk-82_TER_2_R}",
        "name": "2 x Mk-82 - 500lb GP Bomb LD (TER)",
        "weight": 529.6,
    }
    _2_x_Mk_83___1000lb_GP_Bomb_LD__TER_ = {
        "clsid": "{Mk-83_TER_2_C}",
        "name": "2 x Mk-83 - 1000lb GP Bomb LD (TER)",
        "weight": 941.6,
    }
    _3_x_AN_M57___250lb_GP_Bomb_LD__TER_ = {
        "clsid": "{AN-M57_TER_3_C}",
        "name": "3 x AN-M57 - 250lb GP Bomb LD (TER)",
        "weight": 386.6,
    }
    _3_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER_ = {
        "clsid": "{LAU-10 ZUNI_TER_3_C}",
        "name": "3 x LAU-10 pod - 4 x 127mm ZUNI, UnGd Rkts MK 71, HE/FRAG (TER)",
        "weight": 870.788,
    }
    _3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = {
        "clsid": "{LAU-3 FFAR WP156_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 789.7121768,
    }
    _3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 706.976996,
    }
    _3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER_ = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" FFAR, UnGd Rkts  Mk5, HEAT (TER)',
        "weight": 709.5624704,
    }
    _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = {
        "clsid": "{LAU3_HE151_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 750.17,
    }
    _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = {
        "clsid": "{LAU3_WP156_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 515.33,
    }
    _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = {
        "clsid": "{LAU3_HE5_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 653.27,
    }
    _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = {
        "clsid": "{LAU3_WP1B_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 670.37,
    }
    _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = {
        "clsid": "{LAU3_WP61_TER_3_C}",
        "name": '3 x LAU-3 pod - 19 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 670.37,
    }
    _3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER_ = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 378.5393312,
    }
    _3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = {
        "clsid": "{LAU-68 FFAR WP156_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  M156, Wht Phos (TER)',
        "weight": 408.0681704,
    }
    _3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" FFAR, UnGd Rkts  Mk1, HE (TER)',
        "weight": 377.586788,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = {
        "clsid": "{LAU-68 Hydra M151 HE_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M151, HE (TER)',
        "weight": 387.2,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = {
        "clsid": "{LAU-68 Hydra WP156_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M156, Wht Phos (TER)',
        "weight": 390.98,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER_ = {
        "clsid": "{LAU-68 Hydra M257 PI_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M257, Para Illum (TER)',
        "weight": 404,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER_ = {
        "clsid": "{LAU-68 Hydra M274 PS_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts M274, Practice Smk (TER)',
        "weight": 387.2,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER_ = {
        "clsid": "{LAU-68 Hydra Mk1 Practice_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk1, Practice (TER)',
        "weight": 360.11,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = {
        "clsid": "{LAU-68 Hydra Mk5 HEAT_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk5, HEAT (TER)',
        "weight": 353.81,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = {
        "clsid": "{LAU-68 Hydra Mk61 Practice_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts Mk61, Practice (TER)',
        "weight": 360.11,
    }
    _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = {
        "clsid": "{LAU-68 Hydra WTU1B Practice_TER_3_C}",
        "name": '3 x LAU-68 pod - 7 x 2.75" Hydra, UnGd Rkts WTU-1/B, Practice (TER)',
        "weight": 387.2,
    }
    _3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER_ = {
        "clsid": "{Mk-20_TER_3_C}",
        "name": "3 x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets (TER)",
        "weight": 713.6,
    }
    _3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER_ = {
        "clsid": "{Mk-82 Snakeye_TER_3_C}",
        "name": "3 x Mk-82 Snakeye - 500lb GP Bomb HD (TER)",
        "weight": 770.6,
    }
    _3_x_Mk_82___500lb_GP_Bomb_LD__TER_ = {
        "clsid": "{Mk-82_TER_3_C}",
        "name": "3 x Mk-82 - 500lb GP Bomb LD (TER)",
        "weight": 770.6,
    }
    _3_x_Mk_83___1000lb_GP_Bomb_LD__TER_ = {
        "clsid": "{Mk-83_TER_3_C}",
        "name": "3 x Mk-83 - 1000lb GP Bomb LD (TER)",
        "weight": 1388.6,
    }
    _4_x_Mk_77_mod_1___500lb_Fire_Bomb_LD__MER_ = {
        "clsid": "{Mk-77 mod 1_MER_4_C}",
        "name": "4 x Mk-77 mod 1 - 500lb Fire Bomb LD (MER)",
        "weight": 1019.8,
    }
    _4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER_ = {
        "clsid": "{Mk-82 Snakeye_MER_4_C}",
        "name": "4 x Mk-82 Snakeye - 500lb GP Bomb HD (MER)",
        "weight": 1063.8,
    }
    _4_x_Mk_82___500lb_GP_Bomb_LD__MER_ = {
        "clsid": "{Mk-82_MER_4_C}",
        "name": "4 x Mk-82 - 500lb GP Bomb LD (MER)",
        "weight": 1063.8,
    }
    _5_x_AN_M57___250lb_GP_Bomb_LD__MER_ = {
        "clsid": "{AN-M57_MER_5_L}",
        "name": "5 x AN-M57 - 250lb GP Bomb LD (MER)",
        "weight": 664.8,
    }
    _5_x_AN_M57___250lb_GP_Bomb_LD__MER__ = {
        "clsid": "{AN-M57_MER_5_R}",
        "name": "5 x AN-M57 - 250lb GP Bomb LD (MER)",
        "weight": 664.8,
    }
    _5_x_AN_M81___260lb_GP_Bomb_LD__MER_ = {
        "clsid": "{AN-M81_MER_5_L}",
        "name": "5 x AN-M81 - 260lb GP Bomb LD (MER)",
        "weight": 689.4696,
    }
    _5_x_AN_M81___260lb_GP_Bomb_LD__MER__ = {
        "clsid": "{AN-M81_MER_5_R}",
        "name": "5 x AN-M81 - 260lb GP Bomb LD (MER)",
        "weight": 689.4696,
    }
    _5_x_AN_M88___220lb_GP_Bomb_LD__MER_ = {
        "clsid": "{AN-M88_MER_5_L}",
        "name": "5 x AN-M88 - 220lb GP Bomb LD (MER)",
        "weight": 590.132952,
    }
    _5_x_AN_M88___220lb_GP_Bomb_LD__MER__ = {
        "clsid": "{AN-M88_MER_5_R}",
        "name": "5 x AN-M88 - 220lb GP Bomb LD (MER)",
        "weight": 590.132952,
    }
    _5_x_BDU_33___25lb_Practice_Bomb_LD__MER_ = {
        "clsid": "{BDU-33_MER_5_L}",
        "name": "5 x BDU-33 - 25lb Practice Bomb LD (MER)",
        "weight": 156.3,
    }
    _5_x_BDU_33___25lb_Practice_Bomb_LD__MER__ = {
        "clsid": "{BDU-33_MER_5_R}",
        "name": "5 x BDU-33 - 25lb Practice Bomb LD (MER)",
        "weight": 156.3,
    }
    _5_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER_ = {
        "clsid": "{Mk-81SE_MER_5_L}",
        "name": "5 x Mk-81 Snakeye - 250lb GP Bomb HD (MER)",
        "weight": 666.79,
    }
    _5_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER__ = {
        "clsid": "{Mk-81SE_MER_5_R}",
        "name": "5 x Mk-81 Snakeye - 250lb GP Bomb HD (MER)",
        "weight": 666.79,
    }
    _5_x_Mk_81___250lb_GP_Bomb_LD__MER_ = {
        "clsid": "{Mk-81_MER_5_L}",
        "name": "5 x Mk-81 - 250lb GP Bomb LD (MER)",
        "weight": 689.8,
    }
    _5_x_Mk_81___250lb_GP_Bomb_LD__MER__ = {
        "clsid": "{Mk-81_MER_5_R}",
        "name": "5 x Mk-81 - 250lb GP Bomb LD (MER)",
        "weight": 689.8,
    }
    _6_x_AN_M57___250lb_GP_Bomb_LD__MER_ = {
        "clsid": "{AN-M57_MER_6_C}",
        "name": "6 x AN-M57 - 250lb GP Bomb LD (MER)",
        "weight": 777.8,
    }
    _6_x_AN_M81___260lb_GP_Bomb_LD__MER_ = {
        "clsid": "{AN-M81_MER_6_C}",
        "name": "6 x AN-M81 - 260lb GP Bomb LD (MER)",
        "weight": 807.40352,
    }
    _6_x_AN_M88___220lb_GP_Bomb_LD__MER_ = {
        "clsid": "{AN-M88_MER_6_C}",
        "name": "6 x AN-M88 - 220lb GP Bomb LD (MER)",
        "weight": 688.1995424,
    }
    _6_x_BDU_33___25lb_Practice_Bomb_LD__MER_ = {
        "clsid": "{BDU-33_MER_6_C}",
        "name": "6 x BDU-33 - 25lb Practice Bomb LD (MER)",
        "weight": 167.6,
    }
    _6_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER_ = {
        "clsid": "{Mk-81SE_MER_6_C}",
        "name": "6 x Mk-81 Snakeye - 250lb GP Bomb HD (MER)",
        "weight": 780.188,
    }
    _6_x_Mk_81___250lb_GP_Bomb_LD__MER_ = {
        "clsid": "{Mk-81_MER_6_C}",
        "name": "6 x Mk-81 - 250lb GP Bomb LD (MER)",
        "weight": 807.8,
    }
    _6_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER_ = {
        "clsid": "{Mk-82 Snakeye_MER_6_C}",
        "name": "6 x Mk-82 Snakeye - 500lb GP Bomb HD (MER)",
        "weight": 1545.8,
    }
    _6_x_Mk_82___500lb_GP_Bomb_LD__MER_ = {
        "clsid": "{Mk-82_MER_6_C}",
        "name": "6 x Mk-82 - 500lb GP Bomb LD (MER)",
        "weight": 1545.8,
    }


inject_weapons(WeaponsA4EC)


@planemod
class A_4E_C(PlaneType):
    id = "A-4E-C"
    flyable = True
    height = 4.57
    width = 8.38
    length = 12.22
    fuel_max = 2467.5454273299
    max_speed = 1082.88
    chaff = 30
    flare = 30
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 254

    panel_radio = {
        1: {
            "channels": {
                1: 264,
                2: 265,
                4: 254,
                8: 258,
                16: 267,
                17: 251,
                9: 262,
                18: 253,
                5: 250,
                10: 259,
                20: 252,
                11: 268,
                3: 256,
                6: 270,
                12: 269,
                13: 260,
                7: 257,
                14: 263,
                19: 266,
                15: 261,
            },
        },
    }

    property_defaults: Dict[str, Any] = {
        "HideECMPanel": False,
        "Auto_Catapult_Power": False,
        "Night_Vision": False,
        "CBU2ATPP": 0,
        "CBU2BATPP": 0,
        "CMS_BURSTS": 1,
        "CMS_BURST_INTERVAL": 1,
        "CMS_SALVOS": 1,
        "CMS_SALVO_INTERVAL": 1,
    }

    class Properties:
        class HideECMPanel:
            id = "HideECMPanel"

        class Auto_Catapult_Power:
            id = "Auto_Catapult_Power"

        class Night_Vision:
            id = "Night_Vision"

        class CBU2ATPP:
            id = "CBU2ATPP"

            class Values:
                x_1_tube = 0
                x_2_tubes = 1
                x_3_tubes = 2
                x_4_tubes = 3
                x_6_tubes = 4
                x_17_tubes__salvo = 5

        class CBU2BATPP:
            id = "CBU2BATPP"

            class Values:
                x_2_tubes = 0
                x_4_tubes = 1
                x_6_tubes = 2

        class CMS_BURSTS:
            id = "CMS_BURSTS"

            class Values:
                x_1 = 1
                x_2 = 2
                x_3 = 3
                x_4 = 4

        class CMS_BURST_INTERVAL:
            id = "CMS_BURST_INTERVAL"

            class Values:
                x_0_2_seconds = 1
                x_0_3_seconds = 2
                x_0_4_seconds = 3
                x_0_5_seconds = 4

        class CMS_SALVOS:
            id = "CMS_SALVOS"

            class Values:
                x_8 = 1
                x_12 = 2
                x_16 = 3
                x_20 = 4
                x_24 = 5
                x_28 = 6
                x_32 = 7

        class CMS_SALVO_INTERVAL:
            id = "CMS_SALVO_INTERVAL"

            class Values:
                x_2_seconds = 1
                x_4_seconds = 2
                x_6_seconds = 3
                x_8_seconds = 4
                x_10_seconds = 5
                x_12_seconds = 6
                x_14_seconds = 7

    livery_name = "A-4E-C"  # from type

    class Pylon1:
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P5_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9P5_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P3_Sidewinder_IR_AAM = (
            1,
            WeaponsA4EC.LAU_7_with_AIM_9P3_Sidewinder_IR_AAM,
        )
        LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_ = (
            1,
            WeaponsA4EC.LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            1,
            WeaponsA4EC.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            1,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            1,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            1,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            1,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU3_WP61 = (1, Weapons.LAU3_WP61)
        LAU3_WP1B = (1, Weapons.LAU3_WP1B)
        LAU3_HE5 = (1, Weapons.LAU3_HE5)
        LAU3_WP156 = (1, Weapons.LAU3_WP156)
        LAU3_HE151 = (1, Weapons.LAU3_HE151)
        AGM_45A_Shrike_ARM = (1, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM__Imp_ = (1, Weapons.AGM_45B_Shrike_ARM__Imp_)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81_Snakeye___250lb_GP_Bomb_HD = (
            1,
            WeaponsA4EC.Mk_81_Snakeye___250lb_GP_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_77_mod_1___500lb_Fire_Bomb_LD = (
            1,
            WeaponsA4EC.Mk_77_mod_1___500lb_Fire_Bomb_LD,
        )
        AN_M30A1___100lb_GP_Bomb_LD = (1, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (1, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (1, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (1, WeaponsA4EC.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (1, WeaponsA4EC.AN_M88___220lb_GP_Bomb_LD)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            1,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )

    # ERRR <CLEAN>

    class Pylon2:
        Fuel_Tank_300_gallons_ = (2, WeaponsA4EC.Fuel_Tank_300_gallons_)
        Fuel_Tank_300_gallons__EMPTY__ = (2, WeaponsA4EC.Fuel_Tank_300_gallons__EMPTY__)
        Fuel_Tank_150_gallons = (2, WeaponsA4EC.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (2, WeaponsA4EC.Fuel_Tank_150_gallons__EMPTY_)
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            2,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            2,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P5_Sidewinder_IR_AAM = (
            2,
            Weapons.LAU_7_with_AIM_9P5_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P3_Sidewinder_IR_AAM = (
            2,
            WeaponsA4EC.LAU_7_with_AIM_9P3_Sidewinder_IR_AAM,
        )
        LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_ = (
            2,
            WeaponsA4EC.LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            2,
            WeaponsA4EC.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            2,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER__,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER__,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER__,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER__,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER__,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER__,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER__,
        )
        LAU3_WP61 = (2, Weapons.LAU3_WP61)
        LAU3_WP1B = (2, Weapons.LAU3_WP1B)
        LAU3_HE5 = (2, Weapons.LAU3_HE5)
        LAU3_WP156 = (2, Weapons.LAU3_WP156)
        LAU3_HE151 = (2, Weapons.LAU3_HE151)
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER__,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER__,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER__,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER__,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER__ = (
            2,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER__,
        )
        AGM_45A_Shrike_ARM = (2, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM__Imp_ = (2, Weapons.AGM_45B_Shrike_ARM__Imp_)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81_Snakeye___250lb_GP_Bomb_HD = (
            2,
            WeaponsA4EC.Mk_81_Snakeye___250lb_GP_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_77_mod_0___750lb_Fire_Bomb_LD = (
            2,
            WeaponsA4EC.Mk_77_mod_0___750lb_Fire_Bomb_LD,
        )
        Mk_77_mod_1___500lb_Fire_Bomb_LD = (
            2,
            WeaponsA4EC.Mk_77_mod_1___500lb_Fire_Bomb_LD,
        )
        AN_M30A1___100lb_GP_Bomb_LD = (2, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (2, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (2, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (2, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (2, WeaponsA4EC.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (2, WeaponsA4EC.AN_M88___220lb_GP_Bomb_LD)
        CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE = (
            2,
            WeaponsA4EC.CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE,
        )
        CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE = (
            2,
            WeaponsA4EC.CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE,
        )
        CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE = (
            2,
            WeaponsA4EC.CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE,
        )
        _2_x_CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE__TER_ = (
            2,
            WeaponsA4EC._2_x_CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE__TER_,
        )
        _2_x_CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER_ = (
            2,
            WeaponsA4EC._2_x_CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER_,
        )
        _2_x_CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER_ = (
            2,
            WeaponsA4EC._2_x_CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER_,
        )
        _2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER_ = (
            2,
            WeaponsA4EC._2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER_,
        )
        _5_x_Mk_81___250lb_GP_Bomb_LD__MER_ = (
            2,
            WeaponsA4EC._5_x_Mk_81___250lb_GP_Bomb_LD__MER_,
        )
        _5_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER_ = (
            2,
            WeaponsA4EC._5_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER_,
        )
        _2_x_Mk_82___500lb_GP_Bomb_LD__TER_ = (
            2,
            WeaponsA4EC._2_x_Mk_82___500lb_GP_Bomb_LD__TER_,
        )
        _2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER_ = (
            2,
            WeaponsA4EC._2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER_,
        )
        _5_x_AN_M57___250lb_GP_Bomb_LD__MER_ = (
            2,
            WeaponsA4EC._5_x_AN_M57___250lb_GP_Bomb_LD__MER_,
        )
        _2_x_AN_M57___250lb_GP_Bomb_LD__TER_ = (
            2,
            WeaponsA4EC._2_x_AN_M57___250lb_GP_Bomb_LD__TER_,
        )
        _5_x_AN_M81___260lb_GP_Bomb_LD__MER_ = (
            2,
            WeaponsA4EC._5_x_AN_M81___260lb_GP_Bomb_LD__MER_,
        )
        _5_x_AN_M88___220lb_GP_Bomb_LD__MER_ = (
            2,
            WeaponsA4EC._5_x_AN_M88___220lb_GP_Bomb_LD__MER_,
        )
        _5_x_BDU_33___25lb_Practice_Bomb_LD__MER_ = (
            2,
            WeaponsA4EC._5_x_BDU_33___25lb_Practice_Bomb_LD__MER_,
        )
        Mk4_HIPEG___Gunpod = (2, WeaponsA4EC.Mk4_HIPEG___Gunpod)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (2, Weapons.Smokewinder___orange)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            2,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )

    # ERRR <CLEAN>

    class Pylon3:
        Fuel_Tank_400_gallons = (3, WeaponsA4EC.Fuel_Tank_400_gallons)
        Fuel_Tank_300_gallons = (3, WeaponsA4EC.Fuel_Tank_300_gallons)
        Fuel_Tank_150_gallons = (3, WeaponsA4EC.Fuel_Tank_150_gallons)
        Fuel_Tank_400_gallons__EMPTY_ = (3, WeaponsA4EC.Fuel_Tank_400_gallons__EMPTY_)
        Fuel_Tank_300_gallons__EMPTY_ = (3, WeaponsA4EC.Fuel_Tank_300_gallons__EMPTY_)
        Fuel_Tank_150_gallons__EMPTY_ = (3, WeaponsA4EC.Fuel_Tank_150_gallons__EMPTY_)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            3,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            3,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER_,
        )
        _3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_,
        )
        _3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_,
        )
        _3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER_,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER_,
        )
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            3,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_,
        )
        _3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER_,
        )
        _3_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER_,
        )
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_,
        )
        _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_,
        )
        _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_,
        )
        _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_,
        )
        _3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = (
            3,
            WeaponsA4EC._3_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER_,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER_,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER_,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER_,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_ = (
            3,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER_,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81_Snakeye___250lb_GP_Bomb_HD = (
            3,
            WeaponsA4EC.Mk_81_Snakeye___250lb_GP_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (3, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_77_mod_0___750lb_Fire_Bomb_LD = (
            3,
            WeaponsA4EC.Mk_77_mod_0___750lb_Fire_Bomb_LD,
        )
        Mk_77_mod_1___500lb_Fire_Bomb_LD = (
            3,
            WeaponsA4EC.Mk_77_mod_1___500lb_Fire_Bomb_LD,
        )
        AN_M30A1___100lb_GP_Bomb_LD = (3, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (3, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (3, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (3, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M66A2___2000lb_GP_Bomb_LD = (3, WeaponsA4EC.AN_M66A2___2000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (3, WeaponsA4EC.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (3, WeaponsA4EC.AN_M88___220lb_GP_Bomb_LD)
        _3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER_ = (
            3,
            WeaponsA4EC._3_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER_,
        )
        _2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER___ = (
            3,
            WeaponsA4EC._2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER___,
        )
        _6_x_Mk_81___250lb_GP_Bomb_LD__MER_ = (
            3,
            WeaponsA4EC._6_x_Mk_81___250lb_GP_Bomb_LD__MER_,
        )
        _6_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER_ = (
            3,
            WeaponsA4EC._6_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER_,
        )
        _6_x_Mk_82___500lb_GP_Bomb_LD__MER_ = (
            3,
            WeaponsA4EC._6_x_Mk_82___500lb_GP_Bomb_LD__MER_,
        )
        _4_x_Mk_82___500lb_GP_Bomb_LD__MER_ = (
            3,
            WeaponsA4EC._4_x_Mk_82___500lb_GP_Bomb_LD__MER_,
        )
        _3_x_Mk_82___500lb_GP_Bomb_LD__TER_ = (
            3,
            WeaponsA4EC._3_x_Mk_82___500lb_GP_Bomb_LD__TER_,
        )
        _6_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER_ = (
            3,
            WeaponsA4EC._6_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER_,
        )
        _4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER_ = (
            3,
            WeaponsA4EC._4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__MER_,
        )
        _3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER_ = (
            3,
            WeaponsA4EC._3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER_,
        )
        _3_x_Mk_83___1000lb_GP_Bomb_LD__TER_ = (
            3,
            WeaponsA4EC._3_x_Mk_83___1000lb_GP_Bomb_LD__TER_,
        )
        _2_x_Mk_83___1000lb_GP_Bomb_LD__TER_ = (
            3,
            WeaponsA4EC._2_x_Mk_83___1000lb_GP_Bomb_LD__TER_,
        )
        _2_x_Mk_77_mod_1___500lb_Fire_Bomb_LD__TER___ = (
            3,
            WeaponsA4EC._2_x_Mk_77_mod_1___500lb_Fire_Bomb_LD__TER___,
        )
        _6_x_AN_M57___250lb_GP_Bomb_LD__MER_ = (
            3,
            WeaponsA4EC._6_x_AN_M57___250lb_GP_Bomb_LD__MER_,
        )
        _3_x_AN_M57___250lb_GP_Bomb_LD__TER_ = (
            3,
            WeaponsA4EC._3_x_AN_M57___250lb_GP_Bomb_LD__TER_,
        )
        _6_x_AN_M81___260lb_GP_Bomb_LD__MER_ = (
            3,
            WeaponsA4EC._6_x_AN_M81___260lb_GP_Bomb_LD__MER_,
        )
        _6_x_AN_M88___220lb_GP_Bomb_LD__MER_ = (
            3,
            WeaponsA4EC._6_x_AN_M88___220lb_GP_Bomb_LD__MER_,
        )
        _6_x_BDU_33___25lb_Practice_Bomb_LD__MER_ = (
            3,
            WeaponsA4EC._6_x_BDU_33___25lb_Practice_Bomb_LD__MER_,
        )
        Mk4_HIPEG___Gunpod = (3, WeaponsA4EC.Mk4_HIPEG___Gunpod)
        Smokewinder___red = (3, Weapons.Smokewinder___red)
        Smokewinder___green = (3, Weapons.Smokewinder___green)
        Smokewinder___blue = (3, Weapons.Smokewinder___blue)
        Smokewinder___white = (3, Weapons.Smokewinder___white)
        Smokewinder___yellow = (3, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (3, Weapons.Smokewinder___orange)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            3,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )

    # ERRR <CLEAN>

    class Pylon4:
        Fuel_Tank_300_gallons_ = (4, WeaponsA4EC.Fuel_Tank_300_gallons_)
        Fuel_Tank_300_gallons__EMPTY__ = (4, WeaponsA4EC.Fuel_Tank_300_gallons__EMPTY__)
        Fuel_Tank_150_gallons = (4, WeaponsA4EC.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (4, WeaponsA4EC.Fuel_Tank_150_gallons__EMPTY_)
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            4,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            4,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P5_Sidewinder_IR_AAM = (
            4,
            Weapons.LAU_7_with_AIM_9P5_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P3_Sidewinder_IR_AAM = (
            4,
            WeaponsA4EC.LAU_7_with_AIM_9P3_Sidewinder_IR_AAM,
        )
        LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_ = (
            4,
            WeaponsA4EC.LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            4,
            WeaponsA4EC.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            4,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            4,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER___,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER___,
        )
        _2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts__Mk5__HEAT__TER___,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__M156__Wht_Phos__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts__Mk1__HE__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT__TER___,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER___,
        )
        _2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER___,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_MK_71__HE_FRAG__TER___,
        )
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE__TER___,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos__TER___,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT__TER___,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice__TER___,
        )
        _2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER___ = (
            4,
            WeaponsA4EC._2_x_LAU_3_pod___19_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice__TER___,
        )
        AGM_45A_Shrike_ARM = (4, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM__Imp_ = (4, Weapons.AGM_45B_Shrike_ARM__Imp_)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81_Snakeye___250lb_GP_Bomb_HD = (
            4,
            WeaponsA4EC.Mk_81_Snakeye___250lb_GP_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_77_mod_0___750lb_Fire_Bomb_LD = (
            4,
            WeaponsA4EC.Mk_77_mod_0___750lb_Fire_Bomb_LD,
        )
        Mk_77_mod_1___500lb_Fire_Bomb_LD = (
            4,
            WeaponsA4EC.Mk_77_mod_1___500lb_Fire_Bomb_LD,
        )
        AN_M30A1___100lb_GP_Bomb_LD = (4, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (4, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (4, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (4, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (4, WeaponsA4EC.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (4, WeaponsA4EC.AN_M88___220lb_GP_Bomb_LD)
        CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE = (
            4,
            WeaponsA4EC.CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE,
        )
        CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE = (
            4,
            WeaponsA4EC.CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE,
        )
        CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE = (
            4,
            WeaponsA4EC.CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE,
        )
        _2_x_CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE__TER__ = (
            4,
            WeaponsA4EC._2_x_CBU_1_A_pod___19_x_tubes_of_Bomblets_BLU_4B_x_27__HE__TER__,
        )
        _2_x_CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER__ = (
            4,
            WeaponsA4EC._2_x_CBU_2_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER__,
        )
        _2_x_CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER__ = (
            4,
            WeaponsA4EC._2_x_CBU_2B_A_pod___19_x_tubes_of_Bomblets_BLU_3B_x_19__HE__TER__,
        )
        _2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER__ = (
            4,
            WeaponsA4EC._2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets__TER__,
        )
        _5_x_Mk_81___250lb_GP_Bomb_LD__MER__ = (
            4,
            WeaponsA4EC._5_x_Mk_81___250lb_GP_Bomb_LD__MER__,
        )
        _5_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER__ = (
            4,
            WeaponsA4EC._5_x_Mk_81_Snakeye___250lb_GP_Bomb_HD__MER__,
        )
        _2_x_Mk_82___500lb_GP_Bomb_LD__TER__ = (
            4,
            WeaponsA4EC._2_x_Mk_82___500lb_GP_Bomb_LD__TER__,
        )
        _2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER__ = (
            4,
            WeaponsA4EC._2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD__TER__,
        )
        _5_x_AN_M57___250lb_GP_Bomb_LD__MER__ = (
            4,
            WeaponsA4EC._5_x_AN_M57___250lb_GP_Bomb_LD__MER__,
        )
        _2_x_AN_M57___250lb_GP_Bomb_LD__TER__ = (
            4,
            WeaponsA4EC._2_x_AN_M57___250lb_GP_Bomb_LD__TER__,
        )
        _5_x_AN_M81___260lb_GP_Bomb_LD__MER__ = (
            4,
            WeaponsA4EC._5_x_AN_M81___260lb_GP_Bomb_LD__MER__,
        )
        _5_x_AN_M88___220lb_GP_Bomb_LD__MER__ = (
            4,
            WeaponsA4EC._5_x_AN_M88___220lb_GP_Bomb_LD__MER__,
        )
        _5_x_BDU_33___25lb_Practice_Bomb_LD__MER__ = (
            4,
            WeaponsA4EC._5_x_BDU_33___25lb_Practice_Bomb_LD__MER__,
        )
        Mk4_HIPEG___Gunpod = (4, WeaponsA4EC.Mk4_HIPEG___Gunpod)
        Smokewinder___red = (4, Weapons.Smokewinder___red)
        Smokewinder___green = (4, Weapons.Smokewinder___green)
        Smokewinder___blue = (4, Weapons.Smokewinder___blue)
        Smokewinder___white = (4, Weapons.Smokewinder___white)
        Smokewinder___yellow = (4, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (4, Weapons.Smokewinder___orange)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            4,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )

    # ERRR <CLEAN>

    class Pylon5:
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            5,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            5,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P5_Sidewinder_IR_AAM = (
            5,
            Weapons.LAU_7_with_AIM_9P5_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P3_Sidewinder_IR_AAM = (
            5,
            WeaponsA4EC.LAU_7_with_AIM_9P3_Sidewinder_IR_AAM,
        )
        LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_ = (
            5,
            WeaponsA4EC.LAU_7_with_AN_ASQ_T50_TCTS_Pod___ACMI_Pod_,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            5,
            WeaponsA4EC.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            5,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            5,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk1__HE,
        )
        LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            5,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU3_WP61 = (5, Weapons.LAU3_WP61)
        LAU3_WP1B = (5, Weapons.LAU3_WP1B)
        LAU3_HE5 = (5, Weapons.LAU3_HE5)
        LAU3_WP156 = (5, Weapons.LAU3_WP156)
        LAU3_HE151 = (5, Weapons.LAU3_HE151)
        AGM_45A_Shrike_ARM = (5, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM__Imp_ = (5, Weapons.AGM_45B_Shrike_ARM__Imp_)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (5, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81_Snakeye___250lb_GP_Bomb_HD = (
            5,
            WeaponsA4EC.Mk_81_Snakeye___250lb_GP_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (5, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_77_mod_1___500lb_Fire_Bomb_LD = (
            5,
            WeaponsA4EC.Mk_77_mod_1___500lb_Fire_Bomb_LD,
        )
        AN_M30A1___100lb_GP_Bomb_LD = (5, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (5, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (5, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (5, WeaponsA4EC.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (5, WeaponsA4EC.AN_M88___220lb_GP_Bomb_LD)
        Smokewinder___red = (5, Weapons.Smokewinder___red)
        Smokewinder___green = (5, Weapons.Smokewinder___green)
        Smokewinder___blue = (5, Weapons.Smokewinder___blue)
        Smokewinder___white = (5, Weapons.Smokewinder___white)
        Smokewinder___yellow = (5, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (5, Weapons.Smokewinder___orange)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            5,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5}

    tasks = [
        task.CAP,
        task.CAS,
        task.SEAD,
        task.Reconnaissance,
        task.GroundAttack,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.Refueling,
        task.Escort,
    ]
    task_default = task.CAS
