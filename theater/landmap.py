import pickle
from typing import Collection, Optional, Tuple
import logging

Zone = Collection[Tuple[float, float]]
Landmap = Tuple[Collection[Zone], Collection[Zone], Collection[Zone]]


def load_landmap(filename: str) -> Optional[Landmap]:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except:
        logging.exception(f"Failed to load landmap {filename}")
        return None


def poly_contains(x, y, poly):
    n = len(poly)
    inside = False
    xints = 0.0
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def poly_centroid(poly) -> Tuple[float, float]:
    x_list = [vertex[0] for vertex in poly]
    y_list = [vertex[1] for vertex in poly]
    x = sum(x_list) / len(poly)
    y = sum(y_list) / len(poly)
    return (x, y)

