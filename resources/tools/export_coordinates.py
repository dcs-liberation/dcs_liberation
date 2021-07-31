"""Command line tool for exporting coordinates from DCS to derive projection data.

DCS X/Z coordinates are meter-scale projections of a transverse mercator grid. The
projection has a few required parameters:

1. Scale factor. Is 0.9996 for most regions:
   https://proj.org/operations/projections/tmerc.html.
2. Central meridian of the projection. Easily guessed because there are only 60 UTM
   zones and one of those is always used.
3. A false easting and northing (offsets from UTM's center point to DCS's). These aren't
   easily guessed, but can be computed by using an offset of 0 and finding the error of
   projecting the 0 point from DCS.

This tool creates a mission that will dump the lat/lon and x/z coordinates of the 0/0
point and also every airport in the given theater. The data for the zero point is used
to compute the false easting and northing for the map. The data for each airport is used
to test the projection for errors.

The resulting data is exported to game/theater/<map>.py as a TransverseMercator object.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import textwrap
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from dcs import Mission
from dcs.action import DoScriptFile
from dcs.terrain.caucasus import Caucasus
from dcs.terrain.nevada import Nevada
from dcs.terrain.normandy import Normandy
from dcs.terrain.persiangulf import PersianGulf
from dcs.terrain.syria import Syria
from dcs.terrain.terrain import Terrain
from dcs.terrain.thechannel import TheChannel
from dcs.terrain.marianaislands import MarianaIslands
from dcs.triggers import TriggerStart
from pyproj import CRS, Transformer

from game import persistency
from game.theater.projections import TransverseMercator
from qt_ui import liberation_install

THIS_DIR = Path(__file__).resolve().parent
JSON_LUA = THIS_DIR.parent / "plugins/base/json.lua"
EXPORT_LUA = THIS_DIR / "coord_export.lua"
SAVE_DIR = THIS_DIR.parent / "coordinate_reference"


ARG_TO_TERRAIN_MAP = {
    "caucasus": Caucasus(),
    "nevada": Nevada(),
    "normandy": Normandy(),
    "persiangulf": PersianGulf(),
    "thechannel": TheChannel(),
    "syria": Syria(),
    "marianaislands": MarianaIslands(),
}

# https://gisgeography.com/central-meridian/
# UTM zones determined by guess and check. There are only a handful in the region for
# each map and getting the wrong one will be flagged with errors when processing.
CENTRAL_MERIDIANS = {
    "caucasus": 33,
    "nevada": -117,
    "normandy": -3,
    "persiangulf": 57,
    "thechannel": 3,
    "syria": 39,
    "marianaislands": 147,
}


@dataclass(frozen=True)
class Coordinates:
    x: float
    y: float
    z: float

    latitude: float
    longitude: float
    altitude: float

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Coordinates:
        return cls(
            x=data["point"]["x"],
            y=data["point"]["y"],
            z=data["point"]["z"],
            latitude=data["LL"]["lat"],
            longitude=data["LL"]["lon"],
            altitude=data["LL"]["alt"],
        )


def create_mission(terrain: Terrain) -> Path:
    m = Mission(terrain)

    json_trigger = TriggerStart(comment=f"Load JSON")
    json_lua = m.map_resource.add_resource_file(JSON_LUA)
    json_trigger.add_action(DoScriptFile(json_lua))
    m.triggerrules.triggers.append(json_trigger)

    export_trigger = TriggerStart(comment=f"Load coordinate export")
    export_lua = m.map_resource.add_resource_file(EXPORT_LUA)
    export_trigger.add_action(DoScriptFile(export_lua))
    m.triggerrules.triggers.append(export_trigger)

    mission_path = persistency.mission_path_for(f"export_{terrain.name.lower()}.miz")
    m.save(mission_path)
    return Path(mission_path)


def load_coordinate_data(data: Dict[str, Any]) -> Dict[str, Coordinates]:
    airbases = {}
    for name, coord_data in data.items():
        airbases[name] = Coordinates.from_json(coord_data)
    return airbases


def test_for_errors(
    name: str,
    lat_lon_to_x_z: Transformer,
    x_z_to_lat_lon: Transformer,
    coords: Coordinates,
) -> bool:
    errors = False

    x, z = lat_lon_to_x_z.transform(coords.latitude, coords.longitude)
    if not math.isclose(x, coords.x) or not math.isclose(z, coords.z):
        error_x = x - coords.x
        error_z = z - coords.z
        error_pct_x = error_x / coords.x * 100
        error_pct_z = error_z / coords.z * 100
        print(f"{name} has error of {error_pct_x}% {error_pct_z}%")
        errors = True

    lat, lon = x_z_to_lat_lon.transform(coords.x, coords.z)
    if not math.isclose(lat, coords.latitude) or not math.isclose(
        lon, coords.longitude
    ):
        error_lat = lat - coords.latitude
        error_lon = lon - coords.longitude
        error_pct_lon = error_lat / coords.latitude * 100
        error_pct_lat = error_lon / coords.longitude * 100
        print(f"{name} has error of {error_pct_lat}% {error_pct_lon}%")
        errors = True

    return errors


def test_parameters(
    airbases: Dict[str, Coordinates], parameters: TransverseMercator
) -> bool:
    errors = False
    wgs84 = CRS("WGS84")
    crs = parameters.to_crs()
    lat_lon_to_x_z = Transformer.from_crs(wgs84, crs)
    x_z_to_lat_lon = Transformer.from_crs(crs, wgs84)
    for name, coords in airbases.items():
        if name == "zero":
            continue
        if test_for_errors(name, lat_lon_to_x_z, x_z_to_lat_lon, coords):
            errors = True
    return errors


def compute_tmerc_parameters(
    coordinates_file: Path, terrain: str
) -> TransverseMercator:

    data = json.loads(coordinates_file.read_text())
    airbases = load_coordinate_data(data)
    wgs84 = CRS("WGS84")

    # Creates a transformer with 0 for the false easting and northing, but otherwise has
    # the correct parameters. We'll use this to transform the zero point from the
    # mission to calculate the error from the actual zero point to determine the correct
    # false easting and northing.
    bad = TransverseMercator(
        central_meridian=CENTRAL_MERIDIANS[terrain],
        false_easting=0,
        false_northing=0,
        scale_factor=0.9996,
    ).to_crs()
    zero_finder = Transformer.from_crs(wgs84, bad)
    z, x = zero_finder.transform(airbases["zero"].latitude, airbases["zero"].longitude)

    parameters = TransverseMercator(
        central_meridian=CENTRAL_MERIDIANS[terrain],
        false_easting=-x,
        false_northing=-z,
        scale_factor=0.9996,
    )

    if test_parameters(airbases, parameters):
        sys.exit("Found errors in projection parameters. Quitting.")

    return parameters


@contextmanager
def mission_scripting():
    liberation_install.replace_mission_scripting_file()
    try:
        yield
    finally:
        liberation_install.restore_original_mission_scripting()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("map", choices=list(ARG_TO_TERRAIN_MAP.keys()))

    return parser.parse_args()


def main() -> None:
    if liberation_install.init():
        print("Set up Liberation first.")
        return

    args = parse_args()
    terrain = ARG_TO_TERRAIN_MAP[args.map]
    mission = create_mission(terrain)
    with mission_scripting():
        input(
            f"Created {mission} and replaced MissionScript.lua. Open DCS and load the "
            "mission. Once the mission starts running, close it and press enter."
        )
    coords_path = Path(persistency.base_path()) / "coords.json"
    parameters = compute_tmerc_parameters(coords_path, args.map)
    out_file = THIS_DIR.parent.parent / "game/theater" / f"{args.map}.py"
    out_file.write_text(
        textwrap.dedent(
            f"""\
            # DO NOT EDIT:
            # This file is generated by resources/tools/export_coordinates.py.
            from game.theater.projections import TransverseMercator

            PARAMETERS = TransverseMercator(
                central_meridian={parameters.central_meridian},
                false_easting={parameters.false_easting},
                false_northing={parameters.false_northing},
                scale_factor={parameters.scale_factor},
            )
            """
        )
    )


if __name__ == "__main__":
    main()
