import logging

from PySide2.QtWidgets import QWidget, QSpinBox, QComboBox


class QPylonEditor(QComboBox):

    def __init__(self, flight, pylon, pylon_number):
        super(QPylonEditor, self).__init__()
        self.pylon = pylon
        self.pylon_number = pylon_number
        self.flight = flight

        possible_loadout = [i for i in self.pylon.__dict__.keys() if i[:1] != '_']

        if not str(self.pylon_number) in self.flight.loadout.keys():
            self.flight.loadout[str(self.pylon_number)] = ""

        self.addItem("None")
        for i,k in enumerate(possible_loadout):
            self.addItem(str(k))
            if self.flight.loadout[str(self.pylon_number)] == str(k):
                self.setCurrentIndex(i + 1)

        self.currentTextChanged.connect(self.on_pylon_change)

    def on_pylon_change(self):
        selected = self.currentText()
        if selected == "None":
            logging.info("Pylon " + str(self.pylon_number) + " emptied")
            self.flight.loadout[str(self.pylon_number)] = ""
        else:
            logging.info("Pylon " + str(self.pylon_number) + " changed to " + selected)
            self.flight.loadout[str(self.pylon_number)] = selected

