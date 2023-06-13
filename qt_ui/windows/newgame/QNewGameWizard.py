from __future__ import unicode_literals

import logging
import textwrap
from datetime import datetime, timedelta
from typing import List

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QDate, QItemSelectionModel, QPoint, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QDialog,
)
from jinja2 import Environment, FileSystemLoader, select_autoescape

from game.campaignloader.campaign import Campaign, DEFAULT_BUDGET
from game.factions import Faction
from game.factions.factions import Factions
from game.plugins import LuaPlugin, LuaPluginManager
from game.plugins.luaplugin import LuaPluginOption
from game.settings import Settings
from game.theater.start_generator import GameGenerator, GeneratorSettings, ModSettings
from qt_ui.widgets.QLiberationCalendar import QLiberationCalendar
from qt_ui.widgets.spinsliders import CurrencySpinner, FloatSpinSlider, TimeInputs
from qt_ui.windows.AirWingConfigurationDialog import AirWingConfigurationDialog
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.newgame.QCampaignList import QCampaignList

jinja_env = Environment(
    loader=FileSystemLoader("resources/ui/templates"),
    autoescape=select_autoescape(
        disabled_extensions=("",),
        default_for_string=True,
        default=True,
    ),
    trim_blocks=True,
    lstrip_blocks=True,
)

"""
Possible time periods for new games

    `Name`: daytime(day, month, year),

`Identifier` is the name that will appear in the menu
The object is a python datetime object
"""
TIME_PERIODS = {
    "WW2 - Winter [1944]": datetime(1944, 1, 1),
    "WW2 - Spring [1944]": datetime(1944, 4, 1),
    "WW2 - Summer [1944]": datetime(1944, 6, 1),
    "WW2 - Fall [1944]": datetime(1944, 10, 1),
    "Early Cold War - Winter [1952]": datetime(1952, 1, 1),
    "Early Cold War - Spring [1952]": datetime(1952, 4, 1),
    "Early Cold War - Summer [1952]": datetime(1952, 6, 1),
    "Early Cold War - Fall [1952]": datetime(1952, 10, 1),
    "Cold War - Winter [1970]": datetime(1970, 1, 1),
    "Cold War - Spring [1970]": datetime(1970, 4, 1),
    "Cold War - Summer [1970]": datetime(1970, 6, 1),
    "Cold War - Fall [1970]": datetime(1970, 10, 1),
    "Late Cold War - Winter [1985]": datetime(1985, 1, 1),
    "Late Cold War - Spring [1985]": datetime(1985, 4, 1),
    "Late Cold War - Summer [1985]": datetime(1985, 6, 1),
    "Late Cold War - Fall [1985]": datetime(1985, 10, 1),
    "Gulf War - Winter [1990]": datetime(1990, 1, 1),
    "Gulf War - Spring [1990]": datetime(1990, 4, 1),
    "Gulf War - Summer [1990]": datetime(1990, 6, 1),
    "Mid-90s - Winter [1995]": datetime(1995, 1, 1),
    "Mid-90s - Spring [1995]": datetime(1995, 4, 1),
    "Mid-90s - Summer [1995]": datetime(1995, 6, 1),
    "Mid-90s - Fall [1995]": datetime(1995, 10, 1),
    "Gulf War - Fall [1990]": datetime(1990, 10, 1),
    "Modern - Winter [2010]": datetime(2010, 1, 1),
    "Modern - Spring [2010]": datetime(2010, 4, 1),
    "Modern - Summer [2010]": datetime(2010, 6, 1),
    "Modern - Fall [2010]": datetime(2010, 10, 1),
    "Georgian War [2008]": datetime(2008, 8, 7),
    "Syrian War [2011]": datetime(2011, 3, 15),
    "6 days war [1967]": datetime(1967, 6, 5),
    "Yom Kippour War [1973]": datetime(1973, 10, 6),
    "First Lebanon War [1982]": datetime(1982, 6, 6),
    "Arab-Israeli War [1948]": datetime(1948, 5, 15),
}


def wrap_label_text(text: str, width: int = 100) -> str:
    return "<br />".join(textwrap.wrap(text, width=width))


class NewGameWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewGameWizard, self).__init__(parent)
        self.setModal(True)

        # The wizard should probably be refactored to edit this directly, but for now we
        # just create a Settings object so that we can load the player's preserved
        # defaults. We'll recreate a new settings and merge in the wizard options later.
        default_settings = Settings()
        default_settings.merge_player_settings()

        mod_settings = ModSettings()
        mod_settings.merge_player_settings()

        self.lua_plugin_manager = LuaPluginManager.load()
        self.lua_plugin_manager.merge_player_settings()

        factions = Factions.load()

        self.campaigns = list(sorted(Campaign.load_each(), key=lambda x: x.name))

        self.faction_selection_page = FactionSelection(factions)
        self.addPage(IntroPage())
        self.theater_page = TheaterConfiguration(
            self.campaigns, self.faction_selection_page
        )
        self.addPage(self.theater_page)
        self.addPage(self.faction_selection_page)
        self.addPage(GeneratorOptions(default_settings, mod_settings))
        self.difficulty_page = DifficultyAndAutomationOptions(
            default_settings, self.theater_page.campaignList.selected_campaign
        )
        self.plugins_page = PluginsPage(self.lua_plugin_manager)

        # Update difficulty page on campaign select
        self.theater_page.campaign_selected.connect(
            lambda c: self.difficulty_page.set_campaign_values(c)
        )
        self.addPage(self.difficulty_page)
        self.addPage(self.plugins_page)
        self.addPage(ConclusionPage())

        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark1.png"),
        )
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)

        self.setWindowTitle("New Game")

    def accept(self):
        logging.info("New Game Wizard accept")
        logging.info("======================")

        campaign = self.field("selectedCampaign")
        if campaign is None:
            campaign = self.theater_page.campaignList.selected_campaign
        if campaign is None:
            campaign = self.campaigns[0]

        logging.info("New campaign selected: %s", campaign.name)

        if self.field("usePreset"):
            start_date = TIME_PERIODS[
                list(TIME_PERIODS.keys())[self.field("timePeriod")]
            ]
        else:
            start_date = self.theater_page.calendar.selectedDate().toPython()

        self.lua_plugin_manager.save_player_settings()

        use_new_squadron_rules = self.field("use_new_squadron_rules")
        logging.info("New campaign start date: %s", start_date.strftime("%m/%d/%Y"))
        settings = Settings(
            player_income_multiplier=self.field("player_income_multiplier") / 10,
            enemy_income_multiplier=self.field("enemy_income_multiplier") / 10,
            automate_runway_repair=self.field("automate_runway_repairs"),
            automate_front_line_reinforcements=self.field(
                "automate_front_line_purchases"
            ),
            desired_player_mission_duration=timedelta(
                minutes=self.field("desired_player_mission_duration")
            ),
            automate_aircraft_reinforcements=self.field("automate_aircraft_purchases"),
            supercarrier=self.field("supercarrier"),
            enable_squadron_aircraft_limits=use_new_squadron_rules,
        )
        settings.save_player_settings()
        generator_settings = GeneratorSettings(
            start_date=start_date,
            start_time=campaign.recommended_start_time,
            player_budget=int(self.field("starting_money")),
            enemy_budget=int(self.field("enemy_starting_money")),
            # QSlider forces integers, so we use 1 to 50 and divide by 10 to
            # give 0.1 to 5.0.
            inverted=self.field("invertMap"),
            advanced_iads=self.field("advanced_iads"),
            no_carrier=self.field("no_carrier"),
            no_lha=self.field("no_lha"),
            no_player_navy=self.field("no_player_navy"),
            no_enemy_navy=self.field("no_enemy_navy"),
        )
        mod_settings = ModSettings(
            a4_skyhawk=self.field("a4_skyhawk"),
            f22_raptor=self.field("f22_raptor"),
            f104_starfighter=self.field("f104_starfighter"),
            f4_phantom=self.field("f4_phantom"),
            hercules=self.field("hercules"),
            uh_60l=self.field("uh_60l"),
            jas39_gripen=self.field("jas39_gripen"),
            su57_felon=self.field("su57_felon"),
            ov10a_bronco=self.field("ov10a_bronco"),
            frenchpack=self.field("frenchpack"),
            high_digit_sams=self.field("high_digit_sams"),
        )
        mod_settings.save_player_settings()

        blue_faction = self.faction_selection_page.selected_blue_faction
        red_faction = self.faction_selection_page.selected_red_faction

        logging.info("New campaign blue faction: %s", blue_faction.name)
        logging.info("New campaign red faction: %s", red_faction.name)

        theater = campaign.load_theater(generator_settings.advanced_iads)

        logging.info("New campaign theater: %s", theater.terrain.name)

        generator = GameGenerator(
            blue_faction,
            red_faction,
            theater,
            campaign.load_air_wing_config(theater),
            settings,
            generator_settings,
            mod_settings,
            self.lua_plugin_manager,
        )
        game = generator.generate()

        if AirWingConfigurationDialog(game, self).exec() == QDialog.DialogCode.Rejected:
            logging.info("Aborted air wing configuration")
            return

        game.begin_turn_0(squadrons_start_full=use_new_squadron_rules)
        GameUpdateSignal.get_instance().game_generated.emit(game)

        super(NewGameWizard, self).accept()


class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")
        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark1.png"),
        )

        label = QtWidgets.QLabel(
            "This wizard will help you setup a new game.\n\n"
            "Please make sure you saved and backed up your previous game before going through."
        )
        label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class FactionSelection(QtWidgets.QWizardPage):
    def __init__(self, factions: Factions, parent=None) -> None:
        super().__init__(parent)

        self.factions = factions

        self.setTitle("Faction selection")
        self.setSubTitle(
            "\nChoose the two opposing factions and select the player side."
        )
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/misc/generator.png"),
        )

        self.setMinimumHeight(250)

        # Factions selection
        self.factionsGroup = QtWidgets.QGroupBox("Factions")
        self.factionsGroupLayout = QtWidgets.QHBoxLayout()
        self.blueGroupLayout = QtWidgets.QGridLayout()
        self.redGroupLayout = QtWidgets.QGridLayout()

        blueFaction = QtWidgets.QLabel("<b>Player Faction :</b>")
        self.blueFactionSelect = QtWidgets.QComboBox()
        for f in self.factions.iter_faction_names():
            self.blueFactionSelect.addItem(f)
        blueFaction.setBuddy(self.blueFactionSelect)

        redFaction = QtWidgets.QLabel("<b>Enemy Faction :</b>")
        self.redFactionSelect = QtWidgets.QComboBox()
        redFaction.setBuddy(self.redFactionSelect)

        # Faction description
        self.blueFactionDescription = QTextEdit("")
        self.blueFactionDescription.setReadOnly(True)

        self.redFactionDescription = QTextEdit("")
        self.redFactionDescription.setReadOnly(True)

        # Setup default selected factions
        for i, r in enumerate(self.factions.iter_faction_names()):
            self.redFactionSelect.addItem(r)
            if r == "Russia 1990":
                self.redFactionSelect.setCurrentIndex(i)
            if r == "USA 2005":
                self.blueFactionSelect.setCurrentIndex(i)

        self.blueGroupLayout.addWidget(blueFaction, 0, 0)
        self.blueGroupLayout.addWidget(self.blueFactionSelect, 0, 1)
        self.blueGroupLayout.addWidget(self.blueFactionDescription, 1, 0, 1, 2)

        self.redGroupLayout.addWidget(redFaction, 0, 0)
        self.redGroupLayout.addWidget(self.redFactionSelect, 0, 1)
        self.redGroupLayout.addWidget(self.redFactionDescription, 1, 0, 1, 2)

        self.factionsGroupLayout.addLayout(self.blueGroupLayout)
        self.factionsGroupLayout.addLayout(self.redGroupLayout)
        self.factionsGroup.setLayout(self.factionsGroupLayout)

        # Docs Link
        docsText = QtWidgets.QLabel(
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Factions"><span style="color:#FFFFFF;">How to create your own faction</span></a>'
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        # Link form fields
        self.registerField("blueFaction", self.blueFactionSelect)
        self.registerField("redFaction", self.redFactionSelect)

        # Build layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.factionsGroup)
        layout.addWidget(docsText)
        self.setLayout(layout)
        self.updateUnitRecap()

        self.blueFactionSelect.activated.connect(self.updateUnitRecap)
        self.redFactionSelect.activated.connect(self.updateUnitRecap)

    def setDefaultFactions(self, campaign: Campaign):
        """Set default faction for selected campaign"""

        self.blueFactionSelect.clear()
        self.redFactionSelect.clear()

        self.factions.reset_campaign_defined()
        campaign.register_campaign_specific_factions(self.factions)

        for name in self.factions.iter_faction_names():
            self.blueFactionSelect.addItem(name)
            self.redFactionSelect.addItem(name)

        self.blueFactionSelect.setCurrentText(campaign.recommended_player_faction.name)
        self.redFactionSelect.setCurrentText(campaign.recommended_enemy_faction.name)

        self.updateUnitRecap()

    def updateUnitRecap(self):
        red_faction = self.factions.get_by_name(self.redFactionSelect.currentText())
        blue_faction = self.factions.get_by_name(self.blueFactionSelect.currentText())

        template = jinja_env.get_template("factiontemplate_EN.j2")

        blue_faction_txt = template.render({"faction": blue_faction})
        red_faction_txt = template.render({"faction": red_faction})

        self.blueFactionDescription.setText(blue_faction_txt)
        self.redFactionDescription.setText(red_faction_txt)

    @property
    def selected_blue_faction(self) -> Faction:
        return self.factions.get_by_name(self.blueFactionSelect.currentText())

    @property
    def selected_red_faction(self) -> Faction:
        return self.factions.get_by_name(self.redFactionSelect.currentText())


class TheaterConfiguration(QtWidgets.QWizardPage):
    campaign_selected = Signal(Campaign)

    def __init__(
        self,
        campaigns: List[Campaign],
        faction_selection: FactionSelection,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.faction_selection = faction_selection

        self.setTitle("Theater configuration")
        self.setSubTitle("\nChoose a terrain and time period for this game.")
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark3.png"),
        )

        # List of campaigns
        show_incompatible_campaigns_checkbox = QCheckBox(
            text="Show incompatible campaigns"
        )
        show_incompatible_campaigns_checkbox.setChecked(False)
        self.campaignList = QCampaignList(
            campaigns, show_incompatible_campaigns_checkbox.isChecked()
        )
        show_incompatible_campaigns_checkbox.toggled.connect(
            lambda checked: self.campaignList.setup_content(show_incompatible=checked)
        )
        self.registerField("selectedCampaign", self.campaignList)

        # Faction description
        self.campaignMapDescription = QTextEdit("")
        self.campaignMapDescription.setReadOnly(True)
        self.campaignMapDescription.setMaximumHeight(200)

        self.performanceText = QTextEdit("")
        self.performanceText.setReadOnly(True)
        self.performanceText.setMaximumHeight(90)

        # Campaign settings
        mapSettingsGroup = QtWidgets.QGroupBox("Map Settings")
        mapSettingsLayout = QtWidgets.QGridLayout()
        invertMap = QtWidgets.QCheckBox()
        self.registerField("invertMap", invertMap)
        mapSettingsLayout.addWidget(QtWidgets.QLabel("Invert Map"), 0, 0)
        mapSettingsLayout.addWidget(invertMap, 0, 1)
        self.advanced_iads = QtWidgets.QCheckBox()
        self.registerField("advanced_iads", self.advanced_iads)
        self.iads_label = QtWidgets.QLabel("Advanced IADS (WIP)")
        mapSettingsLayout.addWidget(self.iads_label, 1, 0)
        mapSettingsLayout.addWidget(self.advanced_iads, 1, 1)
        mapSettingsGroup.setLayout(mapSettingsLayout)

        # Time Period
        timeGroup = QtWidgets.QGroupBox("Time Period")
        timePeriod = QtWidgets.QLabel("Start date :")
        timePeriodSelect = QtWidgets.QComboBox()
        timePeriodPresetLabel = QLabel("Use preset :")
        timePeriodPreset = QtWidgets.QCheckBox()
        timePeriodPreset.setChecked(True)
        self.calendar = QLiberationCalendar()
        self.calendar.setSelectedDate(QDate())
        self.calendar.setDisabled(True)

        def onTimePeriodChanged():
            self.calendar.setSelectedDate(
                list(TIME_PERIODS.values())[timePeriodSelect.currentIndex()]
            )

        timePeriodSelect.currentTextChanged.connect(onTimePeriodChanged)

        for r in TIME_PERIODS:
            timePeriodSelect.addItem(r)
        timePeriod.setBuddy(timePeriodSelect)
        timePeriodSelect.setCurrentIndex(21)

        def onTimePeriodCheckboxChanged():
            if timePeriodPreset.isChecked():
                self.calendar.setDisabled(True)
                timePeriodSelect.setDisabled(False)
                onTimePeriodChanged()
            else:
                self.calendar.setDisabled(False)
                timePeriodSelect.setDisabled(True)

        timePeriodPreset.stateChanged.connect(onTimePeriodCheckboxChanged)

        # Bind selection method for campaign selection
        def on_campaign_selected():
            template = jinja_env.get_template("campaigntemplate_EN.j2")
            template_perf = jinja_env.get_template(
                "campaign_performance_template_EN.j2"
            )
            campaign = self.campaignList.selected_campaign
            self.setField("selectedCampaign", campaign)
            if campaign is None:
                self.campaignMapDescription.setText("No campaign selected")
                self.performanceText.setText("No campaign selected")
                return

            self.campaignMapDescription.setText(template.render({"campaign": campaign}))
            self.faction_selection.setDefaultFactions(campaign)
            self.performanceText.setText(
                template_perf.render({"performance": campaign.performance})
            )

            if (start_date := campaign.recommended_start_date) is not None:
                self.calendar.setSelectedDate(
                    QDate(start_date.year, start_date.month, start_date.day)
                )
                timePeriodPreset.setChecked(False)
            else:
                timePeriodPreset.setChecked(True)
            self.advanced_iads.setEnabled(campaign.advanced_iads)
            self.iads_label.setEnabled(campaign.advanced_iads)
            self.advanced_iads.setChecked(campaign.advanced_iads)
            if not campaign.advanced_iads:
                self.advanced_iads.setToolTip(
                    "Advanced IADS is not supported by this campaign"
                )
            else:
                self.advanced_iads.setToolTip("Enable Advanced IADS")

            self.campaign_selected.emit(campaign)

        self.campaignList.selectionModel().setCurrentIndex(
            self.campaignList.indexAt(QPoint(1, 1)), QItemSelectionModel.Rows
        )

        self.campaignList.selectionModel().selectionChanged.connect(
            on_campaign_selected
        )
        on_campaign_selected()

        docsText = QtWidgets.QLabel(
            "<p>Want more campaigns? You can "
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Campaign-maintenance"><span style="color:#FFFFFF;">offer to help</span></a>, '
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Community-campaigns"><span style="color:#FFFFFF;">play a community campaign</span></a>, '
            'or <a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Campaigns"><span style="color:#FFFFFF;">create your own</span></a>.'
            "</p>"
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        # Register fields
        self.registerField("timePeriod", timePeriodSelect)
        self.registerField("usePreset", timePeriodPreset)

        timeGroupLayout = QtWidgets.QGridLayout()
        timeGroupLayout.addWidget(timePeriodPresetLabel, 0, 0)
        timeGroupLayout.addWidget(timePeriodPreset, 0, 1)
        timeGroupLayout.addWidget(timePeriod, 1, 0)
        timeGroupLayout.addWidget(timePeriodSelect, 1, 1)
        timeGroupLayout.addWidget(self.calendar, 0, 2, 3, 1)
        timeGroup.setLayout(timeGroupLayout)

        layout = QtWidgets.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(self.campaignList, 0, 0, 5, 1)
        layout.addWidget(show_incompatible_campaigns_checkbox, 5, 0, 1, 1)
        layout.addWidget(docsText, 6, 0, 1, 1)
        layout.addWidget(self.campaignMapDescription, 0, 1, 1, 1)
        layout.addWidget(self.performanceText, 1, 1, 1, 1)
        layout.addWidget(mapSettingsGroup, 2, 1, 1, 1)
        layout.addWidget(timeGroup, 3, 1, 3, 1)
        self.setLayout(layout)


class BudgetInputs(QtWidgets.QGridLayout):
    def __init__(self, label: str, value: int) -> None:
        super().__init__()
        self.addWidget(QtWidgets.QLabel(label), 0, 0)

        minimum = 0
        maximum = 5000

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(value)
        self.starting_money = CurrencySpinner(minimum, maximum, value)
        slider.valueChanged.connect(lambda x: self.starting_money.setValue(x))
        self.starting_money.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider, 1, 0)
        self.addWidget(self.starting_money, 1, 1)


class NewSquadronRulesWarning(QLabel):
    def __init__(
        self, campaign: Campaign | None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.set_campaign(campaign)

    def set_campaign(self, campaign: Campaign | None) -> None:
        if campaign is None:
            self.setText("No campaign selected")
            return
        if campaign.version >= (10, 9):
            text = f"{campaign.name} is compatible with the new squadron rules."
        elif campaign.version >= (10, 7):
            text = (
                f"{campaign.name} has been updated since the new squadron rules were "
                "introduced, but support for those rules was still optional. You may "
                "need to remove, resize, or relocate squadrons before beginning the "
                "game."
            )
        else:
            text = (
                f"{campaign.name} has not been updated since the new squadron rules. "
                "Were introduced. You may need to remove, resize, or relocate "
                "squadrons before beginning the game."
            )
        self.setText(wrap_label_text(text))


class DifficultyAndAutomationOptions(QtWidgets.QWizardPage):
    def __init__(
        self, default_settings: Settings, current_campaign: Campaign | None, parent=None
    ) -> None:
        super().__init__(parent)

        self.setTitle("Difficulty and automation options")
        self.setSubTitle(
            "\nOptions controlling game difficulty and level of " "player involvement."
        )
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        layout = QtWidgets.QVBoxLayout()

        economy_group = QtWidgets.QGroupBox("Economy options")
        layout.addWidget(economy_group)
        economy_layout = QtWidgets.QVBoxLayout()
        economy_group.setLayout(economy_layout)

        economy_layout.addWidget(QLabel("Player income multiplier"))
        self.player_income = FloatSpinSlider(0, 5, 1, divisor=10)
        self.registerField("player_income_multiplier", self.player_income.spinner)
        economy_layout.addLayout(self.player_income)

        economy_layout.addWidget(QLabel("Enemy income multiplier"))
        self.enemy_income = FloatSpinSlider(0, 5, 1, divisor=10)
        self.registerField("enemy_income_multiplier", self.enemy_income.spinner)
        economy_layout.addLayout(self.enemy_income)

        self.player_budget = BudgetInputs("Player starting budget", DEFAULT_BUDGET)
        self.registerField("starting_money", self.player_budget.starting_money)
        economy_layout.addLayout(self.player_budget)

        self.enemy_budget = BudgetInputs("Enemy starting budget", DEFAULT_BUDGET)
        self.registerField("enemy_starting_money", self.enemy_budget.starting_money)
        economy_layout.addLayout(self.enemy_budget)

        new_squadron_rules = QtWidgets.QCheckBox("Enable new squadron rules")
        new_squadron_rules.setChecked(default_settings.enable_squadron_aircraft_limits)
        self.registerField("use_new_squadron_rules", new_squadron_rules)
        economy_layout.addWidget(new_squadron_rules)
        self.new_squadron_rules_warning = NewSquadronRulesWarning(current_campaign)
        economy_layout.addWidget(self.new_squadron_rules_warning)
        economy_layout.addWidget(
            QLabel(
                wrap_label_text(
                    "With new squadron rules enabled, squadrons will not be able to "
                    "exceed a maximum number of aircraft (configurable), and the "
                    "campaign will begin with all squadrons at full strength."
                )
            )
        )

        assist_group = QtWidgets.QGroupBox("Player assists")
        layout.addWidget(assist_group)
        assist_layout = QtWidgets.QGridLayout()
        assist_group.setLayout(assist_layout)

        assist_layout.addWidget(QtWidgets.QLabel("Automate runway repairs"), 0, 0)
        runway_repairs = QtWidgets.QCheckBox()
        runway_repairs.setChecked(default_settings.automate_runway_repair)
        self.registerField("automate_runway_repairs", runway_repairs)
        assist_layout.addWidget(runway_repairs, 0, 1, Qt.AlignRight)

        assist_layout.addWidget(QtWidgets.QLabel("Automate front-line purchases"), 1, 0)
        front_line = QtWidgets.QCheckBox()
        front_line.setChecked(default_settings.automate_front_line_reinforcements)
        self.registerField("automate_front_line_purchases", front_line)
        assist_layout.addWidget(front_line, 1, 1, Qt.AlignRight)

        assist_layout.addWidget(QtWidgets.QLabel("Automate aircraft purchases"), 2, 0)
        aircraft = QtWidgets.QCheckBox()
        aircraft.setChecked(default_settings.automate_aircraft_reinforcements)
        self.registerField("automate_aircraft_purchases", aircraft)
        assist_layout.addWidget(aircraft, 2, 1, Qt.AlignRight)

        self.setLayout(layout)

    def set_campaign_values(self, campaign: Campaign) -> None:
        self.player_budget.starting_money.setValue(campaign.recommended_player_money)
        self.enemy_budget.starting_money.setValue(campaign.recommended_enemy_money)
        self.player_income.spinner.setValue(
            int(campaign.recommended_player_income_multiplier * 10)
        )
        self.enemy_income.spinner.setValue(
            int(campaign.recommended_enemy_income_multiplier * 10)
        )
        self.new_squadron_rules_warning.set_campaign(campaign)


class PluginOptionCheckbox(QCheckBox):
    def __init__(self, option: LuaPluginOption) -> None:
        super().__init__(option.name)
        self.option = option
        self.setChecked(self.option.enabled)
        self.toggled.connect(self.on_toggle)

    def on_toggle(self, enabled: bool) -> None:
        self.option.enabled = enabled


class PluginGroupBox(QtWidgets.QGroupBox):
    def __init__(self, plugin: LuaPlugin) -> None:
        super().__init__(plugin.name)
        self.plugin = plugin

        self.setCheckable(True)
        self.setChecked(self.plugin.enabled)
        self.toggled.connect(self.on_toggle)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.checkboxes = []
        for option in self.plugin.options:
            checkbox = PluginOptionCheckbox(option)
            checkbox.setEnabled(self.plugin.enabled)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        if not self.plugin.options:
            layout.addWidget(QLabel("Plugin has no settings."))

    def on_toggle(self, enabled: bool) -> None:
        self.plugin.enabled = enabled
        for checkbox in self.checkboxes:
            checkbox.setEnabled(enabled)


class PluginsPage(QtWidgets.QWizardPage):
    def __init__(self, lua_plugins_manager: LuaPluginManager, parent=None) -> None:
        super().__init__(parent)
        self.lua_plugins_manager = lua_plugins_manager

        self.setTitle("Plugins")
        self.setSubTitle("Enable plugins with the checkbox next to their name")
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        scroll_content = QWidget()
        layout = QVBoxLayout()
        scroll_content.setLayout(layout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        self.group_boxes = []
        for plugin in self.lua_plugins_manager.iter_plugins():
            if plugin.show_in_ui:
                group_box = PluginGroupBox(plugin)
                layout.addWidget(group_box)
                self.group_boxes.append(group_box)


class GeneratorOptions(QtWidgets.QWizardPage):
    def __init__(
        self, default_settings: Settings, mod_settings: ModSettings, parent=None
    ) -> None:
        super().__init__(parent)
        self.setTitle("Generator settings")
        self.setSubTitle("\nOptions affecting the generation of the game.")
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        # Campaign settings
        generatorSettingsGroup = QtWidgets.QGroupBox("Generator Settings")
        no_carrier = QtWidgets.QCheckBox()
        self.registerField("no_carrier", no_carrier)
        no_lha = QtWidgets.QCheckBox()
        self.registerField("no_lha", no_lha)
        supercarrier = QtWidgets.QCheckBox()
        supercarrier.setChecked(default_settings.supercarrier)
        self.registerField("supercarrier", supercarrier)
        no_player_navy = QtWidgets.QCheckBox()
        self.registerField("no_player_navy", no_player_navy)
        no_enemy_navy = QtWidgets.QCheckBox()
        self.registerField("no_enemy_navy", no_enemy_navy)
        desired_player_mission_duration = TimeInputs(
            default_settings.desired_player_mission_duration, minimum=30, maximum=150
        )
        self.registerField(
            "desired_player_mission_duration", desired_player_mission_duration.spinner
        )

        generatorLayout = QtWidgets.QGridLayout()
        generatorLayout.addWidget(QtWidgets.QLabel("No Aircraft Carriers"), 1, 0)
        generatorLayout.addWidget(no_carrier, 1, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("No LHA"), 2, 0)
        generatorLayout.addWidget(no_lha, 2, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("Use Supercarrier module"), 3, 0)
        generatorLayout.addWidget(supercarrier, 3, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("No Player Navy"), 4, 0)
        generatorLayout.addWidget(no_player_navy, 4, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("No Enemy Navy"), 5, 0)
        generatorLayout.addWidget(no_enemy_navy, 5, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("Desired mission duration"), 6, 0)
        generatorLayout.addLayout(desired_player_mission_duration, 7, 0)
        generatorSettingsGroup.setLayout(generatorLayout)

        modSettingsGroup = QtWidgets.QGroupBox("Mod Settings")

        a4_skyhawk = QtWidgets.QCheckBox()
        a4_skyhawk.setChecked(mod_settings.a4_skyhawk)
        self.registerField("a4_skyhawk", a4_skyhawk)

        hercules = QtWidgets.QCheckBox()
        hercules.setChecked(mod_settings.hercules)
        self.registerField("hercules", hercules)

        uh_60l = QtWidgets.QCheckBox()
        uh_60l.setChecked(mod_settings.uh_60l)
        self.registerField("uh_60l", uh_60l)

        f22_raptor = QtWidgets.QCheckBox()
        f22_raptor.setChecked(mod_settings.f22_raptor)
        self.registerField("f22_raptor", f22_raptor)

        f104_starfighter = QtWidgets.QCheckBox()
        f104_starfighter.setChecked(mod_settings.f104_starfighter)
        self.registerField("f104_starfighter", f104_starfighter)

        f4_phantom = QtWidgets.QCheckBox()
        f4_phantom.setChecked(mod_settings.f4_phantom)
        self.registerField("f4_phantom", f4_phantom)

        jas39_gripen = QtWidgets.QCheckBox()
        jas39_gripen.setChecked(mod_settings.jas39_gripen)
        self.registerField("jas39_gripen", jas39_gripen)

        su57_felon = QtWidgets.QCheckBox()
        su57_felon.setChecked(mod_settings.su57_felon)
        self.registerField("su57_felon", su57_felon)

        ov10a_bronco = QtWidgets.QCheckBox()
        ov10a_bronco.setChecked(mod_settings.ov10a_bronco)
        self.registerField("ov10a_bronco", ov10a_bronco)

        frenchpack = QtWidgets.QCheckBox()
        frenchpack.setChecked(mod_settings.frenchpack)
        self.registerField("frenchpack", frenchpack)

        high_digit_sams = QtWidgets.QCheckBox()
        high_digit_sams.setChecked(mod_settings.high_digit_sams)
        self.registerField("high_digit_sams", high_digit_sams)

        modHelpText = QtWidgets.QLabel(
            "<p>Select the mods you have installed. If your chosen factions support them, you'll be able to use these mods in your campaign.</p>"
        )
        modHelpText.setAlignment(Qt.AlignCenter)

        modLayout = QtWidgets.QGridLayout()
        modLayout_row = 1
        modLayout.addWidget(
            QtWidgets.QLabel("A-4E Skyhawk (version 2.1.0)"), modLayout_row, 0
        )
        modLayout.addWidget(a4_skyhawk, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(QtWidgets.QLabel("F-22A Raptor"), modLayout_row, 0)
        modLayout.addWidget(f22_raptor, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(QtWidgets.QLabel("F-104 Starfighter"), modLayout_row, 0)
        modLayout.addWidget(f104_starfighter, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(QtWidgets.QLabel("F-4B&C Phantom"), modLayout_row, 0)
        modLayout.addWidget(f4_phantom, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(
            QtWidgets.QLabel("C-130J-30 Super Hercules"), modLayout_row, 0
        )
        modLayout.addWidget(hercules, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(
            QtWidgets.QLabel("UH-60L Black Hawk (version 1.3.1)"), modLayout_row, 0
        )
        modLayout.addWidget(uh_60l, modLayout_row, 1)
        modLayout_row += 1
        # Section break here for readability
        modLayout.addWidget(QtWidgets.QWidget(), modLayout_row, 0)
        modLayout_row += 1
        modLayout.addWidget(
            QtWidgets.QLabel("JAS 39 Gripen (version v1.8.0-beta)"), modLayout_row, 0
        )
        modLayout.addWidget(jas39_gripen, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(QtWidgets.QLabel("Su-57 Felon"), modLayout_row, 0)
        modLayout.addWidget(su57_felon, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(QtWidgets.QLabel("OV-10A Bronco"), modLayout_row, 0)
        modLayout.addWidget(ov10a_bronco, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(QtWidgets.QLabel("Frenchpack"), modLayout_row, 0)
        modLayout.addWidget(frenchpack, modLayout_row, 1)
        modLayout_row += 1
        modLayout.addWidget(QtWidgets.QLabel("High Digit SAMs"), modLayout_row, 0)
        modLayout.addWidget(high_digit_sams, modLayout_row, 1)
        modSettingsGroup.setLayout(modLayout)

        mlayout = QVBoxLayout()
        mlayout.addWidget(generatorSettingsGroup)
        mlayout.addWidget(modSettingsGroup)
        mlayout.addWidget(modHelpText)
        self.setLayout(mlayout)


class ConclusionPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("Conclusion")
        self.setSubTitle("\n\n")
        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark2.png"),
        )

        self.label = QtWidgets.QLabel(
            "Click 'Finish' to generate and start the new game."
        )
        self.label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
