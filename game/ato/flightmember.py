from __future__ import annotations

from typing import TYPE_CHECKING

from game.ato.loadouts import Loadout

if TYPE_CHECKING:
    from game.squadrons import Pilot


class FlightMember:
    def __init__(self, pilot: Pilot | None, loadout: Loadout) -> None:
        self.pilot = pilot
        self.loadout = loadout
        self.use_custom_loadout = False
        self.properties: dict[str, bool | float | int] = {}

    @property
    def is_player(self) -> bool:
        if self.pilot is None:
            return False
        return self.pilot.player
