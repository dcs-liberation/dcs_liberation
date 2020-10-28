import uuid
from typing import List, TYPE_CHECKING

from dcs.mapping import Point
from dcs.unitgroup import Group

if TYPE_CHECKING:
    from .conflicttheater import ConflictTheater
    from .controlpoint import ControlPoint
from .missiontarget import MissionTarget

NAME_BY_CATEGORY = {
    "power": "Power plant",
    "ammo": "Ammo depot",
    "fuel": "Fuel depot",
    "aa": "AA Defense Site",
    "ware": "Warehouse",
    "farp": "FARP",
    "fob": "FOB",
    "factory": "Factory",
    "comms": "Comms. tower",
    "oil": "Oil platform",
    "derrick": "Derrick",
    "ww2bunker": "Bunker",
    "village": "Village",
    "allycamp": "Camp"
}

ABBREV_NAME = {
    "power": "PLANT",
    "ammo": "AMMO",
    "fuel": "FUEL",
    "aa": "AA",
    "ware": "WARE",
    "farp": "FARP",
    "fob": "FOB",
    "factory": "FACTORY",
    "comms": "COMMST",
    "oil": "OILP",
    "derrick": "DERK",
    "ww2bunker": "BUNK",
    "village": "VLG",
    "allycamp": "CMP",
}

CATEGORY_MAP = {

    # Special cases
    "CARRIER": ["CARRIER"],
    "LHA": ["LHA"],
    "aa": ["AA"],

    # Buildings
    "power": ["Workshop A", "Electric power box", "Garage small A", "Farm B", "Repair workshop", "Garage B"],
    "ware": ["Warehouse", "Hangar A"],
    "fuel": ["Tank", "Tank 2", "Tank 3", "Fuel tank"],
    "ammo": [".Ammunition depot", "Hangar B"],
    "farp": ["FARP Tent", "FARP Ammo Dump Coating", "FARP Fuel Depot", "FARP Command Post", "FARP CP Blindage"],
    "fob": ["Bunker 2", "Bunker 1", "Garage small B", ".Command Center", "Barracks 2"],
    "factory": ["Tech combine", "Tech hangar A"],
    "comms": ["TV tower", "Comms tower M"],
    "oil": ["Oil platform"],
    "derrick": ["Oil derrick", "Pump station", "Subsidiary structure 2"],
    "ww2bunker": ["Siegfried Line", "Fire Control Bunker", "SK_C_28_naval_gun", "Concertina Wire", "Czech hedgehogs 1"],
    "village": ["Small house 1B", "Small House 1A", "Small warehouse 1"],
    "allycamp": [],
    "iads-commnode": [], # I don't think the list of objects (value of the key in this dict) is ever used...
    "iads-controlcenter": [], # I don't think the list of objects (value of the key in this dict) is ever used...
    "iads-ewr": [], # I don't think the list of objects (value of the key in this dict) is ever used...
    "iads-power": [], # I don't think the list of objects (value of the key in this dict) is ever used...
}


class TheaterGroundObject(MissionTarget):
    cp_id = 0
    group_id = 0
    object_id = 0
    dcs_identifier = None  # type: str
    is_dead = False
    airbase_group = False
    heading = 0
    position = None  # type: Point
    groups: List[Group] = []
    obj_name = ""
    sea_object = False
    uuid = uuid.uuid1()

    def __init__(self, category: str):
        self.category = category

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

    @property
    def name(self) -> str:
        return self.obj_name

    def parent_control_point(
            self, theater: "ConflictTheater") -> "ControlPoint":
        """Searches the theater for the parent control point."""
        for cp in theater.controlpoints:
            if cp.id == self.cp_id:
                return cp
        raise RuntimeError("Could not find matching control point in theater")
