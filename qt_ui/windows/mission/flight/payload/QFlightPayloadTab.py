from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QVBoxLayout,
)

from game import Game
from game.ato.flight import Flight
from game.ato.loadouts import Loadout
from .QLoadoutEditor import QLoadoutEditor
from .propertyeditor import PropertyEditor


class DcsLoadoutSelector(QComboBox):
    def __init__(self, flight: Flight) -> None:
        super().__init__()
        for loadout in Loadout.iter_for(flight):
            self.addItem(loadout.name, loadout)
        self.model().sort(0)
        self.setDisabled(flight.loadout.is_custom)
        if flight.loadout.is_custom:
            self.setCurrentText(Loadout.default_for(flight).name)
        else:
            self.setCurrentText(flight.loadout.name)


class QFlightPayloadTab(QFrame):
    def __init__(self, flight: Flight, game: Game):
        super(QFlightPayloadTab, self).__init__()
        self.flight = flight
        self.payload_editor = QLoadoutEditor(flight, game)
        self.payload_editor.toggled.connect(self.on_custom_toggled)

        layout = QVBoxLayout()

        # Docs Link
        docsText = QLabel(
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Loadouts"><span style="color:#FFFFFF;">How to create your own default loadout</span></a>'
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        layout.addLayout(PropertyEditor(self.flight))
        self.loadout_selector = DcsLoadoutSelector(flight)
        self.loadout_selector.currentIndexChanged.connect(self.on_new_loadout)
        layout.addWidget(self.loadout_selector)
        layout.addWidget(self.payload_editor)
        layout.addWidget(docsText)

        self.setLayout(layout)

    def reload_from_flight(self) -> None:
        self.loadout_selector.setCurrentText(self.flight.loadout.name)

    def loadout_at(self, index: int) -> Loadout:
        loadout = self.loadout_selector.itemData(index)
        if loadout is None:
            return Loadout.empty_loadout()
        return loadout

    def current_loadout(self) -> Loadout:
        loadout = self.loadout_selector.currentData()
        if loadout is None:
            return Loadout.empty_loadout()
        return loadout

    def on_new_loadout(self, index: int) -> None:
        self.flight.loadout = self.loadout_at(index)
        self.payload_editor.reset_pylons()

    def on_custom_toggled(self, use_custom: bool) -> None:
        self.loadout_selector.setDisabled(use_custom)
        if use_custom:
            self.flight.loadout = self.flight.loadout.derive_custom("Custom")
        else:
            self.flight.loadout = self.current_loadout()
            self.payload_editor.reset_pylons()
