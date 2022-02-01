from __future__ import annotations

from enum import unique, Enum

from game.data.groups import GroupRole, GroupTask


@unique
class UnitClass(Enum):
    Unknown = "Unknown"
    Tank = "Tank"
    Atgm = "ATGM"
    Ifv = "IFV"
    Apc = "APC"
    Artillery = "Artillery"
    Logistics = "Logistics"
    Recon = "Recon"
    Infantry = "Infantry"
    AAA = "AAA"
    SHORAD = "SHORAD"
    Manpad = "Manpad"
    SR = "SearchRadar"
    STR = "SearchTrackRadar"
    LowAltSR = "LowAltSearchRadar"
    TR = "TrackRadar"
    LN = "Launcher"
    EWR = "EarlyWarningRadar"
    TELAR = "TELAR"
    Missile = "Missile"
    AircraftCarrier = "AircraftCarrier"
    HelicopterCarrier = "HelicopterCarrier"
    Destroyer = "Destroyer"
    Frigate = "Frigate"
    Cruiser = "Cruiser"
    Submarine = "Submarine"
    LandingShip = "LandingShip"
    Boat = "Boat"
    Plane = "Plane"
    Fortification = "Fortification"

    def to_dict(self) -> str:
        return self.value
