from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, QSlider
from typing import Optional
from qt_ui.widgets.floatspinners import TenthsSpinner


class TenthsSpinSlider(QGridLayout):
    def __init__(self, label: str, minimum: int, maximum: int, initial: int) -> None:
        super().__init__()
        self.addWidget(QLabel(label), 0, 0)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(initial)
        self.spinner = TenthsSpinner(minimum, maximum, initial)
        slider.valueChanged.connect(lambda x: self.spinner.setValue(x))
        self.spinner.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider, 1, 0)
        self.addWidget(self.spinner, 1, 1)

    @property
    def value(self) -> float:
        return self.spinner.value() / 10


class TimeInputs(QtWidgets.QGridLayout):
    def __init__(self, label: str, initial: int) -> None:
        super().__init__()
        self.addWidget(QtWidgets.QLabel(label), 0, 0)

        minimum = 30
        maximum = 150

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(initial)
        self.spinner = TimeSpinner(minimum, maximum, initial)
        slider.valueChanged.connect(lambda x: self.spinner.setValue(x))
        self.spinner.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider, 1, 0)
        self.addWidget(self.spinner, 1, 1)

    @property
    def value(self) -> int:
        return self.spinner.value()


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
