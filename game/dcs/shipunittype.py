from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Iterator, Type

import yaml
from dcs.ships import ship_map
from dcs.unittype import ShipType

from game.data.units import UnitClass
from game.dcs.unittype import UnitType


@dataclass(frozen=True)
class ShipUnitType(UnitType[Type[ShipType]]):
    _by_name: ClassVar[dict[str, ShipUnitType]] = {}
    _by_unit_type: ClassVar[dict[type[ShipType], list[ShipUnitType]]] = defaultdict(
        list
    )

    @classmethod
    def register(cls, unit_type: ShipUnitType) -> None:
        cls._by_name[unit_type.name] = unit_type
        cls._by_unit_type[unit_type.dcs_unit_type].append(unit_type)

    @classmethod
    def named(cls, name: str) -> ShipUnitType:
        if not cls._loaded:
            cls.load_all()
        return cls._by_name[name]

    @classmethod
    def for_dcs_type(cls, dcs_unit_type: Type[ShipType]) -> Iterator[ShipUnitType]:
        if not cls._loaded:
            cls.load_all()
        yield from cls._by_unit_type[dcs_unit_type]

    @staticmethod
    def each_dcs_type() -> Iterator[Type[ShipType]]:
        yield from ship_map.values()

    @classmethod
    def _each_variant_of(cls, ship: Type[ShipType]) -> Iterator[ShipUnitType]:
        data_path = Path("resources/units/ships") / f"{ship.id}.yaml"
        if not data_path.exists():
            logging.warning(f"No data for {ship.id}; it will not be available")
            return

        with data_path.open(encoding="utf-8") as data_file:
            data = yaml.safe_load(data_file)

        try:
            introduction = data["introduced"]
            if introduction is None:
                introduction = "N/A"
        except KeyError:
            introduction = "No data."

        class_name = data.get("class")
        unit_class = UnitClass(class_name)

        for variant in data.get("variants", [ship.id]):
            yield ShipUnitType(
                dcs_unit_type=ship,
                unit_class=unit_class,
                name=variant,
                description=data.get(
                    "description",
                    f"No data. <a href=\"https://google.com/search?q=DCS+{variant.replace(' ', '+')}\"><span style=\"color:#FFFFFF\">Google {variant}</span></a>",
                ),
                year_introduced=introduction,
                country_of_origin=data.get("origin", "No data."),
                manufacturer=data.get("manufacturer", "No data."),
                role=data.get("role", "No data."),
                price=data.get("price"),
            )
