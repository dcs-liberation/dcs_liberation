from __future__ import annotations

import itertools
import logging
from abc import ABC
from collections.abc import Sequence
from typing import Generic, Iterator, List, TYPE_CHECKING, TypeVar, Union

from dcs.mapping import Point
from dcs.triggers import TriggerZone
from dcs.unit import Unit
from dcs.unitgroup import ShipGroup, VehicleGroup

from .. import db
from ..data.radar_db import LAUNCHER_TRACKER_PAIRS, TELARS, TRACK_RADARS
from ..utils import Distance, Heading, meters

if TYPE_CHECKING:
    from .controlpoint import ControlPoint
    from ..ato.flighttype import FlightType

from .missiontarget import MissionTarget

NAME_BY_CATEGORY = {
    "ewr": "Early Warning Radar",
    "aa": "AA Defense Site",
    "allycamp": "Camp",
    "ammo": "Ammo depot",
    "armor": "Armor group",
    "coastal": "Coastal defense",
    "comms": "Communications tower",
    "derrick": "Derrick",
    "factory": "Factory",
    "farp": "FARP",
    "fob": "FOB",
    "fuel": "Fuel depot",
    "missile": "Missile site",
    "oil": "Oil platform",
    "power": "Power plant",
    "ship": "Ship",
    "village": "Village",
    "ware": "Warehouse",
    "ww2bunker": "Bunker",
}


GroupT = TypeVar("GroupT", ShipGroup, VehicleGroup)


class TheaterGroundObject(MissionTarget, Generic[GroupT]):
    def __init__(
        self,
        name: str,
        category: str,
        group_id: int,
        position: Point,
        heading: Heading,
        control_point: ControlPoint,
        dcs_identifier: str,
        sea_object: bool,
    ) -> None:
        super().__init__(name, position)
        self.category = category
        self.group_id = group_id
        self.heading = heading
        self.control_point = control_point
        self.dcs_identifier = dcs_identifier
        self.sea_object = sea_object
        self.groups: List[GroupT] = []

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
        from game.ato import FlightType

        if self.is_friendly(for_player):
            yield from [
                # TODO: FlightType.LOGISTICS
                # TODO: FlightType.TROOP_TRANSPORT
            ]
        else:
            yield from [
                FlightType.STRIKE,
                FlightType.BAI,
                FlightType.REFUELING,
            ]
        yield from super().mission_types(for_player)

    @property
    def alive_unit_count(self) -> int:
        return sum(len(g.units) for g in self.groups)

    @property
    def might_have_aa(self) -> bool:
        return False

    @property
    def has_live_radar_sam(self) -> bool:
        """Returns True if the ground object contains a unit with working radar SAM."""
        for group in self.groups:
            if self.threat_range(group, radar_only=True):
                return True
        return False

    def _max_range_of_type(self, group: GroupT, range_type: str) -> Distance:
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

    def max_detection_range(self) -> Distance:
        return max(self.detection_range(g) for g in self.groups)

    def detection_range(self, group: GroupT) -> Distance:
        return self._max_range_of_type(group, "detection_range")

    def max_threat_range(self) -> Distance:
        return max(self.threat_range(g) for g in self.groups)

    def threat_range(self, group: GroupT, radar_only: bool = False) -> Distance:
        return self._max_range_of_type(group, "threat_range")

    @property
    def is_ammo_depot(self) -> bool:
        return self.category == "ammo"

    @property
    def is_factory(self) -> bool:
        return self.category == "factory"

    @property
    def is_control_point(self) -> bool:
        """True if this TGO is the group for the control point itself (CVs and FOBs)."""
        return False

    @property
    def strike_targets(self) -> Sequence[Union[MissionTarget, Unit]]:
        return self.units

    @property
    def mark_locations(self) -> Iterator[Point]:
        yield self.position

    def clear(self) -> None:
        self.groups = []

    @property
    def capturable(self) -> bool:
        raise NotImplementedError

    @property
    def purchasable(self) -> bool:
        raise NotImplementedError


class BuildingGroundObject(TheaterGroundObject[VehicleGroup]):
    def __init__(
        self,
        name: str,
        category: str,
        group_id: int,
        object_id: int,
        position: Point,
        heading: Heading,
        control_point: ControlPoint,
        dcs_identifier: str,
        is_fob_structure: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            category=category,
            group_id=group_id,
            position=position,
            heading=heading,
            control_point=control_point,
            dcs_identifier=dcs_identifier,
            sea_object=False,
        )
        self.is_fob_structure = is_fob_structure
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

    def iter_building_group(self) -> Iterator[BuildingGroundObject]:
        for tgo in self.control_point.ground_objects:
            if (
                tgo.obj_name == self.obj_name
                and not tgo.is_dead
                and isinstance(tgo, BuildingGroundObject)
            ):
                yield tgo

    @property
    def strike_targets(self) -> List[BuildingGroundObject]:
        return list(self.iter_building_group())

    @property
    def mark_locations(self) -> Iterator[Point]:
        for building in self.iter_building_group():
            yield building.position

    @property
    def is_control_point(self) -> bool:
        return self.is_fob_structure

    @property
    def capturable(self) -> bool:
        return True

    @property
    def purchasable(self) -> bool:
        return False

    def max_threat_range(self) -> Distance:
        return meters(0)

    def max_detection_range(self) -> Distance:
        return meters(0)


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
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier=dcs_identifier,
            is_fob_structure=False,
        )
        self.zone = zone


class FactoryGroundObject(BuildingGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        heading: Heading,
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
            is_fob_structure=False,
        )


class NavalGroundObject(TheaterGroundObject[ShipGroup]):
    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.ANTISHIP
        yield from super().mission_types(for_player)

    @property
    def might_have_aa(self) -> bool:
        return True

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return False


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
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier="CARRIER",
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"

    def __str__(self) -> str:
        return f"CV {self.name}"


# TODO: Why is this both a CP and a TGO?
class LhaGroundObject(GenericCarrierGroundObject):
    def __init__(self, name: str, group_id: int, control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="LHA",
            group_id=group_id,
            position=control_point.position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier="LHA",
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"

    def __str__(self) -> str:
        return f"LHA {self.name}"


class MissileSiteGroundObject(TheaterGroundObject[VehicleGroup]):
    def __init__(
        self, name: str, group_id: int, position: Point, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="missile",
            group_id=group_id,
            position=position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=False,
        )

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return False


class CoastalSiteGroundObject(TheaterGroundObject[VehicleGroup]):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
        heading: Heading,
    ) -> None:
        super().__init__(
            name=name,
            category="coastal",
            group_id=group_id,
            position=position,
            heading=heading,
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=False,
        )

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return False


class IadsGroundObject(TheaterGroundObject[VehicleGroup], ABC):
    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.DEAD
        yield from super().mission_types(for_player)


# The SamGroundObject represents all type of AA
# The TGO can have multiple types of units (AAA,SAM,Support...)
# Differentiation can be made during generation with the airdefensegroupgenerator
class SamGroundObject(IadsGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            group_id=group_id,
            position=position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=False,
        )

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.DEAD
            yield FlightType.SEAD
        for mission_type in super().mission_types(for_player):
            # We yielded this ourselves to move it to the top of the list. Don't yield
            # it twice.
            if mission_type is not FlightType.DEAD:
                yield mission_type

    @property
    def might_have_aa(self) -> bool:
        return True

    def threat_range(self, group: VehicleGroup, radar_only: bool = False) -> Distance:
        max_non_radar = meters(0)
        live_trs = set()
        max_telar_range = meters(0)
        launchers = set()
        for unit in group.units:
            unit_type = db.vehicle_type_from_name(unit.type)
            if unit_type in TRACK_RADARS:
                live_trs.add(unit_type)
            elif unit_type in TELARS:
                max_telar_range = max(max_telar_range, meters(unit_type.threat_range))
            elif unit_type in LAUNCHER_TRACKER_PAIRS:
                launchers.add(unit_type)
            else:
                max_non_radar = max(max_non_radar, meters(unit_type.threat_range))
        max_tel_range = meters(0)
        for launcher in launchers:
            if LAUNCHER_TRACKER_PAIRS[launcher] in live_trs:
                max_tel_range = max(max_tel_range, meters(launcher.threat_range))
        if radar_only:
            return max(max_tel_range, max_telar_range)
        else:
            return max(max_tel_range, max_telar_range, max_non_radar)

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return True


class VehicleGroupGroundObject(TheaterGroundObject[VehicleGroup]):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="armor",
            group_id=group_id,
            position=position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=False,
        )

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return True


class EwrGroundObject(IadsGroundObject):
    def __init__(
        self,
        name: str,
        group_id: int,
        position: Point,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="ewr",
            group_id=group_id,
            position=position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier="EWR",
            sea_object=False,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them.
        # Use Group Id and uppercase EWR
        return f"{self.faction_color}|EWR|{self.group_id}"

    @property
    def might_have_aa(self) -> bool:
        return True

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return True


class ShipGroundObject(NavalGroundObject):
    def __init__(
        self, name: str, group_id: int, position: Point, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="ship",
            group_id=group_id,
            position=position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"
