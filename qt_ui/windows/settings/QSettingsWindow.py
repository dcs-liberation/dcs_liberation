import logging
import textwrap
from typing import Callable

from PySide2.QtCore import QItemSelectionModel, QPoint, QSize, Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QListView,
    QPushButton,
    QSpinBox,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

import qt_ui.uiconstants as CONST
from game.game import Game
from game.server import EventStream
from game.settings import (
    BooleanOption,
    BoundedFloatOption,
    BoundedIntOption,
    ChoicesOption,
    MinutesOption,
    OptionDescription,
    Settings,
)
from game.sim import GameUpdateEvents
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.spinsliders import FloatSpinSlider, TimeInputs
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.settings.plugins import PluginOptionsPage, PluginsPage


class CheatSettingsBox(QGroupBox):
    def __init__(self, game: Game, apply_settings: Callable[[], None]) -> None:
        super().__init__("Cheat Settings")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.red_ato_checkbox = QCheckBox()
        self.red_ato_checkbox.setChecked(game.settings.show_red_ato)
        self.red_ato_checkbox.toggled.connect(apply_settings)

        self.frontline_cheat_checkbox = QCheckBox()
        self.frontline_cheat_checkbox.setChecked(game.settings.enable_frontline_cheats)
        self.frontline_cheat_checkbox.toggled.connect(apply_settings)

        self.base_capture_cheat_checkbox = QCheckBox()
        self.base_capture_cheat_checkbox.setChecked(
            game.settings.enable_base_capture_cheat
        )
        self.base_capture_cheat_checkbox.toggled.connect(apply_settings)

        self.red_ato = QLabeledWidget("Show Red ATO:", self.red_ato_checkbox)
        self.main_layout.addLayout(self.red_ato)
        self.frontline_cheat = QLabeledWidget(
            "Enable Frontline Cheats:", self.frontline_cheat_checkbox
        )
        self.main_layout.addLayout(self.frontline_cheat)
        self.base_capture_cheat = QLabeledWidget(
            "Enable Base Capture Cheat:", self.base_capture_cheat_checkbox
        )
        self.main_layout.addLayout(self.base_capture_cheat)

    @property
    def show_red_ato(self) -> bool:
        return self.red_ato_checkbox.isChecked()

    @property
    def show_frontline_cheat(self) -> bool:
        return self.frontline_cheat_checkbox.isChecked()

    @property
    def show_base_capture_cheat(self) -> bool:
        return self.base_capture_cheat_checkbox.isChecked()


class AutoSettingsLayout(QGridLayout):
    def __init__(
        self,
        page: str,
        section: str,
        settings: Settings,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__()
        self.settings = settings
        self.write_full_settings = write_full_settings

        for row, (name, description) in enumerate(Settings.fields(page, section)):
            self.add_label(row, description)
            if isinstance(description, BooleanOption):
                self.add_checkbox_for(row, name, description)
            elif isinstance(description, ChoicesOption):
                self.add_combobox_for(row, name, description)
            elif isinstance(description, BoundedFloatOption):
                self.add_float_spin_slider_for(row, name, description)
            elif isinstance(description, BoundedIntOption):
                self.add_spinner_for(row, name, description)
            elif isinstance(description, MinutesOption):
                self.add_duration_controls_for(row, name, description)
            else:
                raise TypeError(f"Unhandled option type: {description}")

    def add_label(self, row: int, description: OptionDescription) -> None:
        text = f"<strong>{description.text}</strong>"
        if description.detail is not None:
            wrapped = "<br />".join(textwrap.wrap(description.detail, width=55))
            text += f"<br />{wrapped}"
        label = QLabel(text)
        if description.tooltip is not None:
            label.setToolTip(description.tooltip)
        self.addWidget(label, row, 0)

    def add_checkbox_for(self, row: int, name: str, description: BooleanOption) -> None:
        def on_toggle(value: bool) -> None:
            if description.invert:
                value = not value
            self.settings.__dict__[name] = value
            if description.causes_expensive_game_update:
                self.write_full_settings()

        checkbox = QCheckBox()
        value = self.settings.__dict__[name]
        if description.invert:
            value = not value
        checkbox.setChecked(value)
        checkbox.toggled.connect(on_toggle)
        self.addWidget(checkbox, row, 1, Qt.AlignRight)

    def add_combobox_for(self, row: int, name: str, description: ChoicesOption) -> None:
        combobox = QComboBox()

        def on_changed(index: int) -> None:
            self.settings.__dict__[name] = combobox.itemData(index)

        for text, value in description.choices.items():
            combobox.addItem(text, value)
        combobox.setCurrentText(
            description.text_for_value(self.settings.__dict__[name])
        )
        combobox.currentIndexChanged.connect(on_changed)
        self.addWidget(combobox, row, 1, Qt.AlignRight)

    def add_float_spin_slider_for(
        self, row: int, name: str, description: BoundedFloatOption
    ) -> None:
        spinner = FloatSpinSlider(
            description.min,
            description.max,
            self.settings.__dict__[name],
            divisor=description.divisor,
        )

        def on_changed() -> None:
            self.settings.__dict__[name] = spinner.value

        spinner.spinner.valueChanged.connect(on_changed)
        self.addLayout(spinner, row, 1, Qt.AlignRight)

    def add_spinner_for(
        self, row: int, name: str, description: BoundedIntOption
    ) -> None:
        def on_changed(value: int) -> None:
            self.settings.__dict__[name] = value
            if description.causes_expensive_game_update:
                self.write_full_settings()

        spinner = QSpinBox()
        spinner.setMinimum(description.min)
        spinner.setMaximum(description.max)
        spinner.setValue(self.settings.__dict__[name])

        spinner.valueChanged.connect(on_changed)
        self.addWidget(spinner, row, 1, Qt.AlignRight)

    def add_duration_controls_for(
        self, row: int, name: str, description: MinutesOption
    ) -> None:
        inputs = TimeInputs(
            self.settings.__dict__[name], description.min, description.max
        )

        def on_changed() -> None:
            self.settings.__dict__[name] = inputs.value

        inputs.spinner.valueChanged.connect(on_changed)
        self.addLayout(inputs, row, 1, Qt.AlignRight)


class AutoSettingsGroup(QGroupBox):
    def __init__(
        self,
        page: str,
        section: str,
        settings: Settings,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__(section)
        self.setLayout(AutoSettingsLayout(page, section, settings, write_full_settings))


class AutoSettingsPageLayout(QVBoxLayout):
    def __init__(
        self,
        page: str,
        settings: Settings,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignTop)

        for section in Settings.sections(page):
            self.addWidget(
                AutoSettingsGroup(page, section, settings, write_full_settings)
            )


class AutoSettingsPage(QWidget):
    def __init__(
        self,
        page: str,
        settings: Settings,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__()
        self.setLayout(AutoSettingsPageLayout(page, settings, write_full_settings))


class QSettingsWindow(QDialog):
    def __init__(self, game: Game):
        super().__init__()

        self.game = game
        self.pluginsPage = None
        self.pluginsOptionsPage = None

        self.pages: dict[str, AutoSettingsPage] = {}
        for page in Settings.pages():
            self.pages[page] = AutoSettingsPage(page, game.settings, self.applySettings)

        self.setModal(True)
        self.setWindowTitle("Settings")
        self.setWindowIcon(CONST.ICONS["Settings"])
        self.setMinimumSize(600, 250)

        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()

        self.categoryList = QListView()
        self.right_layout = QStackedLayout()

        self.categoryList.setMaximumWidth(175)

        self.categoryModel = QStandardItemModel(self.categoryList)

        self.categoryList.setIconSize(QSize(32, 32))

        for name, page in self.pages.items():
            page_item = QStandardItem(name)
            if name in CONST.ICONS:
                page_item.setIcon(CONST.ICONS[name])
            else:
                page_item.setIcon(CONST.ICONS["Generator"])
            page_item.setEditable(False)
            page_item.setSelectable(True)
            self.categoryModel.appendRow(page_item)
            self.right_layout.addWidget(page)

        self.initCheatLayout()
        cheat = QStandardItem("Cheat Menu")
        cheat.setIcon(CONST.ICONS["Cheat"])
        cheat.setEditable(False)
        cheat.setSelectable(True)
        self.categoryModel.appendRow(cheat)
        self.right_layout.addWidget(self.cheatPage)

        self.pluginsPage = PluginsPage()
        plugins = QStandardItem("LUA Plugins")
        plugins.setIcon(CONST.ICONS["Plugins"])
        plugins.setEditable(False)
        plugins.setSelectable(True)
        self.categoryModel.appendRow(plugins)
        self.right_layout.addWidget(self.pluginsPage)

        self.pluginsOptionsPage = PluginOptionsPage()
        pluginsOptions = QStandardItem("LUA Plugins Options")
        pluginsOptions.setIcon(CONST.ICONS["PluginsOptions"])
        pluginsOptions.setEditable(False)
        pluginsOptions.setSelectable(True)
        self.categoryModel.appendRow(pluginsOptions)
        self.right_layout.addWidget(self.pluginsOptionsPage)

        self.categoryList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.categoryList.setModel(self.categoryModel)
        self.categoryList.selectionModel().setCurrentIndex(
            self.categoryList.indexAt(QPoint(1, 1)), QItemSelectionModel.Select
        )
        self.categoryList.selectionModel().selectionChanged.connect(
            self.onSelectionChanged
        )

        self.layout.addWidget(self.categoryList, 0, 0, 1, 1)
        self.layout.addLayout(self.right_layout, 0, 1, 5, 1)

        self.setLayout(self.layout)

    def initCheatLayout(self):

        self.cheatPage = QWidget()
        self.cheatLayout = QVBoxLayout()
        self.cheatPage.setLayout(self.cheatLayout)

        self.cheat_options = CheatSettingsBox(self.game, self.applySettings)
        self.cheatLayout.addWidget(self.cheat_options)

        self.moneyCheatBox = QGroupBox("Money Cheat")
        self.moneyCheatBox.setAlignment(Qt.AlignTop)
        self.moneyCheatBoxLayout = QGridLayout()
        self.moneyCheatBox.setLayout(self.moneyCheatBoxLayout)

        cheats_amounts = [25, 50, 100, 200, 500, 1000, -25, -50, -100, -200]
        for i, amount in enumerate(cheats_amounts):
            if amount > 0:
                btn = QPushButton("Cheat +" + str(amount) + "M")
                btn.setProperty("style", "btn-success")
            else:
                btn = QPushButton("Cheat " + str(amount) + "M")
                btn.setProperty("style", "btn-danger")
            btn.clicked.connect(self.cheatLambda(amount))
            self.moneyCheatBoxLayout.addWidget(btn, i / 2, i % 2)
        self.cheatLayout.addWidget(self.moneyCheatBox, stretch=1)

    def cheatLambda(self, amount):
        return lambda: self.cheatMoney(amount)

    def cheatMoney(self, amount):
        logging.info("CHEATING FOR AMOUNT : " + str(amount) + "M")
        self.game.blue.budget += amount
        GameUpdateSignal.get_instance().updateGame(self.game)

    def applySettings(self):
        self.game.settings.show_red_ato = self.cheat_options.show_red_ato
        self.game.settings.enable_frontline_cheats = (
            self.cheat_options.show_frontline_cheat
        )
        self.game.settings.enable_base_capture_cheat = (
            self.cheat_options.show_base_capture_cheat
        )

        events = GameUpdateEvents()
        self.game.compute_unculled_zones(events)
        EventStream.put_nowait(events)
        GameUpdateSignal.get_instance().updateGame(self.game)

    def onSelectionChanged(self):
        index = self.categoryList.selectionModel().currentIndex().row()
        self.right_layout.setCurrentIndex(index)
