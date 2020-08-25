import logging
import sys
import webbrowser
from os import environ

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QAction, QMessageBox, QDesktopWidget, \
    QSplitter, QFileDialog
from requests import get
from packaging import version

import qt_ui.uiconstants as CONST
from game import Game
from qt_ui.uiconstants import URLS
from qt_ui.widgets.QTopPanel import QTopPanel
from qt_ui.widgets.map.QLiberationMap import QLiberationMap
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal, DebriefingSignal
from qt_ui.windows.QDebriefingWindow import QDebriefingWindow
from qt_ui.windows.newgame.QNewGameWizard import NewGameWizard
from qt_ui.windows.infos.QInfoPanel import QInfoPanel
from qt_ui.windows.preferences.QLiberationPreferencesWindow import QLiberationPreferencesWindow
from userdata import persistency


class QLiberationWindow(QMainWindow):

    def __init__(self):
        super(QLiberationWindow, self).__init__()

        self.info_panel = None
        self.setGame(persistency.restore_game())

        self.setGeometry(300, 100, 270, 100)
        self.setWindowTitle("DCS Liberation")
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.statusBar().showMessage('Ready')

        self.initUi()
        self.initActions()
        self.initMenuBar()
        self.initToolbar()
        self.connectSignals()
        self.onGameGenerated(self.game)

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setWindowState(Qt.WindowMaximized)


    def initUi(self):

        self.liberation_map = QLiberationMap(self.game)
        self.info_panel = QInfoPanel(self.game)

        hbox = QSplitter(Qt.Horizontal)
        hbox.addWidget(self.info_panel)
        hbox.addWidget(self.liberation_map)
        hbox.setSizes([2, 8])

        vbox = QVBoxLayout()
        vbox.setMargin(0)
        vbox.addWidget(QTopPanel(self.game))
        vbox.addWidget(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def connectSignals(self):
        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)
        GameUpdateSignal.get_instance().debriefingReceived.connect(self.onDebriefing)

    def initActions(self):
        self.newGameAction = QAction("New Game", self)
        self.newGameAction.setIcon(QIcon(CONST.ICONS["New"]))
        self.newGameAction.triggered.connect(self.newGame)

        self.openAction = QAction("Open", self)
        self.openAction.setIcon(QIcon(CONST.ICONS["Open"]))
        self.openAction.triggered.connect(self.openFile)

        self.saveGameAction = QAction("Save", self)
        self.saveGameAction.setIcon(QIcon(CONST.ICONS["Save"]))
        self.saveGameAction.triggered.connect(self.saveGame)

        self.saveAsAction = QAction("Save As", self)
        self.saveAsAction.setIcon(QIcon(CONST.ICONS["Save"]))
        self.saveAsAction.triggered.connect(self.saveGameAs)

        self.showAboutDialogAction = QAction("About DCS Liberation", self)
        self.showAboutDialogAction.setIcon(QIcon.fromTheme("help-about"))
        self.showAboutDialogAction.triggered.connect(self.showAboutDialog)

        self.showLiberationPrefDialogAction = QAction("Preferences", self)
        self.showLiberationPrefDialogAction.setIcon(QIcon.fromTheme("help-about"))
        self.showLiberationPrefDialogAction.triggered.connect(self.showLiberationDialog)

    def initToolbar(self):
        self.tool_bar = self.addToolBar("File")
        self.tool_bar.addAction(self.newGameAction)
        self.tool_bar.addAction(self.openAction)
        self.tool_bar.addAction(self.saveGameAction)

    def initMenuBar(self):
        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("File")
        file_menu.addAction(self.newGameAction)
        file_menu.addAction(self.openAction)
        file_menu.addAction(self.saveGameAction)
        file_menu.addAction(self.saveAsAction)
        file_menu.addSeparator()
        file_menu.addAction(self.showLiberationPrefDialogAction)
        file_menu.addSeparator()
        #file_menu.addAction("Close Current Game", lambda: self.closeGame()) # Not working
        file_menu.addAction("Exit" , lambda: self.exit())

        help_menu = self.menu.addMenu("Help")
        help_menu.addAction("Discord Server", lambda: webbrowser.open_new_tab("https://" + "discord.gg" + "/" + "bKrt" + "rkJ"))
        help_menu.addAction("Github Repository", lambda: webbrowser.open_new_tab("https://github.com/khopa/dcs_liberation"))
        help_menu.addAction("Releases", lambda: webbrowser.open_new_tab("https://github.com/Khopa/dcs_liberation/releases"))
        help_menu.addAction("Online Manual", lambda: webbrowser.open_new_tab(URLS["Manual"]))
        help_menu.addAction("ED Forum Thread", lambda: webbrowser.open_new_tab(URLS["ForumThread"]))
        help_menu.addAction("Report an issue", lambda: webbrowser.open_new_tab(URLS["Issues"]))
        help_menu.addAction("Check new version", lambda: self._check_and_download_new_version)

        help_menu.addSeparator()
        help_menu.addAction(self.showAboutDialogAction)

        displayMenu = self.menu.addMenu("Display")

        tg_cp_visibility = QAction('Control Point', displayMenu)
        tg_cp_visibility.setCheckable(True)
        tg_cp_visibility.setChecked(True)
        tg_cp_visibility.toggled.connect(lambda: QLiberationMap.set_display_rule("cp", tg_cp_visibility.isChecked()))

        tg_go_visibility = QAction('Ground Objects', displayMenu)
        tg_go_visibility.setCheckable(True)
        tg_go_visibility.setChecked(True)
        tg_go_visibility.toggled.connect(lambda: QLiberationMap.set_display_rule("go", tg_go_visibility.isChecked()))

        tg_line_visibility = QAction('Lines', displayMenu)
        tg_line_visibility.setCheckable(True)
        tg_line_visibility.setChecked(True)
        tg_line_visibility.toggled.connect(
            lambda: QLiberationMap.set_display_rule("lines", tg_line_visibility.isChecked()))

        tg_event_visibility = QAction('Events', displayMenu)
        tg_event_visibility.setCheckable(True)
        tg_event_visibility.setChecked(True)
        tg_event_visibility.toggled.connect(lambda: QLiberationMap.set_display_rule("events", tg_event_visibility.isChecked()))

        tg_sam_visibility = QAction('SAM Range', displayMenu)
        tg_sam_visibility.setCheckable(True)
        tg_sam_visibility.setChecked(True)
        tg_sam_visibility.toggled.connect(lambda: QLiberationMap.set_display_rule("sam", tg_sam_visibility.isChecked()))

        tg_flight_path_visibility = QAction('Flight Paths', displayMenu)
        tg_flight_path_visibility.setCheckable(True)
        tg_flight_path_visibility.setChecked(False)
        tg_flight_path_visibility.toggled.connect(lambda: QLiberationMap.set_display_rule("flight_paths", tg_flight_path_visibility.isChecked()))

        displayMenu.addAction(tg_go_visibility)
        displayMenu.addAction(tg_cp_visibility)
        displayMenu.addAction(tg_line_visibility)
        displayMenu.addAction(tg_event_visibility)
        displayMenu.addAction(tg_sam_visibility)
        displayMenu.addAction(tg_flight_path_visibility)

    def newGame(self):
        wizard = NewGameWizard(self)
        wizard.show()
        wizard.accepted.connect(lambda: self.onGameGenerated(wizard.generatedGame))

    def openFile(self):
        file = QFileDialog.getOpenFileName(self, "Select game file to open",
                                               dir=persistency._dcs_saved_game_folder,
                                               filter="*.liberation")
        if file is not None:
            game = persistency.load_game(file[0])
            self.setGame(game)
            GameUpdateSignal.get_instance().updateGame(self.game)

    def saveGame(self):
        logging.info("Saving game")

        if self.game.savepath:
            persistency.save_game(self.game)
            GameUpdateSignal.get_instance().updateGame(self.game)
        else:
            self.saveGameAs()

    def saveGameAs(self):
        file = QFileDialog.getSaveFileName(self, "Save As", dir=persistency._dcs_saved_game_folder, filter="*.liberation")
        if file is not None:
            self.game.savepath = file[0]
            persistency.save_game(self.game)

    def onGameGenerated(self, game: Game):
        logging.info("On Game generated")
        self.game = game
        GameUpdateSignal.get_instance().updateGame(self.game)

    def closeGame(self):
        self.game = None
        GameUpdateSignal.get_instance().updateGame(self.game)

    def exit(self):
        sys.exit(0)

    def setGame(self, game: Game):
        self.game = game
        if self.info_panel:
            self.info_panel.setGame(game)

    def showAboutDialog(self):
        text = "<h3>DCS Liberation " + CONST.VERSION_STRING + "</h3>" + \
               "<b>Source code :</b> https://github.com/khopa/dcs_liberation" + \
               "<h4>Authors</h4>" + \
               "<p>DCS Liberation was originally developed by <b>shdwp</b>, DCS Liberation 2.0 is a partial rewrite based on this work by <b>Khopa</b>." \
               "<h4>Contributors</h4>" + \
               "shdwp, Khopa, Wrycu, calvinmorrow, JohanAberg, Deus, root0fall, Captain Cody" + \
               "<h4>Special Thanks  :</h4>" \
               "<b>rp-</b> <i>for the pydcs framework</i><br/>"\
               "<b>Grimes (mrSkortch)</b> & <b>Speed</b> <i>for the MIST framework</i><br/>"\
               "<b>Ciribob </b> <i>for the JTACAutoLase.lua script</i><br/>"
        about = QMessageBox()
        about.setWindowTitle("About DCS Liberation")
        about.setIcon(QMessageBox.Icon.Information)
        about.setText(text)
        logging.info(about.textFormat())
        about.exec_()

    def showLiberationDialog(self):
        self.subwindow = QLiberationPreferencesWindow()
        self.subwindow.show()

    def onDebriefing(self, debrief: DebriefingSignal):
        logging.info("On Debriefing")
        self.debriefing = QDebriefingWindow(debrief.debriefing, debrief.gameEvent, debrief.game)
        self.debriefing.show()

    def _check_and_download_new_version(self):
        file_name, browser_download_url = '', ''
        try:
            response = get('https://api.github.com/repos/Khopa/dcs_liberation/releases/latest')
            if response.status_code == 200:
                online_version = response.json()['tag_name']
                if version.parse(online_version) > version.parse(CONST.VERSION_STRING):
                    print(f'There is new version of dcs_liberation: {online_version}')
                    file_name = response.json()['assets'][0]['name']
                    browser_download_url = response.json()['assets'][0]['browser_download_url']
                elif version.parse(online_version) == version.parse(CONST.VERSION_STRING):
                    print(f'This is up-to-date version: {CONST.VERSION_STRING}')
            else:
                print(f'Unable to check version online. Try again later. Status={response.status_code}')
        except Exception as exc:
            print(f'Unable to check version online: {exc}')

        if browser_download_url:
            full_zip_path, _ = QFileDialog.getSaveFileName(self, caption='Save File', directory=environ['HOME'],
                                                           filter='All Files [*.*](*.*)', options=QFileDialog.ReadOnly)
            if full_zip_path:
                with open(full_zip_path, 'wb') as zip_file:
                    zip_file.write(get(browser_download_url).content)
