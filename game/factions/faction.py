from __future__ import annotations

import itertools
import logging
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Dict, Type, List, Any, Iterator, TYPE_CHECKING

import dcs
from dcs.countries import country_dict
from dcs.unittype import ShipType, StaticType
from dcs.unittype import UnitType as DcsUnitType

from game.data.building_data import (
    WW2_ALLIES_BUILDINGS,
    DEFAULT_AVAILABLE_BUILDINGS,
    WW2_GERMANY_BUILDINGS,
    WW2_FREE,
    REQUIRED_BUILDINGS,
    IADS_BUILDINGS,
)
from game.data.doctrine import (
    Doctrine,
    MODERN_DOCTRINE,
    COLDWAR_DOCTRINE,
    WWII_DOCTRINE,
)
from game.data.units import UnitClass
from game.data.groups import GroupRole
from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.armedforces.forcegroup import ForceGroup
from game.dcs.unittype import UnitType

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

    # Possible Air Defence units, Like EWRs
    air_defense_units: List[GroundUnitType] = field(default_factory=list)

    # A list of all supported sets of units
    preset_groups: list[ForceGroup] = field(default_factory=list)

    # Possible Missile site generators for this faction
    missiles: List[GroundUnitType] = field(default_factory=list)

    # Required mods or asset packs
    requirements: Dict[str, str] = field(default_factory=dict)

    # Possible carrier names
    carrier_names: List[str] = field(default_factory=list)

    # Possible helicopter carrier names
    helicopter_carrier_names: List[str] = field(default_factory=list)

    # Available Naval Units
    naval_units: List[ShipUnitType] = field(default_factory=list)

    # Whether this faction has JTAC access
    has_jtac: bool = field(default=False)

    # Unit to use as JTAC for this faction
    jtac_unit: Optional[AircraftType] = field(default=None)

    # doctrine
    doctrine: Doctrine = field(default=MODERN_DOCTRINE)

    # List of available building layouts for this faction
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

    def has_access_to_dcs_type(self, unit_type: Type[DcsUnitType]) -> bool:
        # Vehicle and Ship Units
        if any(unit_type == u.dcs_unit_type for u in self.accessible_units):
            return True

        # Statics
        if issubclass(unit_type, StaticType):
            # TODO Improve the statics checking
            # We currently do not have any list or similar to check if a faction has
            # access to a specific static. There we accept any static here
            return True
        return False

    def has_access_to_unit_class(self, unit_class: UnitClass) -> bool:
        return any(unit.unit_class is unit_class for unit in self.accessible_units)

    @cached_property
    def accessible_units(self) -> list[UnitType[Any]]:
        all_units: Iterator[UnitType[Any]] = itertools.chain(
            self.ground_units,
            self.infantry_units,
            self.air_defense_units,
            self.naval_units,
            self.missiles,
            (
                unit
                for preset_group in self.preset_groups
                for unit in preset_group.units
            ),
        )
        return list(set(all_units))

    @property
    def air_defenses(self) -> list[str]:
        """Returns the Air Defense types"""
        # This is used for the faction overview in NewGameWizard
        air_defenses = [a.name for a in self.air_defense_units]
        air_defenses.extend(
            [
                pg.name
                for pg in self.preset_groups
                if any(task.role == GroupRole.AIR_DEFENSE for task in pg.tasks)
            ]
        )
        return sorted(air_defenses)

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
        faction.air_defense_units = [
            GroundUnitType.named(n) for n in json.get("air_defense_units", [])
        ]
        faction.missiles = [GroundUnitType.named(n) for n in json.get("missiles", [])]

        faction.naval_units = [
            ShipUnitType.named(n) for n in json.get("naval_units", [])
        ]

        faction.preset_groups = [
            ForceGroup.from_preset_group(g) for g in json.get("preset_groups", [])
        ]

        faction.requirements = json.get("requirements", {})

        faction.carrier_names = json.get("carrier_names", [])
        faction.helicopter_carrier_names = json.get("helicopter_carrier_names", [])

        faction.has_jtac = json.get("has_jtac", False)
        jtac_name = json.get("jtac_unit", None)
        if jtac_name is not None:
            faction.jtac_unit = AircraftType.named(jtac_name)
        else:
            faction.jtac_unit = None

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
        faction.building_set = []
        building_set = json.get("building_set", "default")
        if building_set == "default":
            faction.building_set.extend(DEFAULT_AVAILABLE_BUILDINGS)
        elif building_set == "ww2free":
            faction.building_set.extend(WW2_FREE)
        elif building_set == "ww2ally":
            faction.building_set.extend(WW2_ALLIES_BUILDINGS)
        elif building_set == "ww2germany":
            faction.building_set.extend(WW2_GERMANY_BUILDINGS)
        else:
            faction.building_set.extend(DEFAULT_AVAILABLE_BUILDINGS)

        # Add required buildings for the game logic (e.g. ammo, factory..)
        faction.building_set.extend(REQUIRED_BUILDINGS)
        faction.building_set.extend(IADS_BUILDINGS)

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

    def infantry_with_class(self, unit_class: UnitClass) -> Iterator[GroundUnitType]:
        for unit in self.infantry_units:
            if unit.unit_class is unit_class:
                yield unit

    def apply_mod_settings(self, mod_settings: ModSettings) -> None:
        # aircraft
        if not mod_settings.a4_skyhawk:
            self.remove_aircraft("A-4E-C")
        if not mod_settings.hercules:
            self.remove_aircraft("Hercules")
        if not mod_settings.uh_60l:
            self.remove_aircraft("UH-60L")
            self.remove_aircraft("KC130J")
        if not mod_settings.f22_raptor:
            self.remove_aircraft("F-22A")
        if not mod_settings.f104_starfighter:
            self.remove_aircraft("VSN_F104G")
            self.remove_aircraft("VSN_F104S")
            self.remove_aircraft("VSN_F104S_AG")
        if not mod_settings.jas39_gripen:
            self.remove_aircraft("JAS39Gripen")
            self.remove_aircraft("JAS39Gripen_AG")
        if not mod_settings.su57_felon:
            self.remove_aircraft("Su-57")
        if not mod_settings.ov10a_bronco:
            self.remove_aircraft("Bronco-OV-10A")
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
            self.remove_preset("SA-10B/S-300PS")
            self.remove_preset("SA-12/S-300V")
            self.remove_preset("SA-20/S-300PMU-1")
            self.remove_preset("SA-20B/S-300PMU-2")
            self.remove_preset("SA-23/S-300VM")
            self.remove_preset("SA-17")
            self.remove_preset("KS-19")
            self.remove_preset("HQ-2")
            self.remove_preset("SA-2/S-75 V-759/5V23")
            self.remove_preset("SA-3/S-125 V-601P/5V27")
            self.remove_vehicle("SAM SA-14 Strela-3 manpad")
            self.remove_vehicle("SAM SA-24 Igla-S manpad")
            self.remove_vehicle("Polyana-D4M1 C2 node")

    def remove_aircraft(self, name: str) -> None:
        for i in self.aircrafts:
            if i.dcs_unit_type.id == name:
                self.aircrafts.remove(i)

    def remove_preset(self, name: str) -> None:
        for pg in self.preset_groups:
            if pg.name == name:
                self.preset_groups.remove(pg)

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
