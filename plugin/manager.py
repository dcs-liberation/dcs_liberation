from .luaplugin import LuaPlugin
from typing import List
import glob
from pathlib import Path
import json
import logging


class LuaPluginManager():
    PLUGINS_RESOURCE_PATH = Path("resources/plugins")
    PLUGINS_LIST_FILENAME = "plugins.json"
    PLUGINS_JSON_FILENAME = "plugin.json"

    __plugins = None
    def __init__(self):
        if not LuaPluginManager.__plugins:
            LuaPluginManager.__plugins= []
            jsonFile:Path = Path(LuaPluginManager.PLUGINS_RESOURCE_PATH, LuaPluginManager.PLUGINS_LIST_FILENAME)
            if jsonFile.exists():
                logging.info(f"Reading plugins list from {jsonFile}")

                jsonData = json.loads(jsonFile.read_text())
                for plugin in jsonData:
                    jsonPluginFolder = Path(LuaPluginManager.PLUGINS_RESOURCE_PATH, plugin)
                    jsonPluginFile = Path(jsonPluginFolder, LuaPluginManager.PLUGINS_JSON_FILENAME)
                    if jsonPluginFile.exists():
                        logging.info(f"Reading plugin {plugin} from {jsonPluginFile}")
                        plugin = LuaPlugin(jsonPluginFile)
                        LuaPluginManager.__plugins.append(plugin)
                    else:
                        logging.error(f"Missing configuration file {jsonPluginFile} for plugin {plugin}")
            else:
                logging.error(f"Missing plugins list file {jsonFile}")

    def getPlugins(self):
        return LuaPluginManager.__plugins

    def getPlugin(self, pluginName):
        for plugin in LuaPluginManager.__plugins:
            if plugin.mnemonic == pluginName:
                return plugin
        
        return None