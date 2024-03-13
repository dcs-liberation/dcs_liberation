from PySide6.QtWidgets import QComboBox, QWidget

from game import Game
from game.ato.flightmember import FlightMember
from qt_ui.blocksignals import block_signals


class WeaponLaserCodeSelector(QComboBox):
    def __init__(
        self, game: Game, flight_member: FlightMember, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.game = game
        self.flight_member = flight_member
        self.currentIndexChanged.connect(self.on_index_changed)

        self.rebuild()

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        self.rebuild()

    def on_index_changed(self) -> None:
        self.flight_member.weapon_laser_code = self.currentData()

    def rebuild(self) -> None:
        with block_signals(self):
            self.clear()
            if not self.flight_member.is_player:
                self.setDisabled(True)
                self.addItem("AI does not use laser codes", None)

            self.setEnabled(True)

            self.addItem("Default (1688)", None)
            selected_index: int | None = None
            idx = 1
            if (own := self.flight_member.tgp_laser_code) is not None:
                self.addItem(f"Use own code ({own})", own)
                if own == self.flight_member.weapon_laser_code:
                    selected_index = idx
                idx += 1
            for idx, front in enumerate(self.game.theater.conflicts(), idx):
                self.addItem(
                    f"JTAC {front.name} ({front.laser_code})", front.laser_code
                )
                if front.laser_code == self.flight_member.weapon_laser_code:
                    selected_index = idx

            if selected_index is not None:
                self.setCurrentIndex(selected_index)
