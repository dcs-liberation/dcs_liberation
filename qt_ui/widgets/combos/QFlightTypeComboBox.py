"""Combo box for selecting a flight's task type."""

from PySide2.QtWidgets import QComboBox

from game.theater import ConflictTheater, MissionTarget


class QFlightTypeComboBox(QComboBox):
    """Combo box for selecting a flight task type."""

    def __init__(self, theater: ConflictTheater, target: MissionTarget) -> None:
        super().__init__()
        self.theater = theater
        self.target = target
        for mission_type in self.target.mission_types(for_player=True):
            self.addItem(str(mission_type), userData=mission_type)
