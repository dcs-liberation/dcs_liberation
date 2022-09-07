from __future__ import annotations

from typing import Union

from dcs import Point
from dcs.mapping import LatLng
from pydantic import BaseModel
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon

from game.theater import ConflictTheater


class LeafletPoint(BaseModel):
    lat: float
    lng: float

    class Config:
        orm_mode = True

        title = "LatLng"


LeafletLine = list[LeafletPoint]


# Leaflet allows either a single array of latlng to define the boundary, or an array of
# arrays of latlngs, with the first array being the boundary and the rest defining
# holes. To avoid the UI needing to test for which type of polygon we send, we always
# use the array of arrays type, even for geometries without holes.
# https://leafletjs.com/reference.html#polygon
LeafletPoly = list[LeafletLine]


class ShapelyUtil:
    @staticmethod
    def latlng_to_leaflet(latlng: LatLng) -> LeafletPoint:
        return LeafletPoint(lat=latlng.lat, lng=latlng.lng)

    @classmethod
    def poly_to_leaflet(cls, poly: Polygon, theater: ConflictTheater) -> LeafletPoly:
        if poly.is_empty:
            return []
        try:
            lines = poly.boundary.geoms
        except AttributeError:
            lines = [poly.boundary]
        return cls.lines_to_leaflet(MultiLineString(lines), theater)

    @classmethod
    def polys_to_leaflet(
        cls, poly: Union[Polygon, MultiPolygon], theater: ConflictTheater
    ) -> list[LeafletPoly]:
        if isinstance(poly, MultiPolygon):
            polys = poly.geoms
        else:
            polys = [poly]
        return [cls.poly_to_leaflet(poly, theater) for poly in polys]

    @classmethod
    def line_to_leaflet(cls, line: LineString, theater: ConflictTheater) -> LeafletLine:
        return [
            cls.latlng_to_leaflet(Point(x, y, theater.terrain).latlng())
            for x, y in line.coords
        ]

    @classmethod
    def lines_to_leaflet(
        cls, line_string: MultiLineString | LineString, theater: ConflictTheater
    ) -> list[LeafletLine]:
        if isinstance(line_string, MultiLineString):
            lines = line_string.geoms
        else:
            lines = [line_string]
        return [cls.line_to_leaflet(line, theater) for line in lines]
