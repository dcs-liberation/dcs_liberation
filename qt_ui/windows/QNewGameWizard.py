from __future__ import unicode_literals

import datetime

from PySide2 import QtGui, QtWidgets
from dcs.task import CAP, CAS

import qt_ui.uiconstants as CONST
from game import db, Game
from gen import namegen
from theater import start_generator, persiangulf, nevada, caucasus, ConflictTheater, normandy, thechannel
from userdata.logging import version_string


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

        blueFaction = [c for c in db.FACTIONS if db.FACTIONS[c]["side"] == "blue"][self.field("blueFaction")]
        redFaction = [c for c in db.FACTIONS if db.FACTIONS[c]["side"] == "red"][self.field("redFaction")]
        playerIsBlue = self.field("playerIsBlue")
        isTerrainPg = self.field("isTerrainPg")
        isTerrainNttr = self.field("isTerrainNttr")
        isTerrainCaucasusSmall = self.field("isTerrainCaucasusSmall")
        isTerrainCaucasusSmallInverted = self.field("isTerrainCaucasusSmallInverted")
        isTerrainCaucasusNorth= self.field("isTerrainCaucasusNorth")
        isIranianCampaignTheater = self.field("isIranianCampaignTheater")
        isTerrainNormandy = self.field("isTerrainNormandy")
        isTerrainNormandySmall = self.field("isTerrainNormandySmall")
        isTerrainChannel = self.field("isTerrainChannel")
        isTerrainEmirates = self.field("isTerrainEmirates")
        timePeriod = db.TIME_PERIODS[list(db.TIME_PERIODS.keys())[self.field("timePeriod")]]
        midGame = self.field("midGame")
        multiplier = self.field("multiplier")

        player_name = playerIsBlue and blueFaction or redFaction
        enemy_name = playerIsBlue and redFaction or blueFaction

        if isTerrainPg:
            conflicttheater = persiangulf.PersianGulfTheater()
        elif isTerrainNttr:
            conflicttheater = nevada.NevadaTheater()
        elif isTerrainCaucasusSmall:
            conflicttheater = caucasus.WesternGeorgia()
        elif isTerrainCaucasusSmallInverted:
            conflicttheater = caucasus.WesternGeorgiaInverted()
        elif isTerrainCaucasusNorth:
            conflicttheater = caucasus.NorthCaucasus()
        elif isIranianCampaignTheater:
            conflicttheater = persiangulf.IranianCampaign()
        elif isTerrainEmirates:
            conflicttheater = persiangulf.Emirates()
        elif isTerrainNormandy:
            conflicttheater = normandy.NormandyTheater()
        elif isTerrainNormandySmall:
            conflicttheater = normandy.NormandySmall()
        elif isTerrainChannel:
            conflicttheater = thechannel.ChannelTheater()
        else:
            conflicttheater = caucasus.CaucasusTheater()

        self.generatedGame = self.start_new_game(player_name, enemy_name, conflicttheater, midGame, multiplier,
                                                 timePeriod)

        super(NewGameWizard, self).accept()

    def start_new_game(self, player_name: str, enemy_name: str, conflicttheater: ConflictTheater,
                       midgame: bool, multiplier: float, period: datetime):

        if midgame:
            for i in range(0, int(len(conflicttheater.controlpoints) / 2)):
                conflicttheater.controlpoints[i].captured = True

        # Reset name generator
        namegen.reset()

        print("-- Starting New Game Generator")
        print("Enemy name : " + enemy_name)
        print("Player name : " + player_name)
        print("Midgame : " + str(midgame))
        start_generator.generate_inital_units(conflicttheater, enemy_name, True, multiplier)

        print("-- Initial units generated")
        game = Game(player_name=player_name,
                    enemy_name=enemy_name,
                    theater=conflicttheater,
                    start_date=period)

        print("-- Game Object generated")
        start_generator.generate_groundobjects(conflicttheater, game)
        game.budget = int(game.budget * multiplier)
        game.settings.multiplier = multiplier
        game.settings.sams = True
        game.settings.version = version_string()

        if midgame:
            game.budget = game.budget * 4 * len(list(conflicttheater.conflicts()))

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
                       QtGui.QPixmap('./resources/ui/wizard/logo1.png'))

        self.setMinimumHeight(250)

        blues = [c for c in db.FACTIONS if db.FACTIONS[c]["side"] == "blue"]
        reds = [c for c in db.FACTIONS if db.FACTIONS[c]["side"] == "red"]

        # Create form
        blueFaction = QtWidgets.QLabel("Blue Faction :")
        self.blueFactionSelect = QtWidgets.QComboBox()
        for f in blues:
            self.blueFactionSelect.addItem(f)
        blueFaction.setBuddy(self.blueFactionSelect)

        redFaction = QtWidgets.QLabel("Red Faction :")
        self.redFactionSelect = QtWidgets.QComboBox()
        for r in reds:
            self.redFactionSelect.addItem(r)
        redFaction.setBuddy(self.redFactionSelect)

        sideGroup = QtWidgets.QGroupBox("Player Side")
        blueforRadioButton = QtWidgets.QRadioButton("BLUEFOR")
        redforRadioButton = QtWidgets.QRadioButton("REDFOR")
        blueforRadioButton.setChecked(True)

        # Unit Preview
        self.blueSideRecap = QtWidgets.QLabel("")
        self.blueSideRecap.setFont(QtGui.QFont("Arial", italic=True))
        self.blueSideRecap.setWordWrap(True)
        self.redSideRecap = QtWidgets.QLabel("")
        self.redSideRecap.setFont(QtGui.QFont("Arial", italic=True))
        self.redSideRecap.setWordWrap(True)

        # Link form fields
        self.registerField('blueFaction', self.blueFactionSelect)
        self.registerField('redFaction', self.redFactionSelect)
        self.registerField('playerIsBlue', blueforRadioButton)
        self.registerField('playerIsRed', redforRadioButton)

        # Build layout
        sideGroupLayout = QtWidgets.QVBoxLayout()
        sideGroupLayout.addWidget(blueforRadioButton)
        sideGroupLayout.addWidget(redforRadioButton)
        sideGroup.setLayout(sideGroupLayout)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(blueFaction, 0, 0)
        layout.addWidget(self.blueFactionSelect, 0, 1)
        layout.addWidget(self.blueSideRecap, 1, 0, 1, 2)
        layout.addWidget(redFaction, 2, 0)
        layout.addWidget(self.redFactionSelect, 2, 1)
        layout.addWidget(self.redSideRecap, 3, 0, 1, 2)
        layout.addWidget(sideGroup, 4, 0, 1, 2)
        self.setLayout(layout)
        self.updateUnitRecap()

        self.blueFactionSelect.activated.connect(self.updateUnitRecap)
        self.redFactionSelect.activated.connect(self.updateUnitRecap)

    def updateUnitRecap(self):
        red_units = db.FACTIONS[self.redFactionSelect.currentText()]["units"]
        blue_units = db.FACTIONS[self.blueFactionSelect.currentText()]["units"]

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


class TheaterConfiguration(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(TheaterConfiguration, self).__init__(parent)

        self.setTitle("Theater configuration")
        self.setSubTitle("\nChoose a terrain and time period for this game.")
        self.setPixmap(QtWidgets.QWizard.LogoPixmap,
                       QtGui.QPixmap('./resources/ui/wizard/logo1.png'))

        # Terrain selection
        terrainGroup = QtWidgets.QGroupBox("Terrain")
        terrainCaucasusSmall = QtWidgets.QRadioButton("Caucasus - Western Georgia [RECOMMENDED - Early Cold War Era]")
        terrainCaucasusSmall.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))
        terrainCaucasusSmallInverted = QtWidgets.QRadioButton("Caucasus - Western Georgia Inverted [RECOMMENDED - Early Cold War Era]")
        terrainCaucasusSmallInverted.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))
        terrainCaucasus = QtWidgets.QRadioButton("Caucasus - Full map [NOT TESTED]")
        terrainCaucasus.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))
        terrainCaucasusNorth = QtWidgets.QRadioButton("Caucasus - North - [RECOMMENDED - Modern Era]")
        terrainCaucasusNorth.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Caucasus"]))

        terrainPg = QtWidgets.QRadioButton("Persian Gulf - Full Map [NOT TESTED]")
        terrainPg.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Persian_Gulf"]))
        terrainIran = QtWidgets.QRadioButton("Persian Gulf - Invasion of Iran [RECOMMENDED]")
        terrainIran.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Persian_Gulf"]))
        terrainEmirates = QtWidgets.QRadioButton("Persian Gulf - Emirates [RECOMMENDED]")
        terrainEmirates.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Persian_Gulf"]))
        terrainNttr = QtWidgets.QRadioButton("Nevada - North Nevada [RECOMMENDED]")
        terrainNttr.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Nevada"]))
        terrainNormandy = QtWidgets.QRadioButton("Normandy")
        terrainNormandy.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Normandy"]))
        terrainNormandySmall = QtWidgets.QRadioButton("Normandy Small")
        terrainNormandySmall.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Normandy"]))
        terrainChannel = QtWidgets.QRadioButton("Channel")
        terrainChannel.setIcon(QtGui.QIcon(CONST.ICONS["Terrain_Channel"]))
        terrainCaucasusSmall.setChecked(True)

        # Time Period
        timeGroup = QtWidgets.QGroupBox("Time Period")
        timePeriod = QtWidgets.QLabel("Start date :")
        timePeriodSelect = QtWidgets.QComboBox()
        for r in db.TIME_PERIODS:
            timePeriodSelect.addItem(r)
        timePeriod.setBuddy(timePeriodSelect)
        timePeriodSelect.setCurrentIndex(21)

        # Register fields
        self.registerField('isTerrainCaucasus', terrainCaucasus)
        self.registerField('isTerrainCaucasusSmall', terrainCaucasusSmall)
        self.registerField('isTerrainCaucasusSmallInverted', terrainCaucasusSmallInverted)
        self.registerField('isTerrainCaucasusNorth', terrainCaucasusNorth)
        self.registerField('isTerrainPg', terrainPg)
        self.registerField('isIranianCampaignTheater', terrainIran)
        self.registerField('isTerrainEmirates', terrainEmirates)
        self.registerField('isTerrainNttr', terrainNttr)
        self.registerField('isTerrainNormandy', terrainNormandy)
        self.registerField('isTerrainNormandySmall', terrainNormandySmall)
        self.registerField('isTerrainChannel', terrainChannel)
        self.registerField('timePeriod', timePeriodSelect)

        # Build layout
        terrainGroupLayout = QtWidgets.QVBoxLayout()
        terrainGroupLayout.addWidget(terrainCaucasusSmall)
        terrainGroupLayout.addWidget(terrainCaucasusSmallInverted)
        terrainGroupLayout.addWidget(terrainCaucasusNorth)
        terrainGroupLayout.addWidget(terrainCaucasus)
        terrainGroupLayout.addWidget(terrainIran)
        terrainGroupLayout.addWidget(terrainEmirates)
        terrainGroupLayout.addWidget(terrainPg)
        terrainGroupLayout.addWidget(terrainNttr)
        terrainGroupLayout.addWidget(terrainNormandy)
        terrainGroupLayout.addWidget(terrainNormandySmall)
        terrainGroupLayout.addWidget(terrainChannel)
        terrainGroup.setLayout(terrainGroupLayout)

        timeGroupLayout = QtWidgets.QGridLayout()
        timeGroupLayout.addWidget(timePeriod, 0, 0)
        timeGroupLayout.addWidget(timePeriodSelect, 0, 1)
        timeGroup.setLayout(timeGroupLayout)

        layout = QtWidgets.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(terrainGroup)
        layout.addWidget(timeGroup)
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

        self.registerField('midGame', midGame)
        self.registerField('multiplier', multiplier)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Start at mid game"), 1, 0)
        layout.addWidget(midGame, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Ennemy forces multiplier [Disabled for Now]"), 2, 0)
        layout.addWidget(multiplier, 2, 1)
        self.setLayout(layout)


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
