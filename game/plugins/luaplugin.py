from __future__ import annotations

import json
import logging
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

from game.settings import Settings

if TYPE_CHECKING:
    from game.missiongenerator.luagenerator import LuaGenerator


class LuaPluginWorkOrder:
    def __init__(
        self, parent_mnemonic: str, filename: str, mnemonic: str, disable: bool
    ) -> None:
        self.parent_mnemonic = parent_mnemonic
        self.filename = filename
        self.mnemonic = mnemonic
        self.disable = disable

    def work(self, lua_generator: LuaGenerator) -> None:
        if self.disable:
            lua_generator.bypass_plugin_script(self.mnemonic)
        else:
            lua_generator.inject_plugin_script(
                self.parent_mnemonic, self.filename, self.mnemonic
            )


class PluginSettings:
    def __init__(self, identifier: str, enabled_by_default: bool) -> None:
        self.identifier = identifier
        self.enabled_by_default = enabled_by_default
        self.settings = Settings()
        self.initialize_settings()

    def set_settings(self, settings: Settings) -> None:
        self.settings = settings
        self.initialize_settings()

    def initialize_settings(self) -> None:
        # Plugin options are saved in the game's Settings, but it's possible for
        # plugins to change across loads. If new plugins are added or new
        # options added to those plugins, initialize the new settings.
        self.settings.initialize_plugin_option(self.identifier, self.enabled_by_default)

    @property
    def enabled(self) -> bool:
        return self.settings.plugin_option(self.identifier)

    def set_enabled(self, enabled: bool) -> None:
        self.settings.set_plugin_option(self.identifier, enabled)


class LuaPluginOption(PluginSettings):
    def __init__(self, identifier: str, name: str, enabled_by_default: bool) -> None:
        super().__init__(identifier, enabled_by_default)
        self.name = name


@dataclass(frozen=True)
class LuaPluginDefinition:
    identifier: str
    name: str
    present_in_ui: bool
    enabled_by_default: bool
    options: List[LuaPluginOption]
    work_orders: List[LuaPluginWorkOrder]
    config_work_orders: List[LuaPluginWorkOrder]

    @classmethod
    def from_json(cls, name: str, path: Path) -> LuaPluginDefinition:
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

    @classmethod
    def from_json(cls, name: str, path: Path) -> Optional[LuaPlugin]:
        try:
            definition = LuaPluginDefinition.from_json(name, path)
        except KeyError:
            logging.exception("Required plugin configuration value missing")
            return None

        return cls(definition)

    def set_settings(self, settings: Settings) -> None:
        super().set_settings(settings)
        for option in self.definition.options:
            option.set_settings(self.settings)

    def inject_scripts(self, lua_generator: LuaGenerator) -> None:
        for work_order in self.definition.work_orders:
            work_order.work(lua_generator)

    def inject_configuration(self, lua_generator: LuaGenerator) -> None:
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
