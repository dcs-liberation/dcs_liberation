from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import List, Tuple, Union, Dict

from dcs.terrain import (
    Caucasus,
    PersianGulf,
    Syria,
    Nevada,
    Normandy,
    TheChannel,
    MarianaIslands,
)
from dcs import Mission

Terrain = Union[
    Caucasus, PersianGulf, Syria, Nevada, Normandy, TheChannel, MarianaIslands
]

SAVE_PATH = Path("resources/frontlines")


def validate_miz(file_path: Path) -> bool:
    return bool(file_path.suffix == ".miz" and file_path.exists())


def validate_airports(airports: Tuple[int], terrain: Terrain):
    for airport in airports:
        if terrain.airport_by_id(airport) is None:
            print(f"Cannot load airport for invalid id {airport}")


def load_files(files) -> List[Mission]:
    missions = []
    for file in files:
        if validate_miz(file):
            mission = Mission()
            mission.load_file(file)
            missions.append(mission)
        else:
            print(f"Error: {file} doesn't look like a valid mission file.")
    return missions


def create_frontline_dict(mission: Mission) -> Dict[str, Dict]:
    frontline_dict = {}
    for group in mission.country("USA").vehicle_group:
        groupname = str(group.name).replace(group.name.id, "").replace(":", "")
        control_points = groupname.split("|")
        frontline_dict[groupname] = {
            "points": [(i.position.x, i.position.y) for i in group.points],
            "start_cp": int(control_points[0]),
        }
    return frontline_dict


def process_missions(missions: List[Mission]) -> None:
    for mission in missions:
        frontline_dict = create_frontline_dict(mission)
        write_json(frontline_dict, mission.terrain.name.lower())


def write_json(frontline_dict: Dict[str, Dict], terrain_name: str) -> None:
    with open(SAVE_PATH.joinpath(terrain_name + ".json"), "w") as file:
        json.dump(frontline_dict, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a miz file to create json descriptions of multi-segment frontlines"
    )
    parser.add_argument(
        "files",
        metavar="N",
        type=Path,
        nargs="+",
        help="A list of space separated .miz files to extract frontlines from",
    )

    args = parser.parse_args()
    missions = load_files(args.files)
    process_missions(missions)
    # frontline_dict = create_frontline_dict(missions[0])

    print("Done")
