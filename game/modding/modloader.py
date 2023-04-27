from pathlib import Path

from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.modding.modpack import ModPack


class ModLoader:
    @staticmethod
    def load_mods() -> None:
        # Load pre-emptively so we don't spam the log with warnings about missing yaml
        # files for units already loaded by mods.
        AircraftType.load_all()
        GroundUnitType.load_all()
        ShipUnitType.load_all()

        bundled_mod_dir = Path("resources") / "mods"

        for path in bundled_mod_dir.iterdir():
            ModPack.load(path).inject()
