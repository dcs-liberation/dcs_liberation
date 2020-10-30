from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, Iterator, Optional, Type

from game.factions.faction import Faction

FACTION_DIRECTORY = Path("./resources/factions/")


class FactionLoader:
    def __init__(self) -> None:
        self._factions: Optional[Dict[str, Faction]] = None

    @property
    def factions(self) -> Dict[str, Faction]:
        self.initialize()
        assert self._factions is not None
        return self._factions

    def initialize(self) -> None:
        if self._factions is None:
            self._factions = self.load_factions()

    @classmethod
    def load_factions(cls: Type[FactionLoader]) -> Dict[str, Faction]:
        files = [f for f in FACTION_DIRECTORY.glob("*.json") if f.is_file()]
        factions = {}

        for f in files:
            try:
                with f.open("r", encoding="utf-8") as fdata:
                    data = json.load(fdata, encoding="utf-8")
                    factions[data["name"]] = Faction.from_json(data)
                    logging.info("Loaded faction : " + str(f))
            except Exception:
                logging.exception(f"Unable to load faction : {f}")

        return factions

    def __getitem__(self, name: str) -> Faction:
        return self.factions[name]

    def __iter__(self) -> Iterator[str]:
        return iter(self.factions.keys())
