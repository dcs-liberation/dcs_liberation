from PySide2.QtCore import Signal
from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QComboBox, QLabel

from game import Game


class QChooseAirbase(QGroupBox):

    selected_airbase_changed = Signal(str)

    def __init__(self, game:Game, title=""):
        super(QChooseAirbase, self).__init__(title)
        self.game = game

        self.layout = QHBoxLayout()
        self.depart_from_label = QLabel("Airbase : ")
        self.depart_from = QComboBox()

        for i, cp in enumerate([b for b in self.game.theater.controlpoints if b.captured and b.id in self.game.planners]):
            self.depart_from.addItem(str(cp.name), cp)
        self.depart_from.setCurrentIndex(0)
        self.depart_from.currentTextChanged.connect(self._on_airbase_selected)
        self.layout.addWidget(self.depart_from_label)
        self.layout.addWidget(self.depart_from)
        self.setLayout(self.layout)

    def _on_airbase_selected(self):
        selected = self.depart_from.currentText()
        self.selected_airbase_changed.emit(selected)



