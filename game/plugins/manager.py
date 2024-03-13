from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml

from game.persistence.paths import liberation_user_dir
from .luaplugin import LuaPlugin


class LuaPluginManager:
    """Manages available and loaded lua plugins."""

    def __init__(self, plugins: dict[str, LuaPlugin]) -> None:
        self._plugins: dict[str, LuaPlugin] = plugins

    @staticmethod
    def load() -> LuaPluginManager:
        plugins_path = Path("resources/plugins")

        path = plugins_path / "plugins.json"
        if not path.exists():
            raise RuntimeError(f"{path} does not exist. Cannot continue.")

        logging.info(f"Reading plugins list from {path}")

        plugins = {}
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
                plugins[name] = plugin
        return LuaPluginManager(plugins)

    def update_with(self, other: LuaPluginManager) -> None:
        """Updates all setting values with those in the given plugin manager.

        When a game is loaded, LuaPluginManager.load() is called to load the latest set
        of plugins and settings. This is called with the plugin manager that was saved
        to the Game object to preserve any options that were set, and then the Game is
        updated with this manager.

        This needs to happen because the set of available plugins (or their options) can
        change between runs.
        """
        for plugin in self.iter_plugins():
            try:
                old_plugin = other.by_id(plugin.identifier)
            except KeyError:
                continue
            plugin.update_with(old_plugin)

    def iter_plugins(self) -> Iterator[LuaPlugin]:
        yield from self._plugins.values()

    def by_id(self, identifier: str) -> LuaPlugin:
        return self._plugins[identifier]

    def is_plugin_enabled(self, plugin_id: str) -> bool:
        try:
            return self.by_id(plugin_id).enabled
        except KeyError:
            return False

    def is_option_enabled(self, plugin_id: str, option_id: str) -> bool:
        try:
            return self.by_id(plugin_id).is_option_enabled(option_id)
        except KeyError:
            return False

    def save_player_settings(self) -> None:
        """Saves the player's global settings to the user directory."""
        settings: dict[str, dict[str, Any]] = {}
        for plugin in self.iter_plugins():
            if not plugin.show_in_ui:
                continue

            plugin_settings: dict[str, Any] = {"enabled": plugin.enabled}
            if plugin.options:
                plugin_settings["options"] = {}
            settings[plugin.identifier] = plugin_settings
            for option in plugin.options:
                plugin_settings["options"][option.identifier] = option.enabled

        with self._player_settings_file.open("w", encoding="utf-8") as settings_file:
            yaml.dump(settings, settings_file, sort_keys=False, explicit_start=True)

    def merge_player_settings(self) -> None:
        """Updates with the player's global settings."""
        settings_path = self._player_settings_file
        if not settings_path.exists():
            return
        with settings_path.open(encoding="utf-8") as settings_file:
            data = yaml.safe_load(settings_file)

        for plugin_id, plugin_data in data.items():
            try:
                plugin = self.by_id(plugin_id)
            except KeyError:
                logging.warning(
                    "Unexpected plugin ID found in %s: %s. Ignoring.",
                    settings_path,
                    plugin_id,
                )
                continue

            plugin.enabled = plugin_data["enabled"]
            for option in plugin.options:
                try:
                    option.enabled = plugin_data["options"][option.identifier]
                except KeyError:
                    pass

    @property
    def _player_settings_file(self) -> Path:
        """Returns the path to the player's global settings file."""
        return liberation_user_dir() / "plugins.yaml"
