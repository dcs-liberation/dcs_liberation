import sys
import webbrowser

from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QAction, QMessageBox, QDesktopWidget

import qt_ui.uiconstants as CONST
from game import Game
from qt_ui.uiconstants import URLS
from qt_ui.widgets.QTopPanel import QTopPanel
from qt_ui.widgets.map.QLiberationMap import QLiberationMap
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal, DebriefingSignal
from qt_ui.windows.QDebriefingWindow import QDebriefingWindow
from qt_ui.windows.QNewGameWizard import NewGameWizard
from userdata import persistency


class QLiberationWindow(QMainWindow):

    def __init__(self):
        super(QLiberationWindow, self).__init__()

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

        vbox = QVBoxLayout()
        vbox.setMargin(0)
        vbox.addWidget(QTopPanel(self.game))
        vbox.addWidget(self.liberation_map)

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

        self.saveGameAction = QAction("Save", self)
        self.saveGameAction.setIcon(QIcon(CONST.ICONS["Save"]))
        self.saveGameAction.triggered.connect(self.saveGame)

        self.showAboutDialogAction = QAction("About DCS Liberation", self)
        self.showAboutDialogAction.setIcon(QIcon.fromTheme("help-about"))
        self.showAboutDialogAction.triggered.connect(self.showAboutDialog)

    def initToolbar(self):
        self.tool_bar = self.addToolBar("File")
        self.tool_bar.addAction(self.newGameAction)
        #self.tool_bar.addAction(QIcon(CONST.ICONS["Open"]), "Open")
        self.tool_bar.addAction(self.saveGameAction)

    def initMenuBar(self):
        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("File")
        file_menu.addAction(self.newGameAction)
        #file_menu.addAction(QIcon(CONST.ICONS["Open"]), "Open") # TODO : implement
        file_menu.addAction(self.saveGameAction)
        #file_menu.addAction("Save As") # TODO : implement
        #file_menu.addAction("Close Current Game", lambda: self.closeGame()) # Not working
        file_menu.addAction("Exit" , lambda: self.exit())


        help_menu = self.menu.addMenu("Help")
        #help_menu.addAction("Online Manual", lambda: webbrowser.open_new_tab(URLS["Manual"]))
        #help_menu.addAction("Troubleshooting Guide", lambda: webbrowser.open_new_tab(URLS["Troubleshooting"]))
        #help_menu.addAction("Modding Guide", lambda: webbrowser.open_new_tab(URLS["Modding"]))
        #help_menu.addSeparator() ----> Note from Khopa : I disable these links since it's not up to date for this branch
        help_menu.addAction("Contribute", lambda: webbrowser.open_new_tab(URLS["Repository"]))
        help_menu.addAction("Forum Thread", lambda: webbrowser.open_new_tab(URLS["ForumThread"]))
        help_menu.addAction("Report an issue", lambda: webbrowser.open_new_tab(URLS["Issues"]))
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

    def saveGame(self):
        print("Saving game")
        persistency.save_game(self.game)
        GameUpdateSignal.get_instance().updateGame(self.game)

    def onGameGenerated(self, game: Game):
        print("On Game generated")
        self.game = game
        GameUpdateSignal.get_instance().updateGame(self.game)

    def closeGame(self):
        self.game = None
        GameUpdateSignal.get_instance().updateGame(self.game)

    def exit(self):
        sys.exit(0)

    def setGame(self, game: Game):
        self.game = game

    def showAboutDialog(self):
        text = "<h3>DCS Liberation</h3>" + \
               "<h4>Repository</h4>" + \
               "<b>Source code :</b> https://github.com/shdwp/dcs_liberation<br/>" + \
               "<h4>Authors/Contributors</h4><br/>" + \
               "<b>shdwp</b>, <b>Khopa</b>, <b>Wrycu</b>, <b>calvinmorrow</b>, <b>JohanAberg</b><br/>" + \
               "<h4>Special Thanks  :</h4>" \
               "<b>rp-</b> <i>for the pydcs framework</i><br/>"\
               "<b>Grimes (mrSkortch)</b> & <b>Speed</b> <i>for the MIST framework</i><br/>"

        about = QMessageBox()
        about.setWindowTitle("About DCS Liberation")
        about.setIcon(QMessageBox.Icon.Information)
        about.setText(text)
        print(about.textFormat())
        about.exec_()

    def onDebriefing(self, debrief: DebriefingSignal):
        print("On Debriefing")
        self.debriefing = QDebriefingWindow(debrief.debriefing, debrief.gameEvent, debrief.game)
        self.debriefing.show()
