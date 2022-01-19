from __future__ import annotations

import copy
import json
import logging
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, Any, TYPE_CHECKING, Optional, Tuple, Union

from dcs import Point
from dcs.ships import ship_map
from dcs.unit import Unit
from dcs.unittype import UnitType
from dcs.vehicles import vehicle_map

from game.dcs.groundunittype import GroundUnitType
from game.theater.theatergroundobject import (
    SamGroundObject,
    EwrGroundObject,
    BuildingGroundObject,
    GroundGroup,
    MissileSiteGroundObject,
    ShipGroundObject,
    CarrierGroundObject,
    LhaGroundObject,
    CoastalSiteGroundObject,
    VehicleGroupGroundObject,
    IadsGroundObject,
)
from game.point_with_heading import PointWithHeading

from game.utils import Heading
from game import db

if TYPE_CHECKING:
    from game import Game
    from game.factions.faction import Faction
    from game.theater import TheaterGroundObject, ControlPoint


class TemplateEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> dict[str, Any]:
        if hasattr(obj, "to_json"):
            return obj.to_json()
        else:
            return obj.__dict__


class TemplateCategory(Enum):
    AirDefence = "AirDefence"  # Has subcategories for the AARange
    Building = "Building"  # Has subcategories from
    Naval = "Naval"  # Has subcategories lha, carrier, ship
    Armor = "Armor"
    Missile = "Missile"
    Coastal = "Coastal"


@dataclass
class UnitTemplate:
    name: str
    type: str
    position: Point
    heading: int

    @staticmethod
    def from_unit(unit: Unit) -> UnitTemplate:
        return UnitTemplate(
            unit.name,
            unit.type,
            Point(int(unit.position.x), int(unit.position.y)),
            int(unit.heading),
        )

    @staticmethod
    def from_dict(d_unit: dict[str, Any]) -> UnitTemplate:
        return UnitTemplate(
            d_unit["name"],
            d_unit["type"],
            Point(d_unit["position"]["x"], d_unit["position"]["y"]),
            d_unit["heading"],
        )


@dataclass
class GroupTemplate:
    name: str
    units: list[UnitTemplate]

    # Is Static group
    static: bool = False

    # Every group can only have one Randomizer
    randomizer: Optional[TemplateRandomizer] = None

    # Defines if this groupTemplate is required or not
    optional: bool = False

    @staticmethod
    def from_dict(d_group: dict[str, Any]) -> GroupTemplate:
        units = [UnitTemplate.from_dict(unit) for unit in d_group["units"]]
        randomizer = (
            TemplateRandomizer.from_dict(d_group["randomizer"])
            if d_group["randomizer"]
            else None
        )
        return GroupTemplate(
            d_group["name"], units, d_group["static"], randomizer, d_group["optional"]
        )

    @property
    def unit_types_count(self) -> dict[str, int]:
        units: dict[str, int] = {}
        for unit in self.units:
            if unit.type in units:
                units[unit.type] += 1
            else:
                units[unit.type] = 1
        return units


@dataclass
class TemplateRandomizer:
    # Selection of units to apply the randomization.
    # If left empty the randomizer will be applied to all unit of the group
    units: list[int] = field(default_factory=list)

    # Define the amount of random units to be created by the randomizer.
    # This can be a fixed int or a random value from a range of two ints as tuple
    count: Union[int, list[int]] = field(default=1)

    # The randomizer can pick a random unit type from a faction list like
    # frontline_units or air_defenses to allow faction sensitive randomization
    faction_types: list[str] = field(default_factory=list)

    # Only works for vehicle units. Allows to specify the type class of the unit.
    # For example this allows to select frontline_units as faction_type and also define
    # Shorads as class to only pick AntiAir from the list
    type_classes: list[str] = field(default_factory=list)

    # Allows to define the exact UnitTypes the randomizer picks from. these have to be
    # the dcs_unit_types found in the pydcs arrays
    unit_types: list[str] = field(default_factory=list)

    # Runtime Attributes
    _initialized: bool = False
    _possible_types: list[str] = field(default_factory=list)
    _random_unit_type: Optional[str] = None
    _forced_unit_type: Optional[str] = None
    _unit_counter: Optional[int] = None

    def to_json(self) -> dict[str, Any]:
        d = self.__dict__
        # Do not serialize the runtime attributes
        d.pop("_initialized", None)
        d.pop("_possible_types", None)
        d.pop("_random_unit_type", None)
        d.pop("_forced_unit_type", None)
        d.pop("_unit_counter", None)
        return d

    @staticmethod
    def from_dict(d: dict[str, Any]) -> TemplateRandomizer:
        return TemplateRandomizer(
            d["units"],
            d["count"],
            d["faction_types"],
            d["type_classes"],
            d["unit_types"],
        )

    @property
    def possible_ground_units(self) -> Iterator[GroundUnitType]:
        for unit_type in self._possible_types:
            if unit_type in vehicle_map:
                dcs_unit_type = vehicle_map[unit_type]
                try:
                    yield next(GroundUnitType.for_dcs_type(dcs_unit_type))
                except StopIteration:
                    continue

    def force_type(self, type: str) -> None:
        self._forced_unit_type = type

    def randomize(self) -> None:
        self.randomize_unit_type()
        self.reset_unit_counter()

    def reset_unit_counter(self) -> None:
        if isinstance(self.count, list):
            count = random.choice(range(self.count[0], self.count[1]))
        elif isinstance(self.count, int):
            count = self.count
        self._unit_counter = count

    def init_randomization_for_faction(self, faction: Faction) -> None:
        # Initializes the randomization
        # This sets the random_unit_type and the random_unit_count
        if self._initialized:
            return

        type_list = []
        for faction_type in self.faction_types:
            for unit_type in faction[faction_type]:
                if isinstance(unit_type, GroundUnitType):
                    # GroundUnitType
                    type_list.append(unit_type.dcs_id)
                elif issubclass(unit_type, UnitType):
                    # DCS Unit Type object
                    type_list.append(unit_type.id)
                elif db.unit_type_from_name(unit_type):
                    # DCS Unit Type as string
                    type_list.append(unit_type)
                else:
                    raise KeyError

        if self.unit_types and self.faction_types:
            # If Faction types were defined use unit_types as filter
            filtered_type_list = [
                unit_type for unit_type in type_list if unit_type in self.unit_types
            ]
            type_list = filtered_type_list
        else:
            # If faction_types is not defined append the unit_types
            for unit_type in self.unit_types:
                type_list.append(unit_type)

        if self.type_classes:
            filtered_type_list = []
            for unit_type in type_list:
                if unit_type in vehicle_map:
                    dcs_type = vehicle_map[unit_type]
                else:
                    continue
                try:
                    ground_unit_type = next(GroundUnitType.for_dcs_type(dcs_type))
                except (KeyError, StopIteration):
                    logging.error(f"Unit {unit_type} has no GroundUnitType")
                    continue
                if (
                    ground_unit_type.unit_class
                    and ground_unit_type.unit_class.value in self.type_classes
                ):
                    filtered_type_list.append(unit_type)
            type_list = filtered_type_list
        self._possible_types = type_list
        if self.randomize_unit_type():
            self.reset_unit_counter()
            self._initialized = True

    @property
    def unit_type(self) -> Optional[str]:
        return self._random_unit_type

    def randomize_unit_type(self) -> bool:
        try:
            self._random_unit_type = self._forced_unit_type or random.choice(
                self._possible_types
            )
        except IndexError:
            logging.warning("Can not initialize randomizer")
            return False
        return True

    @property
    def unit_count(self) -> int:
        if not self._unit_counter:
            self.reset_unit_counter()
        return self._unit_counter or 1

    def use_unit(self) -> None:
        if self._unit_counter is None:
            self.reset_unit_counter()
        if self._unit_counter and self._unit_counter > 0:
            self._unit_counter -= 1
        else:
            raise IndexError

    @property
    def unit_range(self) -> list[int]:
        if len(self.units) > 1:
            return list(range(self.units[0], self.units[1] + 1))
        return self.units


class GroundObjectTemplate(ABC):
    def __init__(
        self, name: str, template_type: str = "", description: str = ""
    ) -> None:
        self.name = name
        self.template_type = template_type
        self.description = description
        self.groups: list[GroupTemplate] = []

    @classmethod
    def from_dict(cls, d_object: dict[str, Any]) -> GroundObjectTemplate:
        template = cls(
            d_object["name"], d_object["template_type"], d_object["description"]
        )
        for d_group in d_object["groups"]:
            template.groups.append(GroupTemplate.from_dict(d_group))
        return template

    def generate(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
        game: Game,
        randomization: bool = True,
    ) -> TheaterGroundObject:

        # Create the ground_object based on the type
        ground_object = self._create_ground_object(name, position, control_point)

        # Generate all groups using the randomization if it defined
        for g_id, group in enumerate(self.groups):
            tgo_group = GroundGroup.from_template(
                game.next_group_id(),
                group,
                ground_object,
                randomization,
            )
            # Set Group Name
            tgo_group.name = f"{self.name} {g_id}"

            # Assign UniqueID, name and align relative to ground_object
            for u_id, unit in enumerate(tgo_group.units):
                unit.id = game.next_unit_id()
                unit.name = f"{self.name} {g_id}-{u_id}"
                if isinstance(self, AirDefenceTemplate):
                    # Head SAM and EWR towards the center of the conflict
                    unit.position.heading = (
                        game.theater.heading_to_conflict_from(unit.position)
                        or unit.position.heading
                    )
                unit.position = PointWithHeading.from_point(
                    Point(
                        ground_object.position.x + unit.position.x,
                        ground_object.position.y + unit.position.y,
                    ),
                    unit.position.heading,
                )
            ground_object.groups.append(tgo_group)

        return ground_object

    @abstractmethod
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        raise NotImplementedError

    @property
    def randomizable(self) -> bool:
        # Returns True if any group of the template has a randomizer
        return any(group_template.randomizer for group_template in self.groups)

    def estimated_price_for(self, go: TheaterGroundObject) -> float:
        # Price can only be estimated because of randomization
        template_price = 0
        for g_id, group in enumerate(self.groups):
            tgo_group = GroundGroup.from_template(g_id, group, go)
            for unit in tgo_group.units:
                if unit.type in vehicle_map:
                    dcs_type = vehicle_map[unit.type]
                    try:
                        unit_type = next(GroundUnitType.for_dcs_type(dcs_type))
                    except StopIteration:
                        continue
                    template_price = template_price + unit_type.price
        return template_price

    @property
    def size(self) -> int:
        return sum([len(group.units) for group in self.groups])

    @property
    def min_size(self) -> int:
        return self._size_for_randomized(True)

    @property
    def max_size(self) -> int:
        return self._size_for_randomized(False)

    def _size_for_randomized(self, min_size: bool) -> int:
        size = 0
        for group in self.groups:
            for unit_id, unit in enumerate(group.units):
                if group.randomizer and unit_id in group.randomizer.units:
                    if isinstance(group.randomizer.count, int):
                        size = size + group.randomizer.count
                    else:
                        size = size + group.randomizer.count[0 if min_size else 1]
                else:
                    size = size + 1
        return size

    @property
    def required_units(self) -> list[str]:
        """returns all required unit types by theyre dcs type id"""
        # todo take care for randomizer
        unit_types = []
        for group in self.groups:
            # this completly excludes randomized groups
            if not group.optional and not group.randomizer:
                for unit in group.units:
                    if unit.type not in unit_types:
                        unit_types.append(unit.type)
        return unit_types


class AirDefenceTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> IadsGroundObject:
        if self.template_type == "EWR":
            return EwrGroundObject(name, position, control_point)
        elif self.template_type in ["Long", "Medium", "Short", "AAA"]:
            return SamGroundObject(name, position, control_point)
        raise RuntimeError(
            f" No Template Definition for AirDefence with subcategory {self.template_type}"
        )


class BuildingTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> BuildingGroundObject:
        return BuildingGroundObject(
            name,
            self.template_type,
            position,
            Heading.from_degrees(0),
            control_point,
            self.template_type == "fob",
        )


class NavalTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        if self.template_type == "ship":
            return ShipGroundObject(name, position, control_point)
        elif self.template_type == "carrier":
            return CarrierGroundObject(name, control_point)
        elif self.template_type == "lha":
            return LhaGroundObject(name, control_point)
        raise NotImplementedError


class CoastalTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        return CoastalSiteGroundObject(name, position, control_point, position.heading)


class ArmorTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        return VehicleGroupGroundObject(name, position, control_point)


class MissileTemplate(GroundObjectTemplate):
    def _create_ground_object(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
    ) -> TheaterGroundObject:
        return MissileSiteGroundObject(name, position, control_point)


TEMPLATE_TYPES = {
    TemplateCategory.AirDefence: AirDefenceTemplate,
    TemplateCategory.Building: BuildingTemplate,
    TemplateCategory.Naval: NavalTemplate,
    TemplateCategory.Armor: ArmorTemplate,
    TemplateCategory.Missile: MissileTemplate,
    TemplateCategory.Coastal: CoastalTemplate,
}


class GroundObjectTemplates:
    # list of templates per category. e.g. AA or similar
    _templates: dict[TemplateCategory, list[GroundObjectTemplate]]

    def __init__(self) -> None:
        self._templates = {}

    @property
    def templates(self) -> Iterator[tuple[TemplateCategory, GroundObjectTemplate]]:
        for category, templates in self._templates.items():
            for template in templates:
                yield category, template

    @classmethod
    def from_json(cls, template_file: str) -> GroundObjectTemplates:
        # Rebuild the TemplatesObject from the json dict

        obj = GroundObjectTemplates()
        with open(template_file, "r") as f:
            json_templates: dict[str, list[dict[str, Any]]] = json.load(f)
        for category, templates in json_templates.items():
            for d_template in templates:
                template = TEMPLATE_TYPES[TemplateCategory(category)].from_dict(
                    d_template
                )
                obj.add_template(TemplateCategory(category), template)
        return obj

    def to_json(self) -> dict[str, Any]:
        return {
            category.value: templates for category, templates in self._templates.items()
        }

    @property
    def all(self) -> Iterator[GroundObjectTemplate]:
        for templates in self._templates.values():
            yield from templates

    def by_name(self, template_name: str) -> Optional[GroundObjectTemplate]:
        for template in self.all:
            if template.name == template_name:
                return template
        return None

    def by_category_and_name(
        self, category: TemplateCategory, template_name: str
    ) -> Optional[GroundObjectTemplate]:
        if category in self._templates:
            for template in self._templates[category]:
                if template.name == template_name:
                    return template
        return None

    def add_template(
        self, category: TemplateCategory, template: GroundObjectTemplate
    ) -> None:
        if category not in self._templates:
            self._templates[category] = [template]
        else:
            self._templates[category].append(template)

    def for_category(
        self, category: TemplateCategory, sub_category: Optional[str] = None
    ) -> Iterator[GroundObjectTemplate]:

        if category not in self._templates:
            return None

        for template in self._templates[category]:
            if not sub_category or template.template_type == sub_category:
                yield template
