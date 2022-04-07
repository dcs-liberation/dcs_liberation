from datetime import timedelta
from typing import Optional

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSlider, QHBoxLayout

from qt_ui.widgets.floatspinners import FloatSpinner


class FloatSpinSlider(QHBoxLayout):
    def __init__(
        self, minimum: float, maximum: float, initial: float, divisor: int
    ) -> None:
        super().__init__()

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(int(minimum * divisor))
        slider.setMaximum(int(maximum * divisor))
        slider.setValue(int(initial * divisor))
        self.spinner = FloatSpinner(divisor, minimum, maximum, initial)
        slider.valueChanged.connect(lambda x: self.spinner.setValue(x))
        self.spinner.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider)
        self.addWidget(self.spinner)

    @property
    def value(self) -> float:
        return self.spinner.real_value


class TimeInputs(QtWidgets.QHBoxLayout):
    def __init__(self, initial: timedelta, minimum: int, maximum: int) -> None:
        super().__init__()

        initial_minutes = int(initial.total_seconds() / 60)

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(initial_minutes)
        self.spinner = TimeSpinner(minimum, maximum, initial_minutes)
        slider.valueChanged.connect(lambda x: self.spinner.setValue(x))
        self.spinner.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider)
        self.addWidget(self.spinner)

    @property
    def value(self) -> timedelta:
        return timedelta(minutes=self.spinner.value())


class TimeSpinner(QtWidgets.QSpinBox):
    def __init__(
        self,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        initial: Optional[int] = None,
    ) -> None:
        super().__init__()

        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        if initial is not None:
            self.setValue(initial)

    def textFromValue(self, val: int) -> str:
        return f"{val} minutes"


class CurrencySpinner(QtWidgets.QSpinBox):
    def __init__(
        self,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        initial: Optional[int] = None,
    ) -> None:
        super().__init__()

        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        if initial is not None:
            self.setValue(initial)

    def textFromValue(self, val: int) -> str:
        return f"${val}"
