from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Type, Optional, ClassVar, Iterator

import yaml
from dcs.unittype import VehicleType
from dcs.vehicles import vehicle_map

from game.data.groundunitclass import GroundUnitClass
from game.dcs.unittype import UnitType


@dataclass(frozen=True)
class GroundUnitType(UnitType[Type[VehicleType]]):
    unit_class: Optional[GroundUnitClass]
    spawn_weight: int

    _by_name: ClassVar[dict[str, GroundUnitType]] = {}
    _by_unit_type: ClassVar[
        dict[Type[VehicleType], list[GroundUnitType]]
    ] = defaultdict(list)
    _loaded: ClassVar[bool] = False

    def __str__(self) -> str:
        return self.name

    @property
    def dcs_id(self) -> str:
        return self.dcs_unit_type.id

    @classmethod
    def register(cls, aircraft_type: GroundUnitType) -> None:
        cls._by_name[aircraft_type.name] = aircraft_type
        cls._by_unit_type[aircraft_type.dcs_unit_type].append(aircraft_type)

    @classmethod
    def named(cls, name: str) -> GroundUnitType:
        if not cls._loaded:
            cls._load_all()
        return cls._by_name[name]

    @classmethod
    def for_dcs_type(cls, dcs_unit_type: Type[VehicleType]) -> Iterator[GroundUnitType]:
        if not cls._loaded:
            cls._load_all()
        yield from cls._by_unit_type[dcs_unit_type]

    @staticmethod
    def _each_unit_type() -> Iterator[Type[VehicleType]]:
        yield from vehicle_map.values()

    @classmethod
    def _load_all(cls) -> None:
        for unit_type in cls._each_unit_type():
            for data in cls._each_variant_of(unit_type):
                cls.register(data)
        cls._loaded = True

    @classmethod
    def _each_variant_of(cls, vehicle: Type[VehicleType]) -> Iterator[GroundUnitType]:
        data_path = Path("resources/units/ground_units") / f"{vehicle.id}.yaml"
        if not data_path.exists():
            logging.warning(f"No data for {vehicle.id}; it will not be available")
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
        unit_class: Optional[GroundUnitClass] = None
        if class_name is not None:
            unit_class = GroundUnitClass(class_name)

        for variant in data.get("variants", [vehicle.id]):
            yield GroundUnitType(
                dcs_unit_type=vehicle,
                unit_class=unit_class,
                spawn_weight=data.get("spawn_weight", 0),
                name=variant,
                description=data.get(
                    "description",
                    f"No data. <a href=\"https://google.com/search?q=DCS+{variant.replace(' ', '+')}\"><span style=\"color:#FFFFFF\">Google {variant}</span></a>",
                ),
                year_introduced=introduction,
                country_of_origin=data.get("origin", "No data."),
                manufacturer=data.get("manufacturer", "No data."),
                role=data.get("role", "No data."),
                price=data.get("price", 1),
            )
