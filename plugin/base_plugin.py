from PySide2.QtCore import QSize, Qt, QItemSelectionModel, QPoint
from PySide2.QtWidgets import QLabel, QDialog, QGridLayout, QListView, QStackedLayout, QComboBox, QWidget, \
    QAbstractItemView, QPushButton, QGroupBox, QCheckBox, QVBoxLayout, QSpinBox

class BasePlugin():
    nameInUI:str = "Base plugin"
    nameInSettings:str = "plugin.base"
    enabledDefaultValue:bool = False

    def __init__(self):
        self.uiWidget: QCheckBox = None
        self.enabled = self.enabledDefaultValue
        self.settings = None

    def setupUI(self, settingsWindow, row:int):
        self.settings = settingsWindow.game.settings

        self.uiWidget = QCheckBox()
        self.uiWidget.setChecked(self.isEnabled())
        self.uiWidget.toggled.connect(lambda: self.applySetting(settingsWindow))

        settingsWindow.pluginsGroupLayout.addWidget(QLabel(self.nameInUI), row, 0)
        settingsWindow.pluginsGroupLayout.addWidget(self.uiWidget, row, 1, Qt.AlignRight)

    def setSettings(self, settings):
        self.settings = settings
        if not self.nameInSettings in self.settings.plugins:
            self.settings.plugins[self.nameInSettings] = self.enabledDefaultValue

    def applySetting(self, settingsWindow):
        self.settings.plugins[self.nameInSettings] = self.uiWidget.isChecked()
        self.enabled = self.settings.plugins[self.nameInSettings]
   
    def injectScripts(self, operation):
        self.settings = operation.game.settings
        return self.isEnabled()

    def injectConfiguration(self, operation):
        self.settings = operation.game.settings
        return self.isEnabled()

    def isEnabled(self) -> bool:
        if not self.settings:
            return False

        self.setSettings(self.settings) # create the necessary settings keys if needed

        return self.settings != None and self.settings.plugins[self.nameInSettings]
