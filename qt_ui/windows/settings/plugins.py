from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from game.plugins import LuaPlugin, LuaPluginManager


class PluginsBox(QGroupBox):
    def __init__(self, manager: LuaPluginManager) -> None:
        super().__init__("Plugins")

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        for row, plugin in enumerate(manager.iter_plugins()):
            if not plugin.show_in_ui:
                continue

            layout.addWidget(QLabel(plugin.name), row, 0)

            checkbox = QCheckBox()
            checkbox.setChecked(plugin.enabled)
            checkbox.toggled.connect(plugin.set_enabled)
            layout.addWidget(checkbox, row, 1)


class PluginsPage(QWidget):
    def __init__(self, manager: LuaPluginManager) -> None:
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        layout.addWidget(PluginsBox(manager))


class PluginOptionsBox(QGroupBox):
    def __init__(self, plugin: LuaPlugin) -> None:
        super().__init__(plugin.name)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        for row, option in enumerate(plugin.options):
            layout.addWidget(QLabel(option.name), row, 0)

            checkbox = QCheckBox()
            checkbox.setChecked(option.enabled)
            checkbox.toggled.connect(option.set_enabled)
            layout.addWidget(checkbox, row, 1)


class PluginOptionsPage(QWidget):
    def __init__(self, manager: LuaPluginManager) -> None:
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        for plugin in manager.iter_plugins():
            if plugin.options:
                layout.addWidget(PluginOptionsBox(plugin))
