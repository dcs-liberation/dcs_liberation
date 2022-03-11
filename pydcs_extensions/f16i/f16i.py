from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF16I:
    AN_AAQ_13_LANTIRN = {
        "clsid": "{LANTIRNF16I}",
        "name": "AN/AAQ-13 LANTIRN",
        "weight": 204,
    }
    Fuel_tank_600_gal = {
        "clsid": "{600gal_LAHAK}",
        "name": "Fuel tank 600 gal",
        "weight": 2015.0357515,
    }
    Fuel_tank_600_gal__CFT_225_gal = {
        "clsid": "{CFT_600_R_LAHAK}",
        "name": "Fuel tank 600 gal + CFT 225 gal",
        "weight": 2050.5357515,
    }
    Fuel_tank_600_gal__CFT_225_gal_ = {
        "clsid": "{CFT_600_L_LAHAK}",
        "name": "Fuel tank 600 gal + CFT 225 gal",
        "weight": 2050.5357515,
    }
    LAU_7_with_2_x_Python_5_Sidewinder_IR_AAM = {
        "clsid": "{F4-2-AIM9L}",
        "name": "LAU-7 with 2 x Python 5 Sidewinder IR AAM",
        "weight": 200.8,
    }
    Left_Conformal_fuel_tank_225_gal = {
        "clsid": "{CFT_L_LAHAK}",
        "name": "Left Conformal fuel tank 225 gal",
        "weight": 703.1733636,
    }
    Left_Fuel_tank_370_gal__CFT_225_gal = {
        "clsid": "{CFT_370_L_LAHAK}",
        "name": "Left Fuel tank 370 gal + CFT 225 gal",
        "weight": 1989.8845750252,
    }
    Python_5_Sidewinder_IR_AAM = {
        "clsid": "{AIM-9L}",
        "name": "Python 5 Sidewinder IR AAM",
        "weight": 85.4,
    }
    Right_Conformal_fuel_tank_225_gal = {
        "clsid": "{CFT_R_LAHAK}",
        "name": "Right Conformal fuel tank 225 gal",
        "weight": 703.1733636,
    }
    Right_Fuel_tank_370_gal__CFT_225_gal = {
        "clsid": "{CFT_370_R_LAHAK}",
        "name": "Right Fuel tank 370 gal + CFT 225 gal",
        "weight": 1989.8845750252,
    }


inject_weapons(WeaponsF16I)


@planemod
class F_16I(PlaneType):
    id = "F-16I"
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
                15: 263,
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
                15: 134,
            },
        },
    }

    property_defaults = {
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
        class USSR(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Georgia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Venezuela(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Australia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Israel(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Combined_Joint_Task_Forces_Blue(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Sudan(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Norway(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Romania(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Iran(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Ukraine(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Libya(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Belgium(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Slovakia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Greece(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class UK(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Third_Reich(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Hungary(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Abkhazia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Morocco(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class United_Nations_Peacekeepers(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Switzerland(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class SouthOssetia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Vietnam(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class China(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Yemen(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Kuwait(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Serbia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Oman(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class India(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Egypt(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class TheNetherlands(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Poland(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Syria(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Finland(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Kazakhstan(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Denmark(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Sweden(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Croatia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class CzechRepublic(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class GDR(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Yugoslavia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Bulgaria(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class SouthKorea(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Tunisia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Combined_Joint_Task_Forces_Red(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Lebanon(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Portugal(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Cuba(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Insurgents(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class SaudiArabia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class France(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class USA(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Honduras(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Qatar(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Russia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class United_Arab_Emirates(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Italian_Social_Republi(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Austria(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Bahrain(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Italy(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Chile(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Turkey(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Philippines(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Algeria(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Pakistan(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Malaysia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Indonesia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Iraq(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Germany(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class South_Africa(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Jordan(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Mexico(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class USAFAggressors(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Brazil(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Spain(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Belarus(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Canada(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class NorthKorea(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Ethiopia(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Japan(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

        class Thailand(Enum):
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Python_5_Sidewinder_IR_AAM = (1, WeaponsF16I.Python_5_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (1, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            1,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Python_5_Sidewinder_IR_AAM = (2, WeaponsF16I.Python_5_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (2, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            2,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Python_5_Sidewinder_IR_AAM = (3, WeaponsF16I.Python_5_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            3,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Right_Conformal_fuel_tank_225_gal = (
            4,
            WeaponsF16I.Right_Conformal_fuel_tank_225_gal,
        )
        Right_Fuel_tank_370_gal__CFT_225_gal = (
            4,
            WeaponsF16I.Right_Fuel_tank_370_gal__CFT_225_gal,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )

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
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        Left_Conformal_fuel_tank_225_gal = (
            6,
            WeaponsF16I.Left_Conformal_fuel_tank_225_gal,
        )
        Left_Fuel_tank_370_gal__CFT_225_gal = (
            6,
            WeaponsF16I.Left_Fuel_tank_370_gal__CFT_225_gal,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Python_5_Sidewinder_IR_AAM = (7, WeaponsF16I.Python_5_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            7,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Python_5_Sidewinder_IR_AAM = (8, WeaponsF16I.Python_5_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            8,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        Python_5_Sidewinder_IR_AAM = (9, WeaponsF16I.Python_5_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (9, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            9,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon10:
        AN_AAQ_13_LANTIRN = (10, WeaponsF16I.AN_AAQ_13_LANTIRN)

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

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
