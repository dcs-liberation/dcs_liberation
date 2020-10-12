from dcs.triggers import TriggerStart
from PySide2.QtCore import QSize, Qt, QItemSelectionModel, QPoint
from PySide2.QtWidgets import QLabel, QDialog, QGridLayout, QListView, QStackedLayout, QComboBox, QWidget, \
    QAbstractItemView, QPushButton, QGroupBox, QCheckBox, QVBoxLayout, QSpinBox
from .base_plugin import BasePlugin

class JtacAutolasePlugin(BasePlugin):
    nameInUI:str = "JTAC Autolase"
    nameInSettings:str = "plugin.jtacAutolase"
    enabledDefaultValue:bool = True
    
    #Allow spawn option
    nameInUI_useSmoke:str = "JTACs use smoke"
    nameInSettings_useSmoke:str = "plugin.jtacAutolase.useSmoke"

    def setupUI(self, settingsWindow, row:int):
        # call the base method to add the plugin selection checkbox
        super().setupUI(settingsWindow, row)

        if settingsWindow.pluginsOptionsPageLayout:
            self.optionsGroup = QGroupBox(self.nameInUI)
            optionsGroupLayout = QGridLayout();
            optionsGroupLayout.setAlignment(Qt.AlignTop)
            self.optionsGroup.setLayout(optionsGroupLayout)
            settingsWindow.pluginsOptionsPageLayout.addWidget(self.optionsGroup)

            # JTAC use smoke
            if not self.nameInSettings_useSmoke in self.settings.plugins:
                self.settings.plugins[self.nameInSettings_useSmoke] = True

            self.uiWidget_useSmoke = QCheckBox()
            self.uiWidget_useSmoke.setChecked(self.settings.plugins[self.nameInSettings_useSmoke])
            self.uiWidget_useSmoke.toggled.connect(lambda: self.applySetting(settingsWindow))

            optionsGroupLayout.addWidget(QLabel(self.nameInUI_useSmoke), 0, 0)
            optionsGroupLayout.addWidget(self.uiWidget_useSmoke, 0, 1, Qt.AlignRight)

            # disable or enable the UI in the plugins special page
            self.enableOptionsGroup()

    def enableOptionsGroup(self):
        pluginEnabled = self.uiWidget.isChecked()
        self.optionsGroup.setEnabled(pluginEnabled)

    def applySetting(self, settingsWindow):
        # call the base method to apply the plugin selection checkbox value
        super().applySetting(settingsWindow)

        # save the "use smoke" option
        self.settings.plugins[self.nameInSettings_useSmoke] = self.uiWidget_useSmoke.isChecked()

        # disable or enable the UI in the plugins special page
        self.enableOptionsGroup()

    def injectScripts(self, operation):
        if super().injectScripts(operation):
            operation.injectPluginScript("jtacautolase", "JTACAutoLase.lua", "jtacautolase")

    def injectConfiguration(self, operation):
        if super().injectConfiguration(operation):

            # add a configuration for JTACAutoLase and start lasing for all JTACs
            smoke = "local smoke = false"
            if self.settings.plugins[self.nameInSettings_useSmoke]:
                smoke = "local smoke = true"

            lua = smoke + """

            -- setting and starting JTACs
            env.info("DCSLiberation|: setting and starting JTACs")

            for _, jtac in pairs(dcsLiberation.JTACs) do
                if dcsLiberation.JTACAutoLase then 
                    dcsLiberation.JTACAutoLase(jtac.dcsUnit, jtac.code, smoke, 'vehicle') 
                end
            end
            """

            operation.injectLuaTrigger(lua, "Setting and starting JTACs")

