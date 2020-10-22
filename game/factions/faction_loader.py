import json
import os
import logging

from game.factions.faction import Faction

FACTION_DIRECTORY = "./resources/factions/"


def load_factions() -> {str, Faction}:
    files = os.listdir(FACTION_DIRECTORY)
    files = [f for f in files if f.endswith(".json")]

    factions = {}

    for f in files:
        print(f)
        path = os.path.join(FACTION_DIRECTORY, f)
        logging.info("Loading faction" + path)
        #try:
        with open(path, "r", encoding="utf-8") as fdata:
            data = json.load(fdata, encoding="utf-8")
            factions[data["name"]] = Faction.from_json(data)
            logging.info("Loaded faction : " + path)
        #except Exception as e:
        #    print(e)
        #    logging.error("Unable to load faction : " + path)

    print(factions)
    return factions