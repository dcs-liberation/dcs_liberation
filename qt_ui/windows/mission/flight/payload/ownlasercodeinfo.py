from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from game import Game
from game.ato.flightmember import FlightMember


class OwnLaserCodeInfo(QHBoxLayout):
    assigned_laser_code_changed = Signal()

    def __init__(
        self, game: Game, flight_member: FlightMember, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.game = game
        self.flight_member = flight_member

        self.addWidget(QLabel("Assigned laser code:"))
        self.addStretch()

        self.code_display = QLabel()
        self.addWidget(self.code_display)

        self.alloc_dealloc_button = QPushButton()
        self.alloc_dealloc_button.clicked.connect(self.on_alloc_dealloc_clicked)
        self.addWidget(self.alloc_dealloc_button)

        self.bind_to_selected_member()

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        self.bind_to_selected_member()

    def bind_to_selected_member(self) -> None:
        if (code := self.flight_member.tgp_laser_code) is not None:
            self.alloc_dealloc_button.setEnabled(True)
            self.alloc_dealloc_button.setText("Release")
            self.code_display.setText(f"{code}")
        elif self.flight_member.is_player:
            self.alloc_dealloc_button.setText("Assign")
            self.alloc_dealloc_button.setEnabled(True)
            self.code_display.setText("Not assigned")
        else:
            self.alloc_dealloc_button.setText("Assign")
            self.alloc_dealloc_button.setEnabled(False)
            self.code_display.setText("AI does not use laser codes")

    def on_alloc_dealloc_clicked(self) -> None:
        if self.flight_member.tgp_laser_code is not None:
            self.flight_member.release_tgp_laser_code()
        else:
            self.flight_member.assign_tgp_laser_code(
                self.game.laser_code_registry.alloc_laser_code()
            )
        self.bind_to_selected_member()
        self.assigned_laser_code_changed.emit()
