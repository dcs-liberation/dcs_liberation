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
    # Anti Air
    EWR = "EarlyWarningRadar"
    AAA = "AAA"
    SHORAD = "SHORAD"
    MERAD = "MERAD"
    LORAD = "LORAD"

    # Naval
    AircraftCarrier = "AircraftCarrier"
    HelicopterCarrier = "HelicopterCarrier"
    Navy = "Navy"

    # Armor
    BaseDefense = "BaseDefense"
    FrontLine = "FrontLine"

    # Additional things
    Air = "Air"
    Missile = "Missile"
    Coastal = "Coastal"

    # Buildings
    Factory = "Factory"
    Ammo = "Ammo"
    Oil = "Oil"
    Fuel = "Fuel"
    FOB = "FOB"
    StrikeTarget = "StrikeTarget"
    OffShoreStrikeTarget = "OffShoreStrikeTarget"
    Comms = "Comms"
    Power = "Power"
    Farp = "Farp"
    Derrick = "Derrick"
    AllyCamp = "AllyCamp"
    Village = "Village"
    Ware = "Ware"
    WW2Bunker = "WW2Bunker"
    CommandCenter = "CommandCenter"


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
        GroupTask.Fuel,
        GroupTask.FOB,
        GroupTask.StrikeTarget,
        GroupTask.OffShoreStrikeTarget,
        GroupTask.Comms,
        GroupTask.Power,
        GroupTask.Farp,
        GroupTask.Derrick,
        GroupTask.AllyCamp,
        GroupTask.Village,
        GroupTask.Ware,
        GroupTask.WW2Bunker,
    ],
    GroupRole.Defenses: [GroupTask.Missile, GroupTask.Coastal],
    GroupRole.Air: [GroupTask.Air],
}
