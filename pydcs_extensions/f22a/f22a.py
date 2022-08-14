from typing import Any, Dict, Set

from dcs import task
from dcs.liveries_scanner import Liveries
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class F22AWeapons:
    AIM_9XX = {"clsid": "{AIM-9XX}", "name": "AIM-9XX", "weight": 85}
    AIM_120D = {"clsid": "{AIM-120D}", "name": "AIM-120D", "weight": 152}


inject_weapons(F22AWeapons)


@planemod
class F_22A(PlaneType):
    id = "F-22A"
    flyable = True
    height = 4.88
    width = 13.05
    length = 19.1
    fuel_max = 6103
    max_speed = 2649.996
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    property_defaults: Dict[str, Any] = {
        "BAY_DOOR_OPTION": False,
    }

    class Properties:
        class BAY_DOOR_OPTION:
            id = "BAY_DOOR_OPTION"

    livery_name = "F-22A"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9XX = (1, F22AWeapons.AIM_9XX)

    class Pylon2:
        Fuel_tank_610_gal = (2, Weapons.Fuel_tank_610_gal)

    class Pylon3:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            3,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_120D = (3, F22AWeapons.AIM_120D)

    class Pylon4:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            4,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_120D = (4, F22AWeapons.AIM_120D)

    class Pylon5:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            5,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_120D = (5, F22AWeapons.AIM_120D)

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)

    class Pylon7:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            7,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_120D = (7, F22AWeapons.AIM_120D)

    class Pylon8:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            8,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_120D = (8, F22AWeapons.AIM_120D)

    class Pylon9:
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            9,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        AIM_120D = (9, F22AWeapons.AIM_120D)

    class Pylon10:
        Fuel_tank_610_gal = (10, Weapons.Fuel_tank_610_gal)

    class Pylon11:
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9XX = (11, F22AWeapons.AIM_9XX)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP
