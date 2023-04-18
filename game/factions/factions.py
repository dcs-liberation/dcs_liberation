from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path

import yaml

from game import persistence
from .faction import Faction


class Factions:
    def __init__(self, factions: dict[str, Faction]) -> None:
        self.factions = factions

    def get_by_name(self, name: str) -> Faction:
        return self.factions[name]

    def iter_faction_names(self) -> Iterator[str]:
        return iter(self.factions.keys())

    @staticmethod
    def iter_faction_files_in(path: Path) -> Iterator[Path]:
        yield from path.glob("*.json")
        yield from path.glob("*.yaml")

    @classmethod
    def iter_faction_files(cls) -> Iterator[Path]:
        yield from cls.iter_faction_files_in(Path("resources/factions/"))
        yield from cls.iter_faction_files_in(
            Path(persistence.base_path()) / "Liberation/Factions"
        )

    @classmethod
    def load(cls) -> Factions:
        factions = {}
        for path in cls.iter_faction_files():
            try:
                with path.open("r", encoding="utf-8") as fdata:
                    if path.suffix == ".yaml":
                        data = yaml.safe_load(fdata)
                    else:
                        data = json.load(fdata)
                    faction = Faction.from_dict(data)
                    factions[faction.name] = faction
                    logging.info("Loaded faction from %s", path)
            except Exception:
                logging.exception(f"Unable to load faction from %s", path)

        return Factions(factions)
