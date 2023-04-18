from __future__ import annotations

import itertools
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
        self.campaign_defined_factions: dict[str, Faction] = {}

    def get_by_name(self, name: str) -> Faction:
        try:
            return self.factions[name]
        except KeyError:
            return self.campaign_defined_factions[name]

    def iter_faction_names(self) -> Iterator[str]:
        # Campaign defined factions first so they show up at the top of the list in the
        # UI.
        return itertools.chain(self.campaign_defined_factions, self.factions)

    def add_campaign_defined(self, faction: Faction) -> None:
        if (
            faction.name in self.factions
            or faction.name in self.campaign_defined_factions
        ):
            raise KeyError(f"Duplicate faction {faction.name}")
        self.campaign_defined_factions[faction.name] = faction

    def reset_campaign_defined(self) -> None:
        self.campaign_defined_factions = {}

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
