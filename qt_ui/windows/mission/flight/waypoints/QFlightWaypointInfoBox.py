from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout

from game.ato.flightwaypoint import FlightWaypoint


class QFlightWaypointInfoBox(QGroupBox):
    def __init__(self) -> None:
        super(QFlightWaypointInfoBox, self).__init__("Waypoint")
        self.x_position_label = QLabel("0")
        self.y_position_label = QLabel("0")
        self.alt_label = QLabel("0")
        self.name_label = QLabel("")
        self.desc_label = QLabel("")
        self.init_ui()

    def init_ui(self) -> None:

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

        # layout.addLayout(name_layout)
        layout.addLayout(x_pos_layout)
        layout.addLayout(y_pos_layout)
        layout.addLayout(alt_layout)
        layout.addLayout(desc_layout)

        self.setLayout(layout)

    def set_flight_waypoint(self, flight_wpt: FlightWaypoint) -> None:
        self.x_position_label.setText(str(flight_wpt.x))
        self.y_position_label.setText(str(flight_wpt.y))
        self.alt_label.setText(str(int(flight_wpt.alt.feet)))
        self.name_label.setText(str(flight_wpt.name))
        self.desc_label.setText(str(flight_wpt.description))
        self.setTitle(flight_wpt.name)
