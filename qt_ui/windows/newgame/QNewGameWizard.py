from __future__ import unicode_literals

import logging
from typing import List, Optional

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QItemSelectionModel, QPoint, Qt, QDate
from PySide2.QtWidgets import QVBoxLayout, QTextEdit, QLabel
from jinja2 import Environment, FileSystemLoader, select_autoescape

from game import db
from game.settings import Settings
from game.theater.start_generator import GameGenerator, GeneratorSettings
from qt_ui.widgets.QLiberationCalendar import QLiberationCalendar
from qt_ui.widgets.spinsliders import TenthsSpinSlider
from qt_ui.windows.newgame.QCampaignList import (
    Campaign,
    QCampaignList,
    load_campaigns,
)
from qt_ui.windows.settings.QSettingsWindow import (
    NEW_GROUND_UNIT_RECRUITMENT_BEHAVIOR_LABEL,
)

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


DEFAULT_BUDGET = 2000
DEFUALT_MISSION_TIME = 90


class NewGameWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewGameWizard, self).__init__(parent)

        self.campaigns = load_campaigns()

        self.faction_selection_page = FactionSelection()
        self.addPage(IntroPage())
        self.theater_page = TheaterConfiguration(
            self.campaigns, self.faction_selection_page
        )
        self.addPage(self.theater_page)
        self.addPage(self.faction_selection_page)
        self.addPage(GeneratorOptions())
        self.addPage(DifficultyAndAutomationOptions())
        self.addPage(ConclusionPage())

        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark1.png"),
        )
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)

        self.setWindowTitle("New Game")
        self.generatedGame = None

    def accept(self):
        logging.info("New Game Wizard accept")
        logging.info("======================")

        campaign = self.field("selectedCampaign")
        if campaign is None:
            campaign = self.campaigns[0]

        if self.field("usePreset"):
            start_date = db.TIME_PERIODS[
                list(db.TIME_PERIODS.keys())[self.field("timePeriod")]
            ]
        else:
            start_date = self.theater_page.calendar.selectedDate().toPython()

        settings = Settings(
            player_income_multiplier=self.field("player_income_multiplier") / 10,
            enemy_income_multiplier=self.field("enemy_income_multiplier") / 10,
            automate_runway_repair=self.field("automate_runway_repairs"),
            automate_front_line_reinforcements=self.field(
                "automate_front_line_purchases"
            ),
            mission_length=self.field("mission_length"),
            automate_aircraft_reinforcements=self.field("automate_aircraft_purchases"),
            supercarrier=self.field("supercarrier"),
            enable_new_ground_unit_recruitment=self.field(
                "new_ground_unit_recruitment"
            ),
        )
        generator_settings = GeneratorSettings(
            start_date=start_date,
            player_budget=int(self.field("starting_money")),
            enemy_budget=int(self.field("enemy_starting_money")),
            # QSlider forces integers, so we use 1 to 50 and divide by 10 to
            # give 0.1 to 5.0.
            midgame=False,
            inverted=self.field("invertMap"),
            no_carrier=self.field("no_carrier"),
            no_lha=self.field("no_lha"),
            no_player_navy=self.field("no_player_navy"),
            no_enemy_navy=self.field("no_enemy_navy"),
        )

        blue_faction = [c for c in db.FACTIONS][self.field("blueFaction")]
        red_faction = [c for c in db.FACTIONS][self.field("redFaction")]
        generator = GameGenerator(
            blue_faction,
            red_faction,
            campaign.load_theater(),
            settings,
            generator_settings,
        )
        self.generatedGame = generator.generate()

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
    def __init__(self, parent=None):
        super(FactionSelection, self).__init__(parent)

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
        for f in db.FACTIONS:
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
        for i, r in enumerate(db.FACTIONS):
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

        # Create required mod layout
        self.requiredModsGroup = QtWidgets.QGroupBox("Required Mods")
        self.requiredModsGroupLayout = QtWidgets.QHBoxLayout()
        self.requiredMods = QtWidgets.QLabel("<ul><li>None</li></ul>")
        self.requiredMods.setOpenExternalLinks(True)
        self.requiredModsGroupLayout.addWidget(self.requiredMods)
        self.requiredModsGroup.setLayout(self.requiredModsGroupLayout)

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
        layout.addWidget(self.requiredModsGroup)
        layout.addWidget(docsText)
        self.setLayout(layout)
        self.updateUnitRecap()

        self.blueFactionSelect.activated.connect(self.updateUnitRecap)
        self.redFactionSelect.activated.connect(self.updateUnitRecap)

    def setDefaultFactions(self, campaign: Campaign):
        """Set default faction for selected campaign"""

        self.blueFactionSelect.clear()
        self.redFactionSelect.clear()

        for f in db.FACTIONS:
            self.blueFactionSelect.addItem(f)

        for i, r in enumerate(db.FACTIONS):
            self.redFactionSelect.addItem(r)
            if r == campaign.recommended_enemy_faction:
                self.redFactionSelect.setCurrentIndex(i)
            if r == campaign.recommended_player_faction:
                self.blueFactionSelect.setCurrentIndex(i)

        self.updateUnitRecap()

    def updateUnitRecap(self):

        red_faction = db.FACTIONS[self.redFactionSelect.currentText()]
        blue_faction = db.FACTIONS[self.blueFactionSelect.currentText()]

        template = jinja_env.get_template("factiontemplate_EN.j2")

        blue_faction_txt = template.render({"faction": blue_faction})
        red_faction_txt = template.render({"faction": red_faction})

        self.blueFactionDescription.setText(blue_faction_txt)
        self.redFactionDescription.setText(red_faction_txt)

        # Compute mod requirements txt
        self.requiredMods.setText("<ul>")
        has_mod = False
        if len(red_faction.requirements.keys()) > 0:
            has_mod = True
            for mod in red_faction.requirements.keys():
                self.requiredMods.setText(
                    self.requiredMods.text()
                    + "\n<li>"
                    + mod
                    + ': <a href="'
                    + red_faction.requirements[mod]
                    + '">'
                    + red_faction.requirements[mod]
                    + "</a></li>"
                )

        if len(blue_faction.requirements.keys()) > 0:
            has_mod = True
            for mod in blue_faction.requirements.keys():
                if mod not in red_faction.requirements.keys():
                    self.requiredMods.setText(
                        self.requiredMods.text()
                        + "\n<li>"
                        + mod
                        + ': <a href="'
                        + blue_faction.requirements[mod]
                        + '">'
                        + blue_faction.requirements[mod]
                        + "</a></li>"
                    )

        if has_mod:
            self.requiredMods.setText(self.requiredMods.text() + "</ul>\n\n")
        else:
            self.requiredMods.setText(self.requiredMods.text() + "<li>None</li></ul>\n")


class TheaterConfiguration(QtWidgets.QWizardPage):
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
        campaignList = QCampaignList(campaigns)
        self.registerField("selectedCampaign", campaignList)

        # Faction description
        self.campaignMapDescription = QTextEdit("")
        self.campaignMapDescription.setReadOnly(True)
        self.campaignMapDescription.setMaximumHeight(200)

        self.performanceText = QTextEdit("")
        self.performanceText.setReadOnly(True)
        self.performanceText.setMaximumHeight(90)

        # Campaign settings
        mapSettingsGroup = QtWidgets.QGroupBox("Map Settings")
        invertMap = QtWidgets.QCheckBox()
        self.registerField("invertMap", invertMap)
        mapSettingsLayout = QtWidgets.QGridLayout()
        mapSettingsLayout.addWidget(QtWidgets.QLabel("Invert Map"), 0, 0)
        mapSettingsLayout.addWidget(invertMap, 0, 1)
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
                list(db.TIME_PERIODS.values())[timePeriodSelect.currentIndex()]
            )

        timePeriodSelect.currentTextChanged.connect(onTimePeriodChanged)

        for r in db.TIME_PERIODS:
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
            index = campaignList.selectionModel().currentIndex().row()
            campaign = campaignList.campaigns[index]
            self.setField("selectedCampaign", campaign)
            self.campaignMapDescription.setText(template.render({"campaign": campaign}))
            self.faction_selection.setDefaultFactions(campaign)
            self.performanceText.setText(
                template_perf.render({"performance": campaign.performance})
            )

        campaignList.selectionModel().setCurrentIndex(
            campaignList.indexAt(QPoint(1, 1)), QItemSelectionModel.Rows
        )

        campaignList.selectionModel().selectionChanged.connect(on_campaign_selected)
        on_campaign_selected()

        # Docs Link
        docsText = QtWidgets.QLabel(
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Campaigns"><span style="color:#FFFFFF;">How to create your own theater</span></a>'
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
        layout.addWidget(campaignList, 0, 0, 5, 1)
        layout.addWidget(docsText, 5, 0, 1, 1)
        layout.addWidget(self.campaignMapDescription, 0, 1, 1, 1)
        layout.addWidget(self.performanceText, 1, 1, 1, 1)
        layout.addWidget(mapSettingsGroup, 2, 1, 1, 1)
        layout.addWidget(timeGroup, 3, 1, 3, 1)
        self.setLayout(layout)


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


class BudgetInputs(QtWidgets.QGridLayout):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.addWidget(QtWidgets.QLabel(label), 0, 0)

        minimum = 0
        maximum = 5000
        initial = DEFAULT_BUDGET

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(initial)
        self.starting_money = CurrencySpinner(minimum, maximum, initial)
        slider.valueChanged.connect(lambda x: self.starting_money.setValue(x))
        self.starting_money.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider, 1, 0)
        self.addWidget(self.starting_money, 1, 1)


class TimeInputs(QtWidgets.QGridLayout):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.addWidget(QtWidgets.QLabel(label), 0, 0)

        minimum = 30
        maximum = 150
        initial = DEFUALT_MISSION_TIME

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(initial)
        self.mission_length = TimeSpinner(minimum, maximum, initial)
        slider.valueChanged.connect(lambda x: self.mission_length.setValue(x))
        self.mission_length.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider, 1, 0)
        self.addWidget(self.mission_length, 1, 1)


class DifficultyAndAutomationOptions(QtWidgets.QWizardPage):
    def __init__(self, parent=None) -> None:
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

        player_income = TenthsSpinSlider("Player income multiplier", 0, 50, 10)
        self.registerField("player_income_multiplier", player_income.spinner)
        economy_layout.addLayout(player_income)

        enemy_income = TenthsSpinSlider("Enemy income multiplier", 0, 50, 10)
        self.registerField("enemy_income_multiplier", enemy_income.spinner)
        economy_layout.addLayout(enemy_income)

        player_budget = BudgetInputs("Player starting budget")
        self.registerField("starting_money", player_budget.starting_money)
        economy_layout.addLayout(player_budget)

        enemy_budget = BudgetInputs("Enemy starting budget")
        self.registerField("enemy_starting_money", enemy_budget.starting_money)
        economy_layout.addLayout(enemy_budget)

        assist_group = QtWidgets.QGroupBox("Player assists")
        layout.addWidget(assist_group)
        assist_layout = QtWidgets.QGridLayout()
        assist_group.setLayout(assist_layout)

        assist_layout.addWidget(QtWidgets.QLabel("Automate runway repairs"), 0, 0)
        runway_repairs = QtWidgets.QCheckBox()
        self.registerField("automate_runway_repairs", runway_repairs)
        assist_layout.addWidget(runway_repairs, 0, 1, Qt.AlignRight)

        assist_layout.addWidget(QtWidgets.QLabel("Automate front-line purchases"), 1, 0)
        front_line = QtWidgets.QCheckBox()
        self.registerField("automate_front_line_purchases", front_line)
        assist_layout.addWidget(front_line, 1, 1, Qt.AlignRight)

        assist_layout.addWidget(QtWidgets.QLabel("Automate aircraft purchases"), 2, 0)
        aircraft = QtWidgets.QCheckBox()
        self.registerField("automate_aircraft_purchases", aircraft)
        assist_layout.addWidget(aircraft, 2, 1, Qt.AlignRight)

        flags_group = QtWidgets.QGroupBox("Feature flags")
        layout.addWidget(flags_group)
        flags_layout = QtWidgets.QGridLayout()
        flags_group.setLayout(flags_layout)

        new_ground_unit_recruitment_label = QtWidgets.QLabel(
            NEW_GROUND_UNIT_RECRUITMENT_BEHAVIOR_LABEL
        )
        new_ground_unit_recruitment_label.setOpenExternalLinks(True)
        flags_layout.addWidget(new_ground_unit_recruitment_label, 0, 0)
        new_ground_unit_recruitment = QtWidgets.QCheckBox()
        new_ground_unit_recruitment.setChecked(True)
        self.registerField("new_ground_unit_recruitment", new_ground_unit_recruitment)
        flags_layout.addWidget(new_ground_unit_recruitment, 0, 1, Qt.AlignRight)

        self.setLayout(layout)


class GeneratorOptions(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
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
        self.registerField("supercarrier", supercarrier)
        no_player_navy = QtWidgets.QCheckBox()
        self.registerField("no_player_navy", no_player_navy)
        no_enemy_navy = QtWidgets.QCheckBox()
        self.registerField("no_enemy_navy", no_enemy_navy)
        mission_length = TimeInputs("Expected mission length")
        self.registerField("mission_length", mission_length.mission_length)
        

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
        generatorLayout.addLayout(mission_length,6,0)
        generatorSettingsGroup.setLayout(generatorLayout)

        mlayout = QVBoxLayout()
        mlayout.addWidget(generatorSettingsGroup)
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
