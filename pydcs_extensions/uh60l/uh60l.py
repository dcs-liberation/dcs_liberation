from typing import Any, Dict, Set

from dcs import task
from dcs.helicopters import HelicopterType
from dcs.liveries_scanner import Liveries
from dcs.planes import PlaneType

from game.modsupport import helicoptermod, planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsUH60L:
    CEFS_Fuel_Tank_200_gallons = {
        "clsid": "{UH60_FUEL_TANK_230}",
        "name": "CEFS Fuel Tank 200 gallons",
        "weight": 730.09478,
    }
    Cargo_Seats__Rear_Row_ = {
        "clsid": "{UH60_SEAT_CARGO_REAR}",
        "name": "Cargo Seats (Rear Row)",
        "weight": 300,
    }
    Cargo_Seats__Three_Rows_ = {
        "clsid": "{UH60_SEAT_CARGO_ALL}",
        "name": "Cargo Seats (Three Rows)",
        "weight": 900,
    }
    Left_Gunner_Seat = {
        "clsid": "{UH60_SEAT_GUNNER_L}",
        "name": "Left Gunner Seat",
        "weight": 100,
    }
    Right_Gunner_Seat = {
        "clsid": "{UH60_SEAT_GUNNER_R}",
        "name": "Right Gunner Seat",
        "weight": 100,
    }


inject_weapons(WeaponsUH60L)


@helicoptermod
class UH_60L(HelicopterType):
    id = "UH-60L"
    flyable = True
    height = 5.13
    width = 16.4
    length = 19.76
    fuel_max = 1362
    max_speed = 355.584
    chaff = 30
    flare = 60
    charge_total = 90
    chaff_charge_size = 1
    flare_charge_size = 1
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
        "NetCrewControlPriority": 1,
    }

    class Properties:
        class FuelProbeEnabled:
            id = "FuelProbeEnabled"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Instructor = 1
                Ask_Always = -1
                Equally_Responsible = -2

    livery_name = "UH-60L"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        CEFS_Fuel_Tank_200_gallons = (1, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    class Pylon2:
        CEFS_Fuel_Tank_200_gallons = (2, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    class Pylon3:
        Left_Gunner_Seat = (3, WeaponsUH60L.Left_Gunner_Seat)

    class Pylon4:
        Cargo_Seats__Rear_Row_ = (4, WeaponsUH60L.Cargo_Seats__Rear_Row_)
        Cargo_Seats__Three_Rows_ = (4, WeaponsUH60L.Cargo_Seats__Three_Rows_)

    class Pylon5:
        Right_Gunner_Seat = (5, WeaponsUH60L.Right_Gunner_Seat)

    class Pylon6:
        CEFS_Fuel_Tank_200_gallons = (6, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    class Pylon7:
        CEFS_Fuel_Tank_200_gallons = (7, WeaponsUH60L.CEFS_Fuel_Tank_200_gallons)

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7}

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


@planemod
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

    livery_name = "KC130J"  # from type
    Liveries = Liveries()[livery_name]

    pylons: Set[int] = set()

    tasks = [task.Refueling]
    task_default = task.Refueling
