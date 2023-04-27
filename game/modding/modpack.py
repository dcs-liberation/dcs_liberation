from __future__ import annotations

import importlib.util
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from game.dcs.aircrafttype import AircraftType


@dataclass(frozen=True)
class ModPack:
    path: Path
    identifier: str
    name: str
    url: str | None

    @staticmethod
    def load(path: Path) -> ModPack:
        descriptor = path / "mod.yaml"
        with descriptor.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return ModPack(path, data["id"], data["name"], data.get("url"))

    def inject(self) -> None:
        logging.info("Loading mod %s from %s", self.name, self.path)
        self._inject_each_aircraft()
        # TODO: Squadrons, loadouts, ground units, weapons, plugins

    def _inject_each_aircraft(self) -> None:
        aircraft_mod_dir = self.path / "aircraft"
        if not aircraft_mod_dir.exists():
            return
        for aircraft_dir in aircraft_mod_dir.iterdir():
            self._inject_aircraft(aircraft_dir)

    def _inject_aircraft(self, path: Path) -> None:
        for python_file in path.glob("*.py"):
            logging.debug("Importing Python code from %s: %s", self.name, python_file)
            name = f"liberationmods.{self.identifier}.{path.stem}"
            spec = importlib.util.spec_from_file_location(name, python_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)

        for yaml_file in path.glob("*.yaml"):
            AircraftType.register_from_file(yaml_file)
