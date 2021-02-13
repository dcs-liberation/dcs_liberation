"""Spin box for selecting the number of aircraft in a flight."""
from PySide2.QtWidgets import QSpinBox


class QFlightSizeSpinner(QSpinBox):
    """Spin box for selecting the number of aircraft in a flight."""

    def __init__(
        self, min_size: int = 1, max_size: int = 4, default_size: int = 2
    ) -> None:
        super().__init__()
        self.setMinimum(min_size)
        self.setMaximum(max_size)
        self.setValue(default_size)
