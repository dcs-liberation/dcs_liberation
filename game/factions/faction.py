import logging
from dataclasses import dataclass
from typing import Optional

import dcs
from dcs.planes import PlaneType, plane_map
from dcs.unittype import VehicleType, UnitType
from dcs.vehicles import vehicle_map, Armor, Unarmed, Infantry, Fortification, Artillery, AirDefence

from game.data.doctrine import Doctrine, MODERN_DOCTRINE, COLDWAR_DOCTRINE, WWII_DOCTRINE


@dataclass
class Faction:

    # Country used by this faction
    country: str

    # Nice name of the faction
    name: str

    # Available aircraft
    aircrafts: [UnitType]

    # Available awacs aircraft
    awacs: [UnitType]

    # Available tanker aircraft
    tankers: [UnitType]

    # Available frontline units
    frontline_units: [VehicleType]

    # Available artillery units
    artillery_units: [VehicleType]

    # Infantry units used
    infantry_units: [VehicleType]

    # Logistics units used
    logistics_units: [VehicleType]

    # List of units that can be deployed as SHORAD
    shorad_units: [VehicleType]

    # Possible SAMS site generators for this faction
    sams: [str]

    # Required mods or asset packs
    requirements: {str: str}

    # Possible carrier names
    carrier_names: [str]

    # Possible helicopter carrier names
    lha_names: [str]

    # Navy group generators
    navy_generators: [str]

    # Available destroyers
    destroyers: [str]

    # Available cruisers
    cruisers: [str]

    # JTAC
    has_jtac: bool

    # Unit to use as JTAC
    jtac_unit: str

    # doctrine
    doctrine: Doctrine

    def __init__(self):
        self.country = ""
        self.name = ""
        self.aircrafts = []
        self.awacs = []
        self.tankers = []
        self.frontline_units = []
        self.artillery_units = []
        self.infantry_units = []
        self.logistics_units = []
        self.shorad_units = []
        self.sams = []
        self.requirements = {}
        self.carrier_names = []
        self.lha_names = []
        self.navy_generators = []
        self.destroyers = []
        self.cruisers = []
        self.has_jtac = False
        self.jtac_unit = ""
        self.doctrine = None

    @classmethod
    def from_json(cls, json):

        faction = Faction()

        faction.country = json.get("country", "USA")
        faction.name = json.get("name", "???")

        faction.aircrafts = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("aircrafts", [])] if f is not None]
        faction.awacs = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("awacs", [])] if f is not None]
        faction.tankers = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("tankers", [])] if f is not None]

        faction.frontline_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("frontline_units", [])] if f is not None]
        faction.artillery_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("artillery_units", [])] if f is not None]
        faction.infantry_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("infantry_units", [])] if f is not None]
        faction.logistics_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("logistics_units", [])] if f is not None]
        faction.shorad_units = [f for f in [vehicle_loader(vehicle) for vehicle in json.get("shorad_units", [])] if f is not None]

        faction.sams = json.get("sams", [])
        faction.name = json.get("requirements", {})

        faction.carrier_names = json.get("carrier_names", [])
        faction.lha_names = json.get("lha_names", [])
        faction.navy_generators = json.get("navy_generators", [])
        faction.destroyers = [f for f in [ship_loader(vehicle) for vehicle in json.get("destroyers", [])] if f is not None]
        faction.cruisers = [f for f in [ship_loader(vehicle) for vehicle in json.get("cruisers", [])] if f is not None]
        faction.has_jtac = json.get("has_jtac", False)
        faction.jtac_unit = json.get("jtac_unit", "")

        # Load doctrine
        doctrine = json.get("doctrine", "modern")
        if doctrine == "modern":
            faction.doctrine = MODERN_DOCTRINE
        if doctrine == "coldwar":
            faction.doctrine = COLDWAR_DOCTRINE
        else:
            faction.doctrine = WWII_DOCTRINE

        return faction

    @property
    def units(self):
        return self.infantry_units + self.aircrafts + self.awacs + self.artillery_units + self.frontline_units + self.tankers + self.logistics_units


def unit_loader(unit: str, class_repository:[]) -> Optional[PlaneType]:
    """
    Find unit by name
    :param unit: Unit name as string
    :return: The unit as a PyDCS type
    """
    if unit in plane_map.keys():
        return plane_map[unit]
    else:
        for mother_class in class_repository:
            if getattr(mother_class, unit, None) is not None:
                return getattr(mother_class, unit)
        logging.info("FACTION ERROR : Unable to find " + unit + " in pydcs")
        print("FACTION ERROR : Unable to find " + unit + " in pydcs")
        return None


aircraft_loader = lambda x: unit_loader(x, [dcs.planes, dcs.helicopters])
vehicle_loader = lambda x: unit_loader(x, [Infantry, Unarmed, Armor, AirDefence, Artillery])
ship_loader = lambda x: unit_loader(x, [dcs.ships])






