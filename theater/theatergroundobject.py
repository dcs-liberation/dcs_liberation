from __future__ import annotations

import itertools
from typing import List, TYPE_CHECKING

from dcs.mapping import Point
from dcs.unit import Unit
from dcs.unitgroup import Group

if TYPE_CHECKING:
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
    "allycamp": "Camp",
    "EWR":"EWR",
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

    def __init__(self, name: str, category: str, group_id: int, position: Point,
                 heading: int, control_point: ControlPoint, dcs_identifier: str,
                 airbase_group: bool, sea_object: bool) -> None:
        super().__init__(name, position)
        self.category = category
        self.group_id = group_id
        self.heading = heading
        self.control_point = control_point
        self.dcs_identifier = dcs_identifier
        self.airbase_group = airbase_group
        self.sea_object = sea_object
        self.is_dead = False
        # TODO: There is never more than one group.
        self.groups: List[Group] = []

    @property
    def units(self) -> List[Unit]:
        """
        :return: all the units at this location
        """
        return list(itertools.chain.from_iterable([g.units for g in self.groups]))

    @property
    def group_name(self) -> str:
        """The name of the unit group."""
        return f"{self.category}|{self.group_id}"

    @property
    def waypoint_name(self) -> str:
        return f"[{self.name}] {self.category}"

    def __str__(self) -> str:
        return NAME_BY_CATEGORY[self.category]

    def is_same_group(self, identifier: str) -> bool:
        return self.group_id == identifier

    @property
    def obj_name(self) -> str:
        return self.name

    @property
    def faction_color(self) -> str:
        return "BLUE" if self.control_point.captured else "RED"


class BuildingGroundObject(TheaterGroundObject):
    def __init__(self, name: str, category: str, group_id: int, object_id: int,
                 position: Point, heading: int, control_point: ControlPoint,
                 dcs_identifier: str) -> None:
        super().__init__(
            name=name,
            category=category,
            group_id=group_id,
            position=position,
            heading=heading,
            control_point=control_point,
            dcs_identifier=dcs_identifier,
            airbase_group=False,
            sea_object=False
        )
        self.object_id = object_id

    @property
    def group_name(self) -> str:
        """The name of the unit group."""
        return f"{self.category}|{self.group_id}|{self.object_id}"

    @property
    def waypoint_name(self) -> str:
        return f"{super().waypoint_name} #{self.object_id}"


class GenericCarrierGroundObject(TheaterGroundObject):
    pass


# TODO: Why is this both a CP and a TGO?
class CarrierGroundObject(GenericCarrierGroundObject):
    def __init__(self, name: str, group_id: int,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="CARRIER",
            group_id=group_id,
            position=control_point.position,
            heading=0,
            control_point=control_point,
            dcs_identifier="CARRIER",
            airbase_group=True,
            sea_object=True
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"


# TODO: Why is this both a CP and a TGO?
class LhaGroundObject(GenericCarrierGroundObject):
    def __init__(self, name: str, group_id: int,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="LHA",
            group_id=group_id,
            position=control_point.position,
            heading=0,
            control_point=control_point,
            dcs_identifier="LHA",
            airbase_group=True,
            sea_object=True
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"


class MissileSiteGroundObject(TheaterGroundObject):
    def __init__(self, name: str, group_id: int, position: Point,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=False,
            sea_object=False
        )


class BaseDefenseGroundObject(TheaterGroundObject):
    """Base type for all base defenses."""


# TODO: Differentiate types.
# This type gets used both for AA sites (SAM, AAA, or SHORAD) but also for the
# armor garrisons at airbases. These should each be split into their own types.
class SamGroundObject(BaseDefenseGroundObject):
    def __init__(self, name: str, group_id: int, position: Point,
                 control_point: ControlPoint, for_airbase: bool) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=for_airbase,
            sea_object=False
        )
        # Set by the SAM unit generator if the generated group is compatible
        # with Skynet.
        self.skynet_capable = False

    @property
    def group_name(self) -> str:
        if self.skynet_capable:
            # Prefix the group names of SAM sites with the side color so Skynet
            # can find them.
            return f"{self.faction_color}|SAM|{self.group_id}"
        else:
            return super().group_name


class EwrGroundObject(BaseDefenseGroundObject):
    def __init__(self, name: str, group_id: int, position: Point,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="EWR",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="EWR",
            airbase_group=True,
            sea_object=False
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them.
        return f"{self.faction_color}|{super().group_name}"


class ShipGroundObject(TheaterGroundObject):
    def __init__(self, name: str, group_id: int, position: Point,
                 control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=False,
            sea_object=True
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"
