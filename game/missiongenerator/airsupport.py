from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.radio.radios import RadioFrequency
    from game.radio.tacan import TacanChannel


@dataclass
class AwacsInfo:
    """AWACS information for the kneeboard."""

    group_name: str
    callsign: str
    freq: RadioFrequency
    depature_location: Optional[str]
    start_time: Optional[timedelta]
    end_time: Optional[timedelta]
    blue: bool


@dataclass
class TankerInfo:
    """Tanker information for the kneeboard."""

    group_name: str
    callsign: str
    variant: str
    freq: RadioFrequency
    tacan: TacanChannel
    start_time: Optional[timedelta]
    end_time: Optional[timedelta]
    blue: bool


@dataclass(frozen=True)
class JtacInfo:
    """JTAC information."""

    group_name: str
    unit_name: str
    callsign: str
    region: str
    code: str
    blue: bool
    freq: RadioFrequency


@dataclass
class AirSupport:
    awacs: list[AwacsInfo] = field(default_factory=list)
    tankers: list[TankerInfo] = field(default_factory=list)
    jtacs: list[JtacInfo] = field(default_factory=list)
