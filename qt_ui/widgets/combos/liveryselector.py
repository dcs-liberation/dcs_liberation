from __future__ import annotations

import dcs.countries
from PySide6.QtWidgets import QComboBox
from dcs.liveries.livery import Livery

from game.squadrons import Squadron


class LiverySelector(QComboBox):
    def __init__(self, squadron: Squadron) -> None:
        super().__init__()
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.set_squadron(squadron)

    @property
    def selected_livery(self) -> Livery | None:
        return self.currentData()

    def set_squadron(self, squadron: Squadron) -> None:
        selected_idx: int | None = None
        self.clear()
        self.addItem("Default", None)
        for idx, livery in enumerate(
            squadron.aircraft.dcs_unit_type.iter_liveries_for_country(
                dcs.countries.get_by_name(squadron.country)
            ),
            1,  # First entry is "Default".
        ):
            self.addItem(livery.name, livery)
            if squadron.livery == livery.id:
                selected_idx = idx
        if selected_idx is not None:
            self.setCurrentIndex(selected_idx)
        self.update()
