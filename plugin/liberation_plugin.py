from .base_plugin import BasePlugin

class LiberationPlugin(BasePlugin):
    nameInUI:str = "Liberation script"
    nameInSettings:str = "plugin.liberation"
    enabledDefaultValue:bool = True

    def setupUI(self, settingsWindow, row:int):
        # Don't setup any UI, this plugin is mandatory
        pass
    
    def injectScripts(self, operation):
        if super().injectScripts(operation):
            operation.injectPluginScript("base", "mist_4_3_74.lua", "mist")
            operation.injectPluginScript("base", "json.lua", "json")
            operation.injectPluginScript("base", "dcs_liberation.lua", "liberation")

    def injectConfiguration(self, operation):
        if super().injectConfiguration(operation):
            pass
