import inspect

from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QSpinBox, QGridLayout, QVBoxLayout, QSizePolicy

from qt_ui.windows.mission.flight.payload.QPylonEditor import QPylonEditor


class QLoadoutEditor(QGroupBox):

    def __init__(self, flight, game):
        super(QLoadoutEditor, self).__init__("Use custom loadout")
        self.flight = flight
        self.game = game
        self.setCheckable(True)
        self.setChecked(flight.use_custom_loadout)

        self.toggled.connect(self.on_toggle)

        layout = QGridLayout()

        pylons = [v for v in self.flight.unit_type.__dict__.values() if inspect.isclass(v) and v.__name__.startswith("Pylon")]
        for i, pylon in enumerate(pylons):
            label = QLabel("<b>{}</b>".format(pylon.__name__[len("Pylon"):]))
            label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            layout.addWidget(label, i, 0)
            layout.addWidget(QPylonEditor(flight, pylon, i+1), i, 1)

        self.setLayout(layout)

    def on_toggle(self):
        self.flight.use_custom_loadout = self.isChecked()


