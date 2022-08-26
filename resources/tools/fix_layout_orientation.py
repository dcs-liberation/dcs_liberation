# Script to update a layout.miz which is not created with an orientation of Heading=0
# It loads the miz as and reorientates all objects


# Requirement: Only ONE Group has to be within the miz file.
# Load miz
# Determine Center and current heading (use first unit for that)
# Rotate everything around the center with the difference to heading 0
# Save the miz

import argparse
import itertools
from typing import Any

import dcs

from game.point_with_heading import PointWithHeading
from game.utils import Heading


def fix_orientation(miz_file: str) -> None:
    mission = dcs.Mission()
    mission.load_file(miz_file)
    groups = []
    # Load all units from the miz
    for country in itertools.chain(
        mission.coalition["red"].countries.values(),
        mission.coalition["blue"].countries.values(),
    ):
        for dcs_group in itertools.chain(
            mission.country(country.name).vehicle_group,
            mission.country(country.name).ship_group,
            mission.country(country.name).static_group,
        ):
            groups.append(dcs_group)

    # Get the center which will be used as origin for the rotation
    center_unit = groups[0].units[0]

    # Calculate the rotation
    rotation = Heading.from_degrees(360 - int(center_unit.heading))

    # Rotate all units
    for group in groups:
        for unit in group.units:
            unit.position = PointWithHeading.from_point(
                unit.position, Heading.from_degrees(int(unit.heading)) + rotation
            )
            unit.heading = unit.position.heading.degrees
            unit.position.rotate(center_unit.position, rotation)
        group.points[0].position = group.units[0].position
    # Save the miz
    mission.save()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mission", type=str, help="The mission which will be fixed")
    args = parser.parse_args()
    fix_orientation(args.mission)


main()
