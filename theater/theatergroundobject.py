from __future__ import annotations

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
}


class TheaterGroundObject(MissionTarget):

    def __init__(self, name: str, category: str, group_id: int, object_id: int,
                 position: Point, heading: int, cp_id: int, dcs_identifier: str,
                 airbase_group: bool, sea_object: bool) -> None:
        super().__init__(name, position)
        self.category = category
        self.group_id = group_id
        self.object_id = object_id
        self.heading = heading
        self.cp_id = cp_id
        self.dcs_identifier = dcs_identifier
        self.airbase_group = airbase_group
        self.sea_object = sea_object
        self.is_dead = False
        self.groups: List[Group] = []

    @property
    def string_identifier(self):
        return "{}|{}|{}|{}".format(self.category, self.cp_id, self.group_id, self.object_id)

    @property
    def group_identifier(self) -> str:
        return "{}|{}".format(self.category, self.group_id)

    @property
    def name_abbrev(self) -> str:
        return ABBREV_NAME[self.category]

    def __str__(self) -> str:
        return NAME_BY_CATEGORY[self.category]

    def matches_string_identifier(self, identifier):
        return self.string_identifier == identifier

    @property
    def obj_name(self) -> str:
        return self.name

    def parent_control_point(self, theater: ConflictTheater) -> ControlPoint:
        """Searches the theater for the parent control point."""
        for cp in theater.controlpoints:
            if cp.id == self.cp_id:
                return cp
        raise RuntimeError("Could not find matching control point in theater")


class BuildingGroundObject(TheaterGroundObject):
    def __init__(self, name: str, category: str, group_id: int, object_id: int,
                 position: Point, heading: int, control_point: ControlPoint,
                 dcs_identifier: str) -> None:
        super().__init__(
            name=name,
            category=category,
            group_id=group_id,
            object_id=object_id,
            position=position,
            heading=heading,
            cp_id=control_point.id,
            dcs_identifier=dcs_identifier,
            airbase_group=False,
            sea_object=False
        )


# TODO: Why is this both a CP and a TGO?
class CarrierGroundObject(TheaterGroundObject):
    def __init__(self, name: str, group_id: int,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="CARRIER",
            group_id=group_id,
            object_id=0,
            position=control_point.position,
            heading=0,
            cp_id=control_point.id,
            dcs_identifier="CARRIER",
            airbase_group=True,
            sea_object=True
        )


# TODO: Why is this both a CP and a TGO?
class LhaGroundObject(TheaterGroundObject):
    def __init__(self, name: str, group_id: int,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="LHA",
            group_id=group_id,
            object_id=0,
            position=control_point.position,
            heading=0,
            cp_id=control_point.id,
            dcs_identifier="LHA",
            airbase_group=True,
            sea_object=True
        )


class MissileSiteGroundObject(TheaterGroundObject):
    def __init__(self, name: str, group_id: int, position: Point,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            object_id=0,
            position=position,
            heading=0,
            cp_id=control_point.id,
            dcs_identifier="AA",
            airbase_group=False,
            sea_object=False
        )


class SamGroundObject(TheaterGroundObject):
    def __init__(self, name: str, group_id: int, position: Point,
                 control_point: ControlPoint, for_airbase: bool) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            object_id=0,
            position=position,
            heading=0,
            cp_id=control_point.id,
            dcs_identifier="AA",
            airbase_group=for_airbase,
            sea_object=False
        )


class ShipGroundObject(TheaterGroundObject):
    def __init__(self, name: str, group_id: int, position: Point,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            object_id=0,
            position=position,
            heading=0,
            cp_id=control_point.id,
            dcs_identifier="AA",
            airbase_group=False,
            sea_object=True
        )
