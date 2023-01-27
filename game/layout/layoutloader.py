from __future__ import annotations
from collections import defaultdict

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
from game.data.groups import GroupRole
from game.layout.layout import (
    TgoLayout,
    TgoLayoutGroup,
    TgoLayoutUnitGroup,
    LayoutUnit,
    AntiAirLayout,
    BuildingLayout,
    NavalLayout,
    GroundForceLayout,
    DefensesLayout,
)
from game.layout.layoutmapping import LayoutMapping
from game.profiling import logged_duration
from game.version import VERSION

LAYOUT_DIR = "resources/layouts/"
LAYOUT_DUMP = "Liberation/layouts.p"

LAYOUT_TYPES = {
    GroupRole.AIR_DEFENSE: AntiAirLayout,
    GroupRole.BUILDING: BuildingLayout,
    GroupRole.NAVAL: NavalLayout,
    GroupRole.GROUND_FORCE: GroundForceLayout,
    GroupRole.DEFENSES: DefensesLayout,
}


class LayoutLoader:
    # Map of all available layouts indexed by name
    _layouts: dict[str, TgoLayout] = {}

    def __init__(self) -> None:
        self._layouts = {}

    def initialize(self) -> None:
        if not self._layouts:
            with logged_duration("Loading layouts"):
                self.load_templates()

    @property
    def layouts(self) -> Iterator[TgoLayout]:
        self.initialize()
        yield from self._layouts.values()

    def load_templates(self) -> None:
        """This will load all pre-loaded layouts from a pickle file.
        If pickle can not be loaded it will import and dump the layouts"""
        # We use a pickle for performance reasons. Importing takes many seconds
        file = Path(persistency.base_path()) / LAYOUT_DUMP
        if file.is_file():
            # Load from pickle if existing
            with file.open("rb") as f:
                try:
                    version, self._layouts = pickle.load(f)
                    # Check if the game version of the dump is identical to the current
                    if version == VERSION:
                        return
                except Exception as e:
                    logging.exception(f"Error {e} reading layouts dump. Recreating.")
        # If no dump is available or game version is different create a new dump
        self.import_templates()

    def import_templates(self) -> None:
        """This will import all layouts from the template folder
        and dumps them to a pickle"""
        self._layouts = {}
        mappings: dict[str, list[LayoutMapping]] = defaultdict(list)
        with logged_duration("Parsing mapping yamls"):
            for file in Path(LAYOUT_DIR).rglob("*.yaml"):
                if not file.is_file():
                    raise RuntimeError(f"{file.name} is not a file")
                with file.open("r", encoding="utf-8") as f:
                    mapping_dict = yaml.safe_load(f)

                template_map = LayoutMapping.from_dict(mapping_dict, f.name)
                mappings[template_map.layout_file].append(template_map)

        with logged_duration(f"Parsing all layout miz multithreaded"):
            with ThreadPoolExecutor() as exe:
                exe.map(self._load_from_miz, mappings.keys(), mappings.values())

        # Sort al the LayoutGroups with the correct index
        for layout in self._layouts.values():
            layout.groups.sort(key=lambda g: g.group_index)
            for group in layout.groups:
                group.unit_groups.sort(key=lambda ug: ug.unit_index)

        logging.info(f"Imported {len(self._layouts)} layouts")
        self._dump_templates()

    def _dump_templates(self) -> None:
        file = Path(persistency.base_path()) / LAYOUT_DUMP
        dump = (VERSION, self._layouts)
        with file.open("wb") as fdata:
            pickle.dump(dump, fdata)

    def _load_from_miz(self, miz: str, mappings: list[LayoutMapping]) -> None:
        template_position: dict[str, Point] = {}
        temp_mis = dcs.Mission()
        with logged_duration(f"Parsing {miz}"):
            # The load_file takes a lot of time to compute. That's why the layouts
            # are written to a pickle and can be reloaded from the ui
            # Example the whole routine: 0:00:00.934417,
            # the .load_file() method: 0:00:00.920409
            temp_mis.load_file(miz)

        for mapping in mappings:
            # Find the group from the mapping in any coalition
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
                        g_id, u_id, group_name, group_mapping = mapping.group_for_name(
                            dcs_group.name
                        )
                    except KeyError:
                        continue

                    if not isinstance(dcs_group, StaticGroup) and max(
                        group_mapping.unit_count
                    ) > len(dcs_group.units):
                        logging.error(
                            f"Incorrect unit_count found in Layout {mapping.name}-{group_mapping.name}"
                        )

                    layout = self._layouts.get(mapping.name, None)
                    if layout is None:
                        # Create a new template
                        layout = LAYOUT_TYPES[mapping.primary_role](
                            mapping.name, mapping.description
                        )
                        layout.generic = mapping.generic
                        layout.tasks = mapping.tasks
                        self._layouts[layout.name] = layout
                    for i, unit in enumerate(dcs_group.units):
                        unit_group = None
                        for _unit_group in layout.all_unit_groups:
                            if _unit_group.name == group_mapping.name:
                                # We already have a layoutgroup for this dcs_group
                                unit_group = _unit_group
                        if not unit_group:
                            unit_group = TgoLayoutUnitGroup(
                                group_mapping.name,
                                [],
                                group_mapping.unit_count,
                                group_mapping.unit_types,
                                group_mapping.unit_classes,
                                group_mapping.fallback_classes,
                                u_id,
                            )
                            unit_group.optional = group_mapping.optional
                            unit_group.fill = group_mapping.fill
                            unit_group.sub_task = group_mapping.sub_task
                            tgo_group = None
                            for _tgo_group in layout.groups:
                                if _tgo_group.group_name == group_name:
                                    tgo_group = _tgo_group
                            if tgo_group is None:
                                tgo_group = TgoLayoutGroup(group_name, g_id)
                                layout.groups.append(tgo_group)
                            tgo_group.unit_groups.append(unit_group)
                        layout_unit = LayoutUnit.from_unit(unit)
                        if i == 0 and layout.name not in template_position:
                            template_position[layout.name] = unit.position
                        layout_unit.position = (
                            layout_unit.position - template_position[layout.name]
                        )
                        unit_group.layout_units.append(layout_unit)

    def by_name(self, name: str) -> TgoLayout:
        self.initialize()
        return self._layouts[name]
