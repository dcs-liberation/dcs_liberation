import inspect

from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QSpinBox, QGridLayout, QVBoxLayout, QSizePolicy

from game.data.weapons import Pylon
from qt_ui.windows.mission.flight.payload.QPylonEditor import QPylonEditor


class QLoadoutEditor(QGroupBox):

    def __init__(self, flight, game):
        super(QLoadoutEditor, self).__init__("Use custom loadout")
        self.flight = flight
        self.game = game
        self.setCheckable(True)
        self.setChecked(flight.use_custom_loadout)

        self.toggled.connect(self.on_toggle)

        hboxLayout = QVBoxLayout(self)
        layout = QGridLayout(self)

        for i, pylon in enumerate(Pylon.iter_pylons(self.flight.unit_type)):
            label = QLabel(f"<b>{pylon.number}</b>")
            label.setSizePolicy(
                QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            layout.addWidget(label, i, 0)
            layout.addWidget(QPylonEditor(flight, pylon), i, 1)

        hboxLayout.addLayout(layout)
        hboxLayout.addStretch()
        self.setLayout(hboxLayout)

    def on_toggle(self):
        self.flight.use_custom_loadout = self.isChecked()


