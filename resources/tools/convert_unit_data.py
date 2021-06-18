from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any
from typing import Type

import yaml
from dcs.unittype import VehicleType
from dcs.vehicles import Infantry, Unarmed, Armor, AirDefence, Artillery, vehicle_map

from game.data.groundunitclass import GroundUnitClass
from game.db import PRICES, INFANTRY, MANPADS
from game.factions.faction import unit_loader
from pydcs_extensions.mod_units import MODDED_VEHICLES

THIS_DIR = Path(__file__).resolve().parent
SRC_ROOT = THIS_DIR.parent.parent
UNIT_DATA_DIR = SRC_ROOT / "resources/units"
FACTIONS_DIR = SRC_ROOT / "resources/factions"


class Converter:
    def __init__(self) -> None:
        self.all_variants: set[str] = set()
        self.variant_map: dict[str, dict[str, str]] = {}
        self.unconverted: set[Type[VehicleType]] = set(
            k for k in PRICES if issubclass(k, VehicleType)
        )
        for infantry_type in set(INFANTRY + MANPADS):
            self.unconverted.add(infantry_type)
            PRICES[infantry_type] = 0
        self.name_to_vehicle_map = {v.name: v for v in vehicle_map.values()}

    @staticmethod
    def find_unit_id_for_faction_name(name: str) -> str:
        unit_type = unit_loader(
            name, [Infantry, Unarmed, Armor, AirDefence, Artillery, MODDED_VEHICLES]
        )
        if unit_type is None:
            raise KeyError(f"Found no unit named {name}")
        return unit_type.id

    def convert(self) -> None:
        data_path = UNIT_DATA_DIR / "unit_info_text.json"
        with data_path.open(encoding="utf-8") as unit_data_file:
            unit_data = json.load(unit_data_file)

        for unit_name, data in dict(unit_data).items():
            if self.convert_unit(unit_name, data):
                unit_data.pop(unit_name)

        with data_path.open("w", encoding="utf-8") as unit_data_file:
            json.dump(unit_data, unit_data_file, indent=2)

        for unconverted in self.unconverted:
            self.generate_basic_info(unconverted)

        for faction_path in FACTIONS_DIR.glob("*.json"):
            self.update_faction(faction_path)

    def update_faction(self, faction_path: Path) -> None:
        with faction_path.open() as faction_file:
            data = json.load(faction_file)

        self.update_vehicle_list(data, "frontline_units")
        self.update_vehicle_list(data, "artillery_units")
        self.update_vehicle_list(data, "infantry_units")
        self.update_vehicle_list(data, "logistics_units")

        with faction_path.open("w") as faction_file:
            json.dump(data, faction_file, indent=2)

    def new_name_for(self, old_name: str, country: str) -> str:
        if old_name in self.all_variants:
            return old_name
        vehicle_id = self.find_unit_id_for_faction_name(old_name)
        return self.variant_map[vehicle_id][country]

    def update_vehicle_list(self, data: dict[str, Any], field: str) -> None:
        if field not in data:
            return

        new_vehicles = []
        for vehicle in data[field]:
            new_vehicles.append(self.new_name_for(vehicle, data["country"]))
        data[field] = sorted(new_vehicles)

    def generate_basic_info(self, unit_type: Type[VehicleType]) -> None:
        self.all_variants.add(unit_type.id)
        output_path = UNIT_DATA_DIR / "ground_units" / f"{unit_type.id}.yaml"
        if output_path.exists():
            # Already have data for this, don't clobber it, but do register the
            # variant names.
            with output_path.open() as unit_info_file:
                data = yaml.safe_load(unit_info_file)
                self.all_variants.update(data["variants"].keys())
            return
        with output_path.open("w") as output_file:
            yaml.safe_dump(
                {
                    "price": PRICES[unit_type],
                    "variants": {unit_type.name: None},
                },
                output_file,
            )

        self.variant_map[unit_type.id] = defaultdict(lambda: unit_type.name)

    def convert_unit(
        self, pydcs_name: str, data: list[dict[str, dict[str, str]]]
    ) -> bool:
        if len(data) != 1:
            raise ValueError(f"Unexpected data format for {pydcs_name}")

        try:
            unit_type: Type[VehicleType] = vehicle_map[pydcs_name]
        except KeyError:
            # The data is probably using the name instead of the key. This has always
            # been absent in the game but we can probably find a vehicle with a matching
            # name.
            unit_type = self.name_to_vehicle_map[pydcs_name]

        try:
            self.unconverted.remove(unit_type)
        except KeyError as ex:
            raise KeyError(
                f"Could not find existing unconverted unit for {pydcs_name}"
            ) from ex

        variants_dict = data[0]
        default = variants_dict.pop("default")

        default_name = default["name"]
        self.all_variants.add(default_name)
        country_to_variant = defaultdict(lambda: default_name)

        variants = {default_name: {}}
        for country, variant_dict in variants_dict.items():
            variant_name = variant_dict["name"]
            self.all_variants.add(variant_name)
            country_to_variant[country] = variant_name
            variants[variant_name] = self.get_variant_data(variant_dict)

        output_dict: dict[str, Any] = {"variants": variants, "price": PRICES[unit_type]}
        output_dict.update(self.get_variant_data(default))

        for unit_class in GroundUnitClass:
            if unit_type in unit_class:
                output_dict["class"] = unit_class.class_name

        output_path = UNIT_DATA_DIR / "ground_units" / f"{unit_type.id}.yaml"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as output_file:
            yaml.safe_dump(output_dict, output_file)

        self.variant_map[unit_type.id] = country_to_variant
        return True

    @staticmethod
    def get_variant_data(variant: dict[str, Any]) -> dict[str, Any]:
        result = {}

        try:
            result["manufacturer"] = variant["manufacturer"]
        except KeyError:
            pass

        try:
            result["origin"] = variant["country-of-origin"]
        except KeyError:
            pass
        try:
            result["role"] = variant["role"]
        except KeyError:
            pass

        try:
            as_str = variant["year-of-variant-introduction"]
            if as_str == "N/A":
                result["introduced"] = None
            else:
                result["introduced"] = int(as_str)
        except KeyError:
            pass

        try:
            result["description"] = variant["text"]
        except KeyError:
            pass

        return result


if __name__ == "__main__":
    Converter().convert()
