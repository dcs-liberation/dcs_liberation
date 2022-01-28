from enum import Enum


class GroupRole(Enum):
    Unknow = "Unknown"
    AntiAir = "AntiAir"
    Building = "Building"
    Naval = "Naval"
    GroundForce = "GroundForce"
    Defenses = "Defenses"
    Air = "Air"


class GroupTask(Enum):
    EWR = "EarlyWarningRadar"
    AAA = "AAA"
    SHORAD = "SHORAD"
    MERAD = "MERAD"
    LORAD = "LORAD"
    AircraftCarrier = "AircraftCarrier"
    HelicopterCarrier = "HelicopterCarrier"
    Navy = "Navy"
    BaseDefense = "BaseDefense"  # Ground
    FrontLine = "FrontLine"
    Air = "Air"
    Missile = "Missile"
    Coastal = "Coastal"
    Factory = "Factory"
    Ammo = "Ammo"
    Oil = "Oil"
    FOB = "FOB"
    StrikeTarget = "StrikeTarget"
    Comms = "Comms"
    Power = "Power"


ROLE_TASKINGS: dict[GroupRole, list[GroupTask]] = {
    GroupRole.Unknow: [],  # No Tasking
    GroupRole.AntiAir: [
        GroupTask.EWR,
        GroupTask.AAA,
        GroupTask.SHORAD,
        GroupTask.MERAD,
        GroupTask.LORAD,
    ],
    GroupRole.GroundForce: [GroupTask.BaseDefense, GroupTask.FrontLine],
    GroupRole.Naval: [
        GroupTask.AircraftCarrier,
        GroupTask.HelicopterCarrier,
        GroupTask.Navy,
    ],
    GroupRole.Building: [
        GroupTask.Factory,
        GroupTask.Ammo,
        GroupTask.Oil,
        GroupTask.FOB,
        GroupTask.StrikeTarget,
        GroupTask.Comms,
        GroupTask.Power,
    ],
    GroupRole.Defenses: [GroupTask.Missile, GroupTask.Coastal],
    GroupRole.Air: [GroupTask.Air],
}
