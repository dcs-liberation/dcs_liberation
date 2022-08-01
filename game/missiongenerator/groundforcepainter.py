from __future__ import annotations

import logging
import random
from typing import Any, Optional

from dcs.unitgroup import Vehicle

from game.factions.faction import Faction


class GroundForcePainter:
    def __init__(self, faction: Faction, vehicle: Vehicle) -> None:
        self.faction = faction
        self.vehicle = vehicle

    def livery_from_faction(self) -> Optional[str]:
        faction = self.faction
        try:
            if (
                choices := faction.liveries_overrides_ground_forces.get(
                    self.vehicle.type
                )
            ) is not None:
                return random.choice(choices)
        except AttributeError:
            logging.warning(
                f"Faction {self.faction.name} is missing livery for ground unit {self.vehicle.type}"
            )
            return None
        logging.warning(
            f"Faction {self.faction.name} is missing livery for ground unit {self.vehicle.type}"
        )
        return None

    def determine_livery(self) -> Optional[str]:
        if (livery := self.livery_from_faction()) is not None:
            return livery
        return None

    def apply_livery(self) -> None:
        livery = self.determine_livery()
        if livery is None:
            return
        self.vehicle.livery_id = livery
