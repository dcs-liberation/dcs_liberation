import json
import logging
from pathlib import Path
from typing import Dict, List

from game.settings import Settings

from .luaplugin import LuaPlugin


class LuaPluginManager:
    _plugins_loaded = False
    _plugins: Dict[str, LuaPlugin] = {}

    @classmethod
    def _load_plugins(cls) -> None:
        plugins_path = Path("resources/plugins")

        path = plugins_path / "plugins.json"
        if not path.exists():
            raise RuntimeError(f"{path} does not exist. Cannot continue.")

        logging.info(f"Reading plugins list from {path}")

        data = json.loads(path.read_text())
        for name in data:
            plugin_path = plugins_path / name / "plugin.json"
            if not plugin_path.exists():
                raise RuntimeError(
                    f"Invalid plugin configuration: required plugin {name} "
                    f"does not exist at {plugin_path}"
                )
            logging.info(f"Loading plugin {name} from {plugin_path}")
            plugin = LuaPlugin.from_json(name, plugin_path)
            if plugin is not None:
                cls._plugins[name] = plugin
        cls._plugins_loaded = True

    @classmethod
    def _get_plugins(cls) -> Dict[str, LuaPlugin]:
        if not cls._plugins_loaded:
            cls._load_plugins()
        return cls._plugins

    @classmethod
    def plugins(cls) -> List[LuaPlugin]:
        return list(cls._get_plugins().values())

    @classmethod
    def load_settings(cls, settings: Settings) -> None:
        for plugin in cls.plugins():
            plugin.set_settings(settings)
