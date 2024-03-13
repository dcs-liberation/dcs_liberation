"""Generates resources/dcs/beacons.json from the DCS installation.

DCS has a beacons.lua file for each terrain mod that includes information about
the radio beacons present on the map:

beacons = {
    {
        display_name = _('INCIRLIC');
        beaconId = 'airfield16_0';
        type = BEACON_TYPE_VORTAC;
        callsign = 'DAN';
        frequency = 108400000.000000;
        channel = 21;
        position = { 222639.437500, 73.699811, -33216.257813 };
        direction = 0.000000;
        positionGeo = { latitude = 37.015611, longitude = 35.448194 };
        sceneObjects = {'t:124814096'};
    };
    ...
}

"""
import argparse
import dataclasses
import gettext
import json
import logging
import os
import textwrap
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterable, Union

import lupa

from game.dcs.beacons import BEACONS_RESOURCE_PATH, Beacon, BeaconType

THIS_DIR = Path(__file__).parent.resolve()
SRC_DIR = THIS_DIR.parents[1]
EXPORT_DIR = SRC_DIR / BEACONS_RESOURCE_PATH


@contextmanager
def cd(path: Path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


def convert_lua_frequency(raw: Union[float, int]) -> int:
    if isinstance(raw, float):
        if not raw.is_integer():
            # The values are in hertz, and everything should be a whole number.
            raise ValueError(f"Unexpected non-integer frequency: {raw}")
        return int(raw)
    else:
        return raw


def beacons_from_terrain(dcs_path: Path, path: Path) -> Iterable[tuple[str, Beacon]]:
    logging.info(f"Loading terrain data from {path}")
    # TODO: Fix case-sensitive issues.
    # The beacons.lua file differs by case in some terrains. Will need to be
    # fixed if the tool is to be run on Linux, but presumably the server
    # wouldn't be able to find these anyway.
    beacons_lua = path / "beacons.lua"
    with cd(dcs_path):
        lua = lupa.LuaRuntime()

        lua.execute(
            textwrap.dedent(
                """\
            function module(name)
            end
            
        """
            )
        )

        bind_gettext = lua.eval(
            textwrap.dedent(
                """\
            function(py_gettext)
                package.preload["i_18n"] = function()
                    return {
                        translate = py_gettext
                    }
                end
            end
            
        """
            )
        )

        try:
            translator = gettext.translation(
                "messages", path / "l10n", languages=["en"]
            )

            def translate(message_name: str) -> str:
                if not message_name:
                    return message_name
                return translator.gettext(message_name)

        except FileNotFoundError:
            # TheChannel has no locale data for English.
            def translate(message_name: str) -> str:
                return message_name

        bind_gettext(translate)

        src = beacons_lua.read_text()
        lua.execute(src)

        beacon_types_map: Dict[int, BeaconType] = {}
        for beacon_type in BeaconType:
            beacon_value = lua.eval(beacon_type.name)
            beacon_types_map[beacon_value] = beacon_type

        beacons = lua.eval("beacons")
        for beacon in beacons.values():
            beacon_type_lua = beacon["type"]
            if beacon_type_lua not in beacon_types_map:
                beacon_types_path = (
                    dcs_path / "MissionEditor/modules/me_beaconsInfo.lua"
                )
                raise KeyError(
                    f"Unknown beacon type {beacon_type_lua}. Check that all "
                    f"beacon types in {beacon_types_path} are present in "
                    f"{BeaconType.__class__.__name__}"
                )
            beacon_type = beacon_types_map[beacon_type_lua]

            yield beacon["beaconId"], Beacon(
                beacon["display_name"],
                beacon["callsign"],
                beacon_type,
                convert_lua_frequency(beacon["frequency"]),
                getattr(beacon, "channel", None),
            )


class Importer:
    """Imports beacon definitions from each available terrain mod.

    Only beacons for maps owned by the user can be imported. Other maps that
    have been previously imported will not be disturbed.
    """

    def __init__(self, dcs_path: Path, export_dir: Path) -> None:
        self.dcs_path = dcs_path
        self.export_dir = export_dir

    def run(self) -> None:
        """Exports the beacons for each available terrain mod."""
        terrains_path = self.dcs_path / "Mods" / "terrains"
        self.export_dir.mkdir(parents=True, exist_ok=True)
        for terrain in terrains_path.iterdir():
            beacons = beacons_from_terrain(self.dcs_path, terrain)
            self.export_beacons(terrain.name, beacons)

    def export_beacons(
        self, terrain: str, beacons: Iterable[tuple[str, Beacon]]
    ) -> None:
        terrain_py_path = self.export_dir / f"{terrain.lower()}.json"

        terrain_py_path.write_text(
            json.dumps({bid: dataclasses.asdict(b) for bid, b in beacons}, indent=True)
        )


def parse_args() -> argparse.Namespace:
    """Parses and returns command line arguments."""
    parser = argparse.ArgumentParser()

    def resolved_path(val: str) -> Path:
        """Returns the given string as a fully resolved Path."""
        return Path(val).resolve()

    parser.add_argument(
        "--export-to",
        type=resolved_path,
        default=EXPORT_DIR,
        help="Output directory for generated JSON files.",
    )

    parser.add_argument(
        "dcs_path",
        metavar="DCS_PATH",
        type=resolved_path,
        help="Path to DCS installation.",
    )

    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    Importer(args.dcs_path, args.export_to).run()


if __name__ == "__main__":
    main()
