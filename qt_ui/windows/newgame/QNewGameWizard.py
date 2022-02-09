from __future__ import unicode_literals

import logging
from datetime import timedelta
from typing import List

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QDate, QItemSelectionModel, QPoint, Qt
from PySide2.QtWidgets import QCheckBox, QLabel, QTextEdit, QVBoxLayout
from jinja2 import Environment, FileSystemLoader, select_autoescape

from game import db
from game.campaignloader.campaign import Campaign
from game.factions.faction import Faction
from game.settings import Settings
from game.theater.start_generator import GameGenerator, GeneratorSettings, ModSettings
from qt_ui.widgets.QLiberationCalendar import QLiberationCalendar
from qt_ui.widgets.spinsliders import CurrencySpinner, FloatSpinSlider, TimeInputs
from qt_ui.windows.AirWingConfigurationDialog import AirWingConfigurationDialog
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

DEFAULT_BUDGET = 2000
DEFAULT_MISSION_LENGTH: timedelta = timedelta(minutes=60)


class NewGameWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewGameWizard, self).__init__(parent)

        self.campaigns = list(sorted(Campaign.load_each(), key=lambda x: x.name))

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
            campaign = self.theater_page.campaignList.selected_campaign
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
            desired_player_mission_duration=timedelta(
                minutes=self.field("desired_player_mission_duration")
            ),
            automate_aircraft_reinforcements=self.field("automate_aircraft_purchases"),
            supercarrier=self.field("supercarrier"),
        )
        generator_settings = GeneratorSettings(
            start_date=start_date,
            player_budget=int(self.field("starting_money")),
            enemy_budget=int(self.field("enemy_starting_money")),
            # QSlider forces integers, so we use 1 to 50 and divide by 10 to
            # give 0.1 to 5.0.
            inverted=self.field("invertMap"),
            no_carrier=self.field("no_carrier"),
            no_lha=self.field("no_lha"),
            no_player_navy=self.field("no_player_navy"),
            no_enemy_navy=self.field("no_enemy_navy"),
        )
        mod_settings = ModSettings(
            a4_skyhawk=self.field("a4_skyhawk"),
            eurofighter=self.field("eurofighter"),
            f22_raptor=self.field("f22_raptor"),
            f104_starfighter=self.field("f104_starfighter"),
            hercules=self.field("hercules"),
            jas39_gripen=self.field("jas39_gripen"),
            rafale=self.field("rafale"),
            su57_felon=self.field("su57_felon"),
            frenchpack=self.field("frenchpack"),
            high_digit_sams=self.field("high_digit_sams"),
        )

        blue_faction = self.faction_selection_page.selected_blue_faction
        red_faction = self.faction_selection_page.selected_red_faction
        theater = campaign.load_theater()
        generator = GameGenerator(
            blue_faction,
            red_faction,
            theater,
            campaign.load_air_wing_config(theater),
            settings,
            generator_settings,
            mod_settings,
        )
        self.generatedGame = generator.generate()

        AirWingConfigurationDialog(self.generatedGame, self).exec_()

        self.generatedGame.begin_turn_0()

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

    @property
    def selected_blue_faction(self) -> Faction:
        return db.FACTIONS[self.blueFactionSelect.currentText()]

    @property
    def selected_red_faction(self) -> Faction:
        return db.FACTIONS[self.redFactionSelect.currentText()]


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

        economy_layout.addWidget(QLabel("Player income multiplier"))
        player_income = FloatSpinSlider(0, 5, 1, divisor=10)
        self.registerField("player_income_multiplier", player_income.spinner)
        economy_layout.addLayout(player_income)

        economy_layout.addWidget(QLabel("Enemy income multiplier"))
        enemy_income = FloatSpinSlider(0, 5, 1, divisor=10)
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
        desired_player_mission_duration = TimeInputs(
            DEFAULT_MISSION_LENGTH, minimum=30, maximum=150
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
        self.registerField("a4_skyhawk", a4_skyhawk)
        eurofighter = QtWidgets.QCheckBox()
        self.registerField("eurofighter", eurofighter)
        hercules = QtWidgets.QCheckBox()
        self.registerField("hercules", hercules)
        f22_raptor = QtWidgets.QCheckBox()
        self.registerField("f22_raptor", f22_raptor)
        f104_starfighter = QtWidgets.QCheckBox()
        self.registerField("f104_starfighter", f104_starfighter)
        jas39_gripen = QtWidgets.QCheckBox()
        self.registerField("jas39_gripen", jas39_gripen)
        rafale = QtWidgets.QCheckBox()
        self.registerField("rafale", rafale)
        su57_felon = QtWidgets.QCheckBox()
        self.registerField("su57_felon", su57_felon)
        frenchpack = QtWidgets.QCheckBox()
        self.registerField("frenchpack", frenchpack)
        high_digit_sams = QtWidgets.QCheckBox()
        self.registerField("high_digit_sams", high_digit_sams)

        modHelpText = QtWidgets.QLabel(
            "<p>Select the mods you have installed. If your chosen factions support them, you'll be able to use these mods in your campaign.</p>"
        )
        modHelpText.setAlignment(Qt.AlignCenter)

        modLayout = QtWidgets.QGridLayout()
        modLayout.addWidget(QtWidgets.QLabel("A-4E Skyhawk"), 1, 0)
        modLayout.addWidget(a4_skyhawk, 1, 1)
        modLayout.addWidget(QtWidgets.QLabel("F-22A Raptor"), 2, 0)
        modLayout.addWidget(f22_raptor, 2, 1)
        modLayout.addWidget(QtWidgets.QLabel("F-104 Starfighter"), 3, 0)
        modLayout.addWidget(f104_starfighter, 3, 1)
        modLayout.addWidget(QtWidgets.QLabel("C-130J-30 Super Hercules"), 4, 0)
        modLayout.addWidget(hercules, 4, 1)
        modLayout.addWidget(QtWidgets.QLabel("JAS 39 Gripen"), 5, 0)
        modLayout.addWidget(jas39_gripen, 5, 1)
        modLayout.addWidget(QtWidgets.QLabel("Su-57 Felon"), 6, 0)
        modLayout.addWidget(su57_felon, 6, 1)
        modLayout.addWidget(QtWidgets.QLabel("Frenchpack"), 7, 0)
        modLayout.addWidget(frenchpack, 7, 1)
        modLayout.addWidget(QtWidgets.QLabel("High Digit SAMs"), 8, 0)
        modLayout.addWidget(high_digit_sams, 8, 1)
        modLayout.addWidget(QtWidgets.QLabel("Eurofighter Typhoon"), 9, 0)
        modLayout.addWidget(eurofighter, 9, 1)
        modLayout.addWidget(QtWidgets.QLabel("Rafale"), 10, 0)
        modLayout.addWidget(rafale, 10, 1)
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
