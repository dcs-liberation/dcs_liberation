from __future__ import annotations

from enum import unique, Enum


@unique
class GroundUnitClass(Enum):
    Tank = "Tank"
    Atgm = "ATGM"
    Ifv = "IFV"
    Apc = "APC"
    Artillery = "Artillery"
    Logistics = "Logistics"
    Recon = "Recon"
    Infantry = "Infantry"
    Shorads = "SHORADS"
    Manpads = "MANPADS"
