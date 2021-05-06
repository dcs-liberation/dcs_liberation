from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Type

from game import persistency
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

    @staticmethod
    def find_faction_files_in(path: Path) -> List[Path]:
        return [f for f in path.glob("*.json") if f.is_file()]

    @classmethod
    def load_factions(cls: Type[FactionLoader]) -> Dict[str, Faction]:
        user_faction_path = Path(persistency.base_path()) / "Liberation/Factions"
        files = cls.find_faction_files_in(
            FACTION_DIRECTORY
        ) + cls.find_faction_files_in(user_faction_path)
        factions = {}

        for f in files:
            try:
                with f.open("r", encoding="utf-8") as fdata:
                    data = json.load(fdata)
                    factions[data["name"]] = Faction.from_json(data)
                    logging.info("Loaded faction : " + str(f))
            except Exception:
                logging.exception(f"Unable to load faction : {f}")

        return factions

    def __getitem__(self, name: str) -> Faction:
        return self.factions[name]

    def __iter__(self) -> Iterator[str]:
        return iter(self.factions.keys())
