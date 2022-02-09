from __future__ import annotations

import itertools
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Type, List, Any, Iterator, TYPE_CHECKING

import dcs
from dcs.countries import country_dict
from dcs.unittype import ShipType, UnitType

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
from game.data.groundunitclass import GroundUnitClass
from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType

if TYPE_CHECKING:
    from game.theater.start_generator import ModSettings


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
    aircrafts: List[AircraftType] = field(default_factory=list)

    # Available awacs aircraft
    awacs: List[AircraftType] = field(default_factory=list)

    # Available tanker aircraft
    tankers: List[AircraftType] = field(default_factory=list)

    # Available frontline units
    frontline_units: List[GroundUnitType] = field(default_factory=list)

    # Available artillery units
    artillery_units: List[GroundUnitType] = field(default_factory=list)

    # Infantry units used
    infantry_units: List[GroundUnitType] = field(default_factory=list)

    # Logistics units used
    logistics_units: List[GroundUnitType] = field(default_factory=list)

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
    aircraft_carrier: List[Type[ShipType]] = field(default_factory=list)

    # possible helicopter carrier units
    helicopter_carrier: List[Type[ShipType]] = field(default_factory=list)

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
    jtac_unit: Optional[AircraftType] = field(default=None)

    # doctrine
    doctrine: Doctrine = field(default=MODERN_DOCTRINE)

    # List of available buildings for this faction
    building_set: List[str] = field(default_factory=list)

    # List of default livery overrides
    liveries_overrides: Dict[AircraftType, List[str]] = field(default_factory=dict)

    #: Set to True if the faction should force the "Unrestricted satnav" option
    #: for the mission. This option enables GPS for capable aircraft regardless
    #: of the time period or operator. For example, the CJTF "countries" don't
    #: appear to have GPS capability, so they need this.
    #:
    #: Note that this option cannot be set per-side. If either faction needs it,
    #: both will use it.
    unrestricted_satnav: bool = False

    def has_access_to_unittype(self, unit_class: GroundUnitClass) -> bool:
        for vehicle in itertools.chain(self.frontline_units, self.artillery_units):
            if vehicle.unit_class is unit_class:
                return True
        return False

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

        faction.aircrafts = [AircraftType.named(n) for n in json.get("aircrafts", [])]
        faction.awacs = [AircraftType.named(n) for n in json.get("awacs", [])]
        faction.tankers = [AircraftType.named(n) for n in json.get("tankers", [])]

        faction.aircrafts = list(
            set(faction.aircrafts + faction.awacs + faction.tankers)
        )

        faction.frontline_units = [
            GroundUnitType.named(n) for n in json.get("frontline_units", [])
        ]
        faction.artillery_units = [
            GroundUnitType.named(n) for n in json.get("artillery_units", [])
        ]
        faction.infantry_units = [
            GroundUnitType.named(n) for n in json.get("infantry_units", [])
        ]
        faction.logistics_units = [
            GroundUnitType.named(n) for n in json.get("logistics_units", [])
        ]

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
            faction.jtac_unit = AircraftType.named(jtac_name)
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
        for name, livery in liveries_overrides.items():
            aircraft = AircraftType.named(name)
            faction.liveries_overrides[aircraft] = [s.lower() for s in livery]

        faction.unrestricted_satnav = json.get("unrestricted_satnav", False)

        return faction

    @property
    def ground_units(self) -> Iterator[GroundUnitType]:
        yield from self.artillery_units
        yield from self.frontline_units
        yield from self.logistics_units

    def infantry_with_class(
        self, unit_class: GroundUnitClass
    ) -> Iterator[GroundUnitType]:
        for unit in self.infantry_units:
            if unit.unit_class is unit_class:
                yield unit

    def apply_mod_settings(self, mod_settings: ModSettings) -> Faction:
        # aircraft
        if not mod_settings.a4_skyhawk:
            self.remove_aircraft("A-4E-C")
        if not mod_settings.eurofighter:
            self.remove_aircraft("Eurofighter")
        if not mod_settings.hercules:
            self.remove_aircraft("Hercules")
        if not mod_settings.f22_raptor:
            self.remove_aircraft("F-22A")
        if not mod_settings.f104_starfighter:
            self.remove_aircraft("VSN_F104G")
            self.remove_aircraft("VSN_F104S")
            self.remove_aircraft("VSN_F104S_AG")
        if not mod_settings.jas39_gripen:
            self.remove_aircraft("JAS39Gripen")
            self.remove_aircraft("JAS39Gripen_AG")
        if not mod_settings.rafale:
            self.remove_aircraft("Rafale_B")
            self.remove_aircraft("Rafale_C")
        if not mod_settings.su57_felon:
            self.remove_aircraft("Su-57")
        # frenchpack
        if not mod_settings.frenchpack:
            self.remove_vehicle("AMX10RCR")
            self.remove_vehicle("SEPAR")
            self.remove_vehicle("ERC")
            self.remove_vehicle("M120")
            self.remove_vehicle("AA20")
            self.remove_vehicle("TRM2000")
            self.remove_vehicle("TRM2000_Citerne")
            self.remove_vehicle("TRM2000_AA20")
            self.remove_vehicle("TRMMISTRAL")
            self.remove_vehicle("VABH")
            self.remove_vehicle("VAB_RADIO")
            self.remove_vehicle("VAB_50")
            self.remove_vehicle("VIB_VBR")
            self.remove_vehicle("VAB_HOT")
            self.remove_vehicle("VAB_MORTIER")
            self.remove_vehicle("VBL50")
            self.remove_vehicle("VBLANF1")
            self.remove_vehicle("VBL-radio")
            self.remove_vehicle("VBAE")
            self.remove_vehicle("VBAE_MMP")
            self.remove_vehicle("AMX-30B2")
            self.remove_vehicle("Tracma")
            self.remove_vehicle("JTACFP")
            self.remove_vehicle("SHERIDAN")
            self.remove_vehicle("Leclerc_XXI")
            self.remove_vehicle("Toyota_bleu")
            self.remove_vehicle("Toyota_vert")
            self.remove_vehicle("Toyota_desert")
            self.remove_vehicle("Kamikaze")
            self.remove_vehicle("AMX1375")
            self.remove_vehicle("AMX1390")
            self.remove_vehicle("VBCI")
            self.remove_vehicle("T62")
            self.remove_vehicle("T64BV")
            self.remove_vehicle("T72M")
            self.remove_vehicle("KORNET")
        # high digit sams
        if not mod_settings.high_digit_sams:
            self.remove_air_defenses("SA10BGenerator")
            self.remove_air_defenses("SA12Generator")
            self.remove_air_defenses("SA20Generator")
            self.remove_air_defenses("SA20BGenerator")
            self.remove_air_defenses("SA23Generator")
            self.remove_air_defenses("SA17Generator")
            self.remove_air_defenses("KS19Generator")
        return self

    def remove_aircraft(self, name: str) -> None:
        for i in self.aircrafts:
            if i.dcs_unit_type.id == name:
                self.aircrafts.remove(i)

    def remove_air_defenses(self, name: str) -> None:
        for i in self.air_defenses:
            if i == name:
                self.air_defenses.remove(i)

    def remove_vehicle(self, name: str) -> None:
        for i in self.frontline_units:
            if i.dcs_unit_type.id == name:
                self.frontline_units.remove(i)


def load_ship(name: str) -> Optional[Type[ShipType]]:
    if (ship := getattr(dcs.ships, name, None)) is not None:
        return ship
    logging.error(f"FACTION ERROR : Unable to find {name} in dcs.ships")
    return None


def load_all_ships(data: list[str]) -> List[Type[ShipType]]:
    items = []
    for name in data:
        item = load_ship(name)
        if item is not None:
            items.append(item)
    return items
