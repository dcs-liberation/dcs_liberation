# mypy can't resolve these if they're wildcard imports for some reason.

# PATCH pydcs data with MODS

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
