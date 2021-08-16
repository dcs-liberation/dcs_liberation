from __future__ import annotations

import itertools
import math
import random
from collections import Iterable
from dataclasses import dataclass
from typing import Union, Any, TypeVar

METERS_TO_FEET = 3.28084
FEET_TO_METERS = 1 / METERS_TO_FEET
NM_TO_METERS = 1852
METERS_TO_NM = 1 / NM_TO_METERS

KNOTS_TO_KPH = 1.852
KPH_TO_KNOTS = 1 / KNOTS_TO_KPH
MS_TO_KPH = 3.6
KPH_TO_MS = 1 / MS_TO_KPH

INHG_TO_HPA = 33.86389
INHG_TO_MMHG = 25.400002776728


@dataclass(frozen=True, order=True)
class Distance:
    distance_in_meters: float

    @property
    def feet(self) -> float:
        return self.distance_in_meters * METERS_TO_FEET

    @property
    def meters(self) -> float:
        return self.distance_in_meters

    @property
    def nautical_miles(self) -> float:
        return self.distance_in_meters * METERS_TO_NM

    @classmethod
    def from_feet(cls, value: float) -> Distance:
        return cls(value * FEET_TO_METERS)

    @classmethod
    def from_meters(cls, value: float) -> Distance:
        return cls(value)

    @classmethod
    def from_nautical_miles(cls, value: float) -> Distance:
        return cls(value * NM_TO_METERS)

    @classmethod
    def inf(cls) -> Distance:
        return cls.from_meters(math.inf)

    def __add__(self, other: Distance) -> Distance:
        return meters(self.meters + other.meters)

    def __sub__(self, other: Distance) -> Distance:
        return meters(self.meters - other.meters)

    def __mul__(self, other: Union[float, int]) -> Distance:
        return meters(self.meters * other)

    __rmul__ = __mul__

    def __truediv__(self, other: Union[float, int]) -> Distance:
        return meters(self.meters / other)

    def __floordiv__(self, other: Union[float, int]) -> Distance:
        return meters(self.meters // other)

    def __bool__(self) -> bool:
        return not math.isclose(self.meters, 0.0)


def feet(value: float) -> Distance:
    return Distance.from_feet(value)


def meters(value: float) -> Distance:
    return Distance.from_meters(value)


def nautical_miles(value: float) -> Distance:
    return Distance.from_nautical_miles(value)


@dataclass(frozen=True, order=True)
class Speed:
    speed_in_kph: float

    @property
    def knots(self) -> float:
        return self.speed_in_kph * KPH_TO_KNOTS

    @property
    def kph(self) -> float:
        return self.speed_in_kph

    @property
    def meters_per_second(self) -> float:
        return self.speed_in_kph * KPH_TO_MS

    def mach(self, altitude: Distance = meters(0)) -> float:
        c_sound = mach(1, altitude)
        return self.speed_in_kph / c_sound.kph

    @classmethod
    def from_knots(cls, value: float) -> Speed:
        return cls(value * KNOTS_TO_KPH)

    @classmethod
    def from_kph(cls, value: float) -> Speed:
        return cls(value)

    @classmethod
    def from_meters_per_second(cls, value: float) -> Speed:
        return cls(value * MS_TO_KPH)

    @classmethod
    def from_mach(cls, value: float, altitude: Distance) -> Speed:
        # https://www.grc.nasa.gov/WWW/K-12/airplane/atmos.html
        if altitude <= feet(36152):
            temperature_f = 59 - 0.00356 * altitude.feet
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
        return mps(c_sound) * value

    def __add__(self, other: Speed) -> Speed:
        return kph(self.kph + other.kph)

    def __sub__(self, other: Speed) -> Speed:
        return kph(self.kph - other.kph)

    def __mul__(self, other: Union[float, int]) -> Speed:
        return kph(self.kph * other)

    __rmul__ = __mul__

    def __truediv__(self, other: Union[float, int]) -> Speed:
        return kph(self.kph / other)

    def __floordiv__(self, other: Union[float, int]) -> Speed:
        return kph(self.kph // other)

    def __bool__(self) -> bool:
        return not math.isclose(self.kph, 0.0)


def knots(value: float) -> Speed:
    return Speed.from_knots(value)


def kph(value: float) -> Speed:
    return Speed.from_kph(value)


def mps(value: float) -> Speed:
    return Speed.from_meters_per_second(value)


def mach(value: float, altitude: Distance) -> Speed:
    return Speed.from_mach(value, altitude)


SPEED_OF_SOUND_AT_SEA_LEVEL = knots(661.5)


@dataclass(frozen=True, order=True)
class Heading:
    heading_in_degrees: int

    @property
    def degrees(self) -> int:
        return Heading.reduce_angle(self.heading_in_degrees)

    @property
    def radians(self) -> float:
        return math.radians(Heading.reduce_angle(self.heading_in_degrees))

    @property
    def opposite(self) -> Heading:
        return self + Heading.from_degrees(180)

    @property
    def right(self) -> Heading:
        return self + Heading.from_degrees(90)

    @property
    def left(self) -> Heading:
        return self - Heading.from_degrees(90)

    def angle_between(self, other: Heading) -> Heading:
        angle_between = abs(self.degrees - other.degrees)
        if angle_between > 180:
            angle_between = 360 - angle_between
        return Heading.from_degrees(angle_between)

    @staticmethod
    def reduce_angle(angle: int) -> int:
        return angle % 360

    @classmethod
    def from_degrees(cls, angle: Union[int, float]) -> Heading:
        return cls(Heading.reduce_angle(round(angle)))

    @classmethod
    def from_radians(cls, angle: Union[int, float]) -> Heading:
        deg = round(math.degrees(angle))
        return cls(Heading.reduce_angle(deg))

    @classmethod
    def random(cls, min_angle: int = 0, max_angle: int = 0) -> Heading:
        return Heading.from_degrees(random.randint(min_angle, max_angle))

    def __add__(self, other: Heading) -> Heading:
        return Heading.from_degrees(self.degrees + other.degrees)

    def __sub__(self, other: Heading) -> Heading:
        return Heading.from_degrees(self.degrees - other.degrees)


@dataclass(frozen=True, order=True)
class Pressure:
    pressure_in_inches_hg: float

    @property
    def inches_hg(self) -> float:
        return self.pressure_in_inches_hg

    @property
    def mm_hg(self) -> float:
        return self.pressure_in_inches_hg * INHG_TO_MMHG

    @property
    def hecto_pascals(self) -> float:
        return self.pressure_in_inches_hg * INHG_TO_HPA


def inches_hg(value: float) -> Pressure:
    return Pressure(value)


PairwiseT = TypeVar("PairwiseT")


def pairwise(iterable: Iterable[PairwiseT]) -> Iterable[tuple[PairwiseT, PairwiseT]]:
    """
    itertools recipe
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def interpolate(value1: float, value2: float, factor: float, clamp: bool) -> float:
    """Inerpolate between two values, factor 0-1"""
    interpolated = value1 + (value2 - value1) * factor

    if clamp:
        bigger_value = max(value1, value2)
        smaller_value = min(value1, value2)
        return min(bigger_value, max(smaller_value, interpolated))
    else:
        return interpolated
