import inspect

import dcs

REQUIRED_BUILDINGS = [
    "ammo",
    "factory",
    "fob",
    "oil",
]

IADS_BUILDINGS = [
    "comms",
    "power",
    "commandcenter",
]

DEFAULT_AVAILABLE_BUILDINGS = [
    "fuel",
    "ware",
    "farp",
    "derrick",
]

WW2_FREE = ["fuel", "ware"]
WW2_GERMANY_BUILDINGS = [
    "fuel",
    "ww2bunker",
    "ww2bunker",
    "ww2bunker",
    "allycamp",
    "allycamp",
]
WW2_ALLIES_BUILDINGS = [
    "fuel",
    "allycamp",
    "allycamp",
    "allycamp",
    "allycamp",
    "allycamp",
]

FORTIFICATION_BUILDINGS = [
    "Siegfried Line",
    "Concertina wire",
    "Concertina Wire",
    "Czech hedgehogs 1",
    "Czech hedgehogs 2",
    "Dragonteeth 1",
    "Dragonteeth 2",
    "Dragonteeth 3",
    "Dragonteeth 4",
    "Dragonteeth 5",
    "Haystack 1",
    "Haystack 2",
    "Haystack 3",
    "Haystack 4",
    "Hemmkurvenvenhindernis",
    "Log posts 1",
    "Log posts 2",
    "Log posts 3",
    "Log ramps 1",
    "Log ramps 2",
    "Log ramps 3",
    "Belgian Gate",
    "Container white",
]

FORTIFICATION_UNITS = [
    c for c in vars(dcs.vehicles.Fortification).values() if inspect.isclass(c)
]
FORTIFICATION_UNITS_ID = [
    c.id for c in vars(dcs.vehicles.Fortification).values() if inspect.isclass(c)
]
