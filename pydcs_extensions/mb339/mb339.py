from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class MB_339PAN_Weapons:
    ARF8M3_TP = {"clsid": "{ARF8M3_TP}", "name": "ARF8M3 TP", "weight": None}
    BRD_4_250_4_MK_76_2_ARF_8M3TP_ = {
        "clsid": "{BRD-4-250}",
        "name": "BRD-4-250(4*MK.76+2*ARF-8M3TP)",
        "weight": 137.6,
    }
    Color_Oil_Tank = {"clsid": "{COLOR-TANK}", "name": "Color Oil Tank", "weight": 183}
    Empty_Pylon = {"clsid": "{VOID-PYLON-MB339A}", "name": "Empty Pylon", "weight": 20}
    Fuel_Tank_330lt = {
        "clsid": "{FUEL-SUBAL_TANK-330}",
        "name": "Fuel Tank 330lt",
        "weight": 315,
    }
    GunPod_AN_M3 = {"clsid": "{MB339-AN-M3_L}", "name": "GunPod AN/M3", "weight": 75}
    GunPod_AN_M3_ = {"clsid": "{MB339-AN-M3_R}", "name": "GunPod AN/M3", "weight": 75}
    GunPod_DEFA553 = {
        "clsid": "{MB339-DEFA553_L}",
        "name": "GunPod DEFA553",
        "weight": 190,
    }
    GunPod_DEFA553_ = {
        "clsid": "{MB339-DEFA553_R}",
        "name": "GunPod DEFA553",
        "weight": 190,
    }
    LAU_10___4_ZUNI_MK_71___ = {
        "clsid": "{LAU-10}",
        "name": "LAU-10 - 4 ZUNI MK 71",
        "weight": 308,
    }
    LR_25___25_ARF_8M3_API_ = {
        "clsid": "{LR-25API}",
        "name": "LR-25 - 25 ARF/8M3(API)",
        "weight": 141,
    }
    LR_25___25_ARF_8M3_HEI_ = {
        "clsid": "{LR-25HEI}",
        "name": "LR-25 - 25 ARF/8M3(HEI)",
        "weight": 161,
    }
    MAK79_2_MK_20 = {"clsid": "{MAK79_MK20 2L}", "name": "MAK79 2 MK-20", "weight": 464}
    MAK79_2_MK_20_ = {
        "clsid": "{MAK79_MK20 2R}",
        "name": "MAK79 2 MK-20",
        "weight": 464,
    }
    MAK79_MK_20 = {"clsid": "{MAK79_MK20 1R}", "name": "MAK79 MK-20", "weight": 232}
    MAK79_MK_20_ = {"clsid": "{MAK79_MK20 1L}", "name": "MAK79 MK-20", "weight": 232}
    MB339_Black_Smoke = {
        "clsid": "{SMOKE-BLACK-MB339}",
        "name": "MB339 Black Smoke",
        "weight": 1,
    }
    MB339_Green_Smoke = {
        "clsid": "{SMOKE-GREEN-MB339}",
        "name": "MB339 Green Smoke",
        "weight": 1,
    }
    MB339_ORANGE_Smoke = {
        "clsid": "{SMOKE-ORANGE-MB339}",
        "name": "MB339 ORANGE Smoke",
        "weight": 1,
    }
    MB339_Red_Smoke = {
        "clsid": "{SMOKE-RED-MB339}",
        "name": "MB339 Red Smoke",
        "weight": 1,
    }
    MB339_White_Smoke = {
        "clsid": "{SMOKE-WHITE-MB339}",
        "name": "MB339 White Smoke",
        "weight": 1,
    }
    MB339_YELLOW_Smoke = {
        "clsid": "{SMOKE-YELLOW-MB339}",
        "name": "MB339 YELLOW Smoke",
        "weight": 1,
    }
    MK76 = {"clsid": "{MK76}", "name": "MK76", "weight": 11.3}
    Tip_Fuel_Tank_500lt = {
        "clsid": "{FUEL-TIP-TANK-500-L}",
        "name": "Tip Fuel Tank 500lt",
        "weight": 471,
    }
    Tip_Fuel_Tank_500lt_ = {
        "clsid": "{FUEL-TIP-TANK-500-R}",
        "name": "Tip Fuel Tank 500lt",
        "weight": 471,
    }
    Tip_Fuel_Tank_Ellittici_320lt = {
        "clsid": "{FUEL-TIP-ELLITTIC-L}",
        "name": "Tip Fuel Tank Ellittici 320lt",
        "weight": 314.2,
    }
    Tip_Fuel_Tank_Ellittici_320lt_ = {
        "clsid": "{FUEL-TIP-ELLITTIC-R}",
        "name": "Tip Fuel Tank Ellittici 320lt",
        "weight": 314.2,
    }


inject_weapons(MB_339PAN_Weapons)


class MB_339PAN(PlaneType):
    id = "MB-339PAN"
    flyable = True
    height = 4.77
    width = 10.5
    length = 12.13
    fuel_max = 626
    max_speed = 763.2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 124

    panel_radio = {
        1: {
            "channels": {
                1: 225,
                2: 258,
                4: 270,
                8: 257,
                16: 252,
                17: 268,
                9: 253,
                18: 269,
                5: 255,
                10: 263,
                20: 269,
                11: 267,
                3: 260,
                6: 259,
                12: 254,
                13: 264,
                7: 262,
                14: 266,
                19: 268,
                15: 265,
            },
        },
        2: {
            "channels": {
                1: 225,
                2: 258,
                4: 270,
                8: 257,
                16: 252,
                17: 268,
                9: 253,
                18: 269,
                5: 255,
                10: 263,
                20: 269,
                30: 263,
                21: 225,
                11: 267,
                22: 258,
                3: 260,
                6: 259,
                12: 254,
                24: 270,
                19: 268,
                25: 255,
                13: 264,
                26: 259,
                27: 262,
                7: 262,
                14: 266,
                28: 257,
                23: 260,
                29: 253,
                15: 265,
            },
        },
    }

    property_defaults = {
        "SoloFlight": False,
        "NetCrewControlPriority": 1,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Instructor = 1
                Ask_Always = -1
                Equally_Responsible = -2

    class Liveries:
        class Georgia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Syria(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Finland(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Australia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Germany(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class SaudiArabia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Israel(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Croatia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class CzechRepublic(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Norway(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Romania(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Spain(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Ukraine(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Belgium(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Slovakia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Greece(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class UK(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Insurgents(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Hungary(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class France(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Abkhazia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Russia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Sweden(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Austria(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Switzerland(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Italy(Enum):
            MB339PAN__Frecce_Tricolori = "MB339PAN 'Frecce Tricolori'"
            MB339A__SVBIA____FACTORY = "MB339A 'SVBIA' - FACTORY"
            MB339A__61BRIGATA____CAMO = "MB339A '61BRIGATA' - CAMO"
            MB339A__61STORMO____CAMO = "MB339A '61STORMO' - CAMO"
            MB339A__61STORMO____GREY = "MB339A '61STORMO' - GREY"
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class SouthOssetia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class SouthKorea(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Iran(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class China(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Pakistan(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Belarus(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class NorthKorea(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Iraq(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Kazakhstan(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Bulgaria(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Serbia(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class India(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class USAFAggressors(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class USA(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Denmark(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Egypt(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Canada(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class TheNetherlands(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Turkey(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Japan(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

        class Poland(Enum):
            MB339AA__ARMADA____Crippa = "MB339AA 'ARMADA' - Crippa"
            MB339AA__ARMADA____Yellow_Band = "MB339AA 'ARMADA' - Yellow Band"
            MB339__Factory = "MB339 'Factory'"

    class Pylon1:
        Tip_Fuel_Tank_500lt = (1, MB_339PAN_Weapons.Tip_Fuel_Tank_500lt)
        Tip_Fuel_Tank_Ellittici_320lt = (
            1,
            MB_339PAN_Weapons.Tip_Fuel_Tank_Ellittici_320lt,
        )

    class Pylon2:
        Empty_Pylon = (2, MB_339PAN_Weapons.Empty_Pylon)
        LR_25___25_ARF_8M3_HEI_ = (2, MB_339PAN_Weapons.LR_25___25_ARF_8M3_HEI_)
        LR_25___25_ARF_8M3_API_ = (2, MB_339PAN_Weapons.LR_25___25_ARF_8M3_API_)
        Mk_82 = (2, Weapons.Mk_82)
        Matra_Type_155_Rocket_Pod = (2, Weapons.Matra_Type_155_Rocket_Pod)

    class Pylon3:
        Fuel_Tank_330lt = (3, MB_339PAN_Weapons.Fuel_Tank_330lt)
        Empty_Pylon = (3, MB_339PAN_Weapons.Empty_Pylon)
        LR_25___25_ARF_8M3_HEI_ = (3, MB_339PAN_Weapons.LR_25___25_ARF_8M3_HEI_)
        LR_25___25_ARF_8M3_API_ = (3, MB_339PAN_Weapons.LR_25___25_ARF_8M3_API_)
        Mk_82 = (3, Weapons.Mk_82)
        LAU_10___4_ZUNI_MK_71___ = (3, MB_339PAN_Weapons.LAU_10___4_ZUNI_MK_71___)
        BRD_4_250_4_MK_76_2_ARF_8M3TP_ = (
            3,
            MB_339PAN_Weapons.BRD_4_250_4_MK_76_2_ARF_8M3TP_,
        )
        Matra_Type_155_Rocket_Pod = (3, Weapons.Matra_Type_155_Rocket_Pod)

    class Pylon4:
        Color_Oil_Tank = (4, MB_339PAN_Weapons.Color_Oil_Tank)
        Empty_Pylon = (4, MB_339PAN_Weapons.Empty_Pylon)
        GunPod_AN_M3 = (4, MB_339PAN_Weapons.GunPod_AN_M3)
        GunPod_DEFA553 = (4, MB_339PAN_Weapons.GunPod_DEFA553)
        LR_25___25_ARF_8M3_HEI_ = (4, MB_339PAN_Weapons.LR_25___25_ARF_8M3_HEI_)
        LR_25___25_ARF_8M3_API_ = (4, MB_339PAN_Weapons.LR_25___25_ARF_8M3_API_)
        Mk_82 = (4, Weapons.Mk_82)
        Matra_Type_155_Rocket_Pod = (4, Weapons.Matra_Type_155_Rocket_Pod)

    class Pylon5:
        MB339_Red_Smoke = (5, MB_339PAN_Weapons.MB339_Red_Smoke)
        MB339_Green_Smoke = (5, MB_339PAN_Weapons.MB339_Green_Smoke)
        MB339_YELLOW_Smoke = (5, MB_339PAN_Weapons.MB339_YELLOW_Smoke)
        MB339_ORANGE_Smoke = (5, MB_339PAN_Weapons.MB339_ORANGE_Smoke)
        MB339_Black_Smoke = (5, MB_339PAN_Weapons.MB339_Black_Smoke)

    class Pylon6:
        MB339_White_Smoke = (6, MB_339PAN_Weapons.MB339_White_Smoke)

    class Pylon7:
        Color_Oil_Tank = (7, MB_339PAN_Weapons.Color_Oil_Tank)
        Empty_Pylon = (7, MB_339PAN_Weapons.Empty_Pylon)
        GunPod_AN_M3_ = (7, MB_339PAN_Weapons.GunPod_AN_M3_)
        GunPod_DEFA553_ = (7, MB_339PAN_Weapons.GunPod_DEFA553_)
        LR_25___25_ARF_8M3_HEI_ = (7, MB_339PAN_Weapons.LR_25___25_ARF_8M3_HEI_)
        LR_25___25_ARF_8M3_API_ = (7, MB_339PAN_Weapons.LR_25___25_ARF_8M3_API_)
        Mk_82 = (7, Weapons.Mk_82)
        Matra_Type_155_Rocket_Pod = (7, Weapons.Matra_Type_155_Rocket_Pod)

    class Pylon8:
        Fuel_Tank_330lt = (8, MB_339PAN_Weapons.Fuel_Tank_330lt)
        Empty_Pylon = (8, MB_339PAN_Weapons.Empty_Pylon)
        LR_25___25_ARF_8M3_HEI_ = (8, MB_339PAN_Weapons.LR_25___25_ARF_8M3_HEI_)
        LR_25___25_ARF_8M3_API_ = (8, MB_339PAN_Weapons.LR_25___25_ARF_8M3_API_)
        Mk_82 = (8, Weapons.Mk_82)
        LAU_10___4_ZUNI_MK_71___ = (8, MB_339PAN_Weapons.LAU_10___4_ZUNI_MK_71___)
        Matra_Type_155_Rocket_Pod = (8, Weapons.Matra_Type_155_Rocket_Pod)
        BRD_4_250_4_MK_76_2_ARF_8M3TP_ = (
            8,
            MB_339PAN_Weapons.BRD_4_250_4_MK_76_2_ARF_8M3TP_,
        )

    class Pylon9:
        Empty_Pylon = (9, MB_339PAN_Weapons.Empty_Pylon)
        LR_25___25_ARF_8M3_HEI_ = (9, MB_339PAN_Weapons.LR_25___25_ARF_8M3_HEI_)
        LR_25___25_ARF_8M3_API_ = (9, MB_339PAN_Weapons.LR_25___25_ARF_8M3_API_)
        Mk_82 = (9, Weapons.Mk_82)
        Matra_Type_155_Rocket_Pod = (9, Weapons.Matra_Type_155_Rocket_Pod)

    class Pylon10:
        Tip_Fuel_Tank_500lt_ = (10, MB_339PAN_Weapons.Tip_Fuel_Tank_500lt_)
        Tip_Fuel_Tank_Ellittici_320lt_ = (
            10,
            MB_339PAN_Weapons.Tip_Fuel_Tank_Ellittici_320lt_,
        )

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.GroundAttack,
        task.RunwayAttack,
        task.CAS,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.Nothing
