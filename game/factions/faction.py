from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Type, List, Any

import dcs
from dcs.countries import country_dict
from dcs.planes import PlaneType, plane_map
from dcs.unittype import VehicleType, UnitType
from dcs.vehicles import Armor, Unarmed, Infantry, Artillery, AirDefence

from game.data.building_data import WW2_ALLIES_BUILDINGS, DEFAULT_AVAILABLE_BUILDINGS, WW2_GERMANY_BUILDINGS
from game.data.doctrine import Doctrine, MODERN_DOCTRINE, COLDWAR_DOCTRINE, WWII_DOCTRINE
from pydcs_extensions.mod_units import MODDED_VEHICLES, MODDED_AIRPLANES


@dataclass
class Faction:

    # Country used by this faction
    country: str = field(default="")

    # Nice name of the faction
    name: str = field(default="")

    # List of faction file authors
    authors: str = field(default="")

    # A description of the faction
    description: str = field(default="")

    # Available aircraft
    aircrafts: List[UnitType] = field(default_factory=list)

    # Available awacs aircraft
    awacs: List[UnitType] = field(default_factory=list)

    # Available tanker aircraft
    tankers: List[UnitType] = field(default_factory=list)

    # Available frontline units
    frontline_units: List[VehicleType] = field(default_factory=list)

    # Available artillery units
    artillery_units: List[VehicleType] = field(default_factory=list)

    # Infantry units used
    infantry_units: List[VehicleType] = field(default_factory=list)

    # Logistics units used
    logistics_units: List[VehicleType] = field(default_factory=list)

    # List of units that can be deployed as SHORAD
    shorads: List[str] = field(default_factory=list)

    # Possible SAMS site generators for this faction
    sams: List[str] = field(default_factory=list)

    # Possible Missile site generators for this faction
    missiles: List[str] = field(default_factory=list)

    # Required mods or asset packs
    requirements: {str: str} = field(default_factory=dict)

    # possible aircraft carrier units
    aircraft_carrier: List[UnitType] = field(default_factory=list)

    # possible helicopter carrier units
    helicopter_carrier: List[UnitType] = field(default_factory=list)

    # Possible carrier names
    carrier_names: List[str] = field(default_factory=list)

    # Possible helicopter carrier names
    helicopter_carrier_names: List[str] = field(default_factory=list)

    # Navy group generators
    navy_generators: List[str] = field(default_factory=list)

    # Available destroyers
    destroyers: List[str] = field(default_factory=list)

    # Available cruisers
    cruisers: List[str] = field(default_factory=list)

    # How many navy group should we try to generate per CP on startup for this faction
    navy_group_count: int = field(default=1)

    # How many missiles group should we try to generate per CP on startup for this faction
    missiles_group_count: int = field(default=1)

    # Whether this faction has JTAC access
    has_jtac: bool = field(default=False)

    # Unit to use as JTAC for this faction
    jtac_unit: str = field(default="")

    # doctrine
    doctrine: Doctrine = field(default=MODERN_DOCTRINE)

    # List of available buildings for this faction
    building_set: List[str] = field(default_factory=list)


    @classmethod
    def from_json(cls: Type[Faction], json: Dict[str, any]) -> Faction:

        faction = Faction()

        faction.country = json.get("country", "/")
        if faction.country not in [c.name for c in country_dict.values()]:
            raise AssertionError("Faction's country (\"{}\") is not a valid DCS country ID".format(faction.country))

        faction.name = json.get("name", "")
        if not faction.name:
            raise AssertionError("Faction has no valid name")

        faction.authors = json.get("authors", "")
        faction.description = json.get("description", "")

        faction.aircrafts = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("aircrafts", [])] if f is not None]
        faction.awacs = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("awacs", [])] if f is not None]
        faction.tankers = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("tankers", [])] if f is not None]

        faction.frontline_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("frontline_units", [])] if f is not None]
        faction.artillery_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("artillery_units", [])] if f is not None]
        faction.infantry_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("infantry_units", [])] if f is not None]
        faction.logistics_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("logistics_units", [])] if f is not None]

        faction.sams = json.get("sams", [])
        faction.shorads = json.get("shorads", [])
        faction.missiles = json.get("missiles", [])
        faction.requirements = json.get("requirements", {})

        faction.carrier_names = json.get("carrier_names", [])
        faction.helicopter_carrier_names = json.get("helicopter_carrier_names", [])
        faction.navy_generators = json.get("navy_generators", [])
        faction.aircraft_carrier = [f for f in [ship_loader(vehicle) for vehicle in json.get("aircraft_carrier", [])] if f is not None]
        faction.helicopter_carrier = [f for f in [ship_loader(vehicle) for vehicle in json.get("helicopter_carrier", [])] if f is not None]
        faction.destroyers = [f for f in [ship_loader(vehicle) for vehicle in json.get("destroyers", [])] if f is not None]
        faction.cruisers = [f for f in [ship_loader(vehicle) for vehicle in json.get("cruisers", [])] if f is not None]
        faction.has_jtac = json.get("has_jtac", False)
        faction.jtac_unit = aircraft_loader(json.get("jtac_unit", None))
        faction.navy_group_count = int(json.get("navy_group_count", 1))
        faction.missiles_group_count = int(json.get("missiles_group_count", 0))

        # Load doctrine
        doctrine = json.get("doctrine", "modern")
        if doctrine == "modern":
            faction.doctrine = MODERN_DOCTRINE
        elif doctrine == "coldwar":
            faction.doctrine = COLDWAR_DOCTRINE
        elif doctrine == "ww2":
            faction.doctrine = WWII_DOCTRINE
        else:
            faction.doctrine = MODERN_DOCTRINE

        # Load the building set
        building_set = json.get("building_set", "default")
        if building_set == "default":
            faction.building_set = DEFAULT_AVAILABLE_BUILDINGS
        elif building_set == "ww2ally":
            faction.building_set = WW2_ALLIES_BUILDINGS
        elif building_set == "ww2germany":
            faction.building_set = WW2_GERMANY_BUILDINGS
        else:
            faction.building_set = DEFAULT_AVAILABLE_BUILDINGS

        return faction

    @property
    def units(self) -> List[UnitType]:
        return self.infantry_units + self.aircrafts + self.awacs + self.artillery_units + self.frontline_units + self.tankers + self.logistics_units


def unit_loader(unit: str, class_repository: List[Any]) -> Optional[PlaneType]:
    """
    Find unit by name
    :param unit: Unit name as string
    :param class_repository: Repository of classes (Either a module, a class, or a list of classes)
    :return: The unit as a PyDCS type
    """
    if unit is None:
        return None
    elif unit in plane_map.keys():
        return plane_map[unit]
    else:
        for mother_class in class_repository:
            if getattr(mother_class, unit, None) is not None:
                return getattr(mother_class, unit)
            if type(mother_class) is list:
                for m in mother_class:
                    if m.__name__ == unit:
                        return m
        logging.info("FACTION ERROR : Unable to find " + unit + " in pydcs")
        return None


aircraft_loader = lambda x: unit_loader(x, [dcs.planes, dcs.helicopters, MODDED_AIRPLANES])
vehicle_loader = lambda x: unit_loader(x, [Infantry, Unarmed, Armor, AirDefence, Artillery, MODDED_VEHICLES])
ship_loader = lambda x: unit_loader(x, [dcs.ships])






