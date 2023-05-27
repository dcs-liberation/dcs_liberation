import os
import pytest

from shapely.geometry import MultiPolygon, Polygon

from dcs.terrain.caucasus.caucasus import Caucasus
from game.theater import landmap


def test_miz() -> None:
    """
    Test miz generation and loading
    """
    test_map = landmap.Landmap(
        inclusion_zones=MultiPolygon([Polygon([(0, 0), (0, 1), (1, 0)])]),
        exclusion_zones=MultiPolygon([Polygon([(1, 1), (0, 1), (1, 0)])]),
        sea_zones=MultiPolygon([Polygon([(0, 0), (0, 2), (1, 0)])]),
    )
    test_filename = "test.miz"
    landmap.to_miz(test_map, Caucasus(), test_filename)
    assert os.path.isfile("test.miz")
    loaded_map = landmap.from_miz("test.miz")
    assert test_map.inclusion_zones.equals_exact(
        loaded_map.inclusion_zones, tolerance=1e-6
    )
    assert test_map.sea_zones.equals_exact(loaded_map.sea_zones, tolerance=1e-6)
    assert test_map.exclusion_zones.equals_exact(
        loaded_map.exclusion_zones, tolerance=1e-6
    )

    if os.path.isfile(test_filename):
        os.remove(test_filename)
