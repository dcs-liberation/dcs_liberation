from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any, Iterator, ClassVar

import yaml
from dcs.unittype import StaticType

from game import db
from game.data.unitclass import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from gen.templates import GroundObjectTemplate


@dataclass(frozen=True)
class UnitSet:
    name: str
    ground_units: list[GroundUnitType]
    ship_units: list[ShipUnitType]
    statics: list[str]
    unit_class: Optional[UnitClass]
    templates: list[GroundObjectTemplate]

    _by_name: ClassVar[dict[str, UnitSet]] = {}
    _by_class: ClassVar[dict[UnitClass, list[UnitSet]]] = {}
    _loaded: bool = False

    def __str__(self) -> str:
        return self.name

    @classmethod
    def named(cls, name: str) -> UnitSet:
        if not cls._loaded:
            cls._load_all()
        return cls._by_name[name]

    @classmethod
    def _load_all(cls) -> None:
        for file in Path("resources/units/sets").glob("*.yaml"):
            if not file.is_file():
                continue

            with file.open(encoding="utf-8") as data_file:
                data = yaml.safe_load(data_file)

            unit_class = UnitClass(data.get("class"))

            ground_units = [
                GroundUnitType.named(n) for n in data.get("ground_units", [])
            ]
            ship_units = [ShipUnitType.named(n) for n in data.get("ship_units", [])]

            # TODO Add support for "variants" of the Set. Like with the S-300 family

            unit_set = UnitSet(
                name=data.get("name"),
                ground_units=ground_units,
                ship_units=ship_units,
                statics=data.get("statics", []),
                unit_class=unit_class,
                templates=data.get("templates", []),
            )

            cls._by_name[unit_set.name] = unit_set
            if unit_class in cls._by_class:
                cls._by_class[unit_class].append(unit_set)
            else:
                cls._by_class[unit_class] = [unit_set]

        cls._loaded = True
