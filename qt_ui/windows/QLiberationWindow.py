import logging
import traceback
import webbrowser
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent, QIcon
from PySide2.QtWidgets import (
    QAction,
    QActionGroup,
    QDesktopWidget,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

import qt_ui.uiconstants as CONST
from game import Game, VERSION, persistency
from game.debriefing import Debriefing
from qt_ui import liberation_install
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel
from qt_ui.simcontroller import SimController
from qt_ui.uiconstants import URLS
from qt_ui.uncaughtexceptionhandler import UncaughtExceptionHandler
from qt_ui.widgets.QTopPanel import QTopPanel
from qt_ui.widgets.ato import QAirTaskingOrderPanel
from qt_ui.widgets.map.QLiberationMap import QLiberationMap
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QDebriefingWindow import QDebriefingWindow
from qt_ui.windows.infos.QInfoPanel import QInfoPanel
from qt_ui.windows.logs.QLogsWindow import QLogsWindow
from qt_ui.windows.newgame.QNewGameWizard import NewGameWizard
from qt_ui.windows.notes.QNotesWindow import QNotesWindow
from qt_ui.windows.preferences.QLiberationPreferencesWindow import (
    QLiberationPreferencesWindow,
)
from qt_ui.windows.settings.QSettingsWindow import QSettingsWindow
from qt_ui.windows.stats.QStatsWindow import QStatsWindow


class QLiberationWindow(QMainWindow):
    def __init__(self, game: Optional[Game]) -> None:
        super().__init__()

        self._uncaught_exception_handler = UncaughtExceptionHandler(self)

        self.game = game
        self.game_model = GameModel(game)
        Dialog.set_game(self.game_model)
        self.sim_controller = SimController(self.game)
        self.ato_panel = QAirTaskingOrderPanel(self.game_model)
        self.info_panel = QInfoPanel(self.game)
        self.liberation_map = QLiberationMap(self.game_model, self.sim_controller, self)

        self.setGeometry(300, 100, 270, 100)
        self.updateWindowTitle()
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.statusBar().showMessage("Ready")

        self.initUi()
        self.initActions()
        self.initToolbar()
        self.initMenuBar()
        self.connectSignals()

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setWindowState(Qt.WindowMaximized)

        if self.game is None:
            last_save_file = liberation_install.get_last_save_file()
            if last_save_file:
                try:
                    logging.info("Loading last saved game : " + str(last_save_file))
                    game = persistency.load_game(last_save_file)
                    self.onGameGenerated(game)
                    self.updateWindowTitle(last_save_file if game else None)
                except:
                    logging.info("Error loading latest save game")
            else:
                logging.info("No existing save game")
        else:
            self.onGameGenerated(self.game)

    def initUi(self):
        hbox = QSplitter(Qt.Horizontal)
        vbox = QSplitter(Qt.Vertical)
        hbox.addWidget(self.ato_panel)
        hbox.addWidget(vbox)
        vbox.addWidget(self.liberation_map)
        vbox.addWidget(self.info_panel)

        # Will make the ATO sidebar as small as necessary to fit the content. In
        # practice this means it is sized by the hints in the panel.
        hbox.setSizes([1, 10000000])
        vbox.setSizes([600, 100])

        vbox = QVBoxLayout()
        vbox.setMargin(0)
        vbox.addWidget(QTopPanel(self.game_model, self.sim_controller))
        vbox.addWidget(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def connectSignals(self):
        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)
        GameUpdateSignal.get_instance().debriefingReceived.connect(self.onDebriefing)

    def initActions(self):
        self.newGameAction = QAction("&New Game", self)
        self.newGameAction.setIcon(QIcon(CONST.ICONS["New"]))
        self.newGameAction.triggered.connect(self.newGame)
        self.newGameAction.setShortcut("CTRL+N")

        self.openAction = QAction("&Open", self)
        self.openAction.setIcon(QIcon(CONST.ICONS["Open"]))
        self.openAction.triggered.connect(self.openFile)
        self.openAction.setShortcut("CTRL+O")

        self.saveGameAction = QAction("&Save", self)
        self.saveGameAction.setIcon(QIcon(CONST.ICONS["Save"]))
        self.saveGameAction.triggered.connect(self.saveGame)
        self.saveGameAction.setShortcut("CTRL+S")

        self.saveAsAction = QAction("Save &As", self)
        self.saveAsAction.setIcon(QIcon(CONST.ICONS["Save"]))
        self.saveAsAction.triggered.connect(self.saveGameAs)
        self.saveAsAction.setShortcut("CTRL+A")

        self.showAboutDialogAction = QAction("&About DCS Liberation", self)
        self.showAboutDialogAction.setIcon(QIcon.fromTheme("help-about"))
        self.showAboutDialogAction.triggered.connect(self.showAboutDialog)

        self.showLiberationPrefDialogAction = QAction("&Preferences", self)
        self.showLiberationPrefDialogAction.setIcon(QIcon.fromTheme("help-about"))
        self.showLiberationPrefDialogAction.triggered.connect(self.showLiberationDialog)

        self.openDiscordAction = QAction("&Discord Server", self)
        self.openDiscordAction.setIcon(CONST.ICONS["Discord"])
        self.openDiscordAction.triggered.connect(
            lambda: webbrowser.open_new_tab(
                "https://" + "discord.gg" + "/" + "bKrt" + "rkJ"
            )
        )

        self.openGithubAction = QAction("&Github Repo", self)
        self.openGithubAction.setIcon(CONST.ICONS["Github"])
        self.openGithubAction.triggered.connect(
            lambda: webbrowser.open_new_tab(
                "https://github.com/dcs-liberation/dcs_liberation"
            )
        )

        self.openLogsAction = QAction("Show &logs", self)
        self.openLogsAction.triggered.connect(self.showLogsDialog)

        self.openSettingsAction = QAction("Settings", self)
        self.openSettingsAction.setIcon(CONST.ICONS["Settings"])
        self.openSettingsAction.triggered.connect(self.showSettingsDialog)

        self.openStatsAction = QAction("Stats", self)
        self.openStatsAction.setIcon(CONST.ICONS["Statistics"])
        self.openStatsAction.triggered.connect(self.showStatsDialog)

        self.openNotesAction = QAction("Notes", self)
        self.openNotesAction.setIcon(CONST.ICONS["Notes"])
        self.openNotesAction.triggered.connect(self.showNotesDialog)

    def initToolbar(self):
        self.tool_bar = self.addToolBar("File")
        self.tool_bar.addAction(self.newGameAction)
        self.tool_bar.addAction(self.openAction)
        self.tool_bar.addAction(self.saveGameAction)

        self.links_bar = self.addToolBar("Links")
        self.links_bar.addAction(self.openDiscordAction)
        self.links_bar.addAction(self.openGithubAction)

        self.actions_bar = self.addToolBar("Actions")
        self.actions_bar.addAction(self.openSettingsAction)
        self.actions_bar.addAction(self.openStatsAction)
        self.actions_bar.addAction(self.openNotesAction)

    def initMenuBar(self):
        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(self.newGameAction)
        file_menu.addAction(self.openAction)
        file_menu.addSeparator()
        file_menu.addAction(self.saveGameAction)
        file_menu.addAction(self.saveAsAction)
        file_menu.addSeparator()
        file_menu.addAction(self.showLiberationPrefDialogAction)
        file_menu.addSeparator()
        file_menu.addAction("E&xit", self.close)

        help_menu = self.menu.addMenu("&Help")
        help_menu.addAction(self.openDiscordAction)
        help_menu.addAction(self.openGithubAction)
        help_menu.addAction(
            "&Releases",
            lambda: webbrowser.open_new_tab(
                "https://github.com/dcs-liberation/dcs_liberation/releases"
            ),
        )
        help_menu.addAction(
            "&Online Manual", lambda: webbrowser.open_new_tab(URLS["Manual"])
        )
        help_menu.addAction(
            "&ED Forum Thread", lambda: webbrowser.open_new_tab(URLS["ForumThread"])
        )
        help_menu.addAction(
            "Report an &issue", lambda: webbrowser.open_new_tab(URLS["Issues"])
        )
        help_menu.addAction(self.openLogsAction)

        help_menu.addSeparator()
        help_menu.addAction(self.showAboutDialogAction)

    @staticmethod
    def make_display_rule_action(
        display_rule, group: Optional[QActionGroup] = None
    ) -> QAction:
        def make_check_closure():
            def closure():
                display_rule.value = action.isChecked()

            return closure

        action = QAction(f"&{display_rule.menu_text}", group)

        if display_rule.menu_text in CONST.ICONS.keys():
            action.setIcon(CONST.ICONS[display_rule.menu_text])

        action.setCheckable(True)
        action.setChecked(display_rule.value)
        action.toggled.connect(make_check_closure())
        return action

    def newGame(self):
        wizard = NewGameWizard(self)
        wizard.show()
        wizard.accepted.connect(lambda: self.onGameGenerated(wizard.generatedGame))

    def openFile(self):
        if self.game is not None and self.game.savepath:
            save_dir = self.game.savepath
        else:
            save_dir = str(persistency.save_dir())
        file = QFileDialog.getOpenFileName(
            self,
            "Select game file to open",
            dir=save_dir,
            filter="*.liberation",
        )
        if file is not None and file[0] != "":
            game = persistency.load_game(file[0])
            GameUpdateSignal.get_instance().game_loaded.emit(game)

            self.updateWindowTitle(file[0])

    def saveGame(self):
        logging.info("Saving game")

        if self.game.savepath:
            persistency.save_game(self.game)
            liberation_install.setup_last_save_file(self.game.savepath)
            liberation_install.save_config()
        else:
            self.saveGameAs()

    def saveGameAs(self):
        if self.game is not None and self.game.savepath:
            save_dir = self.game.savepath
        else:
            save_dir = str(persistency.save_dir())
        file = QFileDialog.getSaveFileName(
            self,
            "Save As",
            dir=save_dir,
            filter="*.liberation",
        )
        if file is not None:
            self.game.savepath = file[0]
            persistency.save_game(self.game)
            liberation_install.setup_last_save_file(self.game.savepath)
            liberation_install.save_config()

            self.updateWindowTitle(file[0])

    def updateWindowTitle(self, save_path: Optional[str] = None) -> None:
        """
        to DCS Liberation - vX.X.X - file_name
        """
        window_title = f"DCS Liberation - v{VERSION}"
        if save_path:  # appending the file name to title as it is updated
            file_name = save_path.split("/")[-1].split(".liberation")[0]
            window_title = f"{window_title} - {file_name}"
        self.setWindowTitle(window_title)

    def onGameGenerated(self, game: Game):
        self.updateWindowTitle()
        logging.info("On Game generated")
        self.game = game
        GameUpdateSignal.get_instance().game_loaded.emit(self.game)

    def setGame(self, game: Optional[Game]):
        try:
            self.game = game
            if self.info_panel is not None:
                self.info_panel.setGame(game)
            self.sim_controller.set_game(game)
            self.game_model.set(self.game)
            self.liberation_map.set_game(game)
        except AttributeError:
            logging.exception("Incompatible save game")
            QMessageBox.critical(
                self,
                "Could not load save game",
                "The save game you have loaded is incompatible with this "
                "version of DCS Liberation.\n"
                "\n"
                f"{traceback.format_exc()}",
                QMessageBox.Ok,
            )
            GameUpdateSignal.get_instance().updateGame(None)

    def showAboutDialog(self):
        text = (
            "<h3>DCS Liberation "
            + VERSION
            + "</h3>"
            + "<b>Source code :</b> https://github.com/dcs-liberation/dcs_liberation"
            + "<h4>Authors</h4>"
            + "<p>DCS Liberation was originally developed by <b>shdwp</b>, DCS Liberation 2.0 is a partial rewrite based on this work by <b>Khopa</b>."
            "<h4>Contributors</h4>"
            + "shdwp, Khopa, ColonelPanic, Roach, Malakhit, Wrycu, calvinmorrow, JohanAberg, Deus, SiKruger, Mustang-25, root0fall, Captain Cody, steveveepee, pedromagueija, parithon, bwRavencl, davidp57, Plob, Hawkmoon"
            + "<h4>Special Thanks  :</h4>"
            "<b>rp-</b> <i>for the pydcs framework</i><br/>"
            "<b>Grimes (mrSkortch)</b> & <b>Speed</b> <i>for the MIST framework</i><br/>"
            "<b>Ciribob </b> <i>for the JTACAutoLase.lua script</i><br/>"
            "<b>Walder </b> <i>for the Skynet-IADS script</i><br/>"
            "<b>Anubis Yinepu </b> <i>for the Hercules Cargo script</i><br/>"
        )
        about = QMessageBox()
        about.setWindowTitle("About DCS Liberation")
        about.setIcon(QMessageBox.Icon.Information)
        about.setText(text)
        logging.info(about.textFormat())
        about.exec_()

    def showLiberationDialog(self):
        self.subwindow = QLiberationPreferencesWindow()
        self.subwindow.show()

    def showSettingsDialog(self) -> None:
        self.dialog = QSettingsWindow(self.game)
        self.dialog.show()

    def showStatsDialog(self):
        self.dialog = QStatsWindow(self.game)
        self.dialog.show()

    def showNotesDialog(self):
        self.dialog = QNotesWindow(self.game)
        self.dialog.show()

    def showLogsDialog(self):
        self.dialog = QLogsWindow()
        self.dialog.show()

    def onDebriefing(self, debrief: Debriefing):
        logging.info("On Debriefing")
        self.debriefing = QDebriefingWindow(debrief)
        self.debriefing.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        result = QMessageBox.question(
            self,
            "Quit Liberation?",
            "Are you sure you want to quit? All unsaved progress will be lost.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if result == QMessageBox.Yes:
            self.sim_controller.shut_down()
            super().closeEvent(event)
            self.dialog = None
        else:
            event.ignore()
