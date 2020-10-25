from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Type

from game.factions.faction import Faction

FACTION_DIRECTORY = "./resources/factions/"


class FactionLoader:

    @classmethod
    def load_factions(cls: Type[FactionLoader]) -> {str, Faction}:

        path = Path(FACTION_DIRECTORY)
        files = [f for f in path.glob("*.json") if f.is_file()]
        factions = {}

        for f in files:
            logging.info("Loading faction" + str(f))
            try:
                with open(f, "r", encoding="utf-8") as fdata:
                    data = json.load(fdata, encoding="utf-8")
                    factions[data["name"]] = Faction.from_json(data)
                    logging.info("Loaded faction : " + str(f))
            except Exception as e:
                logging.error("Unable to load faction : " + path, e)

        return factions
