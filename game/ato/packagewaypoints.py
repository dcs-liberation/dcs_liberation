from dataclasses import dataclass

from dcs import Point


@dataclass(frozen=True)
class PackageWaypoints:
    join: Point
    ingress: Point
    split: Point
