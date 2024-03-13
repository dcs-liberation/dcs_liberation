from __future__ import annotations

import json
import logging
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.missiongenerator.luagenerator import LuaGenerator


class LuaPluginWorkOrder:
    """A script to be loaded at mision start.

    Typically, a work order is used for the main plugin script, and another for
    configuration. The main script is added to scriptsWorkOrders and the configuration
    to configurationWorkOrders. As far as I can tell, there's absolutely no difference
    between those two lists and that could be merged.

    Other scripts can also be run by being added to either of these lists.

    A better name for this is probably just "LuaPluginScript", since that appears to be
    all they are.
    """

    def __init__(
        self, parent_mnemonic: str, filename: str, mnemonic: str, disable: bool
    ) -> None:
        self.parent_mnemonic = parent_mnemonic
        self.filename = filename
        self.mnemonic = mnemonic
        self.disable = disable

    def work(self, lua_generator: LuaGenerator) -> None:
        """Inject the script for this work order into the mission, or ignores it."""
        if self.disable:
            lua_generator.bypass_plugin_script(self.mnemonic)
        else:
            lua_generator.inject_plugin_script(
                self.parent_mnemonic, self.filename, self.mnemonic
            )


class PluginSettings:
    """A common base for plugin configuration and per-plugin option configuration."""

    def __init__(self, identifier: str, enabled_by_default: bool) -> None:
        self.identifier = identifier
        self.enabled = enabled_by_default

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled


class LuaPluginOption(PluginSettings):
    """A boolean option for the plugin."""

    def __init__(self, identifier: str, name: str, enabled_by_default: bool) -> None:
        super().__init__(identifier, enabled_by_default)
        self.name = name


@dataclass(frozen=True)
class LuaPluginDefinition:
    """Object mapping for plugin.json."""

    identifier: str
    name: str
    present_in_ui: bool
    enabled_by_default: bool
    options: List[LuaPluginOption]
    work_orders: List[LuaPluginWorkOrder]
    config_work_orders: List[LuaPluginWorkOrder]

    @classmethod
    def from_json(cls, name: str, path: Path) -> LuaPluginDefinition:
        """Loads teh plugin definitions from the given plugin.json path."""
        data = json.loads(path.read_text())

        options = []
        for option in data.get("specificOptions"):
            option_id = option["mnemonic"]
            options.append(
                LuaPluginOption(
                    identifier=f"{name}.{option_id}",
                    name=option.get("nameInUI", name),
                    enabled_by_default=option.get("defaultValue"),
                )
            )

        work_orders = []
        for work_order in data.get("scriptsWorkOrders"):
            work_orders.append(
                LuaPluginWorkOrder(
                    name,
                    work_order.get("file"),
                    work_order["mnemonic"],
                    work_order.get("disable", False),
                )
            )
        config_work_orders = []
        for work_order in data.get("configurationWorkOrders"):
            config_work_orders.append(
                LuaPluginWorkOrder(
                    name,
                    work_order.get("file"),
                    work_order["mnemonic"],
                    work_order.get("disable", False),
                )
            )

        return cls(
            identifier=name,
            name=data["nameInUI"],
            present_in_ui=not data.get("skipUI", False),
            enabled_by_default=data.get("defaultValue", False),
            options=options,
            work_orders=work_orders,
            config_work_orders=config_work_orders,
        )


class LuaPlugin(PluginSettings):
    """A Liberation lua plugin.

    A plugin is a mod that is able to inject Lua code into the Liberation mission start
    up. Some of these are bundled (Skynet, mist, EWRS, etc), but users can add their own
    as well.

    A plugin is defined by a plugin.json file in resources/plugins/<name>/plugin.json.
    That file defines the name to be shown in the settings UI, whether it should be
    enabled by default, the scripts to run, and (optionally) boolean options for
    controlling plugin behavior.

    The plugin identifier is defined by the name of the directory containing it.

    Plugin options have their own set of default settings, UI names, and IDs.
    """

    def __init__(self, definition: LuaPluginDefinition) -> None:
        self.definition = definition
        super().__init__(self.definition.identifier, self.definition.enabled_by_default)

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def show_in_ui(self) -> bool:
        return self.definition.present_in_ui

    @property
    def options(self) -> List[LuaPluginOption]:
        return self.definition.options

    def is_option_enabled(self, identifier: str) -> bool:
        for option in self.options:
            if option.identifier == identifier:
                return option.enabled
        raise KeyError(f"Plugin {self.identifier} has no option {self.identifier}")

    @classmethod
    def from_json(cls, name: str, path: Path) -> Optional[LuaPlugin]:
        try:
            definition = LuaPluginDefinition.from_json(name, path)
        except KeyError:
            logging.exception("Required plugin configuration value missing")
            return None

        return cls(definition)

    def inject_scripts(self, lua_generator: LuaGenerator) -> None:
        """Injects the plugin's scripts into the mission."""
        for work_order in self.definition.work_orders:
            work_order.work(lua_generator)

    def inject_configuration(self, lua_generator: LuaGenerator) -> None:
        """Injects the plugin's options and configuration scripts into the mission.

        It's not clear why the script portion of this needs to exist, and could probably
        instead be the same as inject_scripts.
        """
        # inject the plugin options
        if self.options:
            option_decls = []
            for option in self.options:
                enabled = str(option.enabled).lower()
                name = option.identifier
                option_decls.append(f"    dcsLiberation.plugins.{name} = {enabled}")

            joined_options = "\n".join(option_decls)

            lua = textwrap.dedent(
                f"""\
                -- {self.identifier} plugin configuration.

                if dcsLiberation then
                    if not dcsLiberation.plugins then
                        dcsLiberation.plugins = {{}}
                    end
                    dcsLiberation.plugins.{self.identifier} = {{}}
                    {joined_options}
                end

            """
            )

            lua_generator.inject_lua_trigger(
                lua, f"{self.identifier} plugin configuration"
            )

        for work_order in self.definition.config_work_orders:
            work_order.work(lua_generator)

    def update_with(self, other: LuaPlugin) -> None:
        self.enabled = other.enabled
        for option in self.options:
            try:
                option.enabled = other.is_option_enabled(option.identifier)
            except KeyError:
                continue
