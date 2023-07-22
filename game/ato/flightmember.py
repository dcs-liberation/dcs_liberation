from __future__ import annotations

from typing import TYPE_CHECKING, Any

from game.ato.loadouts import Loadout
from game.lasercodes import LaserCode
from game.savecompat import has_save_compat_for

if TYPE_CHECKING:
    from game.squadrons import Pilot


class FlightMember:
    def __init__(self, pilot: Pilot | None, loadout: Loadout) -> None:
        self.pilot = pilot
        self.loadout = loadout
        self.use_custom_loadout = False
        self.tgp_laser_code: LaserCode | None = None
        self.properties: dict[str, bool | float | int] = {}

    @has_save_compat_for(9)
    def __setstate__(self, state: dict[str, Any]) -> None:
        if "tgp_laser_code" not in state:
            state["tgp_laser_code"] = None
        self.__dict__.update(state)

    def assign_tgp_laser_code(self, code: LaserCode) -> None:
        if self.tgp_laser_code is not None:
            raise RuntimeError(
                f"{self.pilot} already has already been assigned laser code "
                f"{self.tgp_laser_code}"
            )
        self.tgp_laser_code = code

    def release_tgp_laser_code(self) -> None:
        if self.tgp_laser_code is None:
            raise RuntimeError(f"{self.pilot} has no assigned laser code")

        self.tgp_laser_code.release()
        self.tgp_laser_code = None

    @property
    def is_player(self) -> bool:
        if self.pilot is None:
            return False
        return self.pilot.player
