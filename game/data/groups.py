from __future__ import annotations

from enum import Enum


class GroupRole(Enum):
    """Role of a ForceGroup within the ArmedForces"""

    AIR_DEFENSE = "AntiAir"
    BUILDING = "Building"
    DEFENSES = "Defenses"
    GROUND_FORCE = "GroundForce"
    NAVAL = "Naval"

    @property
    def tasks(self) -> list[GroupTask]:
        return [task for task in GroupTask if task.role == self]


class GroupTask(Enum):
    """Specific Tasking of a ForceGroup"""

    def __init__(self, description: str, role: GroupRole):
        self.description = description
        self.role = role

    @classmethod
    def by_description(cls, description: str) -> GroupTask:
        for task in GroupTask:
            if task.description == description:
                return task
        raise RuntimeError(f"GroupTask with description {description} does not exist")

    # ANTI AIR
    AAA = ("AAA", GroupRole.AIR_DEFENSE)
    EARLY_WARNING_RADAR = ("EarlyWarningRadar", GroupRole.AIR_DEFENSE)
    LORAD = ("LORAD", GroupRole.AIR_DEFENSE)
    MERAD = ("MERAD", GroupRole.AIR_DEFENSE)
    SHORAD = ("SHORAD", GroupRole.AIR_DEFENSE)
    POINT_DEFENSE = ("PointDefense", GroupRole.AIR_DEFENSE)

    # NAVAL
    AIRCRAFT_CARRIER = ("AircraftCarrier", GroupRole.NAVAL)
    HELICOPTER_CARRIER = ("HelicopterCarrier", GroupRole.NAVAL)
    NAVY = ("Navy", GroupRole.NAVAL)

    # GROUND FORCES
    BASE_DEFENSE = ("BaseDefense", GroupRole.GROUND_FORCE)
    FRONT_LINE = ("FrontLine", GroupRole.GROUND_FORCE)

    # DEFENSES
    COASTAL = ("Coastal", GroupRole.DEFENSES)
    MISSILE = ("Missile", GroupRole.DEFENSES)

    # BUILDINGS
    ALLY_CAMP = ("AllyCamp", GroupRole.BUILDING)
    AMMO = ("Ammo", GroupRole.BUILDING)
    DERRICK = ("Derrick", GroupRole.BUILDING)
    FACTORY = ("Factory", GroupRole.BUILDING)
    FARP = ("Farp", GroupRole.BUILDING)
    FOB = ("FOB", GroupRole.BUILDING)
    FUEL = ("Fuel", GroupRole.BUILDING)
    OFFSHORE_STRIKE_TARGET = ("OffShoreStrikeTarget", GroupRole.BUILDING)
    OIL = ("Oil", GroupRole.BUILDING)

    STRIKE_TARGET = ("StrikeTarget", GroupRole.BUILDING)
    VILLAGE = ("Village", GroupRole.BUILDING)
    WARE = ("Ware", GroupRole.BUILDING)
    WW2_BUNKER = ("WW2Bunker", GroupRole.BUILDING)

    # IADS
    COMMS = ("Comms", GroupRole.BUILDING)
    COMMAND_CENTER = ("CommandCenter", GroupRole.BUILDING)
    POWER = ("Power", GroupRole.BUILDING)
