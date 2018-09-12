import typing

from dcs.mapping import Point

NAME_BY_CATEGORY = {
    "power": "Power plant",
    "ammo": "Ammo depot",
    "fuel": "Fuel depot",
    "aa": "AA Defense Site",
    "warehouse": "Warehouse",
    "farp": "FARP",
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
    "comms": "COMMST",
    "oil": "OILP"
}


CATEGORY_MAP = {
    "aa": ["AA"],
    "power": ["Workshop A"],
    "warehouse": ["Warehouse"],
    "fuel": ["Tank"],
    "ammo": [".Ammunition depot"],
    "farp": ["FARP Tent"],
    "comms": ["TV tower", "Comms tower"],
    "oil": ["Oil platform"],
}


class TheaterGroundObject:
    cp_id = 0
    group_id = 0
    object_id = 0

    dcs_identifier = None  # type: str
    is_dead = False

    heading = 0
    position = None  # type: Point

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
