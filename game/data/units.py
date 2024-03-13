from __future__ import annotations

from enum import unique, Enum


@unique
class UnitClass(Enum):
    UNKNOWN = "Unknown"
    AAA = "AAA"
    AIRCRAFT_CARRIER = "AircraftCarrier"
    APC = "APC"
    ARTILLERY = "Artillery"
    ATGM = "ATGM"
    BOAT = "Boat"
    COMMAND_POST = "CommandPost"
    CRUISER = "Cruiser"
    DESTROYER = "Destroyer"
    EARLY_WARNING_RADAR = "EarlyWarningRadar"
    FORTIFICATION = "Fortification"
    FRIGATE = "Frigate"
    HELICOPTER = "Helicopter"
    HELICOPTER_CARRIER = "HelicopterCarrier"
    IFV = "IFV"
    INFANTRY = "Infantry"
    LANDING_SHIP = "LandingShip"
    LAUNCHER = "Launcher"
    LOGISTICS = "Logistics"
    MANPAD = "Manpad"
    MISSILE = "Missile"
    ANTISHIP_MISSILE = "AntiShipMissile"
    OPTICAL_TRACKER = "OpticalTracker"
    PLANE = "Plane"
    POWER = "Power"
    RECON = "Recon"
    SEARCH_LIGHT = "SearchLight"
    SEARCH_RADAR = "SearchRadar"
    SEARCH_TRACK_RADAR = "SearchTrackRadar"
    SHORAD = "SHORAD"
    SPECIALIZED_RADAR = "SpecializedRadar"
    SUBMARINE = "Submarine"
    TANK = "Tank"
    TELAR = "TELAR"
    TRACK_RADAR = "TrackRadar"


# All UnitClasses which can have AntiAir capabilities
ANTI_AIR_UNIT_CLASSES = [
    UnitClass.AAA,
    UnitClass.AIRCRAFT_CARRIER,
    UnitClass.CRUISER,
    UnitClass.DESTROYER,
    UnitClass.EARLY_WARNING_RADAR,
    UnitClass.FRIGATE,
    UnitClass.HELICOPTER_CARRIER,
    UnitClass.LAUNCHER,
    UnitClass.MANPAD,
    UnitClass.SEARCH_RADAR,
    UnitClass.SEARCH_TRACK_RADAR,
    UnitClass.SPECIALIZED_RADAR,
    UnitClass.SHORAD,
    UnitClass.SUBMARINE,
    UnitClass.TELAR,
    UnitClass.TRACK_RADAR,
]
