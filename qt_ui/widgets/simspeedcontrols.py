from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSpinBox, QWidget

from game.sim.simspeedsetting import SimSpeedSetting
from qt_ui.simcontroller import SimController


class SimSpeedSpinner(QSpinBox):
    def __init__(self, sim_controller: SimController, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.sim_controller = sim_controller

        # Disable text editing, which wouldn't work in the first place, but also
        # obnoxiously selects the text on change (highlighting it) and leaves a flashing
        # cursor in the middle of the element when clicked.
        self.lineEdit().setEnabled(False)

        # The value stored by the spinner is the index of the speed setting in the enum.
        # SimSpeedSetting is ordered, so the minimum value is paused, and increasing the
        # value will speed up the game by one speed).
        self.setMinimum(0)
        self.setMaximum(len(SimSpeedSetting) - 1)
        self.setValue(0)

        self.valueChanged.connect(self.on_change)
        self.sim_controller.sim_speed_changed.connect(self.on_sim_speed_reset)

    @staticmethod
    def speed_for_value(value: int) -> SimSpeedSetting:
        return list(SimSpeedSetting)[value]

    def sizeHint(self) -> QSize:
        # The default size hinting fails to deal with label width, and will truncate
        # "Paused".
        size = super().sizeHint()
        size.setWidth(86)
        return size

    def textFromValue(self, value: int) -> str:
        return self.speed_for_value(value).text

    def valueFromText(self, text: str) -> int:
        for idx, speed in enumerate(SimSpeedSetting):
            if speed.text == text:
                return idx
        raise ValueError(f"Unknown SimSpeedSetting: {text}")

    def on_change(self, value: int) -> None:
        self.sim_controller.set_simulation_speed(self.speed_for_value(value))

    def on_sim_speed_reset(self, speed_setting: SimSpeedSetting) -> None:
        self.setValue(list(SimSpeedSetting).index(speed_setting))


class SimSpeedControls(QHBoxLayout):
    def __init__(
        self, sim_controller: SimController, parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.sim_controller = sim_controller

        self.pause_button = QPushButton(text="Pause")
        self.pause_button.clicked.connect(
            lambda: self.sim_controller.set_simulation_speed(SimSpeedSetting.PAUSED)
        )
        self.addWidget(self.pause_button)

        self.speed_spinner = SimSpeedSpinner(sim_controller, parent)
        self.addWidget(self.speed_spinner)
