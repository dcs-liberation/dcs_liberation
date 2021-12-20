from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF104:
    VSN_F104G_L_PTB = {"clsid": "VSN_F104G_L_PTB", "name": "500L Tank L", "weight": 632}
    VSN_F104G_L_PTB_ = {
        "clsid": "VSN_F104G_L_PTB",
        "name": "500L Tank L",
        "weight": 632,
    }
    VSN_F104G_L_PTB__ = {
        "clsid": "VSN_F104G_L_PTB",
        "name": "500L Tank L",
        "weight": 632,
    }
    VSN_F104G_PTB = {"clsid": "VSN_F104G_PTB", "name": "500L Tank", "weight": 632}
    VSN_F104G_PTB_ = {"clsid": "VSN_F104G_PTB", "name": "500L Tank", "weight": 632}
    VSN_F104G_PTB__ = {"clsid": "VSN_F104G_PTB", "name": "500L Tank", "weight": 632}
    VSN_F104G_R_PTB = {"clsid": "VSN_F104G_R_PTB", "name": "500L Tank R", "weight": 632}
    VSN_F104G_R_PTB_ = {
        "clsid": "VSN_F104G_R_PTB",
        "name": "500L Tank R",
        "weight": 632,
    }
    VSN_F104G_R_PTB__ = {
        "clsid": "VSN_F104G_R_PTB",
        "name": "500L Tank R",
        "weight": 632,
    }


inject_weapons(WeaponsF104)


class VSN_F104G(PlaneType):
    id = "VSN_F104G"
    flyable = True
    height = 4.09
    width = 6.36
    length = 16.66
    fuel_max = 2641
    max_speed = 2336.4
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    class Liveries:
        class USSR(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Georgia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Venezuela(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Australia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Israel(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Combined_Joint_Task_Forces_Blue(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Sudan(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Norway(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Romania(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Iran(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Ukraine(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Libya(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Belgium(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Slovakia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Greece(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class UK(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Third_Reich(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Hungary(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Abkhazia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Morocco(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class United_Nations_Peacekeepers(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Switzerland(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class SouthOssetia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Vietnam(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class China(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Yemen(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Kuwait(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Serbia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Oman(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class India(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Egypt(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class TheNetherlands(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Poland(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Syria(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Finland(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Kazakhstan(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Denmark(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Sweden(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Croatia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class CzechRepublic(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class GDR(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Yugoslavia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Bulgaria(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class SouthKorea(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Tunisia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Combined_Joint_Task_Forces_Red(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Lebanon(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Portugal(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Cuba(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Insurgents(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class SaudiArabia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class France(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class USA(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Honduras(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Qatar(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Russia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class United_Arab_Emirates(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Italian_Social_Republi(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Austria(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Bahrain(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Italy(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Chile(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Turkey(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Philippines(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Algeria(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Pakistan(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Malaysia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Indonesia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Iraq(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Germany(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class South_Africa(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Jordan(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Mexico(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class USAFAggressors(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Brazil(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Spain(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Belarus(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Canada(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class NorthKorea(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Ethiopia(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Japan(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

        class Thailand(Enum):
            USAF_70925_Smoke_II = "USAF 70925 Smoke II"
            CAF_Asymmetrical = "CAF Asymmetrical"
            HAF_SEA = "HAF SEA"
            JG_71_Norm_62 = "JG 71 Norm 62"
            JG_74_Norm_62 = "JG 74 Norm 62"
            JaboG_31_NMF = "JaboG 31 NMF"
            JaboG_32___Bavaria = "JaboG 32 - Bavaria"
            JaboG_33_Norm_62 = "JaboG 33 Norm 62"
            JaboG_34_Norm_62 = "JaboG 34 Norm 62"
            JaboG_36_Norm_62 = "JaboG 36 Norm 62"
            JaboG_36_Norm_62_early = "JaboG 36 Norm 62 early"
            MFG_1_MARINE_Norm_62 = "MFG 1 MARINE Norm 62"
            MFG_2_MARINE_Norm_76 = "MFG 2 MARINE Norm 76"
            Turkey_12613 = "Turkey 12613"
            WaSLw_10_Norm_62_early = "WaSLw 10 Norm 62 early"

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (2, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        VSN_F104G_L_PTB__ = (2, Weapons.VSN_F104G_L_PTB__)

    class Pylon4:
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            4,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            4,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            4,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (4, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            4,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP = (
            4,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP,
        )
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        Kormoran___ASM = (4, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (4, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB__ = (4, Weapons.VSN_F104G_PTB__)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon6:
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        RN_24___470kg__nuclear_bomb__free_fall = (
            6,
            Weapons.RN_24___470kg__nuclear_bomb__free_fall,
        )
        RN_28___260_kg__nuclear_bomb__free_fall = (
            6,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon8:
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            8,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            8,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            8,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (8, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            8,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP = (
            8,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP,
        )
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        Kormoran___ASM = (8, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (8, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB__ = (8, Weapons.VSN_F104G_PTB__)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (10, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (10, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        VSN_F104G_R_PTB__ = (10, Weapons.VSN_F104G_R_PTB__)

    class Pylon11:
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons = {1, 2, 4, 5, 6, 7, 8, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep


class VSN_F104S(PlaneType):
    id = "VSN_F104S"
    flyable = True
    height = 4.09
    width = 6.36
    length = 16.66
    fuel_max = 2641
    max_speed = 2336.4
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    class Liveries:
        class USSR(Enum):
            _4_Stormo = "4 Stormo"

        class Georgia(Enum):
            _4_Stormo = "4 Stormo"

        class Venezuela(Enum):
            _4_Stormo = "4 Stormo"

        class Australia(Enum):
            _4_Stormo = "4 Stormo"

        class Israel(Enum):
            _4_Stormo = "4 Stormo"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _4_Stormo = "4 Stormo"

        class Sudan(Enum):
            _4_Stormo = "4 Stormo"

        class Norway(Enum):
            _4_Stormo = "4 Stormo"

        class Romania(Enum):
            _4_Stormo = "4 Stormo"

        class Iran(Enum):
            _4_Stormo = "4 Stormo"

        class Ukraine(Enum):
            _4_Stormo = "4 Stormo"

        class Libya(Enum):
            _4_Stormo = "4 Stormo"

        class Belgium(Enum):
            _4_Stormo = "4 Stormo"

        class Slovakia(Enum):
            _4_Stormo = "4 Stormo"

        class Greece(Enum):
            _4_Stormo = "4 Stormo"

        class UK(Enum):
            _4_Stormo = "4 Stormo"

        class Third_Reich(Enum):
            _4_Stormo = "4 Stormo"

        class Hungary(Enum):
            _4_Stormo = "4 Stormo"

        class Abkhazia(Enum):
            _4_Stormo = "4 Stormo"

        class Morocco(Enum):
            _4_Stormo = "4 Stormo"

        class United_Nations_Peacekeepers(Enum):
            _4_Stormo = "4 Stormo"

        class Switzerland(Enum):
            _4_Stormo = "4 Stormo"

        class SouthOssetia(Enum):
            _4_Stormo = "4 Stormo"

        class Vietnam(Enum):
            _4_Stormo = "4 Stormo"

        class China(Enum):
            _4_Stormo = "4 Stormo"

        class Yemen(Enum):
            _4_Stormo = "4 Stormo"

        class Kuwait(Enum):
            _4_Stormo = "4 Stormo"

        class Serbia(Enum):
            _4_Stormo = "4 Stormo"

        class Oman(Enum):
            _4_Stormo = "4 Stormo"

        class India(Enum):
            _4_Stormo = "4 Stormo"

        class Egypt(Enum):
            _4_Stormo = "4 Stormo"

        class TheNetherlands(Enum):
            _4_Stormo = "4 Stormo"

        class Poland(Enum):
            _4_Stormo = "4 Stormo"

        class Syria(Enum):
            _4_Stormo = "4 Stormo"

        class Finland(Enum):
            _4_Stormo = "4 Stormo"

        class Kazakhstan(Enum):
            _4_Stormo = "4 Stormo"

        class Denmark(Enum):
            _4_Stormo = "4 Stormo"

        class Sweden(Enum):
            _4_Stormo = "4 Stormo"

        class Croatia(Enum):
            _4_Stormo = "4 Stormo"

        class CzechRepublic(Enum):
            _4_Stormo = "4 Stormo"

        class GDR(Enum):
            _4_Stormo = "4 Stormo"

        class Yugoslavia(Enum):
            _4_Stormo = "4 Stormo"

        class Bulgaria(Enum):
            _4_Stormo = "4 Stormo"

        class SouthKorea(Enum):
            _4_Stormo = "4 Stormo"

        class Tunisia(Enum):
            _4_Stormo = "4 Stormo"

        class Combined_Joint_Task_Forces_Red(Enum):
            _4_Stormo = "4 Stormo"

        class Lebanon(Enum):
            _4_Stormo = "4 Stormo"

        class Portugal(Enum):
            _4_Stormo = "4 Stormo"

        class Cuba(Enum):
            _4_Stormo = "4 Stormo"

        class Insurgents(Enum):
            _4_Stormo = "4 Stormo"

        class SaudiArabia(Enum):
            _4_Stormo = "4 Stormo"

        class France(Enum):
            _4_Stormo = "4 Stormo"

        class USA(Enum):
            _4_Stormo = "4 Stormo"

        class Honduras(Enum):
            _4_Stormo = "4 Stormo"

        class Qatar(Enum):
            _4_Stormo = "4 Stormo"

        class Russia(Enum):
            _4_Stormo = "4 Stormo"

        class United_Arab_Emirates(Enum):
            _4_Stormo = "4 Stormo"

        class Italian_Social_Republi(Enum):
            _4_Stormo = "4 Stormo"

        class Austria(Enum):
            _4_Stormo = "4 Stormo"

        class Bahrain(Enum):
            _4_Stormo = "4 Stormo"

        class Italy(Enum):
            _4_Stormo = "4 Stormo"

        class Chile(Enum):
            _4_Stormo = "4 Stormo"

        class Turkey(Enum):
            _4_Stormo = "4 Stormo"

        class Philippines(Enum):
            _4_Stormo = "4 Stormo"

        class Algeria(Enum):
            _4_Stormo = "4 Stormo"

        class Pakistan(Enum):
            _4_Stormo = "4 Stormo"

        class Malaysia(Enum):
            _4_Stormo = "4 Stormo"

        class Indonesia(Enum):
            _4_Stormo = "4 Stormo"

        class Iraq(Enum):
            _4_Stormo = "4 Stormo"

        class Germany(Enum):
            _4_Stormo = "4 Stormo"

        class South_Africa(Enum):
            _4_Stormo = "4 Stormo"

        class Jordan(Enum):
            _4_Stormo = "4 Stormo"

        class Mexico(Enum):
            _4_Stormo = "4 Stormo"

        class USAFAggressors(Enum):
            _4_Stormo = "4 Stormo"

        class Brazil(Enum):
            _4_Stormo = "4 Stormo"

        class Spain(Enum):
            _4_Stormo = "4 Stormo"

        class Belarus(Enum):
            _4_Stormo = "4 Stormo"

        class Canada(Enum):
            _4_Stormo = "4 Stormo"

        class NorthKorea(Enum):
            _4_Stormo = "4 Stormo"

        class Ethiopia(Enum):
            _4_Stormo = "4 Stormo"

        class Japan(Enum):
            _4_Stormo = "4 Stormo"

        class Thailand(Enum):
            _4_Stormo = "4 Stormo"

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (2, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        VSN_F104G_L_PTB__ = (2, Weapons.VSN_F104G_L_PTB__)

    class Pylon3:
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_7E_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        VSN_F104G_PTB__ = (4, Weapons.VSN_F104G_PTB__)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon6:
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (6, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (6, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        VSN_F104G_PTB__ = (8, Weapons.VSN_F104G_PTB__)

    class Pylon9:
        AIM_9B_Sidewinder_IR_AAM = (9, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_7E_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (10, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (10, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        VSN_F104G_R_PTB__ = (10, Weapons.VSN_F104G_R_PTB__)

    class Pylon11:
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep


class VSN_F104S_AG(PlaneType):
    id = "VSN_F104S_AG"
    flyable = True
    height = 4.09
    width = 6.36
    length = 16.66
    fuel_max = 2641
    max_speed = 2336.4
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    class Liveries:
        class USSR(Enum):
            _4_Stormo = "4 Stormo"

        class Georgia(Enum):
            _4_Stormo = "4 Stormo"

        class Venezuela(Enum):
            _4_Stormo = "4 Stormo"

        class Australia(Enum):
            _4_Stormo = "4 Stormo"

        class Israel(Enum):
            _4_Stormo = "4 Stormo"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _4_Stormo = "4 Stormo"

        class Sudan(Enum):
            _4_Stormo = "4 Stormo"

        class Norway(Enum):
            _4_Stormo = "4 Stormo"

        class Romania(Enum):
            _4_Stormo = "4 Stormo"

        class Iran(Enum):
            _4_Stormo = "4 Stormo"

        class Ukraine(Enum):
            _4_Stormo = "4 Stormo"

        class Libya(Enum):
            _4_Stormo = "4 Stormo"

        class Belgium(Enum):
            _4_Stormo = "4 Stormo"

        class Slovakia(Enum):
            _4_Stormo = "4 Stormo"

        class Greece(Enum):
            _4_Stormo = "4 Stormo"

        class UK(Enum):
            _4_Stormo = "4 Stormo"

        class Third_Reich(Enum):
            _4_Stormo = "4 Stormo"

        class Hungary(Enum):
            _4_Stormo = "4 Stormo"

        class Abkhazia(Enum):
            _4_Stormo = "4 Stormo"

        class Morocco(Enum):
            _4_Stormo = "4 Stormo"

        class United_Nations_Peacekeepers(Enum):
            _4_Stormo = "4 Stormo"

        class Switzerland(Enum):
            _4_Stormo = "4 Stormo"

        class SouthOssetia(Enum):
            _4_Stormo = "4 Stormo"

        class Vietnam(Enum):
            _4_Stormo = "4 Stormo"

        class China(Enum):
            _4_Stormo = "4 Stormo"

        class Yemen(Enum):
            _4_Stormo = "4 Stormo"

        class Kuwait(Enum):
            _4_Stormo = "4 Stormo"

        class Serbia(Enum):
            _4_Stormo = "4 Stormo"

        class Oman(Enum):
            _4_Stormo = "4 Stormo"

        class India(Enum):
            _4_Stormo = "4 Stormo"

        class Egypt(Enum):
            _4_Stormo = "4 Stormo"

        class TheNetherlands(Enum):
            _4_Stormo = "4 Stormo"

        class Poland(Enum):
            _4_Stormo = "4 Stormo"

        class Syria(Enum):
            _4_Stormo = "4 Stormo"

        class Finland(Enum):
            _4_Stormo = "4 Stormo"

        class Kazakhstan(Enum):
            _4_Stormo = "4 Stormo"

        class Denmark(Enum):
            _4_Stormo = "4 Stormo"

        class Sweden(Enum):
            _4_Stormo = "4 Stormo"

        class Croatia(Enum):
            _4_Stormo = "4 Stormo"

        class CzechRepublic(Enum):
            _4_Stormo = "4 Stormo"

        class GDR(Enum):
            _4_Stormo = "4 Stormo"

        class Yugoslavia(Enum):
            _4_Stormo = "4 Stormo"

        class Bulgaria(Enum):
            _4_Stormo = "4 Stormo"

        class SouthKorea(Enum):
            _4_Stormo = "4 Stormo"

        class Tunisia(Enum):
            _4_Stormo = "4 Stormo"

        class Combined_Joint_Task_Forces_Red(Enum):
            _4_Stormo = "4 Stormo"

        class Lebanon(Enum):
            _4_Stormo = "4 Stormo"

        class Portugal(Enum):
            _4_Stormo = "4 Stormo"

        class Cuba(Enum):
            _4_Stormo = "4 Stormo"

        class Insurgents(Enum):
            _4_Stormo = "4 Stormo"

        class SaudiArabia(Enum):
            _4_Stormo = "4 Stormo"

        class France(Enum):
            _4_Stormo = "4 Stormo"

        class USA(Enum):
            _4_Stormo = "4 Stormo"

        class Honduras(Enum):
            _4_Stormo = "4 Stormo"

        class Qatar(Enum):
            _4_Stormo = "4 Stormo"

        class Russia(Enum):
            _4_Stormo = "4 Stormo"

        class United_Arab_Emirates(Enum):
            _4_Stormo = "4 Stormo"

        class Italian_Social_Republi(Enum):
            _4_Stormo = "4 Stormo"

        class Austria(Enum):
            _4_Stormo = "4 Stormo"

        class Bahrain(Enum):
            _4_Stormo = "4 Stormo"

        class Italy(Enum):
            _4_Stormo = "4 Stormo"

        class Chile(Enum):
            _4_Stormo = "4 Stormo"

        class Turkey(Enum):
            _4_Stormo = "4 Stormo"

        class Philippines(Enum):
            _4_Stormo = "4 Stormo"

        class Algeria(Enum):
            _4_Stormo = "4 Stormo"

        class Pakistan(Enum):
            _4_Stormo = "4 Stormo"

        class Malaysia(Enum):
            _4_Stormo = "4 Stormo"

        class Indonesia(Enum):
            _4_Stormo = "4 Stormo"

        class Iraq(Enum):
            _4_Stormo = "4 Stormo"

        class Germany(Enum):
            _4_Stormo = "4 Stormo"

        class South_Africa(Enum):
            _4_Stormo = "4 Stormo"

        class Jordan(Enum):
            _4_Stormo = "4 Stormo"

        class Mexico(Enum):
            _4_Stormo = "4 Stormo"

        class USAFAggressors(Enum):
            _4_Stormo = "4 Stormo"

        class Brazil(Enum):
            _4_Stormo = "4 Stormo"

        class Spain(Enum):
            _4_Stormo = "4 Stormo"

        class Belarus(Enum):
            _4_Stormo = "4 Stormo"

        class Canada(Enum):
            _4_Stormo = "4 Stormo"

        class NorthKorea(Enum):
            _4_Stormo = "4 Stormo"

        class Ethiopia(Enum):
            _4_Stormo = "4 Stormo"

        class Japan(Enum):
            _4_Stormo = "4 Stormo"

        class Thailand(Enum):
            _4_Stormo = "4 Stormo"

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (2, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        VSN_F104G_L_PTB__ = (2, Weapons.VSN_F104G_L_PTB__)

    class Pylon3:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            3,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            3,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            3,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (3, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            3,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (3, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (3, Weapons.AGM_119B_Penguin_ASM)

    class Pylon4:
        AIM_7M_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            4,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            4,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            4,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            4,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (4, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            4,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP = (
            4,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP,
        )
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (4, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (4, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB__ = (4, Weapons.VSN_F104G_PTB__)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon6:
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon8:
        AIM_7M_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            8,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            8,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            8,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            8,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (8, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            8,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP = (
            8,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__HEDP,
        )
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (8, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (8, Weapons.AGM_119B_Penguin_ASM)
        VSN_F104G_PTB__ = (8, Weapons.VSN_F104G_PTB__)

    class Pylon9:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        BL_755_CBU___450kg__147_Frag_Pen_bomblets = (
            9,
            Weapons.BL_755_CBU___450kg__147_Frag_Pen_bomblets,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            9,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__ = (
            9,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk__,
        )
        B_8M1___20_S_8OFP2 = (9, Weapons.B_8M1___20_S_8OFP2)
        B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk = (
            9,
            Weapons.B_8M1_pod___20_x_S_8TsM__80mm_UnGd_Rkts__Smk,
        )
        LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM,
        )
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (9, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kormoran___ASM = (9, Weapons.Kormoran___ASM)
        AGM_119B_Penguin_ASM = (9, Weapons.AGM_119B_Penguin_ASM)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        LAU_138_AIM_9L = (10, Weapons.LAU_138_AIM_9L)
        AIM_9B_Sidewinder_IR_AAM = (10, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        VSN_F104G_R_PTB__ = (10, Weapons.VSN_F104G_R_PTB__)

    class Pylon11:
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep
