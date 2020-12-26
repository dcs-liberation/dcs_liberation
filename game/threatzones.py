from __future__ import annotations

from functools import singledispatchmethod
from typing import TYPE_CHECKING, Union

from dcs.mapping import Point as DcsPoint
from shapely.geometry import (
    LineString,
    MultiPolygon,
    Point as ShapelyPoint,
    Polygon,
)
from shapely.geometry.base import BaseGeometry
from shapely.ops import nearest_points, unary_union

from game.utils import Distance, meters, nautical_miles
from gen.flights.flight import Flight

if TYPE_CHECKING:
    from game import Game


ThreatPoly = Union[MultiPolygon, Polygon]


class ThreatZones:
    def __init__(self, airbases: ThreatPoly, air_defenses: ThreatPoly) -> None:
        self.airbases = airbases
        self.air_defenses = air_defenses
        self.all = unary_union([airbases, air_defenses])

    def closest_boundary(self, point: DcsPoint) -> DcsPoint:
        boundary, _ = nearest_points(self.all.boundary,
                                     self.dcs_to_shapely_point(point))
        return DcsPoint(boundary.x, boundary.y)

    @singledispatchmethod
    def threatened(self, position) -> bool:
        raise NotImplementedError

    @threatened.register
    def _threatened_geometry(self, position: BaseGeometry) -> bool:
        return self.all.intersects(position)

    @threatened.register
    def _threatened_dcs_point(self, position: DcsPoint) -> bool:
        return self.all.intersects(self.dcs_to_shapely_point(position))

    def path_threatened(self, a: DcsPoint, b: DcsPoint) -> bool:
        return self.threatened(LineString(
            [self.dcs_to_shapely_point(a), self.dcs_to_shapely_point(b)]))

    @singledispatchmethod
    def threatened_by_aircraft(self, target) -> bool:
        raise NotImplementedError

    @threatened_by_aircraft.register
    def _threatened_by_aircraft_geom(self, position: BaseGeometry) -> bool:
        return self.airbases.intersects(position)

    @threatened_by_aircraft.register
    def _threatened_by_aircraft_flight(self, flight: Flight) -> bool:
        return self.threatened_by_aircraft(LineString((
            self.dcs_to_shapely_point(p.position) for p in flight.points
        )))

    @singledispatchmethod
    def threatened_by_air_defense(self, target) -> bool:
        raise NotImplementedError

    @threatened_by_air_defense.register
    def _threatened_by_air_defense_geom(self, position: BaseGeometry) -> bool:
        return self.air_defenses.intersects(position)

    @threatened_by_air_defense.register
    def _threatened_by_air_defense_flight(self, flight: Flight) -> bool:
        return self.threatened_by_air_defense(LineString((
            self.dcs_to_shapely_point(p.position) for p in flight.points
        )))

    @classmethod
    def for_faction(cls, game: Game, player: bool) -> ThreatZones:
        opposing_doctrine = game.faction_for(not player).doctrine

        airbases = []
        air_defenses = []
        for control_point in game.theater.controlpoints:
            if control_point.captured != player:
                continue
            if control_point.runway_is_operational():
                point = ShapelyPoint(control_point.position.x,
                                     control_point.position.y)
                cap_threat_range = (opposing_doctrine.cap_max_distance_from_cp +
                                    opposing_doctrine.cap_engagement_range)
                airbases.append(point.buffer(cap_threat_range.meters))

            for tgo in control_point.ground_objects:
                for group in tgo.groups:
                    threat_range = tgo.threat_range(group)
                    # Any system with a shorter range than this is not worth
                    # even avoiding.
                    if threat_range > nautical_miles(3):
                        point = ShapelyPoint(tgo.position.x, tgo.position.y)
                        threat_zone = point.buffer(threat_range.meters)
                        air_defenses.append(threat_zone)

        return cls(
            airbases=unary_union(airbases),
            air_defenses=unary_union(air_defenses)
        )

    @staticmethod
    def dcs_to_shapely_point(point: DcsPoint) -> ShapelyPoint:
        return ShapelyPoint(point.x, point.y)