from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Iterator

import yaml
from dcs.ships import ship_map
from dcs.unit import Unit
from dcs.vehicles import vehicle_map
from tabulate import tabulate

import dcs
from dcs import Point

from game import Game, db
from game.campaignloader import CampaignAirWingConfig
from game.data.groups import GroupRole, GroupTask, ROLE_TASKINGS
from game.data.units import UnitClass
from game.db import FACTIONS
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.missiongenerator.tgogenerator import (
    GroundObjectGenerator,
)
from game.point_with_heading import PointWithHeading
from game.settings import Settings
from game.theater import CaucasusTheater, OffMapSpawn
from game.theater.start_generator import GameGenerator, GeneratorSettings, ModSettings
from game.theater.theatergroundobject import AirDefenseRange, SamGroundObject
from game.unitmap import UnitMap
from game.utils import Heading
from gen.templates import (
    GroundObjectTemplates,
    GroupTemplate,
    UnitTemplate,
    BuildingTemplate,
    DefensesTemplate,
    NavalTemplate,
    TemplateMapping,
    GroupTemplateMapping,
    AntiAirTemplate,
    GroundForceTemplate,
)
from gen.naming import namegen
from qt_ui import liberation_install
from gen.to_remove.armored_group_generator import (
    FixedSizeArmorGroupGenerator,
    FixedSizeArmorGroupGeneratorWithAA,
)
from gen.to_remove.carrier_group import (
    CarrierGroupGenerator,
    CarrierStrikeGroup8Generator,
)
from gen.to_remove.lha_group import LHAGroupGenerator
from gen.to_remove.ship_group_generator import SHIP_MAP
from gen.to_remove.coastal_group_generator import COASTAL_MAP
from gen.to_remove.missiles_group_generator import MISSILES_MAP
from gen.to_remove.airdefensegroupgenerator import AirDefenseGroupGenerator
from gen.to_remove.ewr_group_generator import EWR_MAP
from gen.to_remove.ewrs import EwrGenerator
from gen.to_remove.sam_group_generator import SAM_MAP


TEMPLATES_MIZ = "resources/templates/legacy_templates.miz"
MIGRATE_MIZ = "resources/tools/groundobject_templates.miz"
TEMPLATES_FOLDER = "resources/templates/"
TABLE_FILE = "doc/templates/template_list.md"


def export_templates(
    miz_file: str, mapping_folder: str, templates: GroundObjectTemplates
) -> None:
    """Exports the migrated templates to the templates.miz and the mapping"""
    # Prepare game
    theater = CaucasusTheater()
    initial_ground_position = Point(-500000, 250000)
    initial_water_position = Point(-350000, 250000)
    control_point_ground = OffMapSpawn(1, "Spawn Ground", initial_ground_position, True)
    control_point_water = OffMapSpawn(2, "Spawn Water", initial_water_position, True)
    theater.add_controlpoint(control_point_ground)
    theater.add_controlpoint(control_point_water)

    generator = GameGenerator(
        FACTIONS["Bluefor Modern"],
        FACTIONS["Russia 2010"],
        theater,
        CampaignAirWingConfig({control_point_ground: [], control_point_water: []}),
        Settings(),
        GeneratorSettings(
            start_date=datetime.today(),
            player_budget=1000,
            enemy_budget=1000,
            inverted=False,
            no_carrier=False,
            no_lha=False,
            no_player_navy=False,
            no_enemy_navy=False,
        ),
        ModSettings(),
    )
    game = generator.generate()

    # TODO Define combined forces as country so that the missioneditor type is correct

    m = dcs.Mission(game.theater.terrain)
    country = m.country("USA")
    unit_map = UnitMap()

    offset_x = 0
    offset_y = 0

    for group_role in GroupRole:
        temmplates_for_category = list(templates.for_role_and_task(group_role))

        # Define the offset / separation
        category_separation = 10000
        group_separation = 5000

        if group_role == GroupRole.Naval:
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
                template.description,
                template.category,
                template.generic,
                group_role,
                template.tasks,
                [],
                miz_file,
            )
            position = Point(
                initial_position.x + offset_x, initial_position.y + offset_y
            )

            # Initialize the group template so that a unit can be selected
            for group in template.groups:
                game.blue.faction.initialize_group_template(group, False)

            ground_object = template.generate(
                template.name,
                PointWithHeading.from_point(position, Heading.from_degrees(0)),
                control_point,
                game,
                merge_groups=False,  # Do not merge groups for migration
            )

            for g_id, group in enumerate(ground_object.groups):
                group.name = f"{template.name} {g_id}"
                for u_id, unit in enumerate(group.units):
                    unit.name = f"{template.name} {g_id}-{u_id}"
                group_template = template.groups[g_id]
                group_mapping = GroupTemplateMapping(
                    group.name,
                    group_template.optional,
                    [unit.name for unit in group.units] if group.static_group else [],
                    group_template.group,
                    group_template.unit_count,
                    group_template.unit_types,
                    group_template.unit_classes,
                )
                mapping.groups.append(group_mapping)

            generator = GroundObjectGenerator(ground_object, country, game, m, unit_map)
            generator.generate(unique_name=False)  # Prevent the ID prefix

            if ((offset_y - current_separation) / group_separation) < max_cols:
                offset_y += group_separation
            else:
                offset_y = current_separation
                offset_x += group_separation

            # Export the mapping as yaml
            mapping.export(mapping_folder)

    m.save(miz_file)


def update_factions(generator_names) -> None:
    folder: Path = Path("./resources/factions/")
    factions = [f for f in folder.glob("*.json") if f.is_file()]
    for f in factions:
        with open(f, "r", encoding="utf-8") as fdata:
            data = fdata.read()

        with open(f, "w", encoding="utf-8") as fdata:
            for old_name, new_name in generator_names:
                new_name = new_name.replace('"', '\\"')
                data = data.replace(f'"{old_name}"', f'"{new_name}"')
            data = data.replace(f'"ewrs"', f'"air_defense_units"')
            fdata.write(data)

    print("\n \n Faction Updates:")
    print(
        tabulate(
            generator_names,
            headers=["Previous Value", "New Value"],
            tablefmt="github",
        )
    )


def migrate_generators_to_templates(
    input_miz: str,
    templates_miz: str,
    mapping_folder: str,
) -> None:

    templates = GroundObjectTemplates()

    theater = CaucasusTheater()

    initial_position = Point(0, 0)
    control_point = OffMapSpawn(1, "Spawn", initial_position, True)
    theater.add_controlpoint(control_point)

    game = Game(
        FACTIONS["Bluefor Modern"],
        FACTIONS["Russia 2010"],
        theater,
        CampaignAirWingConfig({control_point: []}),
        datetime.today(),
        Settings(),
        10000,
        10000,
    )

    generators: dict[GroupRole, dict[str, Any]] = {
        GroupRole.AntiAir: SAM_MAP,
        GroupRole.Naval: SHIP_MAP,
        GroupRole.Defenses: MISSILES_MAP | COASTAL_MAP,
        GroupRole.GroundForce: {},
    }

    aa_range_taskings = {
        AirDefenseRange.AAA: GroupTask.AAA,
        AirDefenseRange.Short: GroupTask.SHORAD,
        AirDefenseRange.Medium: GroupTask.MERAD,
        AirDefenseRange.Long: GroupTask.LORAD,
    }

    # Only use one EWR generator. The differnt units will be placed as randomizer
    generators[GroupRole.AntiAir]["EWRGenerator"] = EwrGenerator

    generators[GroupRole.Naval]["CarrierGroupGenerator"] = CarrierGroupGenerator
    generators[GroupRole.Naval][
        "CarrierStrikeGroup8Generator"
    ] = CarrierStrikeGroup8Generator
    generators[GroupRole.Naval]["LHAGroupGenerator"] = LHAGroupGenerator
    generators[GroupRole.GroundForce]["RandomArmorGroup"] = FixedSizeArmorGroupGenerator
    generators[GroupRole.GroundForce][
        "RandomArmorGroupWithAA"
    ] = FixedSizeArmorGroupGeneratorWithAA

    generator_names = []

    for category, template_generators in generators.items():
        for generator_name, generator_class in template_generators.items():
            # Just reuse SamGroundObject to make it easy
            ground_object = SamGroundObject(
                namegen.random_objective_name(),
                initial_position,
                Heading.from_degrees(0),
                control_point,
            )

            if category in (GroupRole.Naval, GroupRole.Defenses):
                generator = generator_class(game, ground_object, game.blue.faction)
            elif category == GroupRole.GroundForce:
                unit_type = next(
                    GroundUnitType.for_dcs_type(dcs.vehicles.Armor.M_1_Abrams)
                )
                generator = generator_class(
                    game,
                    ground_object,
                    unit_type,
                    # Create a group of 8 Armored Vehicles
                    8,
                )
            else:
                generator = generator_class(game, ground_object)

            # Generate the DCS Groups
            generator.generate()

            if isinstance(generator, EwrGenerator):
                template = AntiAirTemplate("Early-Warning Radar")
                template.tasks = [GroupTask.EWR]
            elif isinstance(generator, AirDefenseGroupGenerator):
                template = AntiAirTemplate(generator.name)
                template.tasks = [aa_range_taskings[generator.range()]]
            elif generator_name in MISSILES_MAP:
                template = DefensesTemplate(generator_name)
                template.tasks = [GroupTask.Missile]
            elif generator_name in COASTAL_MAP:
                template = DefensesTemplate(generator_name)
                template.tasks = [GroupTask.Coastal]
            elif category == GroupRole.Naval:
                if generator_name == "CarrierGroupGenerator":
                    template = NavalTemplate("Carrier Group")
                    template.tasks = [GroupTask.AircraftCarrier]
                elif generator_name == "CarrierStrikeGroup8Generator":
                    template = NavalTemplate("Carrier Strike Group 8")
                    template.tasks = [GroupTask.AircraftCarrier]
                elif generator_name == "LHAGroupGenerator":
                    template = NavalTemplate("LHA Group")
                    template.tasks = [GroupTask.HelicopterCarrier]
                else:
                    template = NavalTemplate(generator_name)
                    template.tasks = [GroupTask.Navy]
            elif category == GroupRole.GroundForce:
                if generator_name == "RandomArmorGroup":
                    template = GroundForceTemplate("Armor Group")
                    template.tasks = ROLE_TASKINGS[GroupRole.GroundForce]
                elif generator_name == "RandomArmorGroupWithAA":
                    template = GroundForceTemplate("Armor Group with Anti-Air")
                    template.tasks = ROLE_TASKINGS[GroupRole.GroundForce]
            else:
                raise RuntimeError("Generator handling missing")

            # Split groups by the unit_type
            units_of_type: dict[str, tuple[int, list[Unit]]] = {}
            for g_id, group in enumerate(generator.groups):
                for unit in group.units:
                    if unit.type in units_of_type:
                        units_of_type[unit.type][1].append(unit)
                    else:
                        units_of_type[unit.type] = (g_id + 1, [unit])

            i = 0
            for unit_type, data in units_of_type.items():
                g_id, units = data
                for j, unit in enumerate(units):
                    unit.name = f"{template.name} {i}-{j}"

                group_template = GroupTemplate(
                    f"{template.name} #{str(i)}",
                    [UnitTemplate.from_unit(unit) for unit in units],
                )

                # Save the group_id
                group_template.group = g_id

                if generator_name in [
                    "CarrierGroupGenerator",
                    "CarrierStrikeGroup8Generator",
                ]:
                    if i == 0:
                        group_template.unit_classes = [UnitClass.AircraftCarrier]
                        group_template.unit_count = [1]
                    elif i == 1:
                        group_template.unit_count = [
                            5 if generator_name == "CarrierStrikeGroup8Generator" else 4
                        ]
                        group_template.unit_classes = [UnitClass.Destroyer]
                    elif i == 2:
                        group_template.unit_count = [2]
                        group_template.unit_classes = [UnitClass.Cruiser]
                elif generator_name == "LHAGroupGenerator":
                    if i == 0:
                        group_template.unit_classes = [UnitClass.HelicopterCarrier]
                        group_template.unit_count = [1]
                    elif i == 1:
                        group_template.unit_count = [2]
                        group_template.unit_classes = [UnitClass.Destroyer]
                elif generator_name == "RandomArmorGroup" and i == 0:
                    group_template.unit_count = [2, 6]
                    group_template.unit_classes = [
                        UnitClass.Apc,
                        UnitClass.Atgm,
                        UnitClass.Ifv,
                        UnitClass.Tank,
                    ]
                elif generator_name == "RandomArmorGroupWithAA":
                    if i == 0:
                        group_template.unit_count = [2, 6]
                        group_template.unit_classes = [
                            UnitClass.Apc,
                            UnitClass.Atgm,
                            UnitClass.Ifv,
                            UnitClass.Tank,
                        ]
                    elif i == 1:
                        group_template.unit_count = [1, 2]
                        group_template.unit_classes = [
                            UnitClass.AAA,
                            UnitClass.SHORAD,
                            UnitClass.Manpad,
                        ]
                        group_template.optional = True
                elif generator_name == "EWRGenerator" and i == 0:
                    for ewr_generator_name, ewr_generator in EWR_MAP.items():
                        unit_type = next(
                            GroundUnitType.for_dcs_type(ewr_generator.unit_type)
                        )
                        # Update all factions from generator to unit_type
                        generator_names.append(
                            [ewr_generator.unit_type.name, str(unit_type)]
                        )
                        # Update old generator names
                        generator_names.append([ewr_generator_name, str(unit_type)])

                    group_template.unit_classes = [UnitClass.EWR, UnitClass.SR]
                    group_template.unit_count = [1]
                elif generator_name == "ChineseNavyGroupGenerator":
                    if i == 0:
                        group_template.unit_types = [unit_type]
                        group_template.unit_count = [0, 2]
                    if i == 1:
                        group_template.unit_count = [0, 2]
                        group_template.unit_types = ["Type_052C", "Type_052B"]
                elif generator_name == "RussianNavyGroupGenerator":
                    if i == 0:
                        group_template.unit_count = [0, 2]
                        group_template.unit_types = ["ALBATROS", "MOLNIYA"]
                    if i == 1:
                        group_template.unit_count = [0, 2]
                        group_template.unit_types = ["NEUSTRASH", "REZKY"]
                    if i == 2:
                        group_template.unit_count = [1]
                        group_template.unit_types = ["MOSCOW"]
                elif generator_name == "FlakGenerator" and i == 0:
                    group_template.unit_count = [4]
                    group_template.unit_types = [
                        "flak38",
                        "flak18",
                        "flak36",
                        "flak37",
                        "flak41",
                        "flak30",
                    ]
                elif generator_name == "V1GroupGenerator" and i == 2:
                    group_template.unit_types = ["flak38", "flak30"]
                elif generator_name == "SchnellbootGroupGenerator" and i == 0:
                    group_template.unit_types = [unit_type]
                    group_template.unit_count = [2, 4]
                elif generator_name == "UBoatGroupGenerator" and i == 0:
                    group_template.unit_types = [unit_type]
                    group_template.unit_count = [1, 4]
                else:
                    group_template.unit_types = [unit_type]
                    group_template.unit_count = [len(units)]

                template.groups.append(group_template)
                i += 1

            templates.add_template(category, template)
            generator_names.append([generator_name, template.name])

    # Load the basic templates
    temp_mis = dcs.Mission()
    temp_mis.load_file(input_miz)

    position_for_template: dict[str, Point] = {}
    group_for_template_and_type: dict[str, dict[str, GroupTemplate]] = {}
    for static_group in (
        temp_mis.country("USA").static_group
        + temp_mis.country("USAF Aggressors").static_group
    ):
        # Naming is: fob1 #001 -> name: fob1, category fob, group_name: fob1 #001
        template_name = str(static_group.name).split()[0]
        category_name, idx = template_name[:-1], int(template_name[-1])

        template = templates.by_name(template_name)
        if not template:
            template = BuildingTemplate(template_name)
            template.category = category_name
            # Store original position to make the template relative to TGO later
            position_for_template[template_name] = static_group.position
            templates.add_template(GroupRole.Building, template)
            group_for_template_and_type[template_name] = {}

        for unit in static_group.units:
            if unit.type not in group_for_template_and_type[template_name]:
                # Create Group Template for the satic group. Within Liberation we map
                # static units in groups even if dcs can not handle this. The dcs specific
                # handling will happpen later in miz generation again.
                is_static = False if unit.type in vehicle_map else True
                group_template = GroupTemplate(f"{template.name}", [], is_static)
                group_template.unit_types = [unit.type]
                group_template.unit_count = [0]
                group_for_template_and_type[template_name][unit.type] = group_template
                template.groups.append(group_template)
            else:
                group_template = group_for_template_and_type[template_name][unit.type]

            unit_template = UnitTemplate.from_unit(unit)
            unit_template.position = Point(
                int(unit_template.position.x - position_for_template[template_name].x),
                int(unit_template.position.y - position_for_template[template_name].y),
            )
            group_template.units.append(unit_template)
            group_template.unit_count = [group_template.unit_count[0] + 1]

    # Update Faction files
    update_factions(generator_names)

    # Export
    export_templates(templates_miz, mapping_folder, templates)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    my_group = parser.add_mutually_exclusive_group(required=True)
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
    my_group.add_argument(
        "-f",
        "--faction",
        dest="Faction",
        help="Updates all factions",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    liberation_install.init()

    if args.Table:
        export_template_list()
    elif args.Faction:
        migrate_factions()
    elif args.Migrate:
        migrate_generators_to_templates(MIGRATE_MIZ, TEMPLATES_MIZ, TEMPLATES_FOLDER)


def export_template_list() -> None:
    # Extrac UnitMaps from all templates: Units with the GroundUnitType name!
    templates = GroundObjectTemplates.from_folder(TEMPLATES_FOLDER)
    template_maps: dict[str, list[Any]] = {}
    missing_units = []
    for role, template in templates.templates:
        units = []
        for group in template.groups:
            group_units = []
            for unit_type in group.unit_types:
                try:
                    if unit_type in vehicle_map:
                        group_units.append(
                            next(
                                GroundUnitType.for_dcs_type(vehicle_map[unit_type])
                            ).name
                        )
                    elif unit_type in ship_map:
                        group_units.append(
                            next(ShipUnitType.for_dcs_type(ship_map[unit_type])).name
                        )
                    elif db.static_type_from_name(unit_type):
                        group_units.append(unit_type)
                    continue
                except StopIteration:
                    pass
                missing_units.append(unit_type)
            if group.unit_classes:
                group_units.append(
                    f"Classes = [ {', '.join(c.value for c in group.unit_classes)}]"
                )
            units.append(f"<li>{', '.join(group_units)}</li>")
        tasks = ", ".join(t.value for t in template.tasks)
        category = role.value + tasks

        if category not in template_maps:
            template_maps[category] = []

        template_maps[category].append(
            [
                role.value,
                tasks,
                template.name,
                "<ul>" + "".join(units) + "</ul>",
            ]
        )

    templates = [
        template for templates in template_maps.values() for template in templates
    ]

    templates.append(["Missing Units", ", ".join(set(missing_units))])

    table_str = tabulate(
        templates,
        headers=[
            "Role",
            "Tasks",
            "Template Name",
            "Units",
        ],
        tablefmt="github",
    )

    with open(TABLE_FILE, "w", encoding="utf-8") as fdata:
        fdata.write(table_str)


@dataclass
class MigratedTemplate:
    original_key: str
    new_key: str
    original_value: str
    new_value: str


def migrate_factions() -> None:
    # List of all currently migrated templates
    migrated_templates: list[MigratedTemplate] = [
        MigratedTemplate("air_defenses", "preset_groups", "Hawk Site", "Hawk"),
        MigratedTemplate(
            "air_defenses", "preset_groups", "SA-5/S-200 Site", "SA-5/S-200"
        ),
        MigratedTemplate(
            "air_defenses",
            "preset_groups",
            "SA-5/S-200 Site wit FlatFace SR",
            "SA-5/S-200",
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "SA-2/S-75 Site", "SA-2/S-75"
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "SA-3/S-125 Site", "SA-3/S-125"
        ),
        MigratedTemplate("air_defenses", "preset_groups", "SA-6 Kub Site", "SA-6"),
        MigratedTemplate("air_defenses", "preset_groups", "SA-11 Buk Battery", "SA-11"),
        MigratedTemplate("air_defenses", "preset_groups", "Rapier AA Site", "Rapier"),
        MigratedTemplate("air_defenses", "preset_groups", "Roland Site", "Roland"),
        MigratedTemplate("air_defenses", "preset_groups", "Patriot Battery", "Patriot"),
        MigratedTemplate("air_defenses", "preset_groups", "HQ-7 Site", "HQ-7"),
        MigratedTemplate(
            "air_defenses",
            "preset_groups",
            "SA-10/S-300PS Battery - With ZSU-23",
            "SA-10/S-300PS",
        ),
        MigratedTemplate(
            "air_defenses",
            "preset_groups",
            "SA-10/S-300PS Battery - With SA-15 PD",
            "SA-10/S-300PS",
        ),
        MigratedTemplate(
            "air_defenses",
            "preset_groups",
            "SA-10/S-300PS Battery - With SA-15 PD & SA-19 SHORAD",
            "SA-10/S-300PS",
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "SA-10B/S-300PS Battery", "SA-10B/S-300PS"
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "SA-17 Grizzly Battery", "SA-17"
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "SA-12/S-300V Battery", "SA-12/S-300V"
        ),
        MigratedTemplate(
            "air_defenses",
            "preset_groups",
            "SA-20/S-300PMU-1 Battery",
            "SA-20/S-300PMU-1",
        ),
        MigratedTemplate(
            "air_defenses",
            "preset_groups",
            "SA-20B/S-300PMU-2 Battery",
            "SA-20B/S-300PMU-2",
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "SA-23/S-300VM Battery", "SA-23/S-300VM"
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "NASAMS AIM-120B", "NASAMS AIM-120B"
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "NASAMS AIM-120C", "NASAMS AIM-120C"
        ),
        MigratedTemplate("air_defenses", "preset_groups", "KS-19 AAA Site", "KS-19"),
        MigratedTemplate(
            "air_defenses", "preset_groups", "Cold War Flak Site", "Cold-War-Flak"
        ),
        MigratedTemplate(
            "air_defenses", "preset_groups", "Early Cold War Flak Site", "Cold-War-Flak"
        ),
        MigratedTemplate("air_defenses", "preset_groups", "Flak Site", "Flak"),
        MigratedTemplate(
            "air_defenses", "preset_groups", "WW2 Ally Flak Site", "Ally Flak"
        ),
        MigratedTemplate("air_defenses", "preset_groups", "Freya EWR Site", "Freya"),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "Vulcan Group",
            "M163 Vulcan Air Defense System",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "Avenger Group",
            "M1097 Heavy HMMWV Avenger",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "Chaparral Group",
            "M48 Chaparral",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "Gepard Group",
            "Flakpanzer Gepard",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "Linebacker Group",
            "M6 Linebacker",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "SA-8 OSA Site",
            'SAM SA-8 Osa "Gecko" TEL',
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "SA-9 Group",
            "SA-9 Strela",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "SA-13 Strela Group",
            "SA-13 Gopher (9K35 Strela-10M3)",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "SA-15 Tor Group",
            "SA-15 Tor",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "SA-19 Tunguska Group",
            "SA-19 Grison (2K22 Tunguska)",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "Bofors AAA",
            "Bofors 40 mm Gun",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "ZU-23 Group",
            "AAA ZU-23 Closed Emplacement",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "ZU-23 Ural Group",
            "ZU-23 on Ural-375",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "ZU-23 Ural Insurgent Group",
            "ZU-23 on Ural-375",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "Zu-23 Site",
            "AAA ZU-23 Insurgent Closed Emplacement",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "ZSU-23 Group",
            "ZSU-23-4 Shilka",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "WW2 Flak Site",
            "8.8 cm Flak 18",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "ZSU-57-2 Group",
            "ZSU-57-2 'Sparka'",
        ),
        MigratedTemplate(
            "air_defenses",
            "air_defense_units",
            "WW2 Flak Site",
            "8.8 cm Flak 18",
        ),
        MigratedTemplate(
            "missiles",
            "missiles",
            "V1GroupGenerator",
            "V-1 Launch Ramp",
        ),
        MigratedTemplate(
            "missiles",
            "missiles",
            "ScudGenerator",
            "SSM SS-1C Scud-B",
        ),
        MigratedTemplate(
            "coastal_defenses",
            "preset_groups",
            "SilkwormGenerator",
            "Silkworm",
        ),
        MigratedTemplate(
            "navy_generators",
            "destroyers",
            "Type54GroupGenerator",
            "Type 054A Frigate",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "Type54GroupGenerator",
            "Type 054A Frigate",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "SchnellbootGroupGenerator",
            "Boat Schnellboot type S130",
        ),
        MigratedTemplate(
            "navy_generators",
            "preset_groups",
            "WW2LSTGroupGenerator",
            "WW2LST",
        ),
        MigratedTemplate(
            "navy_generators",
            "preset_groups",
            "ChineseNavyGroupGenerator",
            "Chinese Navy",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "UBoatGroupGenerator",
            "U-boat VIIC U-flak",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "OliverHazardPerryGroupGenerator",
            "FFG Oliver Hazard Perry",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "ArleighBurkeGroupGenerator",
            "DDG Arleigh Burke IIa",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "GrishaGroupGenerator",
            "Corvette 1124.4 Grish",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "MolniyaGroupGenerator",
            "Corvette 1241.1 Molniya",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "KiloSubGroupGenerator",
            "SSK 877V Kilo",
        ),
        MigratedTemplate(
            "navy_generators",
            "naval_units",
            "LaCombattanteIIGroupGenerator",
            "FAC La Combattante IIa",
        ),
        MigratedTemplate(
            "navy_generators",
            "preset_groups",
            "RussianNavyGroupGenerator",
            "Russian Navy",
        ),
        MigratedTemplate(
            "aircraft_carrier",
            "naval_units",
            "Forrestal",
            "CV-59 Forrestal",
        ),
        MigratedTemplate(
            "aircraft_carrier",
            "naval_units",
            "KUZNECOW",
            "CV 1143.5 Admiral Kuznetsov",
        ),
        MigratedTemplate(
            "helicopter_carrier",
            "naval_units",
            "LHA_Tarawa",
            "LHA-1 Tarawa",
        ),
        MigratedTemplate(
            "aircraft_carrier",
            "naval_units",
            "Stennis",
            "CVN-74 John C. Stennis",
        ),
        MigratedTemplate(
            "helicopter_carrier",
            "naval_units",
            "Type_071",
            "Type 071 Amphibious Transport Dock",
        ),
    ]
    # Find the "air_defenses" key remove the template name there
    folder: Path = Path("./resources/factions/")
    factions = [f for f in folder.glob("*.json") if f.is_file()]
    for f in factions:
        with open(f, "r", encoding="utf-8") as fdata:
            data = json.load(fdata)

        with open(f, "w", encoding="utf-8") as fdata:
            for migrated_template in migrated_templates:
                if migrated_template.new_key not in data:
                    new_faction = {}
                    for key, value in data.items():
                        new_faction[key] = value
                        if key == "preset_groups":
                            # Add New Key after air_defenses
                            new_faction[migrated_template.new_key] = []
                    data = new_faction
                if (
                    migrated_template.original_key in data
                    and migrated_template.original_value
                    in data[migrated_template.original_key]
                ):
                    data[migrated_template.original_key].remove(
                        migrated_template.original_value
                    )
                    if (
                        migrated_template.new_value
                        not in data[migrated_template.new_key]
                    ):
                        data[migrated_template.new_key].append(
                            migrated_template.new_value
                        )
            # Remove air_defenses and coastal if empty
            if "coastal_defenses" in data and len(data["coastal_defenses"]) == 0:
                data.pop("coastal_defenses")
            if "navy_generators" in data and len(data["navy_generators"]) == 0:
                data.pop("navy_generators")
            if "destroyers" in data:
                for unit in data["destroyers"]:
                    data["naval_units"].append(unit)
                data.pop("destroyers")
            if "cruisers" in data:
                for unit in data["cruisers"]:
                    data["naval_units"].append(unit)
                data.pop("cruisers")
            if "air_defenses" in data and len(data["air_defenses"]) == 0:
                data.pop("air_defenses")
            if "helicopter_carrier" in data and len(data["helicopter_carrier"]) == 0:
                data.pop("helicopter_carrier")
            if "aircraft_carrier" in data and len(data["aircraft_carrier"]) == 0:
                data.pop("aircraft_carrier")
            if "navy_group_count" in data:
                data.pop("navy_group_count")
            if "missiles_group_count" in data:
                data.pop("missiles_group_count")
            if "coastal_group_count" in data:
                data.pop("coastal_group_count")

            for key, value in data.items():
                # Remove duplicates
                if isinstance(value, list):
                    data[key] = []
                    [data[key].append(item) for item in value if item not in data[key]]

            json.dump(data, fdata, indent=2)


def list_units_without_class() -> None:
    folder: Path = Path("./resources/units/ground_units/")
    unit_files = [f for f in folder.glob("*.yaml") if f.is_file()]
    for f in unit_files:
        with f.open(encoding="utf-8") as data_file:
            data = yaml.safe_load(data_file)

        if data.get("class") is None:
            print(f)


if __name__ == "__main__":
    main()
