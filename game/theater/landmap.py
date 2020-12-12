import pickle
from typing import Collection, Optional, Tuple
import logging

from shapely import geometry

Zone = Collection[Tuple[float, float]]
Landmap = Tuple[Collection[geometry.Polygon], Collection[geometry.Polygon], Collection[geometry.Polygon]]


def load_landmap(filename: str) -> Optional[Landmap]:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except:
        logging.exception(f"Failed to load landmap {filename}")
        return None


def poly_contains(x, y, poly:geometry.Polygon):
    return poly.contains(geometry.Point(x, y))


def poly_centroid(poly) -> Tuple[float, float]:
    x_list = [vertex[0] for vertex in poly]
    y_list = [vertex[1] for vertex in poly]
    x = sum(x_list) / len(poly)
    y = sum(y_list) / len(poly)
    return (x, y)

