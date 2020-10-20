import logging
from dataclasses import dataclass
from typing import Optional

from dcs.planes import PlaneType, plane_map
from dcs.unittype import VehicleType, UnitType
from dcs.vehicles import vehicle_map, Armor, Unarmed, Infantry, Fortification, Artillery, AirDefence

from game.data.doctrine import Doctrine


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
        pass

    @classmethod
    def from_json(cls, json):

        faction = Faction()

        faction.country = json.get("country", "USA")
        faction.name = json.get("name", "???")

        faction.aircrafts = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("aircrafts", [])] is not None]
        faction.awacs = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("awacs", [])] is not None]
        faction.tankers = [f for f in [aircraft_loader(aircraft) for aircraft in json.get("tankers", [])] is not None]


def aircraft_loader(aircraft: str) -> Optional[PlaneType]:
    """
    Find aircraft by name
    :param aircraft: Aircraft name as string
    :return: The aircraft as a PyDCS type
    """
    if aircraft in plane_map.keys():
        return plane_map[aircraft]
    else:
        for mother_class in [PlaneType, Unarmed, Infantry, Armor, AirDefence, Artillery, Fortification]:
            if getattr(mother_class, vehicle) is not None:
                return getattr(mother_class, vehicle)
        logging.info("FACTION ERROR : Unable to find " + aircraft + " in pydcs")
        return None

def vehicle_loader(vehicle: str) -> Optional[VehicleType]:
    """
    Find vehicle by name
    :param vehicle: Vehicle name as string
    :return: The vehicle as a PyDCS type
    """
    if vehicle in plane_map.keys():
        return plane_map[vehicle]
    else:
        for mother_class in [Armor, Unarmed, Infantry, Armor, AirDefence, Artillery, Fortification]:
            if getattr(mother_class, vehicle) is not None:
                return getattr(mother_class, vehicle)
        logging.info("FACTION ERROR : Unable to find " + vehicle + " in pydcs")
        return None

vehicle_map






