from __future__ import annotations

import itertools
import uuid
from abc import ABC
from typing import Any, Iterator, List, Optional, TYPE_CHECKING

from dcs.mapping import Point

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
from game.theater.presetlocation import PresetLocation
from .missiontarget import MissionTarget
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
    "commandcenter": "Command Center",
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
        location: PresetLocation,
        control_point: ControlPoint,
        sea_object: bool,
    ) -> None:
        super().__init__(name, location)
        self.id = uuid.uuid4()
        self.category = category
        self.heading = location.heading
        self.control_point = control_point
        self.sea_object = sea_object
        self.groups: List[TheaterGroup] = []
        self.original_name = location.original_name
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
        if self.is_dead:
            return Status.PRESENT_DESTROYED
        elif self.dead_units:
            return Status.PRESENT_DAMAGED
        else:
            return Status.PRESENT

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
    def display_name(self) -> str:
        """The display name of the tgo which will be shown on the map."""
        return self.group_name

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
        return sum(g.unit_count for g in self.groups)

    @property
    def alive_unit_count(self) -> int:
        return sum(g.alive_units for g in self.groups)

    @property
    def has_aa(self) -> bool:
        """Returns True if the ground object contains a working anti air unit"""
        return any(u.alive and u.is_anti_air for u in self.units)

    @property
    def has_live_radar_sam(self) -> bool:
        """Returns True if the ground object contains a unit with working radar SAM."""
        return any(g.max_threat_range(radar_only=True) for g in self.groups)

    def max_detection_range(self) -> Distance:
        """Calculate the maximum detection range of the ground object"""
        return max((g.max_detection_range() for g in self.groups), default=meters(0))

    def max_threat_range(self) -> Distance:
        """Calculate the maximum threat range of the ground object"""
        return max((g.max_threat_range() for g in self.groups), default=meters(0))

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

    def rotate(self, heading: Heading) -> None:
        """Rotate the whole TGO clockwise to the new heading"""
        rotation = heading - self.heading
        if rotation.degrees < 0:
            rotation = Heading.from_degrees(rotation.degrees + 360)

        self.heading = heading
        # Rotate the whole TGO to match the new heading
        for unit in self.units:
            unit.position.heading += rotation
            unit.position.rotate(self.position, rotation)

    @property
    def should_head_to_conflict(self) -> bool:
        """Should this TGO head towards the closest conflict to work properly?"""
        return False


class BuildingGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        category: str,
        location: PresetLocation,
        control_point: ControlPoint,
        is_fob_structure: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            category=category,
            location=location,
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
        elif self.category == "commandcenter":
            entity = LandInstallationEntity.MILITARY_INFRASTRUCTURE
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


class NavalGroundObject(TheaterGroundObject, ABC):
    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.ANTISHIP
        yield from super().mission_types(for_player)

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
    def __init__(
        self, name: str, location: PresetLocation, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="CARRIER",
            location=location,
            control_point=control_point,
            sea_object=True,
        )

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.CARRIER

    def __str__(self) -> str:
        return f"CV {self.name}"


# TODO: Why is this both a CP and a TGO?
class LhaGroundObject(GenericCarrierGroundObject):
    def __init__(
        self, name: str, location: PresetLocation, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="LHA",
            location=location,
            control_point=control_point,
            sea_object=True,
        )

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.AMPHIBIOUS_ASSAULT_SHIP_GENERAL

    def __str__(self) -> str:
        return f"LHA {self.name}"


class MissileSiteGroundObject(TheaterGroundObject):
    def __init__(
        self, name: str, location: PresetLocation, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="missile",
            location=location,
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

    @property
    def should_head_to_conflict(self) -> bool:
        return True


class CoastalSiteGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="coastal",
            location=location,
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

    @property
    def should_head_to_conflict(self) -> bool:
        return True


class IadsGroundObject(TheaterGroundObject, ABC):
    def __init__(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
        category: str = "aa",
    ) -> None:
        super().__init__(
            name=name,
            category=category,
            location=location,
            control_point=control_point,
            sea_object=False,
        )

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.DEAD
        yield from super().mission_types(for_player)

    @property
    def should_head_to_conflict(self) -> bool:
        return True


# The SamGroundObject represents all type of AA
# The TGO can have multiple types of units (AAA,SAM,Support...)
# Differentiation can be made during generation with the airdefensegroupgenerator
class SamGroundObject(IadsGroundObject):
    def __init__(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="aa",
            location=location,
            control_point=control_point,
        )

    @property
    def sidc_status(self) -> Status:
        if self.is_dead:
            return Status.PRESENT_DESTROYED
        elif self.dead_units:
            if self.max_threat_range() > meters(0):
                return Status.PRESENT
            else:
                return Status.PRESENT_DAMAGED
        else:
            return Status.PRESENT_FULLY_CAPABLE

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
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return True


class VehicleGroupGroundObject(TheaterGroundObject):
    def __init__(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            category="armor",
            location=location,
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

    @property
    def should_head_to_conflict(self) -> bool:
        return True


class EwrGroundObject(IadsGroundObject):
    def __init__(
        self,
        name: str,
        location: PresetLocation,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(
            name=name,
            location=location,
            control_point=control_point,
            category="ewr",
        )

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_EQUIPMENT, LandEquipmentEntity.RADAR

    @property
    def capturable(self) -> bool:
        return False

    @property
    def purchasable(self) -> bool:
        return True


class ShipGroundObject(NavalGroundObject):
    def __init__(
        self, name: str, location: PresetLocation, control_point: ControlPoint
    ) -> None:
        super().__init__(
            name=name,
            category="ship",
            location=location,
            control_point=control_point,
            sea_object=True,
        )

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.SURFACE_COMBATANT_LINE


class IadsBuildingGroundObject(BuildingGroundObject):
    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield from [FlightType.STRIKE, FlightType.DEAD]
        skippers = [FlightType.STRIKE]  # prevent yielding twice
        for mission_type in super().mission_types(for_player):
            if mission_type not in skippers:
                yield mission_type
