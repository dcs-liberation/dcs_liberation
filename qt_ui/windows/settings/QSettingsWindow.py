import logging
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
from dcs.forcedoptions import ForcedOptions

import qt_ui.uiconstants as CONST
from game.game import Game
from game.infos.information import Information
from game.settings import Settings
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.spinsliders import TenthsSpinSlider, TimeInputs
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.finances.QFinancesMenu import QHorizontalSeparationLine
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


START_TYPE_TOOLTIP = "Selects the start type used for AI aircraft."


class StartTypeComboBox(QComboBox):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.addItems(["Cold", "Warm", "Runway", "In Flight"])
        self.currentTextChanged.connect(self.on_change)
        self.setToolTip(START_TYPE_TOOLTIP)

    def on_change(self, value: str) -> None:
        self.settings.default_start_type = value


class QSettingsWindow(QDialog):
    def __init__(self, game: Game):
        super(QSettingsWindow, self).__init__()

        self.game = game
        self.pluginsPage = None
        self.pluginsOptionsPage = None
        self.campaign_management_page = QWidget()

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

        self.initDifficultyLayout()
        difficulty = QStandardItem("Difficulty")
        difficulty.setIcon(CONST.ICONS["Missile"])
        difficulty.setEditable(False)
        difficulty.setSelectable(True)
        self.categoryModel.appendRow(difficulty)
        self.right_layout.addWidget(self.difficultyPage)

        self.init_campaign_management_layout()
        campaign_management = QStandardItem("Campaign Management")
        campaign_management.setIcon(CONST.ICONS["Money"])
        campaign_management.setEditable(False)
        campaign_management.setSelectable(True)
        self.categoryModel.appendRow(campaign_management)
        self.right_layout.addWidget(self.campaign_management_page)

        self.initGeneratorLayout()
        generator = QStandardItem("Mission Generator")
        generator.setIcon(CONST.ICONS["Generator"])
        generator.setEditable(False)
        generator.setSelectable(True)
        self.categoryModel.appendRow(generator)
        self.right_layout.addWidget(self.generatorPage)

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

    def init(self):
        pass

    def initDifficultyLayout(self):

        self.difficultyPage = QWidget()
        self.difficultyLayout = QVBoxLayout()
        self.difficultyLayout.setAlignment(Qt.AlignTop)
        self.difficultyPage.setLayout(self.difficultyLayout)

        # DCS AI difficulty settings
        self.aiDifficultySettings = QGroupBox("AI Difficulty")
        self.aiDifficultyLayout = QGridLayout()
        self.playerCoalitionSkill = QComboBox()
        self.enemyCoalitionSkill = QComboBox()
        self.enemyAASkill = QComboBox()
        for skill in CONST.SKILL_OPTIONS:
            self.playerCoalitionSkill.addItem(skill)
            self.enemyCoalitionSkill.addItem(skill)
            self.enemyAASkill.addItem(skill)

        self.playerCoalitionSkill.setCurrentIndex(
            CONST.SKILL_OPTIONS.index(self.game.settings.player_skill)
        )
        self.enemyCoalitionSkill.setCurrentIndex(
            CONST.SKILL_OPTIONS.index(self.game.settings.enemy_skill)
        )
        self.enemyAASkill.setCurrentIndex(
            CONST.SKILL_OPTIONS.index(self.game.settings.enemy_vehicle_skill)
        )

        self.player_income = TenthsSpinSlider(
            "Player income multiplier",
            0,
            50,
            int(self.game.settings.player_income_multiplier * 10),
        )
        self.player_income.spinner.valueChanged.connect(self.applySettings)
        self.enemy_income = TenthsSpinSlider(
            "Enemy income multiplier",
            0,
            50,
            int(self.game.settings.enemy_income_multiplier * 10),
        )
        self.enemy_income.spinner.valueChanged.connect(self.applySettings)

        self.playerCoalitionSkill.currentIndexChanged.connect(self.applySettings)
        self.enemyCoalitionSkill.currentIndexChanged.connect(self.applySettings)
        self.enemyAASkill.currentIndexChanged.connect(self.applySettings)

        # Mission generation settings related to difficulty
        self.missionSettings = QGroupBox("Mission Difficulty")
        self.missionLayout = QGridLayout()

        self.manpads = QCheckBox()
        self.manpads.setChecked(self.game.settings.manpads)
        self.manpads.toggled.connect(self.applySettings)

        self.noNightMission = QCheckBox()
        self.noNightMission.setChecked(self.game.settings.night_disabled)
        self.noNightMission.toggled.connect(self.applySettings)

        # DCS Mission options
        self.missionRestrictionsSettings = QGroupBox("Mission Restrictions")
        self.missionRestrictionsLayout = QGridLayout()

        self.difficultyLabel = QComboBox()
        [self.difficultyLabel.addItem(t) for t in CONST.LABELS_OPTIONS]
        self.difficultyLabel.setCurrentIndex(
            CONST.LABELS_OPTIONS.index(self.game.settings.labels)
        )
        self.difficultyLabel.currentIndexChanged.connect(self.applySettings)

        self.mapVisibiitySelection = QComboBox()
        self.mapVisibiitySelection.addItem("All", ForcedOptions.Views.All)
        if self.game.settings.map_coalition_visibility == ForcedOptions.Views.All:
            self.mapVisibiitySelection.setCurrentIndex(0)
        self.mapVisibiitySelection.addItem("Fog of War", ForcedOptions.Views.Allies)
        if self.game.settings.map_coalition_visibility == ForcedOptions.Views.Allies:
            self.mapVisibiitySelection.setCurrentIndex(1)
        self.mapVisibiitySelection.addItem(
            "Allies Only", ForcedOptions.Views.OnlyAllies
        )
        if (
            self.game.settings.map_coalition_visibility
            == ForcedOptions.Views.OnlyAllies
        ):
            self.mapVisibiitySelection.setCurrentIndex(2)
        self.mapVisibiitySelection.addItem(
            "Own Aircraft Only", ForcedOptions.Views.MyAircraft
        )
        if (
            self.game.settings.map_coalition_visibility
            == ForcedOptions.Views.MyAircraft
        ):
            self.mapVisibiitySelection.setCurrentIndex(3)
        self.mapVisibiitySelection.addItem("Map Only", ForcedOptions.Views.OnlyMap)
        if self.game.settings.map_coalition_visibility == ForcedOptions.Views.OnlyMap:
            self.mapVisibiitySelection.setCurrentIndex(4)
        self.mapVisibiitySelection.currentIndexChanged.connect(self.applySettings)

        self.ext_views = QCheckBox()
        self.ext_views.setChecked(self.game.settings.external_views_allowed)
        self.ext_views.toggled.connect(self.applySettings)

        self.aiDifficultyLayout.addWidget(QLabel("Player coalition skill"), 0, 0)
        self.aiDifficultyLayout.addWidget(
            self.playerCoalitionSkill, 0, 1, Qt.AlignRight
        )
        self.aiDifficultyLayout.addWidget(QLabel("Enemy coalition skill"), 1, 0)
        self.aiDifficultyLayout.addWidget(self.enemyCoalitionSkill, 1, 1, Qt.AlignRight)
        self.aiDifficultyLayout.addWidget(QLabel("Enemy AA and vehicles skill"), 2, 0)
        self.aiDifficultyLayout.addWidget(self.enemyAASkill, 2, 1, Qt.AlignRight)
        self.aiDifficultyLayout.addLayout(self.player_income, 3, 0)
        self.aiDifficultyLayout.addLayout(self.enemy_income, 4, 0)
        self.aiDifficultySettings.setLayout(self.aiDifficultyLayout)
        self.difficultyLayout.addWidget(self.aiDifficultySettings)

        self.missionLayout.addWidget(QLabel("Manpads on frontlines"), 0, 0)
        self.missionLayout.addWidget(self.manpads, 0, 1, Qt.AlignRight)
        self.missionLayout.addWidget(QLabel("No night missions"), 1, 0)
        self.missionLayout.addWidget(self.noNightMission, 1, 1, Qt.AlignRight)
        self.missionSettings.setLayout(self.missionLayout)
        self.difficultyLayout.addWidget(self.missionSettings)

        self.missionRestrictionsLayout.addWidget(QLabel("In Game Labels"), 0, 0)
        self.missionRestrictionsLayout.addWidget(
            self.difficultyLabel, 0, 1, Qt.AlignRight
        )
        self.missionRestrictionsLayout.addWidget(QLabel("Map visibility options"), 1, 0)
        self.missionRestrictionsLayout.addWidget(
            self.mapVisibiitySelection, 1, 1, Qt.AlignRight
        )
        self.missionRestrictionsLayout.addWidget(QLabel("Allow external views"), 2, 0)
        self.missionRestrictionsLayout.addWidget(self.ext_views, 2, 1, Qt.AlignRight)
        self.missionRestrictionsSettings.setLayout(self.missionRestrictionsLayout)
        self.difficultyLayout.addWidget(self.missionRestrictionsSettings)

    def init_campaign_management_layout(self) -> None:
        campaign_layout = QVBoxLayout()
        campaign_layout.setAlignment(Qt.AlignTop)
        self.campaign_management_page.setLayout(campaign_layout)

        general = QGroupBox("General")
        campaign_layout.addWidget(general)

        general_layout = QGridLayout()
        general.setLayout(general_layout)

        def set_restict_weapons_by_date(value: bool) -> None:
            self.game.settings.restrict_weapons_by_date = value

        restrict_weapons = QCheckBox()
        restrict_weapons.setChecked(self.game.settings.restrict_weapons_by_date)
        restrict_weapons.toggled.connect(set_restict_weapons_by_date)

        tooltip_text = (
            "Restricts weapon availability based on the campaign date. Data is "
            "extremely incomplete so does not affect all weapons."
        )
        restrict_weapons.setToolTip(tooltip_text)
        restrict_weapons_label = QLabel("Restrict weapons by date (WIP)")
        restrict_weapons_label.setToolTip(tooltip_text)

        general_layout.addWidget(restrict_weapons_label, 0, 0)
        general_layout.addWidget(restrict_weapons, 0, 1, Qt.AlignRight)

        def set_old_awec(value: bool) -> None:
            self.game.settings.disable_legacy_aewc = value

        old_awac = QCheckBox()
        old_awac.setChecked(self.game.settings.disable_legacy_aewc)
        old_awac.toggled.connect(set_old_awec)

        old_awec_info = (
            "If checked, the invulnerable friendly AEW&C aircraft that begins "
            "the mission in the air will not be spawned. AEW&C missions must "
            "be planned in the ATO and will take time to arrive on-station."
        )

        old_awac.setToolTip(old_awec_info)
        old_awac_label = QLabel("Disable invulnerable, always-available AEW&C (WIP)")
        old_awac_label.setToolTip(old_awec_info)

        general_layout.addWidget(old_awac_label, 1, 0)
        general_layout.addWidget(old_awac, 1, 1, Qt.AlignRight)

        automation = QGroupBox("HQ Automation")
        campaign_layout.addWidget(automation)

        automation_layout = QGridLayout()
        automation.setLayout(automation_layout)

        def set_runway_automation(value: bool) -> None:
            self.game.settings.automate_runway_repair = value

        def set_front_line_automation(value: bool) -> None:
            self.game.settings.automate_front_line_reinforcements = value

        def set_aircraft_automation(value: bool) -> None:
            self.game.settings.automate_aircraft_reinforcements = value

        runway_repair = QCheckBox()
        runway_repair.setChecked(self.game.settings.automate_runway_repair)
        runway_repair.toggled.connect(set_runway_automation)

        automation_layout.addWidget(QLabel("Automate runway repairs"), 0, 0)
        automation_layout.addWidget(runway_repair, 0, 1, Qt.AlignRight)

        front_line = QCheckBox()
        front_line.setChecked(self.game.settings.automate_front_line_reinforcements)
        front_line.toggled.connect(set_front_line_automation)

        automation_layout.addWidget(QLabel("Automate front-line purchases"), 1, 0)
        automation_layout.addWidget(front_line, 1, 1, Qt.AlignRight)

        aircraft = QCheckBox()
        aircraft.setChecked(self.game.settings.automate_aircraft_reinforcements)
        aircraft.toggled.connect(set_aircraft_automation)

        automation_layout.addWidget(QLabel("Automate aircraft purchases"), 2, 0)
        automation_layout.addWidget(aircraft, 2, 1, Qt.AlignRight)

    def initGeneratorLayout(self):
        self.generatorPage = QWidget()
        self.generatorLayout = QVBoxLayout()
        self.generatorLayout.setAlignment(Qt.AlignTop)
        self.generatorPage.setLayout(self.generatorLayout)

        self.gameplay = QGroupBox("Gameplay")
        self.gameplayLayout = QGridLayout()
        self.gameplayLayout.setAlignment(Qt.AlignTop)
        self.gameplay.setLayout(self.gameplayLayout)

        self.supercarrier = QCheckBox()
        self.supercarrier.setChecked(self.game.settings.supercarrier)
        self.supercarrier.toggled.connect(self.applySettings)

        self.generate_marks = QCheckBox()
        self.generate_marks.setChecked(self.game.settings.generate_marks)
        self.generate_marks.toggled.connect(self.applySettings)

        self.generate_dark_kneeboard = QCheckBox()
        self.generate_dark_kneeboard.setChecked(
            self.game.settings.generate_dark_kneeboard
        )
        self.generate_dark_kneeboard.toggled.connect(self.applySettings)

        self.never_delay_players = QCheckBox()
        self.never_delay_players.setChecked(
            self.game.settings.never_delay_player_flights
        )
        self.never_delay_players.toggled.connect(self.applySettings)
        self.never_delay_players.setToolTip(
            "When checked, player flights with a delayed start time will be "
            "spawned immediately. AI wingmen may begin startup immediately."
        )

        self.desired_player_mission_duration = TimeInputs(
            "Desired mission duration",
            self.game.settings.desired_player_mission_duration,
        )
        self.desired_player_mission_duration.spinner.valueChanged.connect(
            self.applySettings
        )

        self.gameplayLayout.addWidget(QLabel("Use Supercarrier Module"), 0, 0)
        self.gameplayLayout.addWidget(self.supercarrier, 0, 1, Qt.AlignRight)
        self.gameplayLayout.addWidget(QLabel("Put Objective Markers on Map"), 1, 0)
        self.gameplayLayout.addWidget(self.generate_marks, 1, 1, Qt.AlignRight)

        dark_kneeboard_label = QLabel(
            "Generate Dark Kneeboard <br />"
            "<strong>Dark kneeboard for night missions.<br />"
            "This will likely make the kneeboard on the pilot leg unreadable.</strong>"
        )
        self.gameplayLayout.addWidget(dark_kneeboard_label, 2, 0)
        self.gameplayLayout.addWidget(self.generate_dark_kneeboard, 2, 1, Qt.AlignRight)
        self.gameplayLayout.addLayout(
            self.desired_player_mission_duration, 5, 0, Qt.AlignRight
        )

        spawn_players_immediately_tooltip = (
            "Always spawns player aircraft immediately, even if their start time is "
            "more than 10 minutes after the start of the mission. <strong>This does "
            "not alter the timing of your mission. Your TOT will not change. This "
            "option only allows the player to wait on the ground.</strong>"
        )
        spawn_immediately_label = QLabel(
            "Player flights ignore TOT and spawn immediately<br />"
            "<strong>Does not adjust package waypoint times.<br />"
            "Should not be used if players have runway or in-air starts.</strong>"
        )
        spawn_immediately_label.setToolTip(spawn_players_immediately_tooltip)
        self.gameplayLayout.addWidget(spawn_immediately_label, 3, 0)
        self.gameplayLayout.addWidget(self.never_delay_players, 3, 1, Qt.AlignRight)

        start_type_label = QLabel(
            "Default start type for AI aircraft<br /><strong>Warning: "
            "Any option other than Cold breaks OCA/Aircraft missions.</strong>"
        )
        start_type_label.setToolTip(START_TYPE_TOOLTIP)
        start_type = StartTypeComboBox(self.game.settings)
        start_type.setCurrentText(self.game.settings.default_start_type)

        self.gameplayLayout.addWidget(start_type_label, 4, 0)
        self.gameplayLayout.addWidget(start_type, 4, 1)

        self.performance = QGroupBox("Performance")
        self.performanceLayout = QGridLayout()
        self.performanceLayout.setAlignment(Qt.AlignTop)
        self.performance.setLayout(self.performanceLayout)

        self.smoke = QCheckBox()
        self.smoke.setChecked(self.game.settings.perf_smoke_gen)
        self.smoke.toggled.connect(self.applySettings)

        self.smoke_spacing = QSpinBox()
        self.smoke_spacing.setMinimum(800)
        self.smoke_spacing.setMaximum(24000)
        self.smoke_spacing.setValue(self.game.settings.perf_smoke_spacing)
        self.smoke_spacing.valueChanged.connect(self.applySettings)

        self.red_alert = QCheckBox()
        self.red_alert.setChecked(self.game.settings.perf_red_alert_state)
        self.red_alert.toggled.connect(self.applySettings)

        self.arti = QCheckBox()
        self.arti.setChecked(self.game.settings.perf_artillery)
        self.arti.toggled.connect(self.applySettings)

        self.moving_units = QCheckBox()
        self.moving_units.setChecked(self.game.settings.perf_moving_units)
        self.moving_units.toggled.connect(self.applySettings)

        self.infantry = QCheckBox()
        self.infantry.setChecked(self.game.settings.perf_infantry)
        self.infantry.toggled.connect(self.applySettings)

        self.destroyed_units = QCheckBox()
        self.destroyed_units.setChecked(self.game.settings.perf_destroyed_units)
        self.destroyed_units.toggled.connect(self.applySettings)

        self.culling = QCheckBox()
        self.culling.setChecked(self.game.settings.perf_culling)
        self.culling.toggled.connect(self.applySettings)

        self.culling_distance = QSpinBox()
        self.culling_distance.setMinimum(10)
        self.culling_distance.setMaximum(10000)
        self.culling_distance.setValue(self.game.settings.perf_culling_distance)
        self.culling_distance.valueChanged.connect(self.applySettings)

        self.culling_do_not_cull_carrier = QCheckBox()
        self.culling_do_not_cull_carrier.setChecked(
            self.game.settings.perf_do_not_cull_carrier
        )
        self.culling_do_not_cull_carrier.toggled.connect(self.applySettings)

        self.performanceLayout.addWidget(
            QLabel("Smoke visual effect on frontline"), 0, 0
        )
        self.performanceLayout.addWidget(self.smoke, 0, 1, alignment=Qt.AlignRight)
        self.performanceLayout.addWidget(
            QLabel("Smoke generator spacing (higher means less smoke)"),
            1,
            0,
            alignment=Qt.AlignRight,
        )
        self.performanceLayout.addWidget(
            self.smoke_spacing, 1, 1, alignment=Qt.AlignRight
        )
        self.performanceLayout.addWidget(QLabel("SAM starts in RED alert mode"), 2, 0)
        self.performanceLayout.addWidget(self.red_alert, 2, 1, alignment=Qt.AlignRight)
        self.performanceLayout.addWidget(QLabel("Artillery strikes"), 3, 0)
        self.performanceLayout.addWidget(self.arti, 3, 1, alignment=Qt.AlignRight)
        self.performanceLayout.addWidget(QLabel("Moving ground units"), 4, 0)
        self.performanceLayout.addWidget(
            self.moving_units, 4, 1, alignment=Qt.AlignRight
        )
        self.performanceLayout.addWidget(
            QLabel("Generate infantry squads along vehicles"), 5, 0
        )
        self.performanceLayout.addWidget(self.infantry, 5, 1, alignment=Qt.AlignRight)
        self.performanceLayout.addWidget(
            QLabel("Include destroyed units carcass"), 6, 0
        )
        self.performanceLayout.addWidget(
            self.destroyed_units, 6, 1, alignment=Qt.AlignRight
        )

        self.performanceLayout.addWidget(QHorizontalSeparationLine(), 7, 0, 1, 2)
        self.performanceLayout.addWidget(
            QLabel("Culling of distant units enabled"), 8, 0
        )
        self.performanceLayout.addWidget(self.culling, 8, 1, alignment=Qt.AlignRight)
        self.performanceLayout.addWidget(QLabel("Culling distance (km)"), 9, 0)
        self.performanceLayout.addWidget(
            self.culling_distance, 9, 1, alignment=Qt.AlignRight
        )
        self.performanceLayout.addWidget(
            QLabel("Do not cull carrier's surroundings"), 10, 0
        )
        self.performanceLayout.addWidget(
            self.culling_do_not_cull_carrier, 10, 1, alignment=Qt.AlignRight
        )

        self.generatorLayout.addWidget(self.gameplay)
        self.generatorLayout.addWidget(
            QLabel(
                "Disabling settings below may improve performance, but will impact the overall quality of the experience."
            )
        )
        self.generatorLayout.addWidget(self.performance)

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
        self.game.budget += amount
        if amount > 0:
            self.game.informations.append(
                Information(
                    "CHEATER",
                    "You are a cheater and you should feel bad",
                    self.game.turn,
                )
            )
        else:
            self.game.informations.append(
                Information("CHEATER", "You are still a cheater !", self.game.turn)
            )
        GameUpdateSignal.get_instance().updateGame(self.game)

    def applySettings(self):
        self.game.settings.player_skill = CONST.SKILL_OPTIONS[
            self.playerCoalitionSkill.currentIndex()
        ]
        self.game.settings.enemy_skill = CONST.SKILL_OPTIONS[
            self.enemyCoalitionSkill.currentIndex()
        ]
        self.game.settings.enemy_vehicle_skill = CONST.SKILL_OPTIONS[
            self.enemyAASkill.currentIndex()
        ]
        self.game.settings.player_income_multiplier = self.player_income.value
        self.game.settings.enemy_income_multiplier = self.enemy_income.value
        self.game.settings.manpads = self.manpads.isChecked()
        self.game.settings.labels = CONST.LABELS_OPTIONS[
            self.difficultyLabel.currentIndex()
        ]
        self.game.settings.night_disabled = self.noNightMission.isChecked()
        self.game.settings.map_coalition_visibility = (
            self.mapVisibiitySelection.currentData()
        )
        self.game.settings.external_views_allowed = self.ext_views.isChecked()
        self.game.settings.generate_marks = self.generate_marks.isChecked()
        self.game.settings.never_delay_player_flights = (
            self.never_delay_players.isChecked()
        )

        self.game.settings.supercarrier = self.supercarrier.isChecked()

        self.game.settings.generate_dark_kneeboard = (
            self.generate_dark_kneeboard.isChecked()
        )

        self.game.settings.desired_player_mission_duration = (
            self.desired_player_mission_duration.value
        )

        self.game.settings.perf_red_alert_state = self.red_alert.isChecked()
        self.game.settings.perf_smoke_gen = self.smoke.isChecked()
        self.game.settings.perf_smoke_spacing = self.smoke_spacing.value()
        self.game.settings.perf_artillery = self.arti.isChecked()
        self.game.settings.perf_moving_units = self.moving_units.isChecked()
        self.game.settings.perf_infantry = self.infantry.isChecked()
        self.game.settings.perf_destroyed_units = self.destroyed_units.isChecked()

        self.game.settings.perf_culling = self.culling.isChecked()
        self.game.settings.perf_culling_distance = int(self.culling_distance.value())
        self.game.settings.perf_do_not_cull_carrier = (
            self.culling_do_not_cull_carrier.isChecked()
        )

        self.game.settings.show_red_ato = self.cheat_options.show_red_ato
        self.game.settings.enable_frontline_cheats = (
            self.cheat_options.show_frontline_cheat
        )
        self.game.settings.enable_base_capture_cheat = (
            self.cheat_options.show_base_capture_cheat
        )

        self.game.compute_conflicts_position()
        GameUpdateSignal.get_instance().updateGame(self.game)

    def onSelectionChanged(self):
        index = self.categoryList.selectionModel().currentIndex().row()
        self.right_layout.setCurrentIndex(index)
