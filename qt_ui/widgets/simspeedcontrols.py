from __future__ import annotations

from typing import Optional

from PySide2.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget

from game.sim.simspeedsetting import SimSpeedSetting
from qt_ui.simcontroller import SimController


class SimSpeedControls(QHBoxLayout):
    def __init__(
        self, sim_controller: SimController, parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.sim_controller = sim_controller
        self.button_group = QButtonGroup(self)
        self.buttons: dict[SimSpeedSetting, QPushButton] = {}

        for speed_setting in SimSpeedSetting:
            button = QPushButton(speed_setting.text)
            button.setCheckable(True)  # TODO: CSS
            self.button_group.addButton(button, id=speed_setting.speed_factor)
            self.addWidget(button)
            self.buttons[speed_setting] = button

        self.button_group.idPressed.connect(self.speed_changed)
        self.sim_controller.sim_speed_reset.connect(self.on_sim_speed_reset)

    def speed_changed(self, speed_factor: int) -> None:
        setting = SimSpeedSetting.from_factor(speed_factor)
        self.sim_controller.set_simulation_speed(setting)

    def on_sim_speed_reset(self, speed_setting: SimSpeedSetting) -> None:
        self.buttons[speed_setting].setChecked(True)
