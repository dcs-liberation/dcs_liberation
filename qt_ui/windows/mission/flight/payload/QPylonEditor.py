import logging
import operator
from typing import Optional

from PySide2.QtWidgets import QComboBox

from game import Game, db
from game.data.weapons import Pylon, Weapon
from gen.flights.flight import Flight
from dcs import weapons_data


class QPylonEditor(QComboBox):

    def __init__(self, game: Game, flight: Flight, pylon: Pylon) -> None:
        super().__init__()
        self.flight = flight
        self.pylon = pylon

        current = self.flight.loadout.get(self.pylon.number)

        self.addItem("None", None)
        if game.settings.restrict_weapons_by_date:
            weapons = pylon.available_on(game.date)
        else:
            weapons = pylon.allowed
        allowed = sorted(weapons, key=operator.attrgetter("name"))
        for i, weapon in enumerate(allowed):
            self.addItem(weapon.name, weapon)
            if current == weapon:
                self.setCurrentIndex(i + 1)

        self.default_loadout(self.pylon)
        self.currentIndexChanged.connect(self.on_pylon_change)

    def on_pylon_change(self):
        selected: Optional[Weapon] = self.currentData()
        self.flight.loadout[self.pylon.number] = selected

        if selected is None:
            logging.debug(f"Pylon {self.pylon.number} emptied")
        else:
            logging.debug(
                f"Pylon {self.pylon.number} changed to {selected.name}")

    def default_loadout(self, pylon: Pylon) -> None:
        self.flight.unit_type.load_payloads()
        loadout = self.flight.unit_type.loadout_by_name(db.EXPANDED_TASK_PAYLOAD_OVERRIDE.get(self.flight.flight_type.name))
        pylon_default_weapon = None
        for i in loadout:
            if i[0] == self.pylon.number:
                pylon_default_weapon = i[1]["clsid"]
        if pylon_default_weapon is not None:
            self.setCurrentText(weapons_data.weapon_ids.get(pylon_default_weapon).get("name"))
        else:
            self.setCurrentText("None")

    def clear_loadout(self) -> None:
        self.setCurrentIndex(0)
