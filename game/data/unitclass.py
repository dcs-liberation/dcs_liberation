from __future__ import annotations

from enum import unique, Enum


@unique
class UnitClass(Enum):
    Tank = "Tank"
    Atgm = "ATGM"
    Ifv = "IFV"
    Apc = "APC"
    Artillery = "Artillery"
    Logistics = "Logistics"
    Recon = "Recon"
    Infantry = "Infantry"
    AAA = "AAA"
    Shorads = "SHORADS"
    Manpads = "MANPADS"
    SR = "SearchRadar"
    TR = "TrackRadar"
    LN = "Launcher"
    EWR = "EarlyWarningRadar"
    MERAD = "MERAD"
    LORAD = "LORAD"
    AircraftCarrier = "AircraftCarrier"
    HelicopterCarrier = "HelicopterCarrier"
    Destroyer = "Destroyer"
    Cruiser = "Cruiser"
    Submarine = "Submarine"
    Boat = "Boat"
