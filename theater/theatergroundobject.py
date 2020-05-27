import typing

from dcs.mapping import Point
from dcs.statics import *

NAME_BY_CATEGORY = {
    "power": "Power plant",
    "ammo": "Ammo depot",
    "fuel": "Fuel depot",
    "aa": "AA Defense Site",
    "warehouse": "Warehouse",
    "farp": "FARP",
    "fob": "FOB",
    "factory": "Factory",
    "comms": "Comms. tower",
    "oil": "Oil platform"
}

ABBREV_NAME = {
    "power": "PLANT",
    "ammo": "AMMO",
    "fuel": "FUEL",
    "aa": "AA",
    "warehouse": "WARE",
    "farp": "FARP",
    "fob": "FOB",
    "factory": "FACTORY",
    "comms": "COMMST",
    "oil": "OILP"
}

CATEGORY_MAP = {
    "CARRIER": ["CARRIER"],
    "LHA": ["LHA"],
    "aa": ["AA"],
    "power": ["Workshop A", "Electric power box", "Garage small A"],
    "warehouse": ["Warehouse", "Hangar A"],
    "fuel": ["Tank", "Tank 2", "Tank 3", "Fuel tank"],
    "ammo": [".Ammunition depot", "Hangar B"],
    "farp": ["FARP Tent", "FARP Ammo Dump Coating", "FARP Fuel Depot", "FARP Command Post", "FARP CP Blindage"],
    "fob": ["Bunker 2", "Bunker 1", "Garage small B", ".Command Center", "Barracks 2"],
    "factory": ["Tech combine", "Tech hangar A"],
    "comms": ["TV tower", "Comms tower M"],
    "oil": ["Oil platform"],
}


class TheaterGroundObject:
    cp_id = 0
    group_id = 0
    object_id = 0

    dcs_identifier = None  # type: str
    is_dead = False
    airbase_group = False

    heading = 0
    position = None  # type: Point

    groups = []

    @property
    def category(self) -> str:
        for k, v in CATEGORY_MAP.items():
            if self.dcs_identifier in v:
                return k
        assert False, "Identifier not found in mapping: {}".format(self.dcs_identifier)

    @property
    def string_identifier(self):
        return "{}|{}|{}|{}".format(self.category, self.cp_id, self.group_id, self.object_id)

    @property
    def group_identifier(self) -> str:
        return "{}|{}".format(self.category, self.group_id)

    @property
    def name_abbrev(self) -> str:
        return ABBREV_NAME[self.category]

    def __str__(self):
        return NAME_BY_CATEGORY[self.category]

    def matches_string_identifier(self, id):
        return self.string_identifier == id
