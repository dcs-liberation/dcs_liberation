import logging
import operator
from typing import Optional

from PySide2.QtWidgets import QComboBox

from game import Game
from game.data.weapons import Pylon, Weapon
from gen.flights.flight import Flight
from gen.flights.loadouts import Loadout


class QPylonEditor(QComboBox):
    def __init__(self, game: Game, flight: Flight, pylon: Pylon) -> None:
        super().__init__()
        self.flight = flight
        self.pylon = pylon
        self.game = game

        current = self.flight.loadout.pylons.get(self.pylon.number)

        self.addItem("None", None)
        if self.game.settings.restrict_weapons_by_date:
            weapons = pylon.available_on(self.game.date)
        else:
            weapons = pylon.allowed
        allowed = sorted(weapons, key=operator.attrgetter("name"))
        for i, weapon in enumerate(allowed):
            self.addItem(weapon.name, weapon)
            if current == weapon:
                self.setCurrentIndex(i + 1)

        self.currentIndexChanged.connect(self.on_pylon_change)

    def on_pylon_change(self):
        selected: Optional[Weapon] = self.currentData()
        self.flight.loadout.pylons[self.pylon.number] = selected

        if selected is None:
            logging.debug(f"Pylon {self.pylon.number} emptied")
        else:
            logging.debug(f"Pylon {self.pylon.number} changed to {selected.name}")

    def weapon_from_loadout(self, loadout: Loadout) -> Optional[Weapon]:
        weapon = loadout.pylons.get(self.pylon.number)
        if weapon is None:
            return None
        # TODO: Handle removed pylons better.
        if weapon.cls_id == "<CLEAN>":
            return None
        return weapon

    def matching_weapon_name(self, loadout: Loadout) -> str:
        if self.game.settings.restrict_weapons_by_date:
            loadout = loadout.degrade_for_date(self.flight.unit_type, self.game.date)
        weapon = self.weapon_from_loadout(loadout)
        if weapon is None:
            return ""
        return weapon.name

    def set_from(self, loadout: Loadout) -> None:
        self.setCurrentText(self.matching_weapon_name(loadout))
