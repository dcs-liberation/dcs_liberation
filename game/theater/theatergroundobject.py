from __future__ import annotations

import itertools
import logging
from abc import ABC
from typing import Iterator, List, TYPE_CHECKING

from dcs.unittype import VehicleType
from dcs.vehicles import vehicle_map

from dcs.mapping import Point


from game.dcs.helpers import unit_type_from_name
from ..data.radar_db import LAUNCHER_TRACKER_PAIRS, TELARS, TRACK_RADARS
from ..utils import Distance, Heading, meters

if TYPE_CHECKING:
    from .theatergroup import TheaterUnit, TheaterGroup
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


class TheaterGroundObject(MissionTarget):
    def __init__(
        self,
        name: str,
        category: str,
        position: Point,
        heading: Heading,
        control_point: ControlPoint,
        sea_object: bool,
    ) -> None:
        super().__init__(name, position)
        self.category = category
        self.heading = heading
        self.control_point = control_point
        self.sea_object = sea_object
        self.groups: List[TheaterGroup] = []

    @property
    def is_dead(self) -> bool:
        return self.alive_unit_count == 0

    @property
    def units(self) -> Iterator[TheaterUnit]:
        """
        :return: all the units at this location
        """
        yield from itertools.chain.from_iterable([g.units for g in self.groups])

    @property
    def statics(self) -> Iterator[TheaterUnit]:
        for group in self.groups:
            for unit in group.units:
                if unit.is_static:
                    yield unit

    @property
    def dead_units(self) -> list[TheaterUnit]:
        """
        :return: all the dead units at this location
        """
        return [unit for unit in self.units if not unit.alive]

    @property
    def group_name(self) -> str:
        """The name of the unit group."""
        return f"{self.category}|{self.name}"

    @property
    def waypoint_name(self) -> str:
        return f"[{self.name}] {self.category}"

    def __str__(self) -> str:
        return NAME_BY_CATEGORY[self.category]

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
    def unit_count(self) -> int:
        return sum([g.unit_count for g in self.groups])

    @property
    def alive_unit_count(self) -> int:
        return sum([g.alive_units for g in self.groups])

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

    def _max_range_of_type(self, group: TheaterGroup, range_type: str) -> Distance:
        if not self.might_have_aa:
            return meters(0)

        max_range = meters(0)
        for u in group.units:
            # Some units in pydcs have detection_range/threat_range defined,
            # but explicitly set to None.
            unit_range = getattr(u.type, range_type, None)
            if unit_range is not None:
                max_range = max(max_range, meters(unit_range))
        return max_range

    def max_detection_range(self) -> Distance:
        return max(self.detection_range(g) for g in self.groups)

    def detection_range(self, group: TheaterGroup) -> Distance:
        return self._max_range_of_type(group, "detection_range")

    def max_threat_range(self) -> Distance:
        return (
            max(self.threat_range(g) for g in self.groups) if self.groups else meters(0)
        )

    def threat_range(self, group: TheaterGroup, radar_only: bool = False) -> Distance:
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
    def strike_targets(self) -> list[TheaterUnit]:
        return [unit for unit in self.units if unit.alive]

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


class BuildingGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        category: str,
        position: Point,
        heading: Heading,
        control_point: ControlPoint,
        is_fob_structure: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            category=category,
            position=position,
            heading=heading,
            control_point=control_point,
            sea_object=False,
        )
        self.is_fob_structure = is_fob_structure

    @property
    def mark_locations(self) -> Iterator[Point]:
        # Special handling to mark all buildings of the TGO
        for unit in self.strike_targets:
            yield unit.position

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


class NavalGroundObject(TheaterGroundObject):
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
    def __init__(self, name: str, control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="CARRIER",
            position=control_point.position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
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
    def __init__(self, name: str, control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="LHA",
            position=control_point.position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"

    def __str__(self) -> str:
        return f"LHA {self.name}"


class MissileSiteGroundObject(TheaterGroundObject):
    def __init__(
        self, name: str, position: Point, heading: Heading, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="missile",
            position=position,
            heading=heading,
            control_point=control_point,
            sea_object=False,
        )

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return False


class CoastalSiteGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        position: Point,
        control_point: ControlPoint,
        heading: Heading,
    ) -> None:
        super().__init__(
            name=name,
            category="coastal",
            position=position,
            heading=heading,
            control_point=control_point,
            sea_object=False,
        )

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return False


class IadsGroundObject(TheaterGroundObject, ABC):
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
        position: Point,
        heading: Heading,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            position=position,
            heading=heading,
            control_point=control_point,
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

    def threat_range(self, group: TheaterGroup, radar_only: bool = False) -> Distance:
        max_non_radar = meters(0)
        live_trs = set()
        max_telar_range = meters(0)
        launchers = set()
        for unit in group.units:
            if not unit.alive or not issubclass(unit.type, VehicleType):
                continue
            unit_type = unit.type
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


class VehicleGroupGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        position: Point,
        heading: Heading,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="armor",
            position=position,
            heading=heading,
            control_point=control_point,
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
        position: Point,
        heading: Heading,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="ewr",
            position=position,
            heading=heading,
            control_point=control_point,
            sea_object=False,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them.
        # Use Group Id and uppercase EWR
        return f"{self.faction_color}|EWR|{self.name}"

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
    def __init__(self, name: str, position: Point, control_point: ControlPoint) -> None:
        super().__init__(
            name=name,
            category="ship",
            position=position,
            heading=Heading.from_degrees(0),
            control_point=control_point,
            sea_object=True,
        )

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"
