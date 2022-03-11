from __future__ import annotations

import itertools
import uuid
from abc import ABC
from typing import Any, Iterator, List, Optional, TYPE_CHECKING

from dcs.mapping import Point
from dcs.unittype import VehicleType
from shapely.geometry import Point as ShapelyPoint

from game.sidc import (
    Entity,
    LandEquipmentEntity,
    LandInstallationEntity,
    LandUnitEntity,
    SeaSurfaceEntity,
    SidcDescribable,
    StandardIdentity,
    Status,
    SymbolSet,
)
from .missiontarget import MissionTarget
from ..data.radar_db import LAUNCHER_TRACKER_PAIRS, TELARS, TRACK_RADARS
from ..utils import Distance, Heading, meters

if TYPE_CHECKING:
    from game.ato.flighttype import FlightType
    from game.threatzones import ThreatPoly
    from .theatergroup import TheaterUnit, TheaterGroup
    from .controlpoint import ControlPoint


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


class TheaterGroundObject(MissionTarget, SidcDescribable, ABC):
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
        self.id = uuid.uuid4()
        self.category = category
        self.heading = heading
        self.control_point = control_point
        self.sea_object = sea_object
        self.groups: List[TheaterGroup] = []
        self._threat_poly: ThreatPoly | None = None

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        del state["_threat_poly"]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        state["_threat_poly"] = None
        self.__dict__.update(state)

    @property
    def sidc_status(self) -> Status:
        return Status.PRESENT_DESTROYED if self.is_dead else Status.PRESENT

    @property
    def standard_identity(self) -> StandardIdentity:
        return (
            StandardIdentity.FRIEND
            if self.control_point.captured
            else StandardIdentity.HOSTILE_FAKER
        )

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
        return (
            max(self.detection_range(g) for g in self.groups)
            if self.groups
            else meters(0)
        )

    def detection_range(self, group: TheaterGroup) -> Distance:
        return self._max_range_of_type(group, "detection_range")

    def max_threat_range(self) -> Distance:
        return (
            max(self.threat_range(g) for g in self.groups) if self.groups else meters(0)
        )

    def threat_range(self, group: TheaterGroup, radar_only: bool = False) -> Distance:
        return self._max_range_of_type(group, "threat_range")

    def threat_poly(self) -> ThreatPoly | None:
        if self._threat_poly is None:
            self._threat_poly = self._make_threat_poly()
        return self._threat_poly

    def invalidate_threat_poly(self) -> None:
        self._threat_poly = None

    def _make_threat_poly(self) -> ThreatPoly | None:
        threat_range = self.max_threat_range()
        if not threat_range:
            return None

        point = ShapelyPoint(self.position.x, self.position.y)
        return point.buffer(threat_range.meters)

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
        self.invalidate_threat_poly()
        self.groups = []

    @property
    def capturable(self) -> bool:
        raise NotImplementedError

    @property
    def purchasable(self) -> bool:
        raise NotImplementedError

    @property
    def value(self) -> int:
        """The value of all units of the Ground Objects"""
        return sum(u.unit_type.price for u in self.units if u.unit_type and u.alive)

    def group_by_name(self, name: str) -> Optional[TheaterGroup]:
        for group in self.groups:
            if group.name == name:
                return group
        return None


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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        if self.category == "allycamp":
            entity = LandInstallationEntity.TENTED_CAMP
        elif self.category == "ammo":
            entity = LandInstallationEntity.AMMUNITION_CACHE
        elif self.category == "comms":
            entity = LandInstallationEntity.TELECOMMUNICATIONS_TOWER
        elif self.category == "derrick":
            entity = LandInstallationEntity.PETROLEUM_FACILITY
        elif self.category == "factory":
            entity = LandInstallationEntity.MAINTENANCE_FACILITY
        elif self.category == "farp":
            entity = LandInstallationEntity.HELICOPTER_LANDING_SITE
        elif self.category == "fuel":
            entity = LandInstallationEntity.WAREHOUSE_STORAGE_FACILITY
        elif self.category == "oil":
            entity = LandInstallationEntity.PETROLEUM_FACILITY
        elif self.category == "power":
            entity = LandInstallationEntity.GENERATION_STATION
        elif self.category == "village":
            entity = LandInstallationEntity.PUBLIC_VENUES_INFRASTRUCTURE
        elif self.category == "ware":
            entity = LandInstallationEntity.WAREHOUSE_STORAGE_FACILITY
        elif self.category == "ww2bunker":
            entity = LandInstallationEntity.MILITARY_BASE
        else:
            raise ValueError(f"Unhandled building category: {self.category}")
        return SymbolSet.LAND_INSTALLATIONS, entity

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


class NavalGroundObject(TheaterGroundObject, ABC):
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


class GenericCarrierGroundObject(NavalGroundObject, ABC):
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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.CARRIER

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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.AMPHIBIOUS_ASSAULT_SHIP_GENERAL

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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_UNIT, LandUnitEntity.MISSILE

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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_UNIT, LandUnitEntity.MISSILE

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

    @property
    def sidc_status(self) -> Status:
        if self.is_dead:
            return Status.PRESENT_DESTROYED
        if self.max_threat_range() > meters(0):
            return Status.PRESENT
        return Status.PRESENT_DAMAGED

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_UNIT, LandUnitEntity.AIR_DEFENSE

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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return (
            SymbolSet.LAND_UNIT,
            LandUnitEntity.ARMOR_ARMORED_MECHANIZED_SELF_PROPELLED_TRACKED,
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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_EQUIPMENT, LandEquipmentEntity.RADAR

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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.SURFACE_COMBATANT_LINE

    @property
    def group_name(self) -> str:
        # Prefix the group names with the side color so Skynet can find them,
        # add to EWR.
        return f"{self.faction_color}|EWR|{super().group_name}"
