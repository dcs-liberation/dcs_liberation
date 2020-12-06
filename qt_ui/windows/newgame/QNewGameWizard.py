from __future__ import unicode_literals

import logging
from typing import List, Optional

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QItemSelectionModel, QPoint, Qt
from PySide2.QtWidgets import QVBoxLayout, QTextEdit
from jinja2 import Environment, FileSystemLoader, select_autoescape

from game import db
from game.settings import Settings
from qt_ui.widgets.spinsliders import TenthsSpinSlider
from qt_ui.windows.newgame.QCampaignList import (
    Campaign,
    QCampaignList,
    load_campaigns,
)
from game.theater.start_generator import GameGenerator, GeneratorSettings

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

class NewGameWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewGameWizard, self).__init__(parent)

        self.campaigns = load_campaigns()

        self.addPage(IntroPage())
        self.addPage(FactionSelection())
        self.addPage(TheaterConfiguration(self.campaigns))
        self.addPage(MiscOptions())
        self.addPage(ConclusionPage())

        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/watermark1.png'))
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)

        self.setWindowTitle("New Game")
        self.generatedGame = None

    def accept(self):
        logging.info("New Game Wizard accept")
        logging.info("======================")

        campaign = self.field("selectedCampaign")
        if campaign is None:
            campaign = self.campaigns[0]

        settings = Settings(
            player_income_multiplier=self.field(
                "player_income_multiplier") / 10,
            enemy_income_multiplier=self.field("enemy_income_multiplier") / 10,
            supercarrier=self.field("supercarrier")
        )
        generator_settings = GeneratorSettings(
            start_date=db.TIME_PERIODS[
                list(db.TIME_PERIODS.keys())[self.field("timePeriod")]],
            starting_budget=int(self.field("starting_money")),
            # QSlider forces integers, so we use 1 to 50 and divide by 10 to
            # give 0.1 to 5.0.
            multiplier=self.field("multiplier") / 10,
            midgame=self.field("midGame"),
            inverted=self.field("invertMap"),
            no_carrier=self.field("no_carrier"),
            no_lha=self.field("no_lha"),
            no_player_navy=self.field("no_player_navy"),
            no_enemy_navy=self.field("no_enemy_navy")
        )

        blue_faction = [c for c in db.FACTIONS][self.field("blueFaction")]
        red_faction = [c for c in db.FACTIONS][self.field("redFaction")]
        generator = GameGenerator(
            blue_faction,
            red_faction,
            campaign.load_theater(),
            settings,
            generator_settings
        )
        self.generatedGame = generator.generate()

        super(NewGameWizard, self).accept()


class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")
        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/watermark1.png'))

        label = QtWidgets.QLabel("This wizard will help you setup a new game.\n\n"
                                 "Please make sure you saved and backed up your previous game before going through.")
        label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class FactionSelection(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(FactionSelection, self).__init__(parent)

        self.setTitle("Faction selection")
        self.setSubTitle("\nChoose the two opposing factions and select the player side.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                       QtGui.QPixmap('./resources/ui/misc/generator.png'))

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
        self.requiredModsGroupLayout.addWidget(self.requiredMods)
        self.requiredModsGroup.setLayout(self.requiredModsGroupLayout)

        # Link form fields
        self.registerField('blueFaction', self.blueFactionSelect)
        self.registerField('redFaction', self.redFactionSelect)

        # Build layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.factionsGroup)
        layout.addWidget(self.requiredModsGroup)
        self.setLayout(layout)
        self.updateUnitRecap()

        self.blueFactionSelect.activated.connect(self.updateUnitRecap)
        self.redFactionSelect.activated.connect(self.updateUnitRecap)

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
                    self.requiredMods.text() + "\n<li>" + mod + ": <a href=\"" + red_faction.requirements[mod] + "\">" +
                    red_faction.requirements[mod] + "</a></li>")

        if len(blue_faction.requirements.keys()) > 0:
            has_mod = True
            for mod in blue_faction.requirements.keys():
                if mod not in red_faction.requirements.keys():
                    self.requiredMods.setText(
                        self.requiredMods.text() + "\n<li>" + mod + ": <a href=\"" + blue_faction.requirements[
                            mod] + "\">" + blue_faction.requirements[mod] + "</a></li>")

        if has_mod:
            self.requiredMods.setText(self.requiredMods.text() + "</ul>\n\n")
        else:
            self.requiredMods.setText(self.requiredMods.text() + "<li>None</li></ul>\n")


class TheaterConfiguration(QtWidgets.QWizardPage):
    def __init__(self, campaigns: List[Campaign], parent=None) -> None:
        super().__init__(parent)

        self.setTitle("Theater configuration")
        self.setSubTitle("\nChoose a terrain and time period for this game.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/logo1.png'))

        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/watermark3.png'))

        # List of campaigns
        campaignList = QCampaignList(campaigns)
        self.registerField("selectedCampaign", campaignList)

        # Faction description
        self.campaignMapDescription = QTextEdit("")
        self.campaignMapDescription.setReadOnly(True)

        def on_campaign_selected():
            template = jinja_env.get_template("campaigntemplate_EN.j2")
            index = campaignList.selectionModel().currentIndex().row()
            campaign = campaignList.campaigns[index]
            self.setField("selectedCampaign", campaign)
            self.campaignMapDescription.setText(template.render({"campaign": campaign}))

        campaignList.selectionModel().setCurrentIndex(campaignList.indexAt(QPoint(1, 1)), QItemSelectionModel.Rows)
        campaignList.selectionModel().selectionChanged.connect(on_campaign_selected)
        on_campaign_selected()

        # Campaign settings
        mapSettingsGroup = QtWidgets.QGroupBox("Map Settings")
        invertMap = QtWidgets.QCheckBox()
        self.registerField('invertMap', invertMap)
        mapSettingsLayout = QtWidgets.QGridLayout()
        mapSettingsLayout.addWidget(QtWidgets.QLabel("Invert Map"), 0, 0)
        mapSettingsLayout.addWidget(invertMap, 0, 1)

        mapSettingsLayout.addWidget(QtWidgets.QLabel("Start at mid game"), 1, 0)
        midgame = QtWidgets.QCheckBox()
        self.registerField('midGame', midgame)
        mapSettingsLayout.addWidget(midgame, 1, 1)
        mapSettingsGroup.setLayout(mapSettingsLayout)

        # Time Period
        timeGroup = QtWidgets.QGroupBox("Time Period")
        timePeriod = QtWidgets.QLabel("Start date :")
        timePeriodSelect = QtWidgets.QComboBox()
        for r in db.TIME_PERIODS:
            timePeriodSelect.addItem(r)
        timePeriod.setBuddy(timePeriodSelect)
        timePeriodSelect.setCurrentIndex(21)

        # Register fields
        self.registerField('timePeriod', timePeriodSelect)
        self.registerField('timePeriod', timePeriodSelect)

        timeGroupLayout = QtWidgets.QGridLayout()
        timeGroupLayout.addWidget(timePeriod, 0, 0)
        timeGroupLayout.addWidget(timePeriodSelect, 0, 1)
        timeGroup.setLayout(timeGroupLayout)

        layout = QtWidgets.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(campaignList, 0, 0, 3, 1)
        layout.addWidget(self.campaignMapDescription, 0, 1, 1, 1)
        layout.addWidget(mapSettingsGroup, 1, 1, 1, 1)
        layout.addWidget(timeGroup, 2, 1, 1, 1)
        self.setLayout(layout)


class CurrencySpinner(QtWidgets.QSpinBox):
    def __init__(self, minimum: Optional[int] = None,
                 maximum: Optional[int] = None,
                 initial: Optional[int] = None) -> None:
        super().__init__()

        if minimum is not None:
            self.setMinimum(minimum)
        if maximum is not None:
            self.setMaximum(maximum)
        if initial is not None:
            self.setValue(initial)

    def textFromValue(self, val: int) -> str:
        return f"${val}"


class BudgetInputs(QtWidgets.QGridLayout):
    def __init__(self) -> None:
        super().__init__()
        self.addWidget(QtWidgets.QLabel("Starting money"), 0, 0)

        minimum = 0
        maximum = 5000
        initial = 650

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(initial)
        self.starting_money = CurrencySpinner(minimum, maximum, initial)
        slider.valueChanged.connect(lambda x: self.starting_money.setValue(x))
        self.starting_money.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider, 1, 0)
        self.addWidget(self.starting_money, 1, 1)


class MiscOptions(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(MiscOptions, self).__init__(parent)

        self.setTitle("Miscellaneous settings")
        self.setSubTitle("\nOthers settings for the game.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/logo1.png'))

        multiplier = TenthsSpinSlider("Enemy forces multiplier", 1, 50, 10)
        self.registerField('multiplier', multiplier.spinner)

        player_income = TenthsSpinSlider("Player income multiplier", 1, 50, 10)
        self.registerField("player_income_multiplier", player_income.spinner)

        enemy_income = TenthsSpinSlider("Enemy income multiplier", 1, 50, 10)
        self.registerField("enemy_income_multiplier", enemy_income.spinner)

        miscSettingsGroup = QtWidgets.QGroupBox("Misc Settings")

        # Campaign settings
        generatorSettingsGroup = QtWidgets.QGroupBox("Generator Settings")
        no_carrier = QtWidgets.QCheckBox()
        self.registerField('no_carrier', no_carrier)
        no_lha = QtWidgets.QCheckBox()
        self.registerField('no_lha', no_lha)
        supercarrier = QtWidgets.QCheckBox()
        self.registerField('supercarrier', supercarrier)
        no_player_navy = QtWidgets.QCheckBox()
        self.registerField('no_player_navy', no_player_navy)
        no_enemy_navy = QtWidgets.QCheckBox()
        self.registerField('no_enemy_navy', no_enemy_navy)

        layout = QtWidgets.QGridLayout()
        layout.addLayout(multiplier, 0, 0)
        layout.addLayout(player_income, 1, 0)
        layout.addLayout(enemy_income, 2, 0)
        miscSettingsGroup.setLayout(layout)

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
        generatorSettingsGroup.setLayout(generatorLayout)

        budget_inputs = BudgetInputs()
        economySettingsGroup = QtWidgets.QGroupBox("Economy")
        economySettingsGroup.setLayout(budget_inputs)
        self.registerField('starting_money', budget_inputs.starting_money)

        mlayout = QVBoxLayout()
        mlayout.addWidget(miscSettingsGroup)
        mlayout.addWidget(generatorSettingsGroup)
        mlayout.addWidget(economySettingsGroup)
        self.setLayout(mlayout)


class ConclusionPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("Conclusion")
        self.setSubTitle("\n\n")
        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/watermark2.png'))

        self.label = QtWidgets.QLabel("Click 'Finish' to generate and start the new game.")
        self.label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
