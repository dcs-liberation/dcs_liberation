import os

from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from qt_ui import liberation_install, liberation_theme
from qt_ui.liberation_theme import THEMES, get_theme_index, set_theme_index
from game.locale import Localize, Locale


class QLiberationPreferences(QFrame):

    def __init__(self):
        super(QLiberationPreferences, self).__init__()
        self.saved_game_dir = ""
        self.dcs_install_dir = ""

        self.dcs_install_dir = liberation_install.get_dcs_install_directory()
        self.saved_game_dir = liberation_install.get_saved_game_dir()

        self.edit_dcs_install_dir = QLineEdit(self.dcs_install_dir)
        self.edit_saved_game_dir = QLineEdit(self.saved_game_dir)

        self.edit_dcs_install_dir.setMinimumWidth(300)
        self.edit_saved_game_dir.setMinimumWidth(300)

        self.browse_saved_game = QPushButton("Browse...")
        self.browse_saved_game.clicked.connect(self.on_browse_saved_games)
        self.browse_install_dir = QPushButton("Browse...")
        self.browse_install_dir.clicked.connect(self.on_browse_installation_dir)
        self.themeSelect = QComboBox()
        [self.themeSelect.addItem(y['themeName']) for x, y in THEMES.items()]

        self.locale_select = QComboBox()
        for i in Locale:
            self.locale_select.addItem(Localize.lang_desc(i))

        self.initUi()

    def initUi(self):
        main_layout = QVBoxLayout()
        layout = QGridLayout()
        layout.addWidget(QLabel("<strong>DCS saved game directory:</strong>"), 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.edit_saved_game_dir, 1, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.browse_saved_game, 1, 1, alignment=Qt.AlignRight)
        layout.addWidget(QLabel("<strong>DCS installation directory:</strong>"), 2, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.edit_dcs_install_dir, 3, 0, alignment=Qt.AlignRight)
        layout.addWidget(self.browse_install_dir, 3, 1, alignment=Qt.AlignRight)
        layout.addWidget(QLabel("<strong>Theme (Requires Restart)</strong>"), 4, 0)
        layout.addWidget(self.themeSelect, 4, 1, alignment=Qt.AlignRight)
        layout.addWidget(QLabel("<strong>Localization</strong>"), 5, 0)
        layout.addWidget(self.locale_select, 5, 1, alignment=Qt.AlignRight)
        self.themeSelect.setCurrentIndex(get_theme_index())

        main_layout.addLayout(layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def on_browse_saved_games(self):
        saved_game_dir = str(QFileDialog.getExistingDirectory(self, "Select DCS Saved Game Directory"))
        if saved_game_dir:
            self.saved_game_dir = saved_game_dir
            self.edit_saved_game_dir.setText(saved_game_dir)

    def on_browse_installation_dir(self):
        install_dir = str(QFileDialog.getExistingDirectory(self, "Select DCS Installation Directory"))
        if install_dir:
            self.dcs_install_dir = install_dir
            self.edit_dcs_install_dir.setText(install_dir)

    def apply(self):

        print("Applying changes")
        self.saved_game_dir = self.edit_saved_game_dir.text()
        self.dcs_install_dir = self.edit_dcs_install_dir.text()
        set_theme_index(self.themeSelect.currentIndex())

        if not os.path.isdir(self.saved_game_dir):
            error_dialog = QMessageBox.critical(self, "Wrong DCS Saved Games directory.",
                                                self.saved_game_dir + " is not a valid directory",
                                                QMessageBox.StandardButton.Ok)
            error_dialog.exec_()
            return False

        if not os.path.isdir(self.dcs_install_dir):
            error_dialog = QMessageBox.critical(self, "Wrong DCS installation directory.",
                                                self.dcs_install_dir + " is not a valid directory",
                                                QMessageBox.StandardButton.Ok)
            error_dialog.exec_()
            return False

        if not os.path.isdir(os.path.join(self.dcs_install_dir, "Scripts")) and os.path.isfile(
                os.path.join(self.dcs_install_dir, "bin", "DCS.exe")):
            error_dialog = QMessageBox.critical(self, "Wrong DCS installation directory.",
                                                self.dcs_install_dir + " is not a valid DCS installation directory",
                                                QMessageBox.StandardButton.Ok)
            error_dialog.exec_()
            return False

        liberation_install.setup(
            self.saved_game_dir,
            self.dcs_install_dir,
            Localize.get_locale_from_desc(self.locale_select.currentText())
        )
        liberation_install.save_config()
        liberation_theme.save_theme_config()
        return True
