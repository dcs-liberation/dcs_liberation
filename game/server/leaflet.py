from __future__ import annotations

from typing import Union

from dcs import Point
from pydantic import BaseModel
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon

from game.theater import ConflictTheater

LeafletLatLon = list[float]
LeafletPoly = list[LeafletLatLon]


class LeafletPoint(BaseModel):
    lat: float
    lng: float

    class Config:
        orm_mode = True


class ShapelyUtil:
    @staticmethod
    def poly_to_leaflet(poly: Polygon, theater: ConflictTheater) -> LeafletPoly:
        if poly.is_empty:
            return []
        return [
            Point(x, y, theater.terrain).latlng().as_list()
            for x, y in poly.exterior.coords
        ]

    @classmethod
    def polys_to_leaflet(
        cls, poly: Union[Polygon, MultiPolygon], theater: ConflictTheater
    ) -> list[LeafletPoly]:
        if isinstance(poly, MultiPolygon):
            polys = poly.geoms
        else:
            polys = [poly]
        return [cls.poly_to_leaflet(poly, theater) for poly in polys]

    @staticmethod
    def line_to_leaflet(
        line: LineString, theater: ConflictTheater
    ) -> list[LeafletLatLon]:
        return [Point(x, y, theater.terrain).latlng().as_list() for x, y in line.coords]

    @classmethod
    def lines_to_leaflet(
        cls, line_string: MultiLineString | LineString, theater: ConflictTheater
    ) -> list[list[LeafletLatLon]]:
        if isinstance(line_string, MultiLineString):
            lines = line_string.geoms
        else:
            lines = [line_string]
        return [cls.line_to_leaflet(line, theater) for line in lines]
