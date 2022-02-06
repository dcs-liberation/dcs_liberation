from enum import Enum
from typing import Dict, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class a_29bWeapons:
    White_Smoke_ = {
        "clsid": "{SMOKE-WHITE-A29B}",
        "name": "White Smoke",
        "weight": 1,
    }
    Red_Smoke_ = {
        "clsid": "{SMOKE-RED-A29B}",
        "name": "Red Smoke",
        "weight": 1,
    }
    Green_Smoke_ = {
        "clsid": "{SMOKE-GREEN-A29B}",
        "name": "Green Smoke",
        "weight": 1,
    }
    Black_Smoke_ = {
        "clsid": "{SMOKE-BLACK-A29B}",
        "name": "Black Smoke",
        "weight": 1,
    }
    Orange_Smoke_ = {
        "clsid": "{SMOKE-ORANGE-A29B}",
        "name": "Black Smoke",
        "weight": 1,
    }
    Yellow_Smoke_ = {
        "clsid": "{SMOKE-YELLOW-A29B}",
        "name": "Yellow Smoke",
        "weight": 1,
    }    
    A_29B_TANK = {
        "clsid": "{A-29B TANK}",
        "name": "A-29B TANK)",
        "weight": 271.0,
    }

inject_weapons(a_29bWeapons)

class A_29B(PlaneType):
    id = "A-29B"
    flyable = True
    height = 3.974
    width = 11.135
    length = 11.332
    fuel_max = 495
    max_speed = 388.88888888889
    chaff = 30
    flare = 30
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  #{78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
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
                15: 265
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
                15: 265
            },
        },
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 1,
        "LGB1000": 1,
        "LGB100": 6,
        "LGB10": 8,
        "LGB1": 8,
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

        class LGB1000:
            id = "LGB1000"

        class LGB100:
            id = "LGB100"

        class LGB10:
            id = "LGB10"

        class LGB1:
            id = "LGB1"

    class Liveries:

        class USSR(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Georgia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Venezuela(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Australia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Israel(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Combined_Joint_Task_Forces_Blue(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USAFAFSOC = "USAFAFSOC"
            USMNSAWC = "USMNSAWC"

        class Sudan(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Norway(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Romania(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Iran(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Ukraine(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Libya(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Belgium(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Slovakia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Greece(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class UK(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Third_Reich(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Hungary(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Abkhazia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Morocco(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class United_Nations_Peacekeepers(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Switzerland(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class SouthOssetia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Vietnam(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class China(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Yemen(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Kuwait(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Serbia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Oman(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class India(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Egypt(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class TheNetherlands(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Poland(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Syria(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Finland(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Kazakhstan(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Denmark(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Sweden(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Croatia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class CzechRepublic(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class GDR(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Yugoslavia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Bulgaria(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class SouthKorea(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Tunisia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Combined_Joint_Task_Forces_Red(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USAFAFSOC = "USAFAFSOC"
            USMNSAWC = "USMNSAWC"

        class Lebanon(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Portugal(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Cuba(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Insurgents(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class SaudiArabia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class France(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class USA(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USAFAFSOC = "USAFAFSOC"
            USMNSAWC = "USMNSAWC"

        class Honduras(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Qatar(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Russia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class United_Arab_Emirates(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Italian_Social_Republi(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Austria(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Bahrain(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Italy(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Chile(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Turkey(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Philippines(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Algeria(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Pakistan(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Malaysia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Indonesia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Iraq(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Germany(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class South_Africa(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Jordan(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Mexico(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class USAFAggressors(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Brazil(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USAFAFSOC = "USAFAFSOC"
            USMNSAWC = "USMNSAWC"

        class Spain(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Belarus(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Canada(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class NorthKorea(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Ethiopia(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Japan(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

        class Thailand(Enum):
            ARGENTINA_3ra_Br = "ARGENTINA 3ra Br"
            ARGENTINA_EAM = "ARGENTINA EAM"
            ARGENTINA_EAM_Gray = "ARGENTINA EAM Gray"
            EDA = "EDA"
            ARGENTINA_9na_Br_Desert = "ARGENTINA 9na Br Desert"
            ARGENTINA_EAM_Fake_Texan = "ARGENTINA EAM Fake Texan"
            FAB = "FAB"
            ISRAEL = "ISRAEL"
            USAF = "USAF"
            USMNSAWC = "USMNSAWC"

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1, Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets
            )
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        M117___750lb_GP_Bomb_LD = (1, Weapons.M117___750lb_GP_Bomb_LD)
        GBU_12___500lb_Laser_Guided_Bomb = (1, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            1, 
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (1, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            1, 
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (1, Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (1, Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE)

    class Pylon2:
        A_29B_TANK = (2, Weapons.A_29B_TANK)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (2, Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets)
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (2, Weapons.GBU_16___1000lb_Laser_Guided_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (2, Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos)
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (2, Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (2, Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE)

    class Pylon3:
        A_29B_TANK = (3, Weapons.A_29B_TANK)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (3, Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets)
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        M117___750lb_GP_Bomb_LD = (3, Weapons.M117___750lb_GP_Bomb_LD)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (3, Weapons.GBU_16___1000lb_Laser_Guided_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon4:
        A_29B_TANK = (4, Weapons.A_29B_TANK)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (4, Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets)
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (4, Weapons.GBU_16___1000lb_Laser_Guided_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (4, Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos)
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (4, Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (4, Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (5, Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets)
        Mk_81___250lb_GP_Bomb_LD = (5, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (5, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        M117___750lb_GP_Bomb_LD = (5, Weapons.M117___750lb_GP_Bomb_LD)
        GBU_12___500lb_Laser_Guided_Bomb = (5, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (5, Weapons.GBU_16___1000lb_Laser_Guided_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (5, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (5, Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos)
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (5, Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (5, Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE)
    
    class Pylon6:
        White_Smoke_ = (6, Weapons.White_Smoke_)
        Red_Smoke_ = (6, Weapons.Red_Smoke_)
        Green_Smoke_ = (6, Weapons.Green_Smoke_)
        Black_Smoke_ = (6, Weapons.Black_Smoke_)
        Orange_Smoke_ = (6, Weapons.Orange_Smoke_)
        Yellow_Smoke_ = (6, Weapons.Yellow_Smoke_)



    pylons = {1, 2, 3, 4, 5, 6}

    tasks = [task.CAP, task.Escort, task.FighterSweep, task.GroundAttack, task.PinpointStrike, task.CAS, task.AFAC, task.RunwayAttack, task.AntishipStrike, task.Intercept]
    task_default = task.CAS

