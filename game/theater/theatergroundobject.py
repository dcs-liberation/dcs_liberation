from __future__ import annotations

import itertools
import logging
from typing import Iterator, List, TYPE_CHECKING

from dcs.mapping import Point
from dcs.unit import Unit
from dcs.unitgroup import Group
from dcs.triggers import TriggerZone, Triggers

from .. import db
from ..data.radar_db import UNITS_WITH_RADAR
from ..utils import Distance, meters

if TYPE_CHECKING:
    from .controlpoint import ControlPoint
    from gen.flights.flight import FlightType

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
    "EWR": "EWR",
    "bridge": "bridge",
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
    "bridge": "BRIDGE",
}

CATEGORY_MAP = {
    # Special cases
    "CARRIER": ["CARRIER"],
    "LHA": ["LHA"],
    "aa": ["AA"],
    # Buildings
    "power": [
        "Workshop A",
        "Electric power box",
        "Garage small A",
        "Farm B",
        "Repair workshop",
        "Garage B",
    ],
    "ware": ["Warehouse", "Hangar A"],
    "fuel": ["Tank", "Tank 2", "Tank 3", "Fuel tank"],
    "ammo": [".Ammunition depot", "Hangar B"],
    "farp": [
        "FARP Tent",
        "FARP Ammo Dump Coating",
        "FARP Fuel Depot",
        "FARP Command Post",
        "FARP CP Blindage",
    ],
    "fob": ["Bunker 2", "Bunker 1", "Garage small B", ".Command Center", "Barracks 2"],
    "factory": ["Tech combine", "Tech hangar A"],
    "comms": ["TV tower", "Comms tower M"],
    "oil": ["Oil platform"],
    "derrick": ["Oil derrick", "Pump station", "Subsidiary structure 2"],
    "ww2bunker": [
        "Siegfried Line",
        "Fire Control Bunker",
        "SK_C_28_naval_gun",
        "Concertina Wire",
        "Czech hedgehogs 1",
    ],
    "village": ["Small house 1B", "Small House 1A", "Small warehouse 1"],
    "allycamp": [],
}


class TheaterGroundObject(MissionTarget):
    def __init__(
        self,
        name: str,
        category: str,
        group_id: int,
        position: Point,
        heading: int,
        control_point: ControlPoint,
        dcs_identifier: str,
        airbase_group: bool,
        sea_object: bool,
    ) -> None:
        super().__init__(name, position)
        self.category = category
        self.group_id = group_id
        self.heading = heading
        self.control_point = control_point
        self.dcs_identifier = dcs_identifier
        self.airbase_group = airbase_group
        self.sea_object = sea_object
        self.groups: List[Group] = []

    @property
    def is_dead(self) -> bool:
        return self.alive_unit_count == 0

    @property
    def units(self) -> List[Unit]:
        """
        :return: all the units at this location
        """
        return list(itertools.chain.from_iterable([g.units for g in self.groups]))

    @property
    def dead_units(self) -> List[Unit]:
        """
        :return: all the dead units at this location
        """
        return list(
            itertools.chain.from_iterable(
                [getattr(g, "units_losts", []) for g in self.groups]
            )
        )

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

    def is_friendly(self, to_player: bool) -> bool:
        return self.control_point.is_friendly(to_player)

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if self.is_friendly(for_player):
            yield from [
                # TODO: FlightType.LOGISTICS
                # TODO: FlightType.TROOP_TRANSPORT
            ]
        else:
            yield from [
                FlightType.STRIKE,
                FlightType.BAI,
            ]
        yield from super().mission_types(for_player)

    @property
    def alive_unit_count(self) -> int:
        return sum(len(g.units) for g in self.groups)

    @property
    def might_have_aa(self) -> bool:
        return False

    @property
    def has_radar(self) -> bool:
        """Returns True if the ground object contains a unit with radar."""
        for group in self.groups:
            for unit in group.units:
                if db.unit_type_from_name(unit.type) in UNITS_WITH_RADAR:
                    return True
        return False

    def _max_range_of_type(self, group: Group, range_type: str) -> Distance:
        if not self.might_have_aa:
            return meters(0)

        max_range = meters(0)
        for u in group.units:
            unit = db.unit_type_from_name(u.type)
            if unit is None:
                logging.error(f"Unknown unit type {u.type}")
                continue

            # Some units in pydcs have detection_range/threat_range defined,
            # but explicitly set to None.
            unit_range = getattr(unit, range_type, None)
            if unit_range is not None:
                max_range = max(max_range, meters(unit_range))
        return max_range

    def detection_range(self, group: Group) -> Distance:
        return self._max_range_of_type(group, "detection_range")

    def threat_range(self, group: Group) -> Distance:
        if not self.detection_range(group):
            # For simple SAMs like shilkas, the unit has both a threat and
            # detection range. For complex sites like SA-2s, the launcher has a
            # threat range and the search/track radars have detection ranges. If
            # the site has no detection range it has no radars and can't fire,
            # so it's not actually a threat even if it still has launchers.
            return meters(0)
        return self._max_range_of_type(group, "threat_range")

    @property
    def is_factory(self) -> bool:
        return self.category == "factory"

    @property
    def is_control_point(self) -> bool:
        """True if this TGO is the group for the control point itself (CVs and FOBs)."""
        return False


class BuildingGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        category: str,
        group_id: int,
        object_id: int,
        position: Point,
        heading: int,
        control_point: ControlPoint,
        dcs_identifier: str,
        airbase_group=False,
    ) -> None:
        super().__init__(
            name=name,
            category=category,
            group_id=group_id,
            position=position,
            heading=heading,
            control_point=control_point,
            dcs_identifier=dcs_identifier,
            airbase_group=airbase_group,
            sea_object=False,
        )
        self.object_id = object_id
        # Other TGOs track deadness based on the number of alive units, but
        # buildings don't have groups assigned to the TGO.
        self._dead = False

    @property
    def group_name(self) -> str:
        """The name of the unit group."""
        return f"{self.category}|{self.group_id}|{self.object_id}"

    @property
    def waypoint_name(self) -> str:
        return f"{super().waypoint_name} #{self.object_id}"

    @property
    def is_dead(self) -> bool:
        if not hasattr(self, "_dead"):
            self._dead = False
        return self._dead

    def kill(self) -> None:
        self._dead = True


class SceneryGroundObject(BuildingGroundObject):
    def __init__(
        self,
        name: str,
        category: str,
        group_id: int,
        object_id: int,
        position: Point,
        control_point: ControlPoint,
        dcs_identifier: str,
        zone: TriggerZone,
    ) -> None:
        super().__init__(
            name=name,
            category=category,
            group_id=group_id,
            object_id=object_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier=dcs_identifier,
            airbase_group=False,
        )
        self.zone = zone
        try:
            # In the default TriggerZone using "assign as..." in the DCS Mission Editor,
            # property three has the scenery's object ID as its value.
            self.map_object_id = self.zone.properties[3]["value"]
        except (IndexError, KeyError):
            logging.exception(
                "Invalid TriggerZone for Scenery definition. The third property must "
                "be the map object ID."
            )
            raise


class FactoryGroundObject(BuildingGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        heading: int,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="factory",
            group_id=group_id,
            object_id=0,
            position=position,
            heading=heading,
            control_point=control_point,
            dcs_identifier="Workshop A",
            airbase_group=False,
        )


class NavalGroundObject(TheaterGroundObject):
    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.ANTISHIP
        yield from super().mission_types(for_player)

    @property
    def might_have_aa(self) -> bool:
        return True


class GenericCarrierGroundObject(NavalGroundObject):
    @property
    def is_control_point(self) -> bool:
        return True


# TODO: Why is this both a CP and a TGO?
class CarrierGroundObject(GenericCarrierGroundObject):
    def __init__(self, name: str, group_id: int, control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="CARRIER",
            group_id=group_id,
            position=control_point.position,
            heading=0,
            control_point=control_point,
            dcs_identifier="CARRIER",
            airbase_group=True,
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"


# TODO: Why is this both a CP and a TGO?
class LhaGroundObject(GenericCarrierGroundObject):
    def __init__(self, name: str, group_id: int, control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="LHA",
            group_id=group_id,
            position=control_point.position,
            heading=0,
            control_point=control_point,
            dcs_identifier="LHA",
            airbase_group=True,
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"


class MissileSiteGroundObject(TheaterGroundObject):
    def __init__(
        self, name: str, group_id: int, position: Point, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=False,
            sea_object=False,
        )


class CoastalSiteGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
        heading,
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=heading,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=False,
            sea_object=False,
        )


class BaseDefenseGroundObject(TheaterGroundObject):
    """Base type for all base defenses."""


# TODO: Differentiate types.
# This type gets used both for AA sites (SAM, AAA, or SHORAD). These should each
# be split into their own types.
class SamGroundObject(BaseDefenseGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
        for_airbase: bool,
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=for_airbase,
            sea_object=False,
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

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.DEAD
        yield from super().mission_types(for_player)

    @property
    def might_have_aa(self) -> bool:
        return True


class VehicleGroupGroundObject(BaseDefenseGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
        for_airbase: bool,
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=for_airbase,
            sea_object=False,
        )


class EwrGroundObject(BaseDefenseGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
        for_airbase: bool,
    ) -> None:
        super().__init__(
            name=name,
            category="EWR",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="EWR",
            airbase_group=for_airbase,
            sea_object=False,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them.
        return f"{self.faction_color}|{super().group_name}"

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.DEAD
        yield from super().mission_types(for_player)

    @property
    def might_have_aa(self) -> bool:
        return True


class ShipGroundObject(NavalGroundObject):
    def __init__(
        self, name: str, group_id: int, position: Point, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            airbase_group=False,
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"
