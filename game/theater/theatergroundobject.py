from __future__ import annotations

import itertools
import logging
from typing import Iterator, List, TYPE_CHECKING, Union

from dcs.mapping import Point
from dcs.triggers import TriggerZone
from dcs.unit import Unit
from dcs.unitgroup import Group
from dcs.unittype import VehicleType

from .. import db
from ..data.radar_db import (
    TRACK_RADARS,
    TELARS,
    LAUNCHER_TRACKER_PAIRS,
)
from ..utils import Distance, meters

if TYPE_CHECKING:
    from .controlpoint import ControlPoint
    from gen.flights.flight import FlightType

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
        sea_object: bool,
    ) -> None:
        super().__init__(name, position)
        self.category = category
        self.group_id = group_id
        self.heading = heading
        self.control_point = control_point
        self.dcs_identifier = dcs_identifier
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
    def has_live_radar_sam(self) -> bool:
        """Returns True if the ground object contains a unit with working radar SAM."""
        for group in self.groups:
            if self.threat_range(group, radar_only=True):
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

    def max_detection_range(self) -> Distance:
        return max(self.detection_range(g) for g in self.groups)

    def detection_range(self, group: Group) -> Distance:
        return self._max_range_of_type(group, "detection_range")

    def max_threat_range(self) -> Distance:
        return max(self.threat_range(g) for g in self.groups)

    def threat_range(self, group: Group, radar_only: bool = False) -> Distance:
        return self._max_range_of_type(group, "threat_range")

    @property
    def is_factory(self) -> bool:
        return self.category == "factory"

    @property
    def is_control_point(self) -> bool:
        """True if this TGO is the group for the control point itself (CVs and FOBs)."""
        return False

    @property
    def strike_targets(self) -> List[Union[MissionTarget, Unit]]:
        return self.units


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
        is_fob_structure=False,
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

    def iter_building_group(self) -> Iterator[TheaterGroundObject]:
        for tgo in self.control_point.ground_objects:
            if tgo.obj_name == self.obj_name and not tgo.is_dead:
                yield tgo

    @property
    def strike_targets(self) -> List[Union[MissionTarget, Unit]]:
        return list(self.iter_building_group())

    @property
    def is_control_point(self) -> bool:
        return self.is_fob_structure


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
            is_fob_structure=False,
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
            is_fob_structure=False,
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
            category="missile",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
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
            category="coastal",
            group_id=group_id,
            position=position,
            heading=heading,
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=False,
        )


# TODO: Differentiate types.
# This type gets used both for AA sites (SAM, AAA, or SHORAD). These should each
# be split into their own types.
class SamGroundObject(TheaterGroundObject):
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
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
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
            yield FlightType.SEAD
        yield from super().mission_types(for_player)

    @property
    def might_have_aa(self) -> bool:
        return True

    def threat_range(self, group: Group, radar_only: bool = False) -> Distance:
        max_non_radar = meters(0)
        live_trs = set()
        max_telar_range = meters(0)
        launchers = set()
        for unit in group.units:
            unit_type = db.unit_type_from_name(unit.type)
            if unit_type is None or not issubclass(unit_type, VehicleType):
                continue
            if unit_type in TRACK_RADARS:
                live_trs.add(unit_type)
            elif unit_type in TELARS:
                max_telar_range = max(
                    max_telar_range, meters(getattr(unit_type, "threat_range", 0))
                )
            elif unit_type in LAUNCHER_TRACKER_PAIRS:
                launchers.add(unit_type)
            else:
                max_non_radar = max(
                    max_non_radar, meters(getattr(unit_type, "threat_range", 0))
                )
        max_tel_range = meters(0)
        for launcher in launchers:
            if LAUNCHER_TRACKER_PAIRS[launcher] in live_trs:
                max_tel_range = max(
                    max_tel_range, meters(getattr(launcher, "threat_range"))
                )
        if radar_only:
            return max(max_tel_range, max_telar_range)
        else:
            return max(max_tel_range, max_telar_range, max_non_radar)


class VehicleGroupGroundObject(TheaterGroundObject):
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
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=False,
        )


class EwrGroundObject(TheaterGroundObject):
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
            heading=0,
            control_point=control_point,
            dcs_identifier="EWR",
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
            category="ship",
            group_id=group_id,
            position=position,
            heading=0,
            control_point=control_point,
            dcs_identifier="AA",
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"
