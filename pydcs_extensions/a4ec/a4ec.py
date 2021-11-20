from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsA4EC:
    AN_M57__2__TER_ = {
        "clsid": "{AN-M57_TER_2_L}",
        "name": "AN-M57 *2 (TER)",
        "weight": 273.6,
    }
    AN_M57__2__TER__ = {
        "clsid": "{AN-M57_TER_2_R}",
        "name": "AN-M57 *2 (TER)",
        "weight": 273.6,
    }
    AN_M57__3__TER_ = {
        "clsid": "{AN-M57_TER_3_C}",
        "name": "AN-M57 *3 (TER)",
        "weight": 386.6,
    }
    AN_M57__5__MER_ = {
        "clsid": "{AN-M57_MER_5_L}",
        "name": "AN-M57 *5 (MER)",
        "weight": 664.8,
    }
    AN_M57__5__MER__ = {
        "clsid": "{AN-M57_MER_5_R}",
        "name": "AN-M57 *5 (MER)",
        "weight": 664.8,
    }
    AN_M57__6__MER_ = {
        "clsid": "{AN-M57_MER_6_C}",
        "name": "AN-M57 *6 (MER)",
        "weight": 777.8,
    }
    AN_M66A2 = {"clsid": "{AN-M66A2}", "name": "AN-M66A2", "weight": 970.68688}
    AN_M81 = {"clsid": "{AN-M81}", "name": "AN-M81", "weight": 117.93392}
    AN_M81__5__MER_ = {
        "clsid": "{AN-M81_MER_5_L}",
        "name": "AN-M81 *5 (MER)",
        "weight": 689.3,
    }
    AN_M81__5__MER__ = {
        "clsid": "{AN-M81_MER_5_R}",
        "name": "AN-M81 *5 (MER)",
        "weight": 689.3,
    }
    AN_M81__6__MER_ = {
        "clsid": "{AN-M81_MER_6_C}",
        "name": "AN-M81 *6 (MER)",
        "weight": 807.2,
    }
    AN_M88 = {"clsid": "{AN-M88}", "name": "AN-M88", "weight": 98.0665904}
    AN_M88__5__MER_ = {
        "clsid": "{AN-M88_MER_5_L}",
        "name": "AN-M88 *5 (MER)",
        "weight": 589.8,
    }
    AN_M88__5__MER__ = {
        "clsid": "{AN-M88_MER_5_R}",
        "name": "AN-M88 *5 (MER)",
        "weight": 589.8,
    }
    AN_M88__6__MER_ = {
        "clsid": "{AN-M88_MER_6_C}",
        "name": "AN-M88 *6 (MER)",
        "weight": 687.8,
    }
    CBU_1_A = {"clsid": "{CBU-1/A}", "name": "CBU-1/A", "weight": 458.921706}
    CBU_1_A__2 = {
        "clsid": "{CBU-1/A_TER_2_L}",
        "name": "CBU-1/A *2",
        "weight": 713.473056,
    }
    CBU_1_A__2_ = {
        "clsid": "{CBU-1/A_TER_2_R}",
        "name": "CBU-1/A *2",
        "weight": 713.473056,
    }
    CBU_2B_A = {"clsid": "{CBU-2B/A}", "name": "CBU-2B/A", "weight": 379.543106}
    CBU_2B_A__2 = {
        "clsid": "{CBU-2B/A_TER_2_L}",
        "name": "CBU-2B/A *2",
        "weight": 806.686212,
    }
    CBU_2B_A__2_ = {
        "clsid": "{CBU-2B/A_TER_2_R}",
        "name": "CBU-2B/A *2",
        "weight": 806.686212,
    }
    CBU_2_A = {"clsid": "{CBU-2/A}", "name": "CBU-2/A", "weight": 343.822736}
    CBU_2_A__2 = {
        "clsid": "{CBU-2/A_TER_2_L}",
        "name": "CBU-2/A *2",
        "weight": 735.245472,
    }
    CBU_2_A__2_ = {
        "clsid": "{CBU-2/A_TER_2_R}",
        "name": "CBU-2/A *2",
        "weight": 735.245472,
    }
    D_704_Refueling_Pod = {
        "clsid": "{D-704_BUDDY_POD}",
        "name": "D-704 Refueling Pod",
        "weight": 1234.532648,
    }
    Fuel_Tank_150_gallons = {
        "clsid": "{DFT-150gal}",
        "name": "Fuel Tank 150 gallons",
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
    Fuel_Tank_400_gallons = {
        "clsid": "{DFT-400gal}",
        "name": "Fuel Tank 400 gallons",
        "weight": 1320.06208,
    }
    LAU_10_2___4_ZUNI_MK_71 = {
        "clsid": "{LAU-10 ZUNI_TER_2_C}",
        "name": "LAU-10*2 - 4 ZUNI MK 71",
        "weight": 927.6,
    }
    LAU_10_2___4_ZUNI_MK_71_ = {
        "clsid": "{LAU-10 ZUNI_TER_2_L}",
        "name": "LAU-10*2 - 4 ZUNI MK 71",
        "weight": 927.6,
    }
    LAU_10_2___4_ZUNI_MK_71__ = {
        "clsid": "{LAU-10 ZUNI_TER_2_R}",
        "name": "LAU-10*2 - 4 ZUNI MK 71",
        "weight": 927.6,
    }
    LAU_10_3___4_ZUNI_MK_71 = {
        "clsid": "{LAU-10 ZUNI_TER_3_C}",
        "name": "LAU-10*3 - 4 ZUNI MK 71",
        "weight": 1367.6,
    }
    LAU_3_2___19_FFAR_M156_WP = {
        "clsid": "{LAU-3 FFAR WP156_TER_2_C}",
        "name": "LAU-3*2 - 19 FFAR M156 WP",
        "weight": 673.3414512,
    }
    LAU_3_2___19_FFAR_M156_WP_ = {
        "clsid": "{LAU-3 FFAR WP156_TER_2_L}",
        "name": "LAU-3*2 - 19 FFAR M156 WP",
        "weight": 673.3414512,
    }
    LAU_3_2___19_FFAR_M156_WP__ = {
        "clsid": "{LAU-3 FFAR WP156_TER_2_R}",
        "name": "LAU-3*2 - 19 FFAR M156 WP",
        "weight": 673.3414512,
    }
    LAU_3_2___19_FFAR_Mk1_HE = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_2_C}",
        "name": "LAU-3*2 - 19 FFAR Mk1 HE",
        "weight": 618.184664,
    }
    LAU_3_2___19_FFAR_Mk1_HE_ = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_2_L}",
        "name": "LAU-3*2 - 19 FFAR Mk1 HE",
        "weight": 618.184664,
    }
    LAU_3_2___19_FFAR_Mk1_HE__ = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_2_R}",
        "name": "LAU-3*2 - 19 FFAR Mk1 HE",
        "weight": 618.184664,
    }
    LAU_3_2___19_FFAR_Mk5_HEAT = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_2_C}",
        "name": "LAU-3*2 - 19 FFAR Mk5 HEAT",
        "weight": 619.9083136,
    }
    LAU_3_2___19_FFAR_Mk5_HEAT_ = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_2_L}",
        "name": "LAU-3*2 - 19 FFAR Mk5 HEAT",
        "weight": 619.9083136,
    }
    LAU_3_2___19_FFAR_Mk5_HEAT__ = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_2_R}",
        "name": "LAU-3*2 - 19 FFAR Mk5 HEAT",
        "weight": 619.9083136,
    }
    LAU_3_3___19_FFAR_M156_WP = {
        "clsid": "{LAU-3 FFAR WP156_TER_3_C}",
        "name": "LAU-3*3 - 19 FFAR M156 WP",
        "weight": 986.2121768,
    }
    LAU_3_3___19_FFAR_Mk1_HE = {
        "clsid": "{LAU-3 FFAR Mk1 HE_TER_3_C}",
        "name": "LAU-3*3 - 19 FFAR Mk1 HE",
        "weight": 903.476996,
    }
    LAU_3_3___19_FFAR_Mk5_HEAT = {
        "clsid": "{LAU-3 FFAR Mk5 HEAT_TER_3_C}",
        "name": "LAU-3*3 - 19 FFAR Mk5 HEAT",
        "weight": 906.0624704,
    }
    LAU_68_2___7_FFAR_M156_WP = {
        "clsid": "{LAU-68 FFAR WP156_TER_2_C}",
        "name": "LAU-68*2 - 7 FFAR M156 WP",
        "weight": 287.9121136,
    }
    LAU_68_2___7_FFAR_M156_WP_ = {
        "clsid": "{LAU-68 FFAR WP156_TER_2_L}",
        "name": "LAU-68*2 - 7 FFAR M156 WP",
        "weight": 287.9121136,
    }
    LAU_68_2___7_FFAR_M156_WP__ = {
        "clsid": "{LAU-68 FFAR WP156_TER_2_R}",
        "name": "LAU-68*2 - 7 FFAR M156 WP",
        "weight": 287.9121136,
    }
    LAU_68_2___7_FFAR_Mk1_HE = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_2_C}",
        "name": "LAU-68*2 - 7 FFAR Mk1 HE",
        "weight": 267.591192,
    }
    LAU_68_2___7_FFAR_Mk1_HE_ = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_2_L}",
        "name": "LAU-68*2 - 7 FFAR Mk1 HE",
        "weight": 267.591192,
    }
    LAU_68_2___7_FFAR_Mk1_HE__ = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_2_R}",
        "name": "LAU-68*2 - 7 FFAR Mk1 HE",
        "weight": 267.591192,
    }
    LAU_68_2___7_FFAR_Mk5_HEAT = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_2_C}",
        "name": "LAU-68*2 - 7 FFAR Mk5 HEAT",
        "weight": 268.2262208,
    }
    LAU_68_2___7_FFAR_Mk5_HEAT_ = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_2_L}",
        "name": "LAU-68*2 - 7 FFAR Mk5 HEAT",
        "weight": 268.2262208,
    }
    LAU_68_2___7_FFAR_Mk5_HEAT__ = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_2_R}",
        "name": "LAU-68*2 - 7 FFAR Mk5 HEAT",
        "weight": 268.2262208,
    }
    LAU_68_3___7_FFAR_M156_WP = {
        "clsid": "{LAU-68 FFAR WP156_TER_3_C}",
        "name": "LAU-68*3 - 7 FFAR M156 WP",
        "weight": 408.0681704,
    }
    LAU_68_3___7_FFAR_Mk1_HE = {
        "clsid": "{LAU-68 FFAR Mk1 HE_TER_3_C}",
        "name": "LAU-68*3 - 7 FFAR Mk1 HE",
        "weight": 377.586788,
    }
    LAU_68_3___7_FFAR_Mk5_HEAT = {
        "clsid": "{LAU-68 FFAR Mk5 HEAT_TER_3_C}",
        "name": "LAU-68*3 - 7 FFAR Mk5 HEAT",
        "weight": 378.5393312,
    }
    MAK79_2_MK_20 = {"clsid": "{MAK79_MK20 2L}", "name": "MAK79 2 MK-20", "weight": 464}
    MAK79_2_MK_20_ = {
        "clsid": "{MAK79_MK20 2R}",
        "name": "MAK79 2 MK-20",
        "weight": 464,
    }
    MAK79_MK_20 = {"clsid": "{MAK79_MK20 1R}", "name": "MAK79 MK-20", "weight": 232}
    MAK79_MK_20_ = {"clsid": "{MAK79_MK20 1L}", "name": "MAK79 MK-20", "weight": 232}
    Mk4_HIPEG = {"clsid": "{Mk4 HIPEG}", "name": "Mk4 HIPEG", "weight": 612.35}
    Mk_20__2__TER_ = {
        "clsid": "{Mk-20_TER_2_L}",
        "name": "Mk-20 *2 (TER)",
        "weight": 491.6,
    }
    Mk_20__2__TER__ = {
        "clsid": "{Mk-20_TER_2_R}",
        "name": "Mk-20 *2 (TER)",
        "weight": 491.6,
    }
    Mk_20__2__TER___ = {
        "clsid": "{Mk-20_TER_2_C}",
        "name": "Mk-20 *2 (TER)",
        "weight": 491.6,
    }
    Mk_20__3__TER_ = {
        "clsid": "{Mk-20_TER_3_C}",
        "name": "Mk-20 *3 (TER)",
        "weight": 713.6,
    }
    Mk_77_mod_0 = {"clsid": "{mk77mod0}", "name": "Mk-77 mod 0", "weight": 340}
    Mk_77_mod_1 = {"clsid": "{mk77mod1}", "name": "Mk-77 mod 1", "weight": 230}
    Mk_77_mod_1__2__TER_ = {
        "clsid": "{Mk-77 mod 1_TER_2_L}",
        "name": "Mk-77 mod 1 *2 (TER)",
        "weight": 507.6,
    }
    Mk_77_mod_1__2__TER__ = {
        "clsid": "{Mk-77 mod 1_TER_2_R}",
        "name": "Mk-77 mod 1 *2 (TER)",
        "weight": 507.6,
    }
    Mk_77_mod_1__2__TER___ = {
        "clsid": "{Mk-77 mod 1_TER_2_C}",
        "name": "Mk-77 mod 1 *2 (TER)",
        "weight": 507.6,
    }
    Mk_77_mod_1__4__MER_ = {
        "clsid": "{Mk-77 mod 1_MER_4_C}",
        "name": "Mk-77 mod 1 *4 (MER)",
        "weight": 1019.8,
    }
    Mk_81SE = {"clsid": "{MK-81SE}", "name": "Mk-81SE", "weight": 113.398}
    Mk_81SE__5__MER_ = {
        "clsid": "{Mk-81SE_MER_5_L}",
        "name": "Mk-81SE *5 (MER)",
        "weight": 689.8,
    }
    Mk_81SE__5__MER__ = {
        "clsid": "{Mk-81SE_MER_5_R}",
        "name": "Mk-81SE *5 (MER)",
        "weight": 689.8,
    }
    Mk_81SE__6__MER_ = {
        "clsid": "{Mk-81SE_MER_6_C}",
        "name": "Mk-81SE *6 (MER)",
        "weight": 807.8,
    }
    Mk_81__5__MER_ = {
        "clsid": "{Mk-81_MER_5_L}",
        "name": "Mk-81 *5 (MER)",
        "weight": 689.8,
    }
    Mk_81__5__MER__ = {
        "clsid": "{Mk-81_MER_5_R}",
        "name": "Mk-81 *5 (MER)",
        "weight": 689.8,
    }
    Mk_81__6__MER_ = {
        "clsid": "{Mk-81_MER_6_C}",
        "name": "Mk-81 *6 (MER)",
        "weight": 807.8,
    }
    Mk_82_Snakeye__2__TER_ = {
        "clsid": "{Mk-82 Snakeye_TER_2_L}",
        "name": "Mk-82 Snakeye *2 (TER)",
        "weight": 529.6,
    }
    Mk_82_Snakeye__2__TER__ = {
        "clsid": "{Mk-82 Snakeye_TER_2_R}",
        "name": "Mk-82 Snakeye *2 (TER)",
        "weight": 529.6,
    }
    Mk_82_Snakeye__3__TER_ = {
        "clsid": "{Mk-82 Snakeye_TER_3_C}",
        "name": "Mk-82 Snakeye *3 (TER)",
        "weight": 770.6,
    }
    Mk_82_Snakeye__4__MER_ = {
        "clsid": "{Mk-82 Snakeye_MER_4_C}",
        "name": "Mk-82 Snakeye *4 (MER)",
        "weight": 1063.8,
    }
    Mk_82_Snakeye__6__MER_ = {
        "clsid": "{Mk-82 Snakeye_MER_6_C}",
        "name": "Mk-82 Snakeye *6 (MER)",
        "weight": 1545.8,
    }
    Mk_82__2__TER_ = {
        "clsid": "{Mk-82_TER_2_L}",
        "name": "Mk-82 *2 (TER)",
        "weight": 529.6,
    }
    Mk_82__2__TER__ = {
        "clsid": "{Mk-82_TER_2_R}",
        "name": "Mk-82 *2 (TER)",
        "weight": 529.6,
    }
    Mk_82__3__TER_ = {
        "clsid": "{Mk-82_TER_3_C}",
        "name": "Mk-82 *3 (TER)",
        "weight": 770.6,
    }
    Mk_82__4__MER_ = {
        "clsid": "{Mk-82_MER_4_C}",
        "name": "Mk-82 *4 (MER)",
        "weight": 1063.8,
    }
    Mk_82__6__MER_ = {
        "clsid": "{Mk-82_MER_6_C}",
        "name": "Mk-82 *6 (MER)",
        "weight": 1545.8,
    }
    Mk_83__2__TER_ = {
        "clsid": "{Mk-83_TER_2_C}",
        "name": "Mk-83 *2 (TER)",
        "weight": 941.6,
    }
    Mk_83__3__TER_ = {
        "clsid": "{Mk-83_TER_3_C}",
        "name": "Mk-83 *3 (TER)",
        "weight": 1388.6,
    }
    _3_LAU_61 = ({"clsid": "{TER,LAU-61*3}", "name": "3*LAU-61", "weight": 98},)
    Fuel_Tank_150_gallons__EMPTY_ = {
        "clsid": "{DFT-150gal_EMPTY}",
        "name": "Fuel_Tank_150_gallons__EMPTY",
        "weight": 61.688512,
    }
    Fuel_Tank_300_gallons__EMPTY_ = {
        "clsid": "{DFT-300gal_EMPTY}",
        "name": "Fuel_Tank_300_gallons__EMPTY",
        "weight": 83.007336,
    }
    Fuel_Tank_300_gallons__EMPTY__ = {
        "clsid": "{DFT-300gal_LR_EMPTY}",
        "name": "Fuel_Tank_300_gallons__EMPTY",
        "weight": 90.264808,
    }
    Fuel_Tank_400_gallons__EMPTY_ = {
        "clsid": "{DFT-400gal_EMPTY}",
        "name": "Fuel_Tank_400_gallons__EMPTY",
        "weight": 108.86208,
    }


inject_weapons(WeaponsA4EC)


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

    property_defaults = {
        "HideECMPanel": False,
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

        class CBU2ATPP:
            id = "CBU2ATPP"

            class Values:
                _1_tube = 0
                _2_tubes = 1
                _3_tubes = 2
                _4_tubes = 3
                _6_tubes = 4
                _17_tubes__salvo = 5

        class CBU2BATPP:
            id = "CBU2BATPP"

            class Values:
                _2_tubes = 0
                _4_tubes = 1
                _6_tubes = 2

        class CMS_BURSTS:
            id = "CMS_BURSTS"

            class Values:
                _1 = 1
                _2 = 2
                _3 = 3
                _4 = 4

        class CMS_BURST_INTERVAL:
            id = "CMS_BURST_INTERVAL"

            class Values:
                _0_2_seconds = 1
                _0_3_seconds = 2
                _0_4_seconds = 3
                _0_5_seconds = 4

        class CMS_SALVOS:
            id = "CMS_SALVOS"

            class Values:
                _8 = 1
                _12 = 2
                _16 = 3
                _20 = 4
                _24 = 5
                _28 = 6
                _32 = 7

        class CMS_SALVO_INTERVAL:
            id = "CMS_SALVO_INTERVAL"

            class Values:
                _2_seconds = 1
                _4_seconds = 2
                _6_seconds = 3
                _8_seconds = 4
                _10_seconds = 5
                _12_seconds = 6
                _14_seconds = 7

    class Liveries:
        class Georgia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Syria(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Finland(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Australia(Enum):
            Unmarked = "Unmarked"
            International_Australia = "International Australia"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"
            International_New_Zealand = "International New Zealand"
            International_New_Zealand_Kiwi_Red = "International New Zealand Kiwi Red"
            International_New_Zealand_Sqn_75 = "International New Zealand Sqn 75"

        class Germany(Enum):
            Unmarked = "Unmarked"
            Trainer_BAE_Systems = "Trainer BAE Systems"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class SaudiArabia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Israel(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"
            International_Israel = "International Israel"

        class Croatia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class CzechRepublic(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Norway(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Romania(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Spain(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Ukraine(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Belgium(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Slovakia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Greece(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class UK(Enum):
            Unmarked = "Unmarked"
            Trainer_BAE_Systems = "Trainer BAE Systems"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Insurgents(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Hungary(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class France(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Abkhazia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Russia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Sweden(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Austria(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Switzerland(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Italy(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class SouthOssetia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class SouthKorea(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Iran(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class China(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Pakistan(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Belarus(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class NorthKorea(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Iraq(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Kazakhstan(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Bulgaria(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Serbia(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class India(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class USAFAggressors(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"
            Aggressor_USMC_TopGun_MiG_17 = "Aggressor USMC TopGun MiG-17"
            Aggressor_USN_TopGun = "Aggressor USN TopGun"
            Aggressor_USN_VF_126_Bandits = "Aggressor USN VF-126 Bandits"
            Aggressor_USN_VF_127_Royal_Blues = "Aggressor USN VF-127 Royal Blues"
            Aggressor_USN_VFA_127_Cyclons__Forest = (
                "Aggressor USN VFA-127 Cyclons (Forest)"
            )
            Aggressor_USN_VFA_127_Cyclons__Sea = "Aggressor USN VFA-127 Cyclons (Sea)"

        class USA(Enum):
            Unmarked = "Unmarked"
            International_Argentina = "International Argentina"
            International_Australia = "International Australia"
            Trainer_BAE_Systems = "Trainer BAE Systems"
            Blue_Angels_no_1 = "Blue Angels no 1"
            Blue_Angels_no_2 = "Blue Angels no 2"
            Blue_Angels_no_3 = "Blue Angels no 3"
            Blue_Angels_no_4 = "Blue Angels no 4"
            Blue_Angels_no_5 = "Blue Angels no 5"
            Blue_Angels_no_6 = "Blue Angels no 6"
            International_Brazil = "International Brazil"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"
            International_Israel = "International Israel"
            International_Kuwait = "International Kuwait"
            International_New_Zealand = "International New Zealand"
            International_New_Zealand_Kiwi_Red = "International New Zealand Kiwi Red"
            International_New_Zealand_Sqn_75 = "International New Zealand Sqn 75"
            Trainer_USMC_PTMC = "Trainer USMC PTMC"
            Aggressor_USMC_TopGun_MiG_17 = "Aggressor USMC TopGun MiG-17"
            USMC_VMA_121_Green_Knights = "USMC VMA-121 Green Knights"
            USMC_VMA_124_Memphis_Marines = "USMC VMA-124 Memphis Marines"
            USMC_VMA_131_Diamondbacks = "USMC VMA-131 Diamondbacks"
            USMC_VMA_142_Flying_Gators = "USMC VMA-142 Flying Gators"
            USMC_VMA_211_Avengers = "USMC VMA-211 Avengers"
            USMC_VMA_311_Tomcats = "USMC VMA-311 Tomcats"
            USMC_VMA_322_Fighting_Gamecocks = "USMC VMA-322 Fighting Gamecocks"
            Trainer_USMC_VMAT_102 = "Trainer USMC VMAT-102"
            Trainer_USN_Bare_Metal_1956 = "Trainer USN Bare Metal 1956"
            Trainer_USN_NFWS_Gray = "Trainer USN NFWS Gray"
            Trainer_USN_NFWS_Green = "Trainer USN NFWS Green"
            Aggressor_USN_TopGun = "Aggressor USN TopGun"
            USN_VA_144_Roadrunners = "USN VA-144 Roadrunners"
            USN_VA_153_Blue_Tail_Flies = "USN VA-153 Blue Tail Flies"
            USN_VA_163_Saints = "USN VA-163 Saints"
            USN_VA_164_Ghostriders = "USN VA-164 Ghostriders"
            USN_VA_195_Dambusters = "USN VA-195 Dambusters"
            USN_VA_212_Rampant_Raiders = "USN VA-212 Rampant Raiders"
            USN_VA_45_Blackbirds = "USN VA-45 Blackbirds"
            USN_VA_55_Warhorses = "USN VA-55 Warhorses"
            USN_VA_64_Black_Lancers = "USN VA-64 Black Lancers"
            Trainer_USN_VC_1_FLECOMPRON_One = "Trainer USN VC-1 FLECOMPRON One"
            Trainer_USN_VC_5_Checkertails = "Trainer USN VC-5 Checkertails"
            USN_VC_7_Tallyhoers = "USN VC-7 Tallyhoers"
            Trainer_USN_VC_8_Redtails = "Trainer USN VC-8 Redtails"
            Aggressor_USN_VF_126_Bandits = "Aggressor USN VF-126 Bandits"
            Aggressor_USN_VF_127_Royal_Blues = "Aggressor USN VF-127 Royal Blues"
            Aggressor_USN_VFA_127_Cyclons__Forest = (
                "Aggressor USN VFA-127 Cyclons (Forest)"
            )
            Aggressor_USN_VFA_127_Cyclons__Sea = "Aggressor USN VFA-127 Cyclons (Sea)"
            Trainer_USN_VT_7_Eagles = "Trainer USN VT-7 Eagles"

        class Denmark(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Egypt(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Canada(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class TheNetherlands(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Turkey(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Japan(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

        class Poland(Enum):
            Unmarked = "Unmarked"
            Community_A_4E = "Community A-4E"
            Community_A_4E_II = "Community A-4E II"

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
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            1,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
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
        AGM_45A_Shrike_ARM = (1, Weapons.AGM_45A_Shrike_ARM)
        # ERRR {AGM12_B}
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81SE = (1, WeaponsA4EC.Mk_81SE)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            1,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_77_mod_1 = (1, WeaponsA4EC.Mk_77_mod_1)
        AN_M30A1___100lb_GP_Bomb_LD = (1, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (1, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (1, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M81 = (1, WeaponsA4EC.AN_M81)
        AN_M88 = (1, WeaponsA4EC.AN_M88)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
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
        Fuel_Tank_300_gallons__EMPTY__ = (
            2,
            WeaponsA4EC.Fuel_Tank_300_gallons__EMPTY__,
        )
        Fuel_Tank_150_gallons = (2, WeaponsA4EC.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (
            2,
            WeaponsA4EC.Fuel_Tank_150_gallons__EMPTY_,
        )
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
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_10_2___4_ZUNI_MK_71_ = (2, WeaponsA4EC.LAU_10_2___4_ZUNI_MK_71_)
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
        LAU_3_2___19_FFAR_M156_WP_ = (2, WeaponsA4EC.LAU_3_2___19_FFAR_M156_WP_)
        LAU_3_2___19_FFAR_Mk1_HE_ = (2, WeaponsA4EC.LAU_3_2___19_FFAR_Mk1_HE_)
        LAU_3_2___19_FFAR_Mk5_HEAT_ = (2, WeaponsA4EC.LAU_3_2___19_FFAR_Mk5_HEAT_)
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
        LAU_68_2___7_FFAR_M156_WP_ = (2, WeaponsA4EC.LAU_68_2___7_FFAR_M156_WP_)
        LAU_68_2___7_FFAR_Mk1_HE_ = (2, WeaponsA4EC.LAU_68_2___7_FFAR_Mk1_HE_)
        LAU_68_2___7_FFAR_Mk5_HEAT_ = (2, WeaponsA4EC.LAU_68_2___7_FFAR_Mk5_HEAT_)
        AGM_45A_Shrike_ARM = (2, Weapons.AGM_45A_Shrike_ARM)
        # ERRR {AGM12_C}
        # ERRR {AGM12_B}
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            2,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81SE = (2, WeaponsA4EC.Mk_81SE)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_77_mod_0 = (2, WeaponsA4EC.Mk_77_mod_0)
        Mk_77_mod_1 = (2, WeaponsA4EC.Mk_77_mod_1)
        AN_M30A1___100lb_GP_Bomb_LD = (2, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (2, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (2, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (2, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81 = (2, WeaponsA4EC.AN_M81)
        AN_M88 = (2, WeaponsA4EC.AN_M88)
        CBU_1_A = (2, WeaponsA4EC.CBU_1_A)
        CBU_2_A = (2, WeaponsA4EC.CBU_2_A)
        CBU_2B_A = (2, WeaponsA4EC.CBU_2B_A)
        CBU_1_A__2 = (2, WeaponsA4EC.CBU_1_A__2)
        CBU_2_A__2 = (2, WeaponsA4EC.CBU_2_A__2)
        CBU_2B_A__2 = (2, WeaponsA4EC.CBU_2B_A__2)
        Mk_20__2__TER_ = (2, WeaponsA4EC.Mk_20__2__TER_)
        Mk_81__5__MER_ = (2, WeaponsA4EC.Mk_81__5__MER_)
        Mk_81SE__5__MER_ = (2, WeaponsA4EC.Mk_81SE__5__MER_)
        Mk_82__2__TER_ = (2, WeaponsA4EC.Mk_82__2__TER_)
        Mk_82_Snakeye__2__TER_ = (2, WeaponsA4EC.Mk_82_Snakeye__2__TER_)
        AN_M57__5__MER_ = (2, WeaponsA4EC.AN_M57__5__MER_)
        AN_M57__2__TER_ = (2, WeaponsA4EC.AN_M57__2__TER_)
        AN_M81__5__MER_ = (2, WeaponsA4EC.AN_M81__5__MER_)
        AN_M88__5__MER_ = (2, WeaponsA4EC.AN_M88__5__MER_)
        Mk4_HIPEG = (2, WeaponsA4EC.Mk4_HIPEG)
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
        Fuel_Tank_400_gallons__EMPTY_ = (
            3,
            WeaponsA4EC.Fuel_Tank_400_gallons__EMPTY_,
        )
        Fuel_Tank_300_gallons__EMPTY_ = (
            3,
            WeaponsA4EC.Fuel_Tank_300_gallons__EMPTY_,
        )
        Fuel_Tank_150_gallons__EMPTY_ = (
            3,
            WeaponsA4EC.Fuel_Tank_150_gallons__EMPTY_,
        )
        # ERRR {3*LAU-61}
        BRU_42_with_3_x_LAU_68_pods___21_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.BRU_42_with_3_x_LAU_68_pods___21_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_10_2___4_ZUNI_MK_71 = (3, WeaponsA4EC.LAU_10_2___4_ZUNI_MK_71)
        LAU_10_3___4_ZUNI_MK_71 = (3, WeaponsA4EC.LAU_10_3___4_ZUNI_MK_71)
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
        LAU_3_2___19_FFAR_M156_WP = (3, WeaponsA4EC.LAU_3_2___19_FFAR_M156_WP)
        LAU_3_2___19_FFAR_Mk1_HE = (3, WeaponsA4EC.LAU_3_2___19_FFAR_Mk1_HE)
        LAU_3_2___19_FFAR_Mk5_HEAT = (3, WeaponsA4EC.LAU_3_2___19_FFAR_Mk5_HEAT)
        LAU_3_3___19_FFAR_M156_WP = (3, WeaponsA4EC.LAU_3_3___19_FFAR_M156_WP)
        LAU_3_3___19_FFAR_Mk1_HE = (3, WeaponsA4EC.LAU_3_3___19_FFAR_Mk1_HE)
        LAU_3_3___19_FFAR_Mk5_HEAT = (3, WeaponsA4EC.LAU_3_3___19_FFAR_Mk5_HEAT)
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
        LAU_68_2___7_FFAR_M156_WP = (3, WeaponsA4EC.LAU_68_2___7_FFAR_M156_WP)
        LAU_68_2___7_FFAR_Mk1_HE = (3, WeaponsA4EC.LAU_68_2___7_FFAR_Mk1_HE)
        LAU_68_2___7_FFAR_Mk5_HEAT = (3, WeaponsA4EC.LAU_68_2___7_FFAR_Mk5_HEAT)
        LAU_68_3___7_FFAR_M156_WP = (3, WeaponsA4EC.LAU_68_3___7_FFAR_M156_WP)
        LAU_68_3___7_FFAR_Mk1_HE = (3, WeaponsA4EC.LAU_68_3___7_FFAR_Mk1_HE)
        LAU_68_3___7_FFAR_Mk5_HEAT = (3, WeaponsA4EC.LAU_68_3___7_FFAR_Mk5_HEAT)
        # ERRR {AGM12_B}
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            3,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81SE = (3, WeaponsA4EC.Mk_81SE)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (3, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_77_mod_0 = (3, WeaponsA4EC.Mk_77_mod_0)
        Mk_77_mod_1 = (3, WeaponsA4EC.Mk_77_mod_1)
        AN_M30A1___100lb_GP_Bomb_LD = (3, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (3, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (3, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (3, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M66A2 = (3, WeaponsA4EC.AN_M66A2)
        AN_M81 = (3, WeaponsA4EC.AN_M81)
        AN_M88 = (3, WeaponsA4EC.AN_M88)
        Mk_20__3__TER_ = (3, WeaponsA4EC.Mk_20__3__TER_)
        Mk_20__2__TER___ = (3, WeaponsA4EC.Mk_20__2__TER___)
        Mk_81__6__MER_ = (3, WeaponsA4EC.Mk_81__6__MER_)
        Mk_81SE__6__MER_ = (3, WeaponsA4EC.Mk_81SE__6__MER_)
        Mk_82__6__MER_ = (3, WeaponsA4EC.Mk_82__6__MER_)
        Mk_82__4__MER_ = (3, WeaponsA4EC.Mk_82__4__MER_)
        Mk_82__3__TER_ = (3, WeaponsA4EC.Mk_82__3__TER_)
        Mk_82_Snakeye__6__MER_ = (3, WeaponsA4EC.Mk_82_Snakeye__6__MER_)
        Mk_82_Snakeye__4__MER_ = (3, WeaponsA4EC.Mk_82_Snakeye__4__MER_)
        Mk_82_Snakeye__3__TER_ = (3, WeaponsA4EC.Mk_82_Snakeye__3__TER_)
        Mk_83__3__TER_ = (3, WeaponsA4EC.Mk_83__3__TER_)
        Mk_83__2__TER_ = (3, WeaponsA4EC.Mk_83__2__TER_)
        Mk_77_mod_1__2__TER___ = (3, WeaponsA4EC.Mk_77_mod_1__2__TER___)
        AN_M57__6__MER_ = (3, WeaponsA4EC.AN_M57__6__MER_)
        AN_M57__3__TER_ = (3, WeaponsA4EC.AN_M57__3__TER_)
        AN_M81__6__MER_ = (3, WeaponsA4EC.AN_M81__6__MER_)
        AN_M88__6__MER_ = (3, WeaponsA4EC.AN_M88__6__MER_)
        Mk4_HIPEG = (3, WeaponsA4EC.Mk4_HIPEG)
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
        Fuel_Tank_300_gallons__EMPTY__ = (
            4,
            WeaponsA4EC.Fuel_Tank_300_gallons__EMPTY__,
        )
        Fuel_Tank_150_gallons = (4, WeaponsA4EC.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (
            4,
            WeaponsA4EC.Fuel_Tank_150_gallons__EMPTY_,
        )
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
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_10_2___4_ZUNI_MK_71__ = (4, WeaponsA4EC.LAU_10_2___4_ZUNI_MK_71__)
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
        LAU_3_2___19_FFAR_M156_WP__ = (4, WeaponsA4EC.LAU_3_2___19_FFAR_M156_WP__)
        LAU_3_2___19_FFAR_Mk1_HE__ = (4, WeaponsA4EC.LAU_3_2___19_FFAR_Mk1_HE__)
        LAU_3_2___19_FFAR_Mk5_HEAT__ = (4, WeaponsA4EC.LAU_3_2___19_FFAR_Mk5_HEAT__)
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
        LAU_68_2___7_FFAR_M156_WP__ = (4, WeaponsA4EC.LAU_68_2___7_FFAR_M156_WP__)
        LAU_68_2___7_FFAR_Mk1_HE__ = (4, WeaponsA4EC.LAU_68_2___7_FFAR_Mk1_HE__)
        LAU_68_2___7_FFAR_Mk5_HEAT__ = (4, WeaponsA4EC.LAU_68_2___7_FFAR_Mk5_HEAT__)
        AGM_45A_Shrike_ARM = (4, Weapons.AGM_45A_Shrike_ARM)
        # ERRR {AGM12_C}
        # ERRR {AGM12_B}
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            4,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81SE = (4, WeaponsA4EC.Mk_81SE)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_77_mod_0 = (4, WeaponsA4EC.Mk_77_mod_0)
        Mk_77_mod_1 = (4, WeaponsA4EC.Mk_77_mod_1)
        AN_M30A1___100lb_GP_Bomb_LD = (4, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (4, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (4, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (4, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81 = (4, WeaponsA4EC.AN_M81)
        AN_M88 = (4, WeaponsA4EC.AN_M88)
        CBU_1_A = (4, WeaponsA4EC.CBU_1_A)
        CBU_2_A = (4, WeaponsA4EC.CBU_2_A)
        CBU_2B_A = (4, WeaponsA4EC.CBU_2B_A)
        CBU_1_A__2_ = (4, WeaponsA4EC.CBU_1_A__2_)
        CBU_2_A__2_ = (4, WeaponsA4EC.CBU_2_A__2_)
        CBU_2B_A__2_ = (4, WeaponsA4EC.CBU_2B_A__2_)
        Mk_20__2__TER__ = (4, WeaponsA4EC.Mk_20__2__TER__)
        Mk_81__5__MER__ = (4, WeaponsA4EC.Mk_81__5__MER__)
        Mk_81SE__5__MER__ = (4, WeaponsA4EC.Mk_81SE__5__MER__)
        Mk_82__2__TER__ = (4, WeaponsA4EC.Mk_82__2__TER__)
        Mk_82_Snakeye__2__TER__ = (4, WeaponsA4EC.Mk_82_Snakeye__2__TER__)
        AN_M57__5__MER__ = (4, WeaponsA4EC.AN_M57__5__MER__)
        AN_M57__2__TER__ = (4, WeaponsA4EC.AN_M57__2__TER__)
        AN_M81__5__MER__ = (4, WeaponsA4EC.AN_M81__5__MER__)
        AN_M88__5__MER__ = (4, WeaponsA4EC.AN_M88__5__MER__)
        Mk4_HIPEG = (4, WeaponsA4EC.Mk4_HIPEG)
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
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            5,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
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
        AGM_45A_Shrike_ARM = (5, Weapons.AGM_45A_Shrike_ARM)
        # ERRR {AGM12_B}
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_81___250lb_GP_Bomb_LD = (5, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_81SE = (5, WeaponsA4EC.Mk_81SE)
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_77_mod_1 = (5, WeaponsA4EC.Mk_77_mod_1)
        AN_M30A1___100lb_GP_Bomb_LD = (5, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (5, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (5, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M81 = (5, WeaponsA4EC.AN_M81)
        AN_M88 = (5, WeaponsA4EC.AN_M88)
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
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            5,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 5}

    tasks = [
        task.CAP,
        task.CAS,
        task.SEAD,
        task.GroundAttack,
        task.AFAC,
        task.Refueling,
    ]
    task_default = task.CAS
