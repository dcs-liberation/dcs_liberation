from __future__ import annotations

import itertools
import logging
import pickle
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterator

import dcs
import yaml
from dcs import Point
from dcs.unitgroup import StaticGroup

from game import persistency
from game.data.groups import GroupRole, GroupTask
from game.layout.layout import (
    TheaterLayout,
    GroupLayout,
    LayoutUnit,
    AntiAirLayout,
    BuildingLayout,
    NavalLayout,
    GroundForceLayout,
    DefensesLayout,
)
from game.layout.layoutmapping import GroupLayoutMapping, LayoutMapping
from game.profiling import logged_duration
from game.version import VERSION

TEMPLATE_DIR = "resources/layouts/"
TEMPLATE_DUMP = "Liberation/layouts.p"

TEMPLATE_TYPES = {
    GroupRole.AIR_DEFENSE: AntiAirLayout,
    GroupRole.BUILDING: BuildingLayout,
    GroupRole.NAVAL: NavalLayout,
    GroupRole.GROUND_FORCE: GroundForceLayout,
    GroupRole.DEFENSES: DefensesLayout,
}


class LayoutLoader:
    # list of layouts per category. e.g. AA or similar
    _templates: dict[str, TheaterLayout] = {}

    def __init__(self) -> None:
        self._templates = {}

    def initialize(self) -> None:
        if not self._templates:
            with logged_duration("Loading layouts"):
                self.load_templates()

    @property
    def layouts(self) -> Iterator[TheaterLayout]:
        self.initialize()
        yield from self._templates.values()

    def load_templates(self) -> None:
        """This will load all pre-loaded layouts from a pickle file.
        If pickle can not be loaded it will import and dump the layouts"""
        # We use a pickle for performance reasons. Importing takes many seconds
        file = Path(persistency.base_path()) / TEMPLATE_DUMP
        if file.is_file():
            # Load from pickle if existing
            with file.open("rb") as f:
                try:
                    version, self._templates = pickle.load(f)
                    # Check if the game version of the dump is identical to the current
                    if version == VERSION:
                        return
                except Exception as e:
                    logging.error(f"Error {e} reading layouts dump. Recreating.")
        # If no dump is available or game version is different create a new dump
        self.import_templates()

    def import_templates(self) -> None:
        """This will import all layouts from the template folder
        and dumps them to a pickle"""
        mappings: dict[str, list[LayoutMapping]] = {}
        with logged_duration("Parsing mapping yamls"):
            for file in Path(TEMPLATE_DIR).rglob("*.yaml"):
                if not file.is_file():
                    continue
                with file.open("r", encoding="utf-8") as f:
                    mapping_dict = yaml.safe_load(f)

                template_map = LayoutMapping.from_dict(mapping_dict, f.name)

                if template_map.layout_file in mappings:
                    mappings[template_map.layout_file].append(template_map)
                else:
                    mappings[template_map.layout_file] = [template_map]

        with logged_duration(f"Parsing all layout miz multithreaded"):
            with ThreadPoolExecutor() as exe:
                for miz, maps in mappings.items():
                    exe.submit(self._load_from_miz, miz, maps)

        logging.info(f"Imported {len(self._templates)} layouts")
        self._dump_templates()

    def _dump_templates(self) -> None:
        file = Path(persistency.base_path()) / TEMPLATE_DUMP
        dump = (VERSION, self._templates)
        with file.open("wb") as fdata:
            pickle.dump(dump, fdata)

    @staticmethod
    def mapping_for_group(
        mappings: list[LayoutMapping], group_name: str
    ) -> tuple[LayoutMapping, int, GroupLayoutMapping]:
        for mapping in mappings:
            for g_id, group_mapping in enumerate(mapping.groups):
                if (
                    group_mapping.name == group_name
                    or group_name in group_mapping.statics
                ):
                    return mapping, g_id, group_mapping
        raise KeyError

    def _load_from_miz(self, miz: str, mappings: list[LayoutMapping]) -> None:
        template_position: dict[str, Point] = {}
        temp_mis = dcs.Mission()
        with logged_duration(f"Parsing {miz}"):
            # The load_file takes a lot of time to compute. That's why the layouts
            # are written to a pickle and can be reloaded from the ui
            # Example the whole routine: 0:00:00.934417,
            # the .load_file() method: 0:00:00.920409
            temp_mis.load_file(miz)

        for country in itertools.chain(
            temp_mis.coalition["red"].countries.values(),
            temp_mis.coalition["blue"].countries.values(),
        ):
            for dcs_group in itertools.chain(
                temp_mis.country(country.name).vehicle_group,
                temp_mis.country(country.name).ship_group,
                temp_mis.country(country.name).static_group,
            ):
                try:
                    mapping, group_id, group_mapping = self.mapping_for_group(
                        mappings, dcs_group.name
                    )
                except KeyError:
                    logging.warning(f"No mapping for dcs group {dcs_group.name}")
                    continue

                template = self._templates.get(mapping.name, None)
                if template is None:
                    # Create a new template
                    template = TEMPLATE_TYPES[mapping.role](
                        mapping.name, mapping.role, mapping.description
                    )
                    template.generic = mapping.generic
                    template.tasks = mapping.tasks
                    self._templates[template.name] = template

                for i, unit in enumerate(dcs_group.units):
                    group_template = None
                    for group in template.groups:
                        if group.name == group_mapping.name:
                            # We already have a layoutgroup for this dcs_group
                            group_template = group
                    if not group_template:
                        group_template = GroupLayout(
                            group_mapping.name,
                            [],
                            group_mapping.group,
                            group_mapping.unit_count,
                            group_mapping.unit_types,
                            group_mapping.unit_classes,
                            group_mapping.alternative_classes,
                        )
                        group_template.optional = group_mapping.optional
                        # Add the group at the correct position
                        template.add_group(group_template, group_id)
                    unit_template = LayoutUnit.from_unit(unit)
                    if i == 0 and template.name not in template_position:
                        template_position[template.name] = unit.position
                    unit_template.position = (
                        unit_template.position - template_position[template.name]
                    )
                    group_template.units.append(unit_template)

    def by_name(self, template_name: str) -> Iterator[TheaterLayout]:
        for template in self.layouts:
            if template.name == template_name:
                yield template

    def by_task(self, group_task: GroupTask) -> Iterator[TheaterLayout]:
        for template in self.layouts:
            if not group_task or group_task in template.tasks:
                yield template

    def by_tasks(self, group_tasks: list[GroupTask]) -> Iterator[TheaterLayout]:
        unique_templates = []
        for group_task in group_tasks:
            for template in self.by_task(group_task):
                if template not in unique_templates:
                    unique_templates.append(template)
        yield from unique_templates
