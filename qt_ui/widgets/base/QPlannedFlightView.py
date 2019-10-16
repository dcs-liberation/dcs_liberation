from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QHBoxLayout

from game import db
from gen.flights.ai_flight_planner import FlightPlanner


class QPlannedFlightView(QGroupBox):

    def __init__(self, flight_planner:FlightPlanner):
        super(QPlannedFlightView, self).__init__("Planned flights")
        self.flight_planner = flight_planner
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()

        for i,f in enumerate(self.flight_planner.flights):
            ftype = QLabel("<b>" + f.flight_type.name + "</b>")
            count = QLabel(str(f.count) + " x " + db.unit_type_name(f.unit_type))
            sched = QLabel("   in " + str(f.scheduled_in) + " minutes")

            self.layout.addWidget(ftype, i, 0)
            self.layout.addWidget(count, i, 1)
            self.layout.addWidget(sched, i, 2)

        stretch = QVBoxLayout()
        stretch.addStretch()
        self.layout.addLayout(stretch, len(self.flight_planner.flights)+1, 0)
        self.setLayout(self.layout)
