from dataclasses import dataclass
from typing import Optional

from dcs import Point


@dataclass(frozen=True)
class PackageWaypoints:
    join: Point
    ingress: Point
    split: Point
    refuel: Point
