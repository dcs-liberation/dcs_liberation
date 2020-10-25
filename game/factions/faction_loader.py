from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, Type

from game.factions.faction import Faction

FACTION_DIRECTORY = Path("./resources/factions/")


class FactionLoader:

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
