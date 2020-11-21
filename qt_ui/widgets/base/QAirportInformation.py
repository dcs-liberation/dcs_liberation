from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QLCDNumber

from game.theater import ControlPoint, Airport


class QAirportInformation(QGroupBox):

    def __init__(self, cp:ControlPoint, airport:Airport):
        super(QAirportInformation, self).__init__(airport.name)
        self.cp = cp
        self.airport = airport
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()

        # Runway information
        self.runways = QGroupBox("Runways")
        self.runwayLayout = QGridLayout()
        for i, runway in enumerate(self.airport.runways):

            # Seems like info is missing in pydcs, even if the attribute is there
            lr = ""
            if runway.leftright == 1:
                lr = "L"
            elif runway.leftright == 2:
                lr = "R"

            self.runwayLayout.addWidget(QLabel("Runway " + str(runway.heading) + lr), i, 0)

            # Seems like info is missing in pydcs, even if the attribute is there
            if runway.ils:
                self.runwayLayout.addWidget(QLabel("ILS "), i, 1)
                self.runwayLayout.addWidget(QLCDNumber(6, runway.ils), i, 1)
            else:
                self.runwayLayout.addWidget(QLabel("NO ILS"), i, 1)


        self.runways.setLayout(self.runwayLayout)
        self.layout.addWidget(self.runways, 0, 0)

        self.layout.addWidget(QLabel("<b>Parking Slots :</b>"), 1, 0)
        self.layout.addWidget(QLabel(str(len(self.airport.parking_slots))), 1, 1)


        stretch = QVBoxLayout()
        stretch.addStretch()

        self.layout.addLayout(stretch, 2, 0)
        self.setLayout(self.layout)


