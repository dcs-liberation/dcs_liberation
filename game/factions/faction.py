from __future__ import annotations
from game.data.groundunitclass import GroundUnitClass

import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Type, List, Any, cast, Iterator

import dcs
from dcs.countries import country_dict
from dcs.planes import plane_map
from dcs.unittype import FlyingType, ShipType, VehicleType, UnitType
from dcs.vehicles import Armor, Unarmed, Infantry, Artillery, AirDefence

from game.data.building_data import (
    WW2_ALLIES_BUILDINGS,
    DEFAULT_AVAILABLE_BUILDINGS,
    WW2_GERMANY_BUILDINGS,
    WW2_FREE,
)
from game.data.doctrine import (
    Doctrine,
    MODERN_DOCTRINE,
    COLDWAR_DOCTRINE,
    WWII_DOCTRINE,
)
from pydcs_extensions.mod_units import MODDED_VEHICLES, MODDED_AIRPLANES


@dataclass
class Faction:
    #: List of locales to use when generating random names. If not set, Faker will
    #: choose the default locale.
    locales: Optional[List[str]]

    # Country used by this faction
    country: str = field(default="")

    # Nice name of the faction
    name: str = field(default="")

    # List of faction file authors
    authors: str = field(default="")

    # A description of the faction
    description: str = field(default="")

    # Available aircraft
    aircrafts: List[Type[FlyingType]] = field(default_factory=list)

    # Available awacs aircraft
    awacs: List[Type[FlyingType]] = field(default_factory=list)

    # Available tanker aircraft
    tankers: List[Type[FlyingType]] = field(default_factory=list)

    # Available frontline units
    frontline_units: List[Type[VehicleType]] = field(default_factory=list)

    # Available artillery units
    artillery_units: List[Type[VehicleType]] = field(default_factory=list)

    # Infantry units used
    infantry_units: List[Type[VehicleType]] = field(default_factory=list)

    # Logistics units used
    logistics_units: List[Type[VehicleType]] = field(default_factory=list)

    # Possible SAMS site generators for this faction
    air_defenses: List[str] = field(default_factory=list)

    # Possible EWR generators for this faction.
    ewrs: List[str] = field(default_factory=list)

    # Possible Missile site generators for this faction
    missiles: List[str] = field(default_factory=list)

    # Possible costal site generators for this faction
    coastal_defenses: List[str] = field(default_factory=list)

    # Required mods or asset packs
    requirements: Dict[str, str] = field(default_factory=dict)

    # possible aircraft carrier units
    aircraft_carrier: List[Type[UnitType]] = field(default_factory=list)

    # possible helicopter carrier units
    helicopter_carrier: List[Type[UnitType]] = field(default_factory=list)

    # Possible carrier names
    carrier_names: List[str] = field(default_factory=list)

    # Possible helicopter carrier names
    helicopter_carrier_names: List[str] = field(default_factory=list)

    # Navy group generators
    navy_generators: List[str] = field(default_factory=list)

    # Available destroyers
    destroyers: List[Type[ShipType]] = field(default_factory=list)

    # Available cruisers
    cruisers: List[Type[ShipType]] = field(default_factory=list)

    # How many navy group should we try to generate per CP on startup for this faction
    navy_group_count: int = field(default=1)

    # How many missiles group should we try to generate per CP on startup for this faction
    missiles_group_count: int = field(default=1)

    # How many coastal group should we try to generate per CP on startup for this faction
    coastal_group_count: int = field(default=1)

    # Whether this faction has JTAC access
    has_jtac: bool = field(default=False)

    # Unit to use as JTAC for this faction
    jtac_unit: Optional[Type[FlyingType]] = field(default=None)

    # doctrine
    doctrine: Doctrine = field(default=MODERN_DOCTRINE)

    # List of available buildings for this faction
    building_set: List[str] = field(default_factory=list)

    # List of default livery overrides
    liveries_overrides: Dict[Type[UnitType], List[str]] = field(default_factory=dict)

    #: Set to True if the faction should force the "Unrestricted satnav" option
    #: for the mission. This option enables GPS for capable aircraft regardless
    #: of the time period or operator. For example, the CJTF "countries" don't
    #: appear to have GPS capability, so they need this.
    #:
    #: Note that this option cannot be set per-side. If either faction needs it,
    #: both will use it.
    unrestricted_satnav: bool = False

    def has_access_to_unittype(self, unitclass: GroundUnitClass) -> bool:
        has_access = False
        for vehicle in unitclass.unit_list:
            if vehicle in self.frontline_units:
                return True
            if vehicle in self.artillery_units:
                return True

        return has_access

    @classmethod
    def from_json(cls: Type[Faction], json: Dict[str, Any]) -> Faction:
        faction = Faction(locales=json.get("locales"))

        faction.country = json.get("country", "/")
        if faction.country not in [c.name for c in country_dict.values()]:
            raise AssertionError(
                'Faction\'s country ("{}") is not a valid DCS country ID'.format(
                    faction.country
                )
            )

        faction.name = json.get("name", "")
        if not faction.name:
            raise AssertionError("Faction has no valid name")

        faction.authors = json.get("authors", "")
        faction.description = json.get("description", "")

        faction.aircrafts = load_all_aircraft(json.get("aircrafts", []))
        faction.awacs = load_all_aircraft(json.get("awacs", []))
        faction.tankers = load_all_aircraft(json.get("tankers", []))

        faction.aircrafts = list(set(faction.aircrafts + faction.awacs))

        faction.frontline_units = load_all_vehicles(json.get("frontline_units", []))
        faction.artillery_units = load_all_vehicles(json.get("artillery_units", []))
        faction.infantry_units = load_all_vehicles(json.get("infantry_units", []))
        faction.logistics_units = load_all_vehicles(json.get("logistics_units", []))

        faction.ewrs = json.get("ewrs", [])

        faction.air_defenses = json.get("air_defenses", [])
        # Compatibility for older factions. All air defenses now belong to a
        # single group and the generator decides what belongs where.
        faction.air_defenses.extend(json.get("sams", []))
        faction.air_defenses.extend(json.get("shorads", []))

        faction.missiles = json.get("missiles", [])
        faction.coastal_defenses = json.get("coastal_defenses", [])
        faction.requirements = json.get("requirements", {})

        faction.carrier_names = json.get("carrier_names", [])
        faction.helicopter_carrier_names = json.get("helicopter_carrier_names", [])
        faction.navy_generators = json.get("navy_generators", [])
        faction.aircraft_carrier = load_all_ships(json.get("aircraft_carrier", []))
        faction.helicopter_carrier = load_all_ships(json.get("helicopter_carrier", []))
        faction.destroyers = load_all_ships(json.get("destroyers", []))
        faction.cruisers = load_all_ships(json.get("cruisers", []))
        faction.has_jtac = json.get("has_jtac", False)
        jtac_name = json.get("jtac_unit", None)
        if jtac_name is not None:
            faction.jtac_unit = load_aircraft(jtac_name)
        else:
            faction.jtac_unit = None
        faction.navy_group_count = int(json.get("navy_group_count", 1))
        faction.missiles_group_count = int(json.get("missiles_group_count", 0))
        faction.coastal_group_count = int(json.get("coastal_group_count", 0))

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
        elif building_set == "ww2free":
            faction.building_set = WW2_FREE
        elif building_set == "ww2ally":
            faction.building_set = WW2_ALLIES_BUILDINGS
        elif building_set == "ww2germany":
            faction.building_set = WW2_GERMANY_BUILDINGS
        else:
            faction.building_set = DEFAULT_AVAILABLE_BUILDINGS

        # Load liveries override
        faction.liveries_overrides = {}
        liveries_overrides = json.get("liveries_overrides", {})
        for k, v in liveries_overrides.items():
            k = load_aircraft(k)
            if k is not None:
                faction.liveries_overrides[k] = [s.lower() for s in v]

        faction.unrestricted_satnav = json.get("unrestricted_satnav", False)

        return faction

    @property
    def all_units(self) -> List[Type[UnitType]]:
        return (
            self.infantry_units
            + self.aircrafts
            + self.awacs
            + self.artillery_units
            + self.frontline_units
            + self.tankers
            + self.logistics_units
        )

    @property
    def ground_units(self) -> Iterator[Type[VehicleType]]:
        yield from self.artillery_units
        yield from self.frontline_units
        yield from self.logistics_units


def unit_loader(unit: str, class_repository: List[Any]) -> Optional[Type[UnitType]]:
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
        logging.error(f"FACTION ERROR : Unable to find {unit} in pydcs")
        return None


def load_aircraft(name: str) -> Optional[Type[FlyingType]]:
    return cast(
        Optional[FlyingType],
        unit_loader(name, [dcs.planes, dcs.helicopters, MODDED_AIRPLANES]),
    )


def load_all_aircraft(data) -> List[Type[FlyingType]]:
    items = []
    for name in data:
        item = load_aircraft(name)
        if item is not None:
            items.append(item)
    return items


def load_vehicle(name: str) -> Optional[Type[VehicleType]]:
    return cast(
        Optional[FlyingType],
        unit_loader(
            name, [Infantry, Unarmed, Armor, AirDefence, Artillery, MODDED_VEHICLES]
        ),
    )


def load_all_vehicles(data) -> List[Type[VehicleType]]:
    items = []
    for name in data:
        item = load_vehicle(name)
        if item is not None:
            items.append(item)
    return items


def load_ship(name: str) -> Optional[Type[ShipType]]:
    return cast(Optional[FlyingType], unit_loader(name, [dcs.ships]))


def load_all_ships(data) -> List[Type[ShipType]]:
    items = []
    for name in data:
        item = load_ship(name)
        if item is not None:
            items.append(item)
    return items
