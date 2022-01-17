from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Iterator

from tabulate import tabulate

import dcs
from dcs import Point

from game import Game
from game.campaignloader import CampaignAirWingConfig
from game.db import FACTIONS
from game.missiongenerator.tgogenerator import (
    GroundObjectGenerator,
)
from game.point_with_heading import PointWithHeading
from game.settings import Settings
from game.theater import CaucasusTheater, OffMapSpawn
from game.unitmap import UnitMap
from game.utils import Heading

# from gen.to_remove.armored_group_generator import (
#     FixedSizeArmorGroupGenerator,
#     FixedSizeArmorGroupGeneratorWithAA,
# )
# from gen.to_remove.carrier_group import (
#     CarrierGroupGenerator,
#     CarrierStrikeGroup8Generator,
# )
# from gen.to_remove.lha_group import LHAGroupGenerator
# from gen.to_remove.ship_group_generator import SHIP_MAP
# from gen.to_remove.coastal_group_generator import COASTAL_MAP
from gen.templates import (
    GroundObjectTemplates,
    TemplateCategory,
    GroupTemplate,
    UnitTemplate,
    TemplateEncoder,
    BuildingTemplate,
    TemplateRandomizer,
    TEMPLATE_TYPES,
)

# from gen.to_remove.missiles_group_generator import MISSILES_MAP
# from gen.to_remove.airdefensegroupgenerator import AirDefenseGroupGenerator
# from gen.to_remove.ewr_group_generator import EWR_MAP
# from gen.to_remove.ewrs import EwrGenerator
# from gen.to_remove.sam_group_generator import SAM_MAP
from qt_ui import liberation_install


TEMPLATES_MIZ = "resources/templates/templates.miz"
MIGRATE_MIZ = "resources/tools/groundobject_templates.miz"
TEMPLATES_BLOB = "resources/templates/templates.json"
TEMPLATES_MAP = "resources/templates/template_map.json"
TABLE_FILE = "doc/templates/template_list.md"


@dataclass
class GroupTemplateMapping:
    name: str
    optional: bool
    randomizer: Optional[TemplateRandomizer] = None

    def to_json(self) -> dict[str, Any]:
        d = self.__dict__
        if not self.optional:
            d.pop("optional")
        if not self.randomizer:
            d.pop("randomizer")
        return d

    @staticmethod
    def from_dict(d: dict[str, Any]) -> GroupTemplateMapping:
        randomizer = (
            TemplateRandomizer.from_dict(d["randomizer"]) if "randomizer" in d else None
        )
        optional = d["optional"] if "optional" in d else False
        return GroupTemplateMapping(d["name"], optional, randomizer)


@dataclass
class TemplateMapping:
    name: str
    template_type: str
    description: str
    groups: list[GroupTemplateMapping]
    statics: list[str]
    static_mapping: Optional[GroupTemplateMapping] = None

    def to_json(self) -> dict[str, Any]:
        d = self.__dict__
        if not self.static_mapping:
            d.pop("static_mapping")
        return d

    @staticmethod
    def from_dict(d: dict[str, Any]) -> TemplateMapping:
        groups = [GroupTemplateMapping.from_dict(group) for group in d["groups"]]
        static_mapping = (
            GroupTemplateMapping.from_dict(d["static_mapping"])
            if "static_mapping" in d
            else None
        )
        return TemplateMapping(
            d["name"],
            d["template_type"],
            d["description"],
            groups,
            d["statics"],
            static_mapping,
        )


class TemplateMap:
    _map: dict[str, list[TemplateMapping]] = {}

    def __init__(self):
        self._map = {}

    def __getitem__(self, item: str) -> list[TemplateMapping]:
        return self._map[item]

    def __setitem__(self, key, value) -> None:
        self._map[key] = value

    def to_json(self) -> dict[str, Any]:
        return self._map

    def mapping_for_template(self, template_name: str) -> tuple[str, TemplateMapping]:
        for category, mappings in self._map.items():
            for mapping in mappings:
                if mapping.name == template_name:
                    return category, mapping
        raise RuntimeError(f"No mapping for template {template_name}")

    def mapping_for_group(
        self, group_name: str
    ) -> tuple[str, TemplateMapping, Optional[GroupTemplateMapping]]:
        for category, mappings in self._map.items():
            for mapping in mappings:
                for group_mapping in mapping.groups:
                    if group_mapping.name == group_name:
                        return category, mapping, group_mapping
                if group_name in mapping.statics:
                    return category, mapping, mapping.static_mapping
        raise RuntimeError(f"No mapping for group {group_name}")

    @property
    def mappings(self) -> Iterator[TemplateMapping]:
        for mapping in self._map.values():
            yield mapping


def import_templates(
    miz_file: str, template_map_file: str, target_file: str, table_file: str
) -> None:
    """Imports the template miz and the template_map as json into liberation"""
    temp_mis = dcs.Mission()
    temp_mis.load_file(miz_file)

    templates = GroundObjectTemplates()

    with open(template_map_file, "r") as f:
        template_map_json = json.load(f)

    template_map = TemplateMap()
    for name, mappings in template_map_json.items():
        template_map[TemplateCategory(name)] = []
        for mapping in mappings:
            template_map[TemplateCategory(name)].append(
                TemplateMapping.from_dict(mapping)
            )

    template_position: dict[str, Point] = {}
    for static_group in temp_mis.country("USA").static_group:
        category, mapping, group_mapping = template_map.mapping_for_group(
            static_group.name
        )
        template = templates.by_category_and_name(
            TemplateCategory(category), mapping.name
        )
        static_template = None
        if not template:
            template = BuildingTemplate(
                mapping.name, mapping.template_type, mapping.description
            )
            static_template = GroupTemplate(mapping.name, [], True)
            if group_mapping:
                static_template.randomizer = group_mapping.randomizer
                static_template.optional = group_mapping.optional
            template.groups.append(static_template)
            templates.add_template(TemplateCategory(category), template)

        else:
            for group in template.groups:
                if mapping.name in group.name:
                    static_template = group

        if not static_template:
            raise RuntimeError(f"No mapping for group {static_group.name}")

        for i, unit in enumerate(static_group.units):
            unit_template = UnitTemplate.from_unit(unit)
            if i == 0 and template.name not in template_position:
                template_position[template.name] = unit.position
            unit_template.position = (
                unit_template.position - template_position[template.name]
            )
            static_template.units.append(unit_template)
        pass

    for vehicle_group in (
        temp_mis.country("USA").vehicle_group + temp_mis.country("USA").ship_group
    ):
        category, mapping, group_mapping = template_map.mapping_for_group(
            vehicle_group.name
        )
        template = templates.by_category_and_name(
            TemplateCategory(category), mapping.name
        )
        if not template:
            template = TEMPLATE_TYPES[TemplateCategory(category)](
                mapping.name, mapping.template_type, mapping.description
            )
            templates.add_template(TemplateCategory(category), template)
        for i, unit in enumerate(vehicle_group.units):
            group_template = None
            for group in template.groups:
                if group.name == vehicle_group.name:
                    group_template = group
            if not group_template:
                group_template = GroupTemplate(
                    vehicle_group.name,
                    [],
                    False,
                    group_mapping.randomizer,
                    group_mapping.optional,
                )
                template.groups.append(group_template)
            unit_template = UnitTemplate.from_unit(unit)
            if i == 0 and template.name not in template_position:
                template_position[template.name] = unit.position
            unit_template.position = (
                unit_template.position - template_position[template.name]
            )
            group_template.units.append(unit_template)
        pass

    with open(target_file, "w") as f:
        json.dump(templates.to_json(), f, cls=TemplateEncoder, indent="\t")

    # print Table
    print_table(target_file, table_file)


def export_templates(
    templates_file: str, miz_file: str, template_map_file: str
) -> None:
    """Exports the templates.json to the templates.miz and the mapping"""
    # This function will only be used on mass jobs or specific fine tuning

    templates = GroundObjectTemplates.from_json(templates_file)

    # Prepare game
    theater = CaucasusTheater()
    initial_ground_position = Point(-500000, 250000)
    initial_water_position = Point(-350000, 250000)
    control_point_ground = OffMapSpawn(1, "Spawn Ground", initial_ground_position, True)
    control_point_water = OffMapSpawn(2, "Spawn Water", initial_water_position, True)
    theater.add_controlpoint(control_point_ground)
    theater.add_controlpoint(control_point_water)

    game = Game(
        FACTIONS["Bluefor Modern"],
        FACTIONS["Russia 2010"],
        theater,
        CampaignAirWingConfig({control_point_ground: [], control_point_water: []}),
        datetime.today(),
        Settings(),
        10000,
        10000,
    )

    m = dcs.Mission(game.theater.terrain)
    country = m.country("USA")
    unit_map = UnitMap()

    template_map = TemplateMap()
    offset_x = 0
    offset_y = 0

    for count, template_category in enumerate(TemplateCategory):
        template_map[template_category.value] = []
        temmplates_for_category = list(templates.for_category(template_category))

        # Define the offset / separation
        category_separation = 10000
        group_separation = 5000

        if template_category in [TemplateCategory.Naval]:
            initial_position = initial_water_position
            control_point = control_point_water
        else:
            initial_position = initial_ground_position
            control_point = control_point_ground

        current_separation = offset_y + category_separation
        offset_x = 0
        offset_y = current_separation
        max_cols = int(math.sqrt(len(temmplates_for_category)))
        for template in temmplates_for_category:
            mapping = TemplateMapping(
                template.name,
                template.template_type,
                template.description,
                [],
                [],
            )
            position = Point(
                initial_position.x + offset_x, initial_position.y + offset_y
            )

            # Initialize the template
            for group_template in template.groups:
                if group_template.randomizer:
                    group_template.randomizer.init_randomization_for_faction(
                        game.blue.faction
                    )

            ground_object = template.generate(
                template.name,
                PointWithHeading.from_point(position, Heading.from_degrees(0)),
                control_point,
                game,
                False,  # Do not use randomization during export!
            )

            for g_id, group in enumerate(ground_object.groups):
                group.name = f"{template.name} {g_id}"
                for u_id, unit in enumerate(group.units):
                    unit.name = f"{template.name} {g_id}-{u_id}"
                group_template = template.groups[g_id]
                group_mapping = GroupTemplateMapping(
                    group.name, group_template.optional, group_template.randomizer
                )
                if group.static_group:
                    for unit in group.units:
                        mapping.statics.append(unit.name)
                    # No mapping as we have no randomization yet
                else:
                    mapping.groups.append(group_mapping)

            generator = GroundObjectGenerator(ground_object, country, game, m, unit_map)
            generator.generate(unique_name=False)  # Prevent the ID prefix

            if ((offset_y - current_separation) / group_separation) < max_cols:
                offset_y += group_separation
            else:
                offset_y = current_separation
                offset_x += group_separation

            template_map[template_category.name].append(mapping)
    # Dump the template_map as json
    with open(template_map_file, "w") as f:
        json.dump(template_map, f, cls=TemplateEncoder, sort_keys=True, indent="\t")

    m.save(miz_file)


def print_table(templates_file: str, table_file: str) -> None:
    # Category # Sub Category # Template Name # Unit_types

    templates = GroundObjectTemplates.from_json(templates_file)
    table = []

    for template_category in TemplateCategory:
        category_templates = list(templates.for_category(template_category))
        for template in sorted(
            category_templates, key=lambda x: (x.template_type, x.name)
        ):
            groups = []
            options = []
            for group in template.groups:
                units = []
                group_options = []
                for unit in group.units:
                    units.append(unit.type)
                groups.append("<li>" + ", ".join(units) + "</li>")
                if group.randomizer:
                    # Add More info about the randomizer?
                    group_options.append("Randomizer")
                if group.static:
                    group_options.append("Static")
                if group_options:
                    options.append("<li>" + ", ".join(group_options) + "</li>")
            table.append(
                [
                    template_category.value,
                    template.template_type,
                    template.name,
                    "<ul>" + "".join(groups) + "</ul>",
                    "<ul>" + "".join(options) + "</ul>",
                ]
            )

    table_str = tabulate(
        table,
        headers=["Category", "Sub-Category", "Template", "Groups & Units", "Options"],
        tablefmt="github",
    )

    with open(table_file, "w", encoding="utf-8") as fdata:
        fdata.write(table_str)


def replace(string: str, replacement) -> str:
    for old_name, new_name in replacement:
        string = string.replace(old_name, new_name)
    return string


def update_factions(generator_names) -> None:
    folder: Path = Path("./resources/factions/")
    factions = [f for f in folder.glob("*.json") if f.is_file()]
    for f in factions:
        with open(f, "r", encoding="utf-8") as fdata:
            data = json.load(fdata)

        updated_faction = {}
        for key, item in data.items():
            if isinstance(item, list):
                updated = []
                for string in item:
                    updated.append(replace(string, generator_names))
                updated_faction[key] = updated
            elif isinstance(item, str):
                updated_faction[key] = replace(item, generator_names)
            else:
                updated_faction[key] = item

        with open(f, "w", encoding="utf-8") as fdata:
            json.dump(updated_faction, fdata, indent=2)

    print("\n \n Faction Updates:")
    print(
        tabulate(
            generator_names,
            headers=["Previous Value", "New Value"],
            tablefmt="github",
        )
    )


# def migrate_generators_to_templates(
#     input_miz: str,
#     templates_file: str,
#     miz_file: str,
#     template_map_file: str,
#     table_file: str,
# ) -> None:
#
#     templates = GroundObjectTemplates()
#
#     theater = CaucasusTheater()
#
#     initial_position = Point(0, 0)
#     control_point = OffMapSpawn(1, "Spawn", initial_position, True)
#     theater.add_controlpoint(control_point)
#
#     game = Game(
#         FACTIONS["Bluefor Modern"],
#         FACTIONS["Russia 2010"],
#         theater,
#         CampaignAirWingConfig({control_point: []}),
#         datetime.today(),
#         Settings(),
#         10000,
#         10000,
#     )
#
#     generators: dict[TemplateCategory, dict[str, Any]] = {
#         TemplateCategory.AirDefence: SAM_MAP,
#         TemplateCategory.Naval: SHIP_MAP,
#         TemplateCategory.Missile: MISSILES_MAP,
#         TemplateCategory.Coastal: COASTAL_MAP,
#         TemplateCategory.Armor: {},
#     }
#
#     # Only use one EWR generator. The differnt units will be placed as randomizer
#     generators[TemplateCategory.AirDefence]["EWRGenerator"] = EwrGenerator
#
#     generators[TemplateCategory.Naval]["CarrierGroupGenerator"] = CarrierGroupGenerator
#     generators[TemplateCategory.Naval][
#         "CarrierStrikeGroup8Generator"
#     ] = CarrierStrikeGroup8Generator
#     generators[TemplateCategory.Naval]["LHAGroupGenerator"] = LHAGroupGenerator
#     generators[TemplateCategory.Armor][
#         "RandomArmorGroup"
#     ] = FixedSizeArmorGroupGenerator
#     generators[TemplateCategory.Armor][
#         "RandomArmorGroupWithAA"
#     ] = FixedSizeArmorGroupGeneratorWithAA
#
#     generator_names = []
#
#     for category, template_generators in generators.items():
#         for generator_name, generator_class in template_generators.items():
#             # Just reuse SamGroundObject to make it easy
#             ground_object = SamGroundObject(
#                 namegen.random_objective_name(),
#                 initial_position,
#                 control_point,
#             )
#
#             if category in (
#                 TemplateCategory.Naval,
#                 TemplateCategory.Missile,
#                 TemplateCategory.Coastal,
#             ):
#                 generator = generator_class(game, ground_object, game.blue.faction)
#             elif category == TemplateCategory.Armor:
#                 unit_type = next(
#                     GroundUnitType.for_dcs_type(dcs.vehicles.Armor.M_1_Abrams)
#                 )
#                 generator = generator_class(
#                     game,
#                     ground_object,
#                     unit_type,
#                     # Create a group of 8 Armored Vehicles
#                     8,
#                 )
#             else:
#                 generator = generator_class(game, ground_object)
#
#             # Generate the DCS Groups
#             generator.generate()
#
#             if isinstance(generator, EwrGenerator):
#                 template = AirDefenceTemplate("Early-Warning Radar", "EWR")
#             elif isinstance(generator, AirDefenseGroupGenerator):
#                 template = AirDefenceTemplate(generator.name, generator.range().name)
#             elif generator_name in MISSILES_MAP:
#                 template = MissileTemplate(generator_name, category.name)
#             elif generator_name in COASTAL_MAP:
#                 template = CoastalTemplate(generator_name, category.name)
#             elif category == TemplateCategory.Naval:
#                 if generator_name == "CarrierGroupGenerator":
#                     template = NavalTemplate("Carrier Group", "carrier")
#                 elif generator_name == "CarrierStrikeGroup8Generator":
#                     template = NavalTemplate("Carrier Strike Group 8", "carrier")
#                 elif generator_name == "LHAGroupGenerator":
#                     template = NavalTemplate("LHA Group", "lha")
#                 else:
#                     template = NavalTemplate(generator_name, "ship")
#             elif category == TemplateCategory.Armor:
#                 if generator_name == "RandomArmorGroup":
#                     template = ArmorTemplate("Armor Group", "armor")
#                 elif generator_name == "RandomArmorGroupWithAA":
#                     template = ArmorTemplate("Armor Group with Anti-Air", "armor_aa")
#             else:
#                 raise RuntimeError("Generator handling missing")
#
#             groups = list(generator.groups)
#
#             # These have to be identical!
#             for i, group in enumerate(groups):
#                 for j, unit in enumerate(group.units):
#                     unit.name = f"{template.name} {i}-{j}"
#
#                 group_template = GroupTemplate(
#                     f"{template.name} #{str(i)}",
#                     [UnitTemplate.from_unit(unit) for unit in group.units],
#                 )
#
#                 if generator_name in [
#                     "CarrierGroupGenerator",
#                     "CarrierStrikeGroup8Generator",
#                 ]:
#                     if i == 0:
#                         group_template.randomizer = TemplateRandomizer(
#                             [0], 1, ["aircraft_carrier"]
#                         )
#                     elif i == 1:
#                         count = (
#                             5 if generator_name == "CarrierStrikeGroup8Generator" else 4
#                         )
#                         group_template.randomizer = TemplateRandomizer(
#                             [], count, ["destroyers"]
#                         )
#                 elif generator_name == "LHAGroupGenerator":
#                     if i == 0:
#                         group_template.randomizer = TemplateRandomizer(
#                             [0], 1, ["helicopter_carrier"]
#                         )
#                     elif i == 1:
#                         group_template.randomizer = TemplateRandomizer(
#                             [], 2, ["destroyers"]
#                         )
#                 elif generator_name == "RandomArmorGroup" and i == 0:
#                     group_template.randomizer = TemplateRandomizer(
#                         [],
#                         [2, 6],
#                         ["frontline_units"],
#                         ["APC", "ATGM", "IFV", "Tank"],
#                     )
#                 elif generator_name == "RandomArmorGroupWithAA":
#                     if i == 0:
#                         group_template.randomizer = TemplateRandomizer(
#                             [],
#                             [2, 6],
#                             ["frontline_units"],
#                             ["APC", "ATGM", "IFV", "Tank"],
#                         )
#                     elif i == 1:
#                         group_template.randomizer = TemplateRandomizer(
#                             [],
#                             [1, 2],
#                             ["frontline_units", "infantry_units"],
#                             ["SHORADS", "MANPADS"],
#                         )
#                         group_template.optional = True
#                 elif generator_name == "EWRGenerator" and i == 0:
#                     for ewr_generator_name, ewr_generator in EWR_MAP.items():
#                         unit_type = next(
#                             GroundUnitType.for_dcs_type(ewr_generator.unit_type)
#                         )
#                         # Update all factions from generator to unit_type
#                         generator_names.append(
#                             [ewr_generator.unit_type.name, str(unit_type)]
#                         )
#                         # Update old generator names
#                         generator_names.append([ewr_generator_name, str(unit_type)])
#
#                     group_template.randomizer = TemplateRandomizer(
#                         [],
#                         1,
#                         ["ewrs"],  # Randomization based on faction template
#                     )
#
#                 template.groups.append(group_template)
#
#             templates.add_template(category, template)
#             generator_names.append([generator_name, template.name])
#
#     # Load the basic templates
#     temp_mis = dcs.Mission()
#     temp_mis.load_file(input_miz)
#
#     position_for_template: dict[str, Point] = {}
#     group_for_template: dict[str, GroupTemplate] = {}
#     for static_group in (
#         temp_mis.country("USA").static_group
#         + temp_mis.country("USAF Aggressors").static_group
#     ):
#         # Naming is: fob1 #001 -> name: fob1, category fob, group_name: fob1 #001
#         template_name = str(static_group.name).split()[0]
#         category_name, idx = template_name[:-1], int(template_name[-1])
#
#         template = templates.by_name(template_name)
#         if not template:
#             template = BuildingTemplate(template_name, category_name)
#
#             # Store original position to make the template relative to TGO later
#             position_for_template[template_name] = static_group.position
#
#             # Create Group Template for the satic group. Within Liberation we map
#             # static units in groups even if dcs can not handle this. The dcs specific
#             # handling will happpen later in miz generation again.
#             group_template = GroupTemplate(f"{template.name}", [], True)
#             group_for_template[template_name] = group_template
#             template.groups.append(group_template)
#
#             templates.add_template(TemplateCategory.Building, template)
#
#         for u_id, unit in enumerate(static_group.units):
#             unit_template = UnitTemplate.from_unit(unit)
#             unit_template.position = Point(
#                 int(unit_template.position.x - position_for_template[template_name].x),
#                 int(unit_template.position.y - position_for_template[template_name].y),
#             )
#             group_for_template[template_name].units.append(unit_template)
#
#     # Dump the template_map as json
#     with open(templates_file, "w") as f:
#         json.dump(templates.to_json(), f, cls=TemplateEncoder, indent=4)
#
#     # Update Faction files
#     update_factions(generator_names)
#

    print(
        "Migrate successful. To finish the migration also run export followed by an import again."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    my_group = parser.add_mutually_exclusive_group(required=True)
    my_group.add_argument(
        "-i",
        "--import",
        dest="Import",
        help="Imports the templates from the miz into liberation",
        action="store_true",
    )
    my_group.add_argument(
        "-e",
        "--export",
        dest="Export",
        help="Exports the templates from liberation to the miz",
        action="store_true",
    )
    my_group.add_argument(
        "-m",
        "--migrate",
        dest="Migrate",
        help="Migrates generators and the current ground object templates to the new system",
        action="store_true",
    )
    my_group.add_argument(
        "-t",
        "--table",
        dest="Table",
        help="Prints a table of all templates",
        action="store_true",
    )

    parser.add_argument(
        "--template_miz", default=TEMPLATES_MIZ, help="Set the template mission (.miz)"
    )
    parser.add_argument(
        "--target_file", default=TEMPLATES_BLOB, help="Set the target file"
    )
    parser.add_argument(
        "--template_map", default=TEMPLATES_MAP, help="Set the template map"
    )
    parser.add_argument(
        "--migrate_file", default=MIGRATE_MIZ, help="Set the migrate mission"
    )
    parser.add_argument(
        "--table_file",
        default=TABLE_FILE,
        help="Output file for template documentation",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    liberation_install.init()

    miz_file = args.template_miz
    target_file = args.target_file
    migrate_file = args.migrate_file
    template_map = args.template_map
    table_file = args.table_file

    if args.Import:
        import_templates(miz_file, template_map, target_file, table_file)
    elif args.Export:
        export_templates(target_file, miz_file, template_map)
    elif args.Table:
        print_table(target_file, table_file)
    # elif args.Migrate:
    #     migrate_generators_to_templates(
    #         migrate_file, target_file, miz_file, template_map, table_file
    #     )


if __name__ == "__main__":
    main()
