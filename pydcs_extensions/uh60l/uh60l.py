from enum import Enum
from typing import Dict, Any

from dcs import task
from dcs.helicopters import HelicopterType
from dcs.planes import PlaneType

from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsUH60L:
    CEFS_Fuel_Tank_200_gallons = {
        "clsid": "{UH60_FUEL_TANK_230}",
        "name": "CEFS Fuel Tank 200 gallons",
        "weight": 730.09478,
    }


inject_weapons(WeaponsUH60L)


class UH_60L(HelicopterType):
    id = "UH-60L"
    flyable = True
    height = 5.13
    width = 16.4
    length = 19.76
    fuel_max = 1362
    max_speed = 355.584
    chaff = 30
    flare = 0
    charge_total = 30
    chaff_charge_size = 1
    flare_charge_size = 0
    radio_frequency = 124

    panel_radio = {
        2: {
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
        3: {
            "channels": {1: 124, 2: 127.5},
        },
        1: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
        4: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
        5: {
            "channels": {1: 3, 2: 10},
        },
    }

    property_defaults: Dict[str, Any] = {
        "FuelProbeEnabled": False,
        "SoloFlight": False,
        "NetCrewControlPriority": 1,
    }

    class Properties:
        class FuelProbeEnabled:
            id = "FuelProbeEnabled"

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
        class USSR(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Georgia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Venezuela(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Australia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Israel(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Combined_Joint_Task_Forces_Blue(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Sudan(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Norway(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Romania(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Iran(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Ukraine(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Libya(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Belgium(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Slovakia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Greece(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class UK(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Third_Reich(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Hungary(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Abkhazia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Morocco(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class United_Nations_Peacekeepers(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Switzerland(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class SouthOssetia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Vietnam(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class China(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Yemen(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Kuwait(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Serbia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Oman(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class India(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Egypt(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class TheNetherlands(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Poland(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Syria(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Finland(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Kazakhstan(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Denmark(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Sweden(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Croatia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class CzechRepublic(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class GDR(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Yugoslavia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Bulgaria(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class SouthKorea(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Tunisia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Combined_Joint_Task_Forces_Red(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Lebanon(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Portugal(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Cuba(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Insurgents(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class SaudiArabia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class France(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class USA(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Honduras(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Qatar(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Russia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class United_Arab_Emirates(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Italian_Social_Republi(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Austria(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Bahrain(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Italy(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Chile(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Turkey(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Philippines(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Algeria(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Pakistan(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Malaysia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Indonesia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Iraq(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Germany(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class South_Africa(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Jordan(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Mexico(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class USAFAggressors(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Brazil(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Spain(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Belarus(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Canada(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class NorthKorea(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Ethiopia(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Japan(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

        class Thailand(Enum):
            default = "default"
            FAB = "FAB"
            Israeli_Air_Force = "Israeli Air Force"
            JASDF_SAR_Yellow = "JASDF SAR Yellow"
            Skyward = "Skyward"
            US_Army_Desert = "US Army Desert"
            US_Army_MEDEVAC = "US Army MEDEVAC"
            US_Army_SOAR = "US Army SOAR"
            US_Navy_Grey = "US Navy Grey"
            USAF_Rescue = "USAF Rescue"
            US_Coast_Guard = "US Coast Guard"
            X51 = "X51"

    class Pylon1:
        CEFS_Fuel_Tank_200_gallons = (1, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    class Pylon2:
        CEFS_Fuel_Tank_200_gallons = (2, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    class Pylon3:
        CEFS_Fuel_Tank_200_gallons = (3, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    class Pylon4:
        CEFS_Fuel_Tank_200_gallons = (4, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4}

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


class KC130J(PlaneType):
    id = "KC130J"
    group_size_max = 1
    height = 11.66
    width = 40.4
    length = 29.79
    fuel_max = 30000
    max_speed = 222.23988
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    tacan = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}

    pylons: {}

    tasks = [task.Refueling]
    task_default = task.Refueling
