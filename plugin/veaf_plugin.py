from PySide2.QtCore import QSize, Qt, QItemSelectionModel, QPoint
from PySide2.QtWidgets import QLabel, QDialog, QGridLayout, QListView, QStackedLayout, QComboBox, QWidget, \
    QAbstractItemView, QPushButton, QGroupBox, QCheckBox, QVBoxLayout, QSpinBox
from .base_plugin import BasePlugin

class VeafPlugin(BasePlugin):
    nameInUI:str = "VEAF framework"
    nameInSettings:str = "plugin.veaf"
    enabledDefaultValue:bool = False

    #Allow spawn option
    nameInUI_allowSpawn:str = "Allow units spawn via markers and CTLD (not implemented yet)"
    nameInSettings_allowSpawn:str = "plugin.veaf.allowSpawn"
    
    def setupUI(self, settingsWindow, row:int):
        # call the base method to add the plugin selection checkbox
        super().setupUI(settingsWindow, row)      

        if settingsWindow.pluginsOptionsPageLayout:
            self.optionsGroup = QGroupBox(self.nameInUI)
            optionsGroupLayout = QGridLayout();
            optionsGroupLayout.setAlignment(Qt.AlignTop)
            self.optionsGroup.setLayout(optionsGroupLayout)
            settingsWindow.pluginsOptionsPageLayout.addWidget(self.optionsGroup)

            # allow spawn of objects
            if not self.nameInSettings_allowSpawn in self.settings.plugins:
                self.settings.plugins[self.nameInSettings_allowSpawn] = True

            self.uiWidget_allowSpawn = QCheckBox()
            self.uiWidget_allowSpawn.setChecked(self.settings.plugins[self.nameInSettings_allowSpawn])
            self.uiWidget_allowSpawn.setEnabled(False)
            self.uiWidget_allowSpawn.toggled.connect(lambda: self.applySetting(settingsWindow))

            optionsGroupLayout.addWidget(QLabel(self.nameInUI_allowSpawn), 0, 0)
            optionsGroupLayout.addWidget(self.uiWidget_allowSpawn, 0, 1, Qt.AlignRight)

            # disable or enable the UI in the plugins special page
            self.enableOptionsGroup()

    def enableOptionsGroup(self):
        pluginEnabled = self.uiWidget.isChecked()
        self.optionsGroup.setEnabled(pluginEnabled)

    def applySetting(self, settingsWindow):
        # call the base method to apply the plugin selection checkbox value
        super().applySetting(settingsWindow)

        # save the "allow spawn" option
        self.settings.plugins[self.nameInSettings_allowSpawn] = self.uiWidget_allowSpawn.isChecked()

        # disable or enable the UI in the plugins special page
        self.enableOptionsGroup()

    def injectScripts(self, operation):
        if super().injectScripts(operation):
            # bypass JTACAutoLase
            operation.bypassPluginScript("veaf", "jtacautolase")
            
            # inject the required scripts
            operation.injectPluginScript("veaf", "src\\scripts\\mist.lua", "mist")
            operation.injectPluginScript("veaf", "src\\scripts\\Moose.lua", "moose")
            operation.injectPluginScript("veaf", "src\\scripts\\CTLD.lua", "ctld")
            #operation.injectPluginScript("veaf", "src\\scripts\\NIOD.lua", "niod")
            operation.injectPluginScript("veaf", "src\\scripts\\WeatherMark.lua", "weathermark")
            operation.injectPluginScript("veaf", "src\\scripts\\veaf.lua", "veaf")
            operation.injectPluginScript("veaf", "src\\scripts\\dcsUnits.lua", "dcsunits")
            operation.injectPluginScript("veaf", "src\\scripts\\veafAssets.lua", "veafassets")
            operation.injectPluginScript("veaf", "src\\scripts\\veafCarrierOperations.lua", "veafcarrieroperations")
            operation.injectPluginScript("veaf", "src\\scripts\\veafCasMission.lua", "veafcasmission")
            operation.injectPluginScript("veaf", "src\\scripts\\veafCombatMission.lua", "veafcombatmission")
            operation.injectPluginScript("veaf", "src\\scripts\\veafCombatZone.lua", "veafcombatzone")
            operation.injectPluginScript("veaf", "src\\scripts\\veafGrass.lua", "veafgrass")
            operation.injectPluginScript("veaf", "src\\scripts\\veafInterpreter.lua", "veafinterpreter")
            operation.injectPluginScript("veaf", "src\\scripts\\veafMarkers.lua", "veafmarkers")
            operation.injectPluginScript("veaf", "src\\scripts\\veafMove.lua", "veafmove")
            operation.injectPluginScript("veaf", "src\\scripts\\veafNamedPoints.lua", "veafnamedpoints")
            operation.injectPluginScript("veaf", "src\\scripts\\veafRadio.lua", "veafradio")
            operation.injectPluginScript("veaf", "src\\scripts\\veafRemote.lua", "veafremote")
            operation.injectPluginScript("veaf", "src\\scripts\\veafSecurity.lua", "veafsecurity")
            operation.injectPluginScript("veaf", "src\\scripts\\veafShortcuts.lua", "veafshortcuts")
            operation.injectPluginScript("veaf", "src\\scripts\\veafSpawn.lua", "veafspawn")
            operation.injectPluginScript("veaf", "src\\scripts\\veafTransportMission.lua", "veaftransportmission")
            operation.injectPluginScript("veaf", "src\\scripts\\veafUnits.lua", "veafunits")


    def injectConfiguration(self, operation):
        if super().injectConfiguration(operation):
            operation.injectPluginScript("veaf", "src\\config\\missionConfig.lua", "veaf-config")

