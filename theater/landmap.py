import pickle
import typing

Zone = typing.Collection[typing.Tuple[float, float]]
Landmap = typing.Tuple[typing.Collection[Zone], typing.Collection[Zone]]


def load_landmap(filename: str) -> Landmap:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except:
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

def poly_centroid(poly) -> typing.Tuple[float, float]:
    x_list = [vertex[0] for vertex in poly]
    y_list = [vertex[1] for vertex in poly]
    x = sum(x_list) / len(poly)
    y = sum(y_list) / len(poly)
    return (x, y)

