from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Union

METERS_TO_FEET = 3.28084
FEET_TO_METERS = 1 / METERS_TO_FEET
NM_TO_METERS = 1852
METERS_TO_NM = 1 / NM_TO_METERS

KNOTS_TO_KPH = 1.852
KPH_TO_KNOTS = 1 / KNOTS_TO_KPH
MS_TO_KPH = 3.6
KPH_TO_MS = 1 / MS_TO_KPH


def heading_sum(h, a) -> int:
    h += a
    if h > 360:
        return h - 360
    elif h < 0:
        return 360 + h
    else:
        return h


def opposite_heading(h):
    return heading_sum(h, 180)


def meter_to_feet(value_in_meter: float) -> int:
    return int(Distance.meters(value_in_meter).to_feet)


def feet_to_meter(value_in_feet: float) -> int:
    return int(Distance.feet(value_in_feet).to_meters)


def meter_to_nm(value_in_meter: float) -> int:
    return int(Distance.meters(value_in_meter).to_nautical_miles)


def nm_to_meter(value_in_nm: float) -> int:
    return int(Distance.nautical_miles(value_in_nm).to_meters)


def knots_to_kph(knots: float) -> int:
    return int(Speed.knots(knots).to_kph)


def kph_to_mps(kph: float) -> int:
    return int(Speed.kph(kph).to_meters_per_second)


def mps_to_kph(mps: float) -> int:
    return int(Speed.meters_per_second(mps).to_kph)


def mps_to_knots(mps: float) -> int:
    return int(Speed.meters_per_second(mps).to_knots)


@dataclass(frozen=True, order=True)
class Distance:
    distance_in_meters: float

    @property
    def to_feet(self) -> float:
        return self.distance_in_meters * METERS_TO_FEET

    @property
    def to_meters(self) -> float:
        return self.distance_in_meters

    @property
    def to_nautical_miles(self) -> float:
        return self.distance_in_meters * METERS_TO_NM

    @classmethod
    def feet(cls, feet: float) -> Distance:
        return cls(feet * FEET_TO_METERS)

    @classmethod
    def meters(cls, meters: float) -> Distance:
        return cls(meters)

    @classmethod
    def nautical_miles(cls, nm: float) -> Distance:
        return cls(nm * NM_TO_METERS)

    def __mul__(self, other: Union[float, int]) -> Distance:
        return Distance(self.to_meters * other)

    def __truediv__(self, other: Union[float, int]) -> Distance:
        return Distance(self.to_meters / other)

    def __floordiv__(self, other: Union[float, int]) -> Distance:
        return Distance(self.to_meters // other)


@dataclass(frozen=True, order=True)
class Speed:
    speed_in_kph: float

    @property
    def to_knots(self) -> float:
        return self.speed_in_kph * KPH_TO_KNOTS

    @property
    def to_kph(self) -> float:
        return self.speed_in_kph

    @property
    def to_meters_per_second(self) -> float:
        return self.speed_in_kph * KPH_TO_MS

    def to_mach(self, altitude: Distance) -> float:
        c_sound = Speed.mach(1, altitude)
        return self.speed_in_kph / c_sound.to_kph

    @classmethod
    def knots(cls, knots: float) -> Speed:
        return cls(knots * KNOTS_TO_KPH)

    @classmethod
    def kph(cls, kph: float) -> Speed:
        return cls(kph)

    @classmethod
    def meters_per_second(cls, ms: float) -> Speed:
        return cls(ms * MS_TO_KPH)

    @classmethod
    def mach(cls, mach: float, altitude: Distance) -> Speed:
        # https://www.grc.nasa.gov/WWW/K-12/airplane/atmos.html
        if altitude <= Distance.feet(36152):
            temperature_f = 59 - 0.00356 * altitude.to_feet
        else:
            # There's another formula for altitudes over 82k feet, but we better
            # not be planning waypoints that high...
            temperature_f = -70

        temperature_k = (temperature_f + 459.67) * (5 / 9)

        # https://www.engineeringtoolbox.com/specific-heat-ratio-d_602.html
        # Dependent on temperature, but varies very little (+/-0.001)
        # between -40F and 180F.
        heat_capacity_ratio = 1.4

        # https://www.grc.nasa.gov/WWW/K-12/airplane/sound.html
        gas_constant = 286  # m^2/s^2/K
        c_sound = math.sqrt(heat_capacity_ratio * gas_constant * temperature_k)
        return Speed.meters_per_second(c_sound) * mach

    def __mul__(self, other: Union[float, int]) -> Speed:
        return Speed(self.to_kph * other)

    def __truediv__(self, other: Union[float, int]) -> Speed:
        return Speed(self.to_kph / other)

    def __floordiv__(self, other: Union[float, int]) -> Speed:
        return Speed(self.to_kph // other)


SPEED_OF_SOUND_AT_SEA_LEVEL = Speed.knots(661.5)
