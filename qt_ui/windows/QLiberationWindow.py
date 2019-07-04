from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMenuBar, QMainWindow
import webbrowser

from qt_ui.uiconstants import URLS
from qt_ui.windows.QLiberationMap import QLiberationMap


class QLiberationWindow(QMainWindow):

    def __init__(self):
        super(QLiberationWindow, self).__init__()
        self.init_ui()

    def init_ui(self):

        self.setGeometry(300, 100, 270, 100)
        self.setWindowTitle("DCS Liberation")
        self.setWindowIcon(QIcon("../resources/icon.png"))
        self.statusBar().showMessage('Ready')
        self.init_menubar()

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        self.liberation_map = QLiberationMap()
        hbox.addWidget(self.liberation_map)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)


    def init_menubar(self):
        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("File")
        file_menu.addAction("New Game")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addAction("Save As")

        help_menu = self.menu.addMenu("Help")
        help_menu.addAction("Online Manual", lambda: webbrowser.open_new_tab(URLS["Manual"]))
        help_menu.addAction("Troubleshooting Guide", lambda: webbrowser.open_new_tab(URLS["Troubleshooting"]))
        help_menu.addAction("Modding Guide", lambda: webbrowser.open_new_tab(URLS["Modding"]))
        help_menu.addSeparator()
        help_menu.addAction("Contribute", lambda: webbrowser.open_new_tab(URLS["Repository"]))
        help_menu.addAction("Forum Thread", lambda: webbrowser.open_new_tab(URLS["ForumThread"]))
        help_menu.addAction("Report an issue", lambda: webbrowser.open_new_tab(URLS["Issues"]))
