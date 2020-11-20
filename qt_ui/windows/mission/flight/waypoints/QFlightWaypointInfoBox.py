from PySide2.QtWidgets import QGroupBox, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout

from gen.flights.flight import FlightWaypoint


class QFlightWaypointInfoBox(QGroupBox):

    def __init__(self, flight_wpt:FlightWaypoint = None):
        super(QFlightWaypointInfoBox, self).__init__("Waypoint")
        self.flight_wpt = flight_wpt
        if flight_wpt is None:
            self.flight_wpt = FlightWaypoint(0,0,0)
        self.x_position_label = QLabel(str(self.flight_wpt.x))
        self.y_position_label = QLabel(str(self.flight_wpt.y))
        self.alt_label = QLabel(str(int(self.flight_wpt.alt.feet)))
        self.name_label = QLabel(str(self.flight_wpt.name))
        self.desc_label = QLabel(str(self.flight_wpt.description))
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        x_pos_layout = QHBoxLayout()
        x_pos_layout.addWidget(QLabel("<b>X : </b>"))
        x_pos_layout.addWidget(self.x_position_label)
        x_pos_layout.addStretch()

        y_pos_layout = QHBoxLayout()
        y_pos_layout.addWidget(QLabel("<b>Y : </b>"))
        y_pos_layout.addWidget(self.y_position_label)
        y_pos_layout.addStretch()

        alt_layout = QHBoxLayout()
        alt_layout.addWidget(QLabel("<b>Alt : </b>"))
        alt_layout.addWidget(self.alt_label)
        alt_layout.addStretch()

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("<b>Name : </b>"))
        name_layout.addWidget(self.name_label)
        name_layout.addStretch()

        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("<b>Description : </b>"))
        desc_layout.addWidget(self.desc_label)
        desc_layout.addStretch()

        #layout.addLayout(name_layout)
        layout.addLayout(x_pos_layout)
        layout.addLayout(y_pos_layout)
        layout.addLayout(alt_layout)
        layout.addLayout(desc_layout)

        self.setLayout(layout)

    def set_flight_waypoint(self, flight_wpt:FlightWaypoint):
        self.flight_wpt = flight_wpt
        if flight_wpt is None:
            self.flight_wpt = FlightWaypoint(0,0,0)
        self.x_position_label.setText(str(self.flight_wpt.x))
        self.y_position_label.setText(str(self.flight_wpt.y))
        self.alt_label.setText(str(int(self.flight_wpt.alt.feet)))
        self.name_label.setText(str(self.flight_wpt.name))
        self.desc_label.setText(str(self.flight_wpt.description))
        self.setTitle(self.flight_wpt.name)
