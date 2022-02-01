from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml
from dcs.ships import ship_map
from dcs.vehicles import vehicle_map
from tabulate import tabulate

from game import db
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from qt_ui import liberation_install


TABLE_FILE = "doc/templates/template_list.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    my_group = parser.add_mutually_exclusive_group(required=True)
    my_group.add_argument(
        "-t",
        "--table",
        dest="Table",
        help="Prints a table of all templates",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    liberation_install.init()

    if args.Table:
        export_template_list()


def export_template_list() -> None:
    # Exports a github compatible table with all templates
    template_maps: dict[str, list[Any]] = {}
    missing_units = []
    for template in db.TEMPLATES.templates:
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
        category = template.role.value + tasks

        if category not in template_maps:
            template_maps[category] = []

        template_maps[category].append(
            [
                template.role.value,
                tasks,
                template.name,
                "<ul>" + "".join(units) + "</ul>",
            ]
        )

    templates = [
        template for templates in template_maps.values() for template in templates
    ]

    if len(missing_units) > 0:
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
