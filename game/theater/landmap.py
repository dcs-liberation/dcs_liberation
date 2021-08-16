from dataclasses import dataclass
import pickle
from functools import cached_property
from typing import Optional, Tuple, Union
import logging
from pathlib import Path

from shapely import geometry
from shapely.geometry import MultiPolygon, Polygon


@dataclass(frozen=True)
class Landmap:
    inclusion_zones: MultiPolygon
    exclusion_zones: MultiPolygon
    sea_zones: MultiPolygon

    def __post_init__(self) -> None:
        if not self.inclusion_zones.is_valid:
            raise RuntimeError("Inclusion zones not valid")
        if not self.exclusion_zones.is_valid:
            raise RuntimeError("Exclusion zones not valid")
        if not self.sea_zones.is_valid:
            raise RuntimeError("Sea zones not valid")

    @cached_property
    def inclusion_zone_only(self) -> MultiPolygon:
        return self.inclusion_zones - self.exclusion_zones - self.sea_zones


def load_landmap(filename: Path) -> Optional[Landmap]:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except:
        logging.exception(f"Failed to load landmap {filename}")
        return None


def poly_contains(x: float, y: float, poly: Union[MultiPolygon, Polygon]) -> bool:
    return poly.contains(geometry.Point(x, y))
