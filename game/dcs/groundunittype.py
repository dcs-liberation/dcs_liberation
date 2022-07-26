from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Optional, Type

import yaml
from dcs.unittype import VehicleType
from dcs.vehicles import vehicle_map

from game.data.units import UnitClass
from game.dcs.unittype import UnitType


@dataclass
class SkynetProperties:
    can_engage_harm: Optional[str] = None
    can_engage_air_weapon: Optional[str] = None
    go_live_range_in_percent: Optional[str] = None
    engagement_zone: Optional[str] = None
    autonomous_behaviour: Optional[str] = None
    harm_detection_chance: Optional[str] = None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> SkynetProperties:
        props = SkynetProperties()
        if "can_engage_harm" in data:
            props.can_engage_harm = str(data["can_engage_harm"]).lower()
        if "can_engage_air_weapon" in data:
            props.can_engage_air_weapon = str(data["can_engage_air_weapon"]).lower()
        if "go_live_range_in_percent" in data:
            props.go_live_range_in_percent = str(data["go_live_range_in_percent"])
        if "engagement_zone" in data:
            props.engagement_zone = str(data["engagement_zone"])
        if "autonomous_behaviour" in data:
            props.autonomous_behaviour = str(data["autonomous_behaviour"])
        if "harm_detection_chance" in data:
            props.harm_detection_chance = str(data["harm_detection_chance"])
        return props

    def to_dict(self) -> dict[str, str]:
        properties: dict[str, str] = {}
        for key, value in self.__dict__.items():
            if value is not None:
                properties[key] = value
        return properties

    def __hash__(self) -> int:
        return hash(id(self))


@dataclass(frozen=True)
class GroundUnitType(UnitType[Type[VehicleType]]):
    spawn_weight: int
    skynet_properties: SkynetProperties

    # Defines if we should place the ground unit with an inverted heading.
    # Some units like few Launchers have to be placed backwards to be able to fire.
    reversed_heading: bool = False

    @classmethod
    def named(cls, name: str) -> GroundUnitType:
        if not cls._loaded:
            cls._load_all()
        unit = cls._by_name[name]
        assert isinstance(unit, GroundUnitType)
        return unit

    @classmethod
    def for_dcs_type(cls, dcs_unit_type: Type[VehicleType]) -> Iterator[GroundUnitType]:
        if not cls._loaded:
            cls._load_all()
        for unit in cls._by_unit_type[dcs_unit_type]:
            assert isinstance(unit, GroundUnitType)
            yield unit

    @staticmethod
    def each_dcs_type() -> Iterator[Type[VehicleType]]:
        yield from vehicle_map.values()

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
        if class_name is None:
            logging.warning(f"{vehicle.id} has no class")
            unit_class = UnitClass.UNKNOWN
        else:
            unit_class = UnitClass(class_name)

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
                skynet_properties=SkynetProperties.from_data(
                    data.get("skynet_properties", {})
                ),
                reversed_heading=data.get("reversed_heading", False),
            )
