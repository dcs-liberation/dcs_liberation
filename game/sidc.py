"""Implements Symbol Identification Codes (SIDCs) as defined by NATO APP-6(D).

This implementation only covers assembly of the identifier strings. The front-end is
responsible for drawing the icons.

The third ten digits (used for national modifications and additions not covered by
APP-6) are not implemented. The third set of ten digits are optional and will be omitted
from the output.

https://nso.nato.int/nso/nsdd/main/standards/ap-details/1912/EN
https://www.spatialillusions.com/milsymbol/docs/milsymbol-APP6d.html
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, unique

# Version field defined by A.5.
VERSION = 10


@unique
class Context(IntEnum):
    """Context field defined by A.6.."""

    REALITY = 0
    EXERCISE = 1
    SIMULATION = 2
    # 3-9 are reserved for future use.

    def __str__(self) -> str:
        return str(self.value)


@unique
class StandardIdentity(IntEnum):
    """Standard identity field defined by A.6."""

    PENDING = 0
    UNKNOWN = 1
    ASSUMED_FRIEND = 2
    FRIEND = 3
    NEUTRAL = 4
    SUSPECT_JOKER = 5
    HOSTILE_FAKER = 6
    # 7-9 are reserved for future use.

    def __str__(self) -> str:
        return str(self.value)


@unique
class SymbolSet(IntEnum):
    """Symbol set field defined by A.7."""

    UNKNOWN = 0
    AIR = 1
    AIR_MISSILE = 2
    SPACE = 5
    SPACE_MISSILE = 6
    LAND_UNIT = 10
    LAND_CIVILIAN_UNIT_ORGANIZATION = 11
    LAND_EQUIPMENT = 15
    LAND_INSTALLATIONS = 20
    CONTROL_MEASURE = 25
    DISMOUNTED_INDIVIDUAL = 27
    SEA_SURFACE = 30
    SEA_SUBSURFACE = 35
    MINE_WARFARE = 36
    ACTIVITY_EVENT = 40
    ATMOSPHERIC = 45
    OCEANOGRAPHIC = 46
    METEOROLOGICAL_SPACE = 47
    SIGNALS_INTELLIGENCE_SPACE = 50
    SIGNALS_INTELLIGENCE_AIR = 51
    SIGNALS_INTELLIGENCE_LAND = 52
    SIGNALS_INTELLIGENCE_SURFACE = 53
    SIGNALS_INTELLIGENCE_SUBSURFACE = 54
    CYBERSPACE_SPACE = 60
    CYBERSPACE_AIR = 61
    CYBERSPACE_LAND = 62
    CYBERSPACE_SURFACE = 63
    CYBERSPACE_SUBSURFACE = 64
    VERSION_EXTENSION_FLAG = 99
    # All other values reserved for future use.

    def __str__(self) -> str:
        return f"{self.value:02}"


@unique
class Status(IntEnum):
    """Status field defined by A.8 Status."""

    PRESENT = 0
    PLANNED_ANTICIPATED_SUSPECT = 1
    PRESENT_FULLY_CAPABLE = 2
    PRESENT_DAMAGED = 3
    PRESENT_DESTROYED = 4
    PRESENT_FULL_TO_CAPACITY = 5
    # 6-8 reserved for future use.
    VERSION_EXTENSION_FLAG = 9

    def __str__(self) -> str:
        return str(self.value)


@unique
class HeadquartersTaskForceDummy(IntEnum):
    """Headquarters/Task Force/Dummy field defined by A.9."""

    NOT_APPLICABLE = 0
    FEINT_DUMMY = 1
    HEADQUARTERS = 2
    FEINT_DUMMY_HEADQUARTERS = 3
    TASK_FORCE = 4
    FEINT_DUMMY_TASK_FORCE = 5
    TASK_FORCE_HEADQUARTERS = 6
    FEINT_DUMMY_TASK_FORCE_HEADQUARTERS = 7
    # 8 reserved for future use.
    VERSION_EXTENSION_FLAG = 9

    def __str__(self) -> str:
        return str(self.value)


@unique
class Amplifier(IntEnum):
    """Unit Echelon/Equipment Mobility/Naval Towed Array Amplifier defined by A.10"""

    UNKNOWN = 0

    # Echelon at brigade and below
    TEAM_CREW = 11
    SQUAD = 12
    SECTION = 13
    PLATOON_DETACHMENT = 14
    COMPANY_BATTERY_TROOP = 15
    BATTALION_SQUADRON = 16
    REGIMENT_GROUP = 17
    BRIGADE = 18
    VERSION_EXTENSION_FLAG = 19

    # Echelon at brigade and above
    DIVISION = 21
    CORP_MARINE_EXPEDITIONARY_FORCE = 22
    ARMY = 23
    ARMY_GROUP_FRONT = 24
    REGION_THEATRE = 25
    COMMAND = 26
    # 27-28 reserved for future use.
    VERSION_EXTENSION_FLAG2 = 29

    # Equipment mobility on land
    WHEELED_LIMITED_CROSS_COUNTRY = 31
    WHEELED_CROSS_COUNTRY = 32
    TRACKED = 33
    WHEELED_AND_TRAKCED_COMBINATION = 34
    TOWED = 35
    RAIL = 36
    PACK_ANIMALS = 37
    # 38 reserved for future use.
    VERSION_EXTENSION_FLAG3 = 39

    # Equipment mobility on snow
    OVER_SNOW = 41
    SLED = 42
    # 3-8 reserved for future use.
    VERSION_EXTENSION_FLAG4 = 49

    # Equipment mobility on water
    BARGE = 51
    AMPHIBIOUS = 52
    # 3-8 reserved for future use.
    VERSION_EXTENSION_FLAG5 = 59

    # Naval towed array
    SHORT_TOWED_ARRAY = 61
    LONG_TOWED_ARRAY = 62
    # 3-8 reserved for future use.
    VERSION_EXTENSION_FLAG6 = 69

    # Leadership indicator
    LEADER_INDIVIDUAL = 71
    DEPUTY_INDIVIDUAL = 72
    # 3-8 reserved for future use.
    VERSION_EXTENSION_FLAG7 = 79

    # 80-89 reserved for future use.
    # 90-99 version extension flag.

    def __str__(self) -> str:
        return f"{self.value:02}"


class Entity(IntEnum):
    def __str__(self) -> str:
        return f"{self.value:06}"


# Entity types (the second set of ten digits are implemented as-needed. These are
# defined by section A.13. Entity/Entity Type/Entity Subtype and Sector 1 and Sector 2
# Modifiers. The specific entity enum used by the SIDC depends on the symbol set used.
@unique
class AirEntity(Entity):
    """Air Entity/Entity Type/Entity Subtype defined by table A-10."""

    UNSPECIFIED = 0
    ATTACK_STRIKE = 110102
    BOMBER = 110103
    FIGHTER = 110104
    FIGHTER_BOMBER = 110105
    CARGO = 110107
    ELECTRONIC_COMBAT_JAMMER = 110108
    TANKER = 110109
    PATROL = 110110
    RECONNAISSANCE = 110111
    UTILITY = 110113
    VSTOL = 110114
    AIRBORNE_EARLY_WARNING = 110116
    ANTISURFACE_WARFARE = 110117
    ANTISUBMARINE_WARFARE = 110118
    COMBAT_SEARCH_AND_RESCUE = 110120
    SUPPRESSION_OF_ENEMY_AIR_DEFENCE = 110130
    ESCORT = 110132
    ELECTRONIC_ATTACK = 110133
    ROTARY_WING = 110200


@unique
class LandUnitEntity(Entity):
    """Land Unit Entity/Entity Type/Entity Subtype defined by table A-19."""

    UNSPECIFIED = 0

    ARMOR_ARMORED_MECHANIZED_SELF_PROPELLED_TRACKED = 120500
    AIR_DEFENSE = 130100
    MISSILE = 130700


@unique
class LandEquipmentEntity(Entity):
    """Land Equipment Entity/Entity Type/Entity Subtype defined by table A-25."""

    UNSPECIFIED = 0

    RADAR = 220300


@unique
class LandInstallationEntity(Entity):
    """Land Installation Entity/Entity Type/Entity Subtype defined by table A-27."""

    UNSPECIFIED = 0

    AMMUNITION_CACHE = 110300
    WAREHOUSE_STORAGE_FACILITY = 112000
    TENTED_CAMP = 111900
    GENERATION_STATION = 120502
    PETROLEUM_FACILITY = 120504
    MILITARY_BASE = 120802
    MILITARY_INFRASTRUCTURE = 120800
    PUBLIC_VENUES_INFRASTRUCTURE = 121000
    TELECOMMUNICATIONS_TOWER = 121203
    AIPORT_AIR_BASE = 121301
    HELICOPTER_LANDING_SITE = 121305
    MAINTENANCE_FACILITY = 121306


@unique
class SeaSurfaceEntity(Entity):
    """Sea Surface Entity/Entity Type/Entity Subtype defined by table A-34."""

    UNSPECIFIED = 0

    CARRIER = 120100
    SURFACE_COMBATANT_LINE = 120200
    AMPHIBIOUS_ASSAULT_SHIP_GENERAL = 120303


@unique
class UnknownEntity(Entity):
    """Fallback entity type used when the symbol set is not known."""

    UNSPECIFIED = 0


class Modifier(IntEnum):
    """Fallback modifier used when the symbol set is not known."""

    UNSPECIFIED = 0

    def __str__(self) -> str:
        return f"{self.value:02}"


@dataclass
class SymbolIdentificationCode:
    version = VERSION
    context: Context = Context.REALITY
    standard_identity: StandardIdentity = StandardIdentity.UNKNOWN
    symbol_set: SymbolSet = SymbolSet.UNKNOWN
    status: Status = Status.PRESENT
    headquarters_task_force_dummy: HeadquartersTaskForceDummy = (
        HeadquartersTaskForceDummy.NOT_APPLICABLE
    )
    amplifier: Amplifier = Amplifier.UNKNOWN
    entity: Entity = UnknownEntity.UNSPECIFIED
    sector_one_modifier = Modifier.UNSPECIFIED
    sector_two_modifier = Modifier.UNSPECIFIED

    def __str__(self) -> str:
        return "".join(
            [
                f"{self.version:02}",
                str(self.context),
                str(self.standard_identity),
                str(self.symbol_set),
                str(self.status),
                str(self.headquarters_task_force_dummy),
                str(self.amplifier),
                str(self.entity),
                str(self.sector_one_modifier),
                str(self.sector_two_modifier),
            ]
        )


class SidcDescribable(ABC):
    @property
    @abstractmethod
    def standard_identity(self) -> StandardIdentity:
        ...

    @property
    @abstractmethod
    def sidc_status(self) -> Status:
        ...

    @property
    @abstractmethod
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        ...

    def sidc(self) -> SymbolIdentificationCode:
        symbol_set, entity = self.symbol_set_and_entity
        return SymbolIdentificationCode(
            standard_identity=self.standard_identity,
            symbol_set=symbol_set,
            status=self.sidc_status,
            entity=entity,
        )
