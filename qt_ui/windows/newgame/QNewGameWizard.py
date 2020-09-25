from __future__ import unicode_literals

import datetime
import logging

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QPoint, QItemSelectionModel
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
from dcs.task import CAP, CAS

import qt_ui.uiconstants as CONST
from game import db, Game
from game.settings import Settings
from gen import namegen
from qt_ui.windows.newgame.QCampaignList import QCampaignList, CAMPAIGNS
from theater import start_generator, persiangulf, nevada, caucasus, ConflictTheater, normandy, thechannel


class NewGameWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewGameWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(FactionSelection())
        self.addPage(TheaterConfiguration())
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

        blueFaction = [c for c in db.FACTIONS][self.field("blueFaction")]
        redFaction = [c for c in db.FACTIONS][self.field("redFaction")]

        selectedCampaign = self.field("selectedCampaign")
        if selectedCampaign is None:
            selectedCampaign = CAMPAIGNS[0]
        conflictTheater = selectedCampaign[1]()

        timePeriod = db.TIME_PERIODS[list(db.TIME_PERIODS.keys())[self.field("timePeriod")]]
        midGame = self.field("midGame")
        multiplier = self.field("multiplier")
        no_carrier = self.field("no_carrier")
        no_lha = self.field("no_lha")
        supercarrier = self.field("supercarrier")
        no_player_navy = self.field("no_player_navy")
        no_enemy_navy = self.field("no_enemy_navy")
        invertMap = self.field("invertMap")

        player_name = blueFaction
        enemy_name = redFaction

        settings = Settings()
        settings.inverted = invertMap
        settings.supercarrier = supercarrier
        settings.do_not_generate_carrier = no_carrier
        settings.do_not_generate_lha = no_lha
        settings.do_not_generate_player_navy = no_player_navy
        settings.do_not_generate_enemy_navy = no_enemy_navy

        self.generatedGame = self.start_new_game(player_name, enemy_name, conflictTheater, midGame, multiplier,
                                                 timePeriod, settings)

        super(NewGameWizard, self).accept()

    def start_new_game(self, player_name: str, enemy_name: str, conflictTheater: ConflictTheater,
                       midgame: bool, multiplier: float, period: datetime, settings:Settings):

        # Reset name generator
        namegen.reset()
        start_generator.prepare_theater(conflictTheater, settings, midgame)

        print("-- Starting New Game Generator")
        print("Enemy name : " + enemy_name)
        print("Player name : " + player_name)
        print("Midgame : " + str(midgame))
        start_generator.generate_inital_units(conflictTheater, enemy_name, True, multiplier)

        print("-- Initial units generated")
        game = Game(player_name=player_name,
                    enemy_name=enemy_name,
                    theater=conflictTheater,
                    start_date=period,
                    settings=settings)

        print("-- Game Object generated")
        start_generator.generate_groundobjects(conflictTheater, game)
        game.budget = int(game.budget * multiplier)
        game.settings.multiplier = multiplier
        game.settings.sams = True
        game.settings.version = CONST.VERSION_STRING

        if midgame:
            game.budget = game.budget * 4 * len(list(conflictTheater.conflicts()))

        return game


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
        self.factionsGroupLayout = QtWidgets.QGridLayout()

        blueFaction = QtWidgets.QLabel("<b>Player Faction :</b>")
        self.blueFactionSelect = QtWidgets.QComboBox()
        for f in db.FACTIONS:
            self.blueFactionSelect.addItem(f)
        blueFaction.setBuddy(self.blueFactionSelect)

        redFaction = QtWidgets.QLabel("<b>Enemy Faction :</b>")
        self.redFactionSelect = QtWidgets.QComboBox()
        for i, r in enumerate(db.FACTIONS):
            self.redFactionSelect.addItem(r)
            if r == "Russia 1990": # Default ennemy
                self.redFactionSelect.setCurrentIndex(i)
        redFaction.setBuddy(self.redFactionSelect)

        self.blueSideRecap = QtWidgets.QLabel("")
        self.blueSideRecap.setFont(CONST.FONT_PRIMARY_I)
        self.blueSideRecap.setWordWrap(True)

        self.redSideRecap = QtWidgets.QLabel("")
        self.redSideRecap.setFont(CONST.FONT_PRIMARY_I)
        self.redSideRecap.setWordWrap(True)

        self.factionsGroupLayout.addWidget(blueFaction, 0, 0)
        self.factionsGroupLayout.addWidget(self.blueFactionSelect, 0, 1)
        self.factionsGroupLayout.addWidget(self.blueSideRecap, 1, 0, 1, 2)
        self.factionsGroupLayout.addWidget(redFaction, 2, 0)
        self.factionsGroupLayout.addWidget(self.redFactionSelect, 2, 1)
        self.factionsGroupLayout.addWidget(self.redSideRecap, 3, 0, 1, 2)
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

        self.requiredMods.setText("<ul>")

        red_faction = db.FACTIONS[self.redFactionSelect.currentText()]
        blue_faction = db.FACTIONS[self.blueFactionSelect.currentText()]

        red_units = red_faction["units"]
        blue_units = blue_faction["units"]

        blue_txt = ""
        for u in blue_units:
            if u in db.UNIT_BY_TASK[CAP] or u in db.UNIT_BY_TASK[CAS]:
                blue_txt = blue_txt + u.id + ", "
        blue_txt = blue_txt + "\n"
        self.blueSideRecap.setText(blue_txt)

        red_txt = ""
        for u in red_units:
            if u in db.UNIT_BY_TASK[CAP] or u in db.UNIT_BY_TASK[CAS]:
                red_txt = red_txt + u.id + ", "
        red_txt = red_txt + "\n"
        self.redSideRecap.setText(red_txt)

        has_mod = False
        if "requirements" in red_faction.keys():
            has_mod = True
            for mod in red_faction["requirements"].keys():
                self.requiredMods.setText(self.requiredMods.text() + "\n<li>" + mod + ": <a href=\""+red_faction["requirements"][mod]+"\">" + red_faction["requirements"][mod] + "</a></li>")

        if "requirements" in blue_faction.keys():
            has_mod = True
            for mod in blue_faction["requirements"].keys():
                if not "requirements" in red_faction.keys() or mod not in red_faction["requirements"].keys():
                    self.requiredMods.setText(self.requiredMods.text() + "\n<li>" + mod + ": <a href=\""+blue_faction["requirements"][mod]+"\">" + blue_faction["requirements"][mod] + "</a></li>")

        if has_mod:
            self.requiredMods.setText(self.requiredMods.text() + "</ul>\n\n")
        else:
            self.requiredMods.setText(self.requiredMods.text() + "<li>None</li></ul>\n")


class TheaterConfiguration(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(TheaterConfiguration, self).__init__(parent)

        self.setTitle("Theater configuration")
        self.setSubTitle("\nChoose a terrain and time period for this game.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/logo1.png'))

        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/watermark3.png'))

        # Terrain selection
        terrainGroup = QtWidgets.QGroupBox("Terrain")
        terrainCaucasusSmall = QtWidgets.QRadioButton("Caucasus - Western Georgia")
        terrainCaucasusSmall.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))
        terrainRussia = QtWidgets.QRadioButton("Caucasus - Russia Small")
        terrainRussia.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))
        terrainCaucasus = QtWidgets.QRadioButton("Caucasus - Full map [NOT RECOMMENDED]")
        terrainCaucasus.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))
        terrainCaucasusNorth = QtWidgets.QRadioButton("Caucasus - North")
        terrainCaucasusNorth.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))

        terrainPg = QtWidgets.QRadioButton("Persian Gulf - Full Map [NOT RECOMMENDED]")
        terrainPg.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Persian_Gulf"]))
        terrainIran = QtWidgets.QRadioButton("Persian Gulf - Invasion of Iran")
        terrainIran.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Persian_Gulf"]))
        terrainEmirates = QtWidgets.QRadioButton("Persian Gulf - Emirates")
        terrainEmirates.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Persian_Gulf"]))
        terrainNttr = QtWidgets.QRadioButton("Nevada - North Nevada")
        terrainNttr.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Nevada"]))
        terrainNormandy = QtWidgets.QRadioButton("Normandy")
        terrainNormandy.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Normandy"]))
        terrainNormandySmall = QtWidgets.QRadioButton("Normandy Small")
        terrainNormandySmall.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Normandy"]))
        terrainChannel = QtWidgets.QRadioButton("The Channel : Start in Dunkirk")
        terrainChannel.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Channel"]))
        terrainChannelComplete = QtWidgets.QRadioButton("The Channel : Battle of Britain")
        terrainChannelComplete.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Channel"]))
        terrainCaucasusSmall.setChecked(True)

        # List of campaigns
        campaignList = QCampaignList()
        self.registerField("selectedCampaign", campaignList)

        def on_campaign_selected():
            index = campaignList.selectionModel().currentIndex().row()
            campaign = campaignList.campaigns[index]
            self.setField("selectedCampaign", campaign)

        campaignList.selectionModel().setCurrentIndex(campaignList.indexAt(QPoint(1, 1)), QItemSelectionModel.Rows)
        campaignList.selectionModel().selectionChanged.connect(on_campaign_selected)
        on_campaign_selected()



        # Campaign settings
        mapSettingsGroup = QtWidgets.QGroupBox("Map Settings")
        invertMap = QtWidgets.QCheckBox()
        self.registerField('invertMap', invertMap)
        mapSettingsLayout = QtWidgets.QGridLayout()
        mapSettingsLayout.addWidget(QtWidgets.QLabel("Invert Map"), 1, 0)
        mapSettingsLayout.addWidget(invertMap, 1, 1)
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
        layout.addWidget(mapSettingsGroup, 0, 1, 1, 1)
        layout.addWidget(timeGroup, 1, 1, 1, 1)
        self.setLayout(layout)


class MiscOptions(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(MiscOptions, self).__init__(parent)

        self.setTitle("Miscellaneous settings")
        self.setSubTitle("\nOthers settings for the game.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/logo1.png'))

        midGame = QtWidgets.QCheckBox()
        multiplier = QtWidgets.QSpinBox()
        multiplier.setEnabled(False)
        multiplier.setMinimum(1)
        multiplier.setMaximum(5)

        miscSettingsGroup = QtWidgets.QGroupBox("Misc Settings")
        self.registerField('midGame', midGame)
        self.registerField('multiplier', multiplier)

        # Campaign settings
        generatorSettingsGroup = QtWidgets.QGroupBox("Generator Settings")
        no_carrier = QtWidgets.QCheckBox()
        self.registerField('no_carrier', no_carrier)
        no_lha = QtWidgets.QCheckBox()
        self.registerField('no_lha', no_lha)
        supercarrier = QtWidgets.QCheckBox()
        self.registerField('supercarrier', supercarrier)
        no_player_navy= QtWidgets.QCheckBox()
        self.registerField('no_player_navy', no_player_navy)
        no_enemy_navy = QtWidgets.QCheckBox()
        self.registerField('no_enemy_navy', no_enemy_navy)

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

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Start at mid game"), 1, 0)
        layout.addWidget(midGame, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Ennemy forces multiplier [Disabled for Now]"), 2, 0)
        layout.addWidget(multiplier, 2, 1)
        miscSettingsGroup.setLayout(layout)

        mlayout = QVBoxLayout()
        mlayout.addWidget(miscSettingsGroup)
        mlayout.addWidget(generatorSettingsGroup)
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
