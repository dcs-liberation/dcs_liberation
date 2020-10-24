import json
from pathlib import Path
from typing import List, Optional

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QCheckBox, QGridLayout, QGroupBox, QLabel


class LuaPluginWorkOrder:

    def __init__(self, parent, filename: str, mnemonic: str,
                 disable: bool) -> None:
        self.filename = filename
        self.mnemonic = mnemonic
        self.disable = disable
        self.parent = parent
    
    def work(self, operation):
        if self.disable:
            operation.bypass_plugin_script(self.mnemonic)
        else:
            operation.inject_plugin_script(self.parent.mnemonic, self.filename,
                                           self.mnemonic)

class LuaPluginSpecificOption:

    def __init__(self, parent, mnemonic: str, nameInUI: str,
                 defaultValue: bool) -> None:
        self.mnemonic = mnemonic
        self.nameInUI = nameInUI
        self.defaultValue = defaultValue
        self.parent = parent

class LuaPlugin:
    NAME_IN_SETTINGS_BASE:str = "plugins."

    def __init__(self, jsonFilename: str) -> None:
        self.mnemonic: Optional[str] = None
        self.skipUI: bool = False
        self.nameInUI: Optional[str] = None
        self.nameInSettings: Optional[str] = None
        self.defaultValue: bool = False
        self.specificOptions: List[LuaPluginSpecificOption] = []
        self.scriptsWorkOrders: List[LuaPluginWorkOrder] = []
        self.configurationWorkOrders: List[LuaPluginWorkOrder] = []
        self.initFromJson(jsonFilename)
        self.enabled = self.defaultValue
        self.settings = None

    def initFromJson(self, jsonFilename:str):
        jsonFile:Path = Path(jsonFilename)
        if jsonFile.exists():
            jsonData = json.loads(jsonFile.read_text())
            self.mnemonic = jsonData.get("mnemonic") 
            self.skipUI = jsonData.get("skipUI", False)
            self.nameInUI = jsonData.get("nameInUI")
            assert self.mnemonic is not None
            self.nameInSettings = LuaPlugin.NAME_IN_SETTINGS_BASE + self.mnemonic
            self.defaultValue = jsonData.get("defaultValue", False)
            self.specificOptions = []
            for jsonSpecificOption in jsonData.get("specificOptions"):
                mnemonic = jsonSpecificOption.get("mnemonic")
                nameInUI = jsonSpecificOption.get("nameInUI", mnemonic)
                defaultValue = jsonSpecificOption.get("defaultValue")
                self.specificOptions.append(LuaPluginSpecificOption(self, mnemonic, nameInUI, defaultValue))
            self.scriptsWorkOrders = []
            for jsonWorkOrder in jsonData.get("scriptsWorkOrders"):
                file = jsonWorkOrder.get("file")
                mnemonic = jsonWorkOrder.get("mnemonic")
                disable = jsonWorkOrder.get("disable", False)                
                self.scriptsWorkOrders.append(LuaPluginWorkOrder(self, file, mnemonic, disable))
            self.configurationWorkOrders = []
            for jsonWorkOrder in jsonData.get("configurationWorkOrders"):
                file = jsonWorkOrder.get("file")
                mnemonic = jsonWorkOrder.get("mnemonic")
                disable = jsonWorkOrder.get("disable", False)                
                self.configurationWorkOrders.append(LuaPluginWorkOrder(self, file, mnemonic, disable))

    def setupUI(self, settingsWindow, row:int):
        # set the game settings 
        self.setSettings(settingsWindow.game.settings)

        if not self.skipUI:
            assert self.nameInSettings is not None
            assert self.settings is not None

            # create the plugin choice checkbox interface
            self.uiWidget: QCheckBox = QCheckBox()
            self.uiWidget.setChecked(self.isEnabled())
            self.uiWidget.toggled.connect(lambda: self.applySetting(settingsWindow))

            settingsWindow.pluginsGroupLayout.addWidget(QLabel(self.nameInUI), row, 0)
            settingsWindow.pluginsGroupLayout.addWidget(self.uiWidget, row, 1, Qt.AlignRight)

            # if needed, create the plugin options special page
            if settingsWindow.pluginsOptionsPageLayout and self.specificOptions != None:
                self.optionsGroup: QGroupBox = QGroupBox(self.nameInUI)
                optionsGroupLayout = QGridLayout();
                optionsGroupLayout.setAlignment(Qt.AlignTop)
                self.optionsGroup.setLayout(optionsGroupLayout)
                settingsWindow.pluginsOptionsPageLayout.addWidget(self.optionsGroup)

                # browse each option in the specific options list
                row = 0
                for specificOption in self.specificOptions:
                    assert specificOption.mnemonic is not None
                    nameInSettings = self.nameInSettings + "." + specificOption.mnemonic
                    if not nameInSettings in self.settings.plugins:
                        self.settings.plugins[nameInSettings] = specificOption.defaultValue

                    specificOption.uiWidget = QCheckBox()
                    specificOption.uiWidget.setChecked(self.settings.plugins[nameInSettings])
                    #specificOption.uiWidget.setEnabled(False)
                    specificOption.uiWidget.toggled.connect(lambda: self.applySetting(settingsWindow))

                    optionsGroupLayout.addWidget(QLabel(specificOption.nameInUI), row, 0)
                    optionsGroupLayout.addWidget(specificOption.uiWidget, row, 1, Qt.AlignRight)

                    row += 1

                # disable or enable the UI in the plugins special page
                self.enableOptionsGroup()

    def enableOptionsGroup(self):
        if self.optionsGroup:
            self.optionsGroup.setEnabled(self.isEnabled())

    def setSettings(self, settings):
        self.settings = settings

        # ensure the setting exist
        if not self.nameInSettings in self.settings.plugins:
            self.settings.plugins[self.nameInSettings] = self.defaultValue

        # do the same for each option in the specific options list
        for specificOption in self.specificOptions:
            nameInSettings = self.nameInSettings + "." + specificOption.mnemonic
            if not nameInSettings in self.settings.plugins:
                self.settings.plugins[nameInSettings] = specificOption.defaultValue

    def applySetting(self, settingsWindow):
        # apply the main setting
        self.settings.plugins[self.nameInSettings] = self.uiWidget.isChecked()
        self.enabled = self.settings.plugins[self.nameInSettings]
   
        # do the same for each option in the specific options list
        for specificOption in self.specificOptions:
            nameInSettings = self.nameInSettings + "." + specificOption.mnemonic              
            self.settings.plugins[nameInSettings] = specificOption.uiWidget.isChecked()
        
        # disable or enable the UI in the plugins special page
        self.enableOptionsGroup()

    def injectScripts(self, operation):
        # set the game settings 
        self.setSettings(operation.game.settings)

        # execute the work order
        if self.scriptsWorkOrders != None:
            for workOrder in self.scriptsWorkOrders:
                workOrder.work(operation)

        # serves for subclasses
        return self.isEnabled()

    def injectConfiguration(self, operation):
        # set the game settings 
        self.setSettings(operation.game.settings)

        # inject the plugin options
        if len(self.specificOptions) > 0:
            defineAllOptions = ""
            for specificOption in self.specificOptions:
                nameInSettings = self.nameInSettings + "." + specificOption.mnemonic
                value = "true" if self.settings.plugins[nameInSettings] else "false"
                defineAllOptions += f"    dcsLiberation.plugins.{self.mnemonic}.{specificOption.mnemonic} = {value} \n"
            
            
            lua  = f"-- {self.mnemonic} plugin configuration.\n"
            lua += "\n"
            lua += "if dcsLiberation then\n"
            lua += "    if not dcsLiberation.plugins then \n"
            lua += "        dcsLiberation.plugins = {}\n"
            lua += "    end\n"
            lua += f"    dcsLiberation.plugins.{self.mnemonic} = {{}}\n"
            lua += defineAllOptions
            lua += "end"
        
            operation.inject_lua_trigger(lua, f"{self.mnemonic} plugin configuration")

        # execute the work order
        if self.configurationWorkOrders != None:
            for workOrder in self.configurationWorkOrders:
                workOrder.work(operation)

        # serves for subclasses
        return self.isEnabled()

    def isEnabled(self) -> bool:
        if not self.settings:
            return False

        self.setSettings(self.settings) # create the necessary settings keys if needed

        return self.settings != None and self.settings.plugins[self.nameInSettings]

    def hasUI(self) -> bool:
        return not self.skipUI