from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, QSlider

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
