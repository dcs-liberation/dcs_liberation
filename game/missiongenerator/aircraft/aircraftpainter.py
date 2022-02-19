from __future__ import annotations

import random
from typing import Any, Optional

from dcs.unitgroup import FlyingGroup

from game.ato import Flight


class AircraftPainter:
    def __init__(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        self.flight = flight
        self.group = group

    def livery_from_unit_type(self) -> Optional[str]:
        return self.flight.unit_type.default_livery

    def livery_from_faction(self) -> Optional[str]:
        faction = self.flight.squadron.coalition.faction
        if (
            choices := faction.liveries_overrides.get(self.flight.unit_type)
        ) is not None:
            return random.choice(choices)
        return None

    def livery_from_squadron(self) -> Optional[str]:
        return self.flight.squadron.livery

    def determine_livery(self) -> Optional[str]:
        if (livery := self.livery_from_squadron()) is not None:
            return livery
        if (livery := self.livery_from_faction()) is not None:
            return livery
        if (livery := self.livery_from_unit_type()) is not None:
            return livery
        return None

    def apply_livery(self) -> None:
        livery = self.determine_livery()
        if livery is None:
            return
        for unit in self.group.units:
            unit.livery_id = livery
