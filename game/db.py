from datetime import datetime
from enum import Enum
from typing import Optional, Type

from dcs.countries import country_dict
from dcs.helicopters import (
    helicopter_map,
)

# mypy can't resolve these if they're wildcard imports for some reason.
from dcs.planes import (
    plane_map,
)
from dcs.ships import (
    CVN_71,
    CVN_72,
    CVN_73,
    CVN_75,
    CV_1143_5,
    KUZNECOW,
    Stennis,
    ship_map,
)
from dcs.unittype import ShipType, UnitType
from dcs.vehicles import (
    vehicle_map,
)

# PATCH pydcs data with MODS
from game.factions.faction_loader import FactionLoader

"""
---------- BEGINNING OF CONFIGURATION SECTION
"""

"""
All aircraft names in this file should correspond with naming provided in following files:

* https://github.com/pydcs/dcs/blob/master/dcs/planes.py - for planes
* https://github.com/pydcs/dcs/blob/master/dcs/helicopters.py - for helicopters
* https://github.com/pydcs/dcs/blob/master/dcs/vehicles.py - for vehicles (this include all of the ground vehicles)

You can find names at the bottom of the file in following format:

x_map = {
    "Name of the unit in game": Identifier,
}

from this example `Identifier` should be used (which may or may not include category of the unit and dot + underscore characters).
For example, player accessible Hornet is called `FA_18C_hornet`, and MANPAD Igla is called `AirDefence.MANPADS_SA_18_Igla_S_Grouse`
"""

# This should probably be much higher, but the AI doesn't rollover their budget
# and isn't smart enough to save to repair a critical runway anyway, so it has
# to be cheap enough to repair with a single turn's income.
RUNWAY_REPAIR_COST = 100

"""
Units separated by country. 
country : DCS Country name
"""
FACTIONS = FactionLoader()

"""
Possible time periods for new games

    `Name`: daytime(day, month, year),

`Identifier` is the name that will appear in the menu
The object is a python datetime object
"""
TIME_PERIODS = {
    "WW2 - Winter [1944]": datetime(1944, 1, 1),
    "WW2 - Spring [1944]": datetime(1944, 4, 1),
    "WW2 - Summer [1944]": datetime(1944, 6, 1),
    "WW2 - Fall [1944]": datetime(1944, 10, 1),
    "Early Cold War - Winter [1952]": datetime(1952, 1, 1),
    "Early Cold War - Spring [1952]": datetime(1952, 4, 1),
    "Early Cold War - Summer [1952]": datetime(1952, 6, 1),
    "Early Cold War - Fall [1952]": datetime(1952, 10, 1),
    "Cold War - Winter [1970]": datetime(1970, 1, 1),
    "Cold War - Spring [1970]": datetime(1970, 4, 1),
    "Cold War - Summer [1970]": datetime(1970, 6, 1),
    "Cold War - Fall [1970]": datetime(1970, 10, 1),
    "Late Cold War - Winter [1985]": datetime(1985, 1, 1),
    "Late Cold War - Spring [1985]": datetime(1985, 4, 1),
    "Late Cold War - Summer [1985]": datetime(1985, 6, 1),
    "Late Cold War - Fall [1985]": datetime(1985, 10, 1),
    "Gulf War - Winter [1990]": datetime(1990, 1, 1),
    "Gulf War - Spring [1990]": datetime(1990, 4, 1),
    "Gulf War - Summer [1990]": datetime(1990, 6, 1),
    "Mid-90s - Winter [1995]": datetime(1995, 1, 1),
    "Mid-90s - Spring [1995]": datetime(1995, 4, 1),
    "Mid-90s - Summer [1995]": datetime(1995, 6, 1),
    "Mid-90s - Fall [1995]": datetime(1995, 10, 1),
    "Gulf War - Fall [1990]": datetime(1990, 10, 1),
    "Modern - Winter [2010]": datetime(2010, 1, 1),
    "Modern - Spring [2010]": datetime(2010, 4, 1),
    "Modern - Summer [2010]": datetime(2010, 6, 1),
    "Modern - Fall [2010]": datetime(2010, 10, 1),
    "Georgian War [2008]": datetime(2008, 8, 7),
    "Syrian War [2011]": datetime(2011, 3, 15),
    "6 days war [1967]": datetime(1967, 6, 5),
    "Yom Kippour War [1973]": datetime(1973, 10, 6),
    "First Lebanon War [1982]": datetime(1982, 6, 6),
    "Arab-Israeli War [1948]": datetime(1948, 5, 15),
}

REWARDS = {
    "power": 4,
    "warehouse": 2,
    "ware": 2,
    "fuel": 2,
    "ammo": 2,
    "farp": 1,
    # TODO: Should generate no cash once they generate units.
    # https://github.com/dcs-liberation/dcs_liberation/issues/1036
    "factory": 10,
    "comms": 10,
    "oil": 10,
    "derrick": 8,
    "village": 0.25,
    "allycamp": 0.5,
}

"""
---------- END OF CONFIGURATION SECTION
"""


def upgrade_to_supercarrier(unit: Type[ShipType], name: str) -> Type[ShipType]:
    if unit == Stennis:
        if name == "CVN-71 Theodore Roosevelt":
            return CVN_71
        elif name == "CVN-72 Abraham Lincoln":
            return CVN_72
        elif name == "CVN-73 George Washington":
            return CVN_73
        elif name == "CVN-75 Harry S. Truman":
            return CVN_75
        elif name == "Carrier Strike Group 8":
            return CVN_75
        else:
            return CVN_71
    elif unit == KUZNECOW:
        return CV_1143_5
    else:
        return unit


def unit_type_from_name(name: str) -> Optional[Type[UnitType]]:
    if name in vehicle_map:
        return vehicle_map[name]
    elif name in plane_map:
        return plane_map[name]
    elif name in ship_map:
        return ship_map[name]
    if name in helicopter_map:
        return helicopter_map[name]
    else:
        return None


def country_id_from_name(name: str) -> int:
    for k, v in country_dict.items():
        if v.name == name:
            return k
    return -1


class DefaultLiveries:
    class Default(Enum):
        af_standard = ""
