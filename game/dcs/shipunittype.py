from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Iterator, Type, Any

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

    def __setstate__(self, state: dict[str, Any]) -> None:
        # Update any existing models with new data on load.
        updated = ShipUnitType.named(state["variant_id"])
        state.update(updated.__dict__)
        self.__dict__.update(state)

    @classmethod
    def register(cls, unit_type: ShipUnitType) -> None:
        cls._by_name[unit_type.variant_id] = unit_type
        cls._by_unit_type[unit_type.dcs_unit_type].append(unit_type)

    @classmethod
    def named(cls, name: str) -> ShipUnitType:
        if not cls._loaded:
            cls._load_all()
        return cls._by_name[name]

    @classmethod
    def for_dcs_type(cls, dcs_unit_type: Type[ShipType]) -> Iterator[ShipUnitType]:
        if not cls._loaded:
            cls._load_all()
        yield from cls._by_unit_type[dcs_unit_type]

    @staticmethod
    def each_dcs_type() -> Iterator[Type[ShipType]]:
        yield from ship_map.values()

    @classmethod
    def _data_directory(cls) -> Path:
        return Path("resources/units/ships")

    @classmethod
    def _variant_from_dict(
        cls, ship: Type[ShipType], variant_id: str, data: dict[str, Any]
    ) -> ShipUnitType:
        try:
            introduction = data["introduced"]
            if introduction is None:
                introduction = "N/A"
        except KeyError:
            introduction = "No data."

        class_name = data.get("class")
        unit_class = UnitClass(class_name)

        display_name = data.get("display_name", variant_id)
        return ShipUnitType(
            dcs_unit_type=ship,
            unit_class=unit_class,
            variant_id=variant_id,
            display_name=data.get("display_name", variant_id),
            description=data.get(
                "description",
                f"No data. <a href=\"https://google.com/search?q=DCS+{display_name.replace(' ', '+')}\"><span style=\"color:#FFFFFF\">Google {display_name}</span></a>",
            ),
            year_introduced=introduction,
            country_of_origin=data.get("origin", "No data."),
            manufacturer=data.get("manufacturer", "No data."),
            role=data.get("role", "No data."),
            price=data["price"],
            hit_points=data.get("hit_points", 1),
        )
