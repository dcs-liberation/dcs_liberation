from __future__ import annotations

import copy
import itertools
import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, TYPE_CHECKING, Any, Iterator, Optional

import yaml

from game.data.groups import GroupRole, GroupTask
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from game.point_with_heading import PointWithHeading
from gen.templates import GroundObjectTemplate

if TYPE_CHECKING:
    from game import Game
    from game.factions.faction import Faction
    from game.theater import TheaterGroundObject, ControlPoint


@dataclass
class UnitGroup:
    name: str
    ground_units: list[GroundUnitType]
    ship_units: list[ShipUnitType]
    statics: list[str]
    role: GroupRole
    tasks: list[GroupTask] = field(default_factory=list)
    template_names: list[str] = field(default_factory=list)

    _by_name: ClassVar[dict[str, UnitGroup]] = {}
    _by_role: ClassVar[dict[GroupRole, list[UnitGroup]]] = {}
    _loaded: bool = False
    _templates: list[GroundObjectTemplate] = field(default_factory=list)

    def __str__(self) -> str:
        return self.name

    def update_from_unit_group(self, unit_group: UnitGroup) -> None:
        # Update tasking and templates
        self.tasks.extend([task for task in unit_group.tasks if task not in self.tasks])
        self._templates.extend(
            [
                template
                for template in unit_group.templates
                if template not in self.templates
            ]
        )

    @property
    def templates(self) -> list[GroundObjectTemplate]:
        return self._templates

    def add_template(self, faction_template: GroundObjectTemplate) -> None:
        template = copy.deepcopy(faction_template)
        updated_groups = []
        for group in template.groups:
            unit_types = list(
                itertools.chain(
                    [u.dcs_id for u in self.ground_units if group.can_use_unit(u)],
                    [s.dcs_id for s in self.ship_units if group.can_use_unit(s)],
                    [s for s in self.statics if group.can_use_unit_type(s)],
                )
            )
            if unit_types:
                group.set_possible_types(unit_types)
                updated_groups.append(group)
        template.groups = updated_groups
        self._templates.append(template)

    def load_templates(self, faction: Faction) -> None:
        self._templates = []
        if self.template_names:
            # Preferred templates
            for template_name in self.template_names:
                template = faction.templates.by_name(template_name)
                if template:
                    self.add_template(template)

        if not self._templates:
            # Find all matching templates if no preferred set or available
            for template in list(
                faction.templates.for_role_and_tasks(self.role, self.tasks)
            ):
                if any(self.has_unit_type(unit) for unit in template.units):
                    self.add_template(template)

    def set_templates(self, templates: list[GroundObjectTemplate]) -> None:
        self._templates = templates

    def has_unit_type(self, unit_type: UnitType[Any]) -> bool:
        return unit_type in self.ground_units or unit_type in self.ship_units

    @property
    def unit_types(self) -> Iterator[str]:
        for unit in self.ground_units:
            yield unit.dcs_id
        for ship in self.ship_units:
            yield ship.dcs_id
        for static in self.statics:
            yield static

    @classmethod
    def named(cls, name: str) -> UnitGroup:
        if not cls._loaded:
            cls._load_all()
        return cls._by_name[name]

    def generate(
        self,
        name: str,
        position: PointWithHeading,
        control_point: ControlPoint,
        game: Game,
        template_name: str = "",
    ) -> TheaterGroundObject:
        template: Optional[GroundObjectTemplate] = None
        if template_name:
            # Forced Template
            template = self._template_by_name(template_name)

        if template is None:
            # Random Template
            template = random.choice(self.templates)

        return template.generate(name, position, control_point, game)

    def _template_by_name(self, template_name: str) -> Optional[GroundObjectTemplate]:
        for available_template in self.templates:
            if available_template.name == template_name:
                return available_template
        logging.error(f"Requested template {template_name} is not available")
        return None

    @classmethod
    def _load_all(cls) -> None:
        for file in Path("resources/units/unit_groups").glob("*.yaml"):
            if not file.is_file():
                continue

            with file.open(encoding="utf-8") as data_file:
                data = yaml.safe_load(data_file)

            group_role = GroupRole(data.get("role"))

            group_tasks = [GroupTask(n) for n in data.get("tasks", [])]

            ground_units = [
                GroundUnitType.named(n) for n in data.get("ground_units", [])
            ]
            ship_units = [ShipUnitType.named(n) for n in data.get("ship_units", [])]

            unit_group = UnitGroup(
                name=data.get("name"),
                ground_units=ground_units,
                ship_units=ship_units,
                statics=data.get("statics", []),
                role=group_role,
                tasks=group_tasks,
                template_names=data.get("templates", []),
            )

            cls._by_name[unit_group.name] = unit_group
            if group_role in cls._by_role:
                cls._by_role[group_role].append(unit_group)
            else:
                cls._by_role[group_role] = [unit_group]

        cls._loaded = True
