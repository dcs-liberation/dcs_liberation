from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout

from qt_ui.windows.preferences.QLiberationPreferences import QLiberationPreferences


class QLiberationPreferencesWindow(QDialog):
    def __init__(self):
        super(QLiberationPreferencesWindow, self).__init__()

        self.setModal(True)
        self.setWindowTitle("Preferences")
        self.setMinimumSize(300, 200)
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.preferences = QLiberationPreferences()
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(lambda: self.apply())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.preferences)
        layout.addStretch()
        apply_btn_layout = QHBoxLayout()
        apply_btn_layout.addStretch()
        apply_btn_layout.addWidget(self.apply_button)
        layout.addLayout(apply_btn_layout)
        self.setLayout(layout)

    def apply(self):
        if self.preferences.apply():
            print("Closing")
            self.close()
        else:
            print("Not Closing")
