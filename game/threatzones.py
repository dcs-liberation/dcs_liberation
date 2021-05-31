from __future__ import annotations

from functools import singledispatchmethod
from typing import Optional, TYPE_CHECKING, Union, Iterable

from dcs.mapping import Point as DcsPoint
from shapely.geometry import (
    LineString,
    MultiPolygon,
    Point as ShapelyPoint,
    Polygon,
)
from shapely.geometry.base import BaseGeometry
from shapely.ops import nearest_points, unary_union

from game.theater import ControlPoint, MissionTarget
from game.utils import Distance, meters, nautical_miles
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.flights.flight import Flight, FlightWaypoint

if TYPE_CHECKING:
    from game import Game


ThreatPoly = Union[MultiPolygon, Polygon]


class ThreatZones:
    def __init__(
        self, airbases: ThreatPoly, air_defenses: ThreatPoly, radar_sam_threats
    ) -> None:
        self.airbases = airbases
        self.air_defenses = air_defenses
        self.radar_sam_threats = radar_sam_threats
        self.all = unary_union([airbases, air_defenses])

    def closest_boundary(self, point: DcsPoint) -> DcsPoint:
        boundary, _ = nearest_points(
            self.all.boundary, self.dcs_to_shapely_point(point)
        )
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
        return self.threatened(
            LineString([self.dcs_to_shapely_point(a), self.dcs_to_shapely_point(b)])
        )

    @singledispatchmethod
    def threatened_by_aircraft(self, target) -> bool:
        raise NotImplementedError

    @threatened_by_aircraft.register
    def _threatened_by_aircraft_geom(self, position: BaseGeometry) -> bool:
        return self.airbases.intersects(position)

    @threatened_by_aircraft.register
    def _threatened_by_aircraft_flight(self, flight: Flight) -> bool:
        return self.threatened_by_aircraft(
            LineString((self.dcs_to_shapely_point(p.position) for p in flight.points))
        )

    def waypoints_threatened_by_aircraft(
        self, waypoints: Iterable[FlightWaypoint]
    ) -> bool:
        return self.threatened_by_aircraft(
            LineString((self.dcs_to_shapely_point(p.position) for p in waypoints))
        )

    @singledispatchmethod
    def threatened_by_air_defense(self, target) -> bool:
        raise NotImplementedError

    @threatened_by_air_defense.register
    def _threatened_by_air_defense_geom(self, position: BaseGeometry) -> bool:
        return self.air_defenses.intersects(position)

    @threatened_by_air_defense.register
    def _threatened_by_air_defense_flight(self, flight: Flight) -> bool:
        return self.threatened_by_air_defense(
            LineString((self.dcs_to_shapely_point(p.position) for p in flight.points))
        )

    @threatened_by_air_defense.register
    def _threatened_by_air_defense_mission_target(self, target: MissionTarget) -> bool:
        return self.threatened_by_air_defense(
            self.dcs_to_shapely_point(target.position)
        )

    @singledispatchmethod
    def threatened_by_radar_sam(self, target) -> bool:
        raise NotImplementedError

    @threatened_by_radar_sam.register
    def _threatened_by_radar_sam_geom(self, position: BaseGeometry) -> bool:
        return self.radar_sam_threats.intersects(position)

    @threatened_by_radar_sam.register
    def _threatened_by_radar_sam_flight(self, flight: Flight) -> bool:
        return self.threatened_by_radar_sam(
            LineString((self.dcs_to_shapely_point(p.position) for p in flight.points))
        )

    def waypoints_threatened_by_radar_sam(
        self, waypoints: Iterable[FlightWaypoint]
    ) -> bool:
        return self.threatened_by_radar_sam(
            LineString((self.dcs_to_shapely_point(p.position) for p in waypoints))
        )

    @classmethod
    def closest_enemy_airbase(
        cls, location: ControlPoint, max_distance: Distance
    ) -> Optional[ControlPoint]:
        airfields = ObjectiveDistanceCache.get_closest_airfields(location)
        for airfield in airfields.all_airfields_within(max_distance):
            if airfield.captured != location.captured:
                return airfield
        return None

    @classmethod
    def barcap_threat_range(cls, game: Game, control_point: ControlPoint) -> Distance:
        doctrine = game.faction_for(control_point.captured).doctrine
        cap_threat_range = (
            doctrine.cap_max_distance_from_cp + doctrine.cap_engagement_range
        )
        opposing_airfield = cls.closest_enemy_airbase(
            control_point, cap_threat_range * 2
        )
        if opposing_airfield is None:
            return cap_threat_range

        airfield_distance = meters(
            opposing_airfield.position.distance_to_point(control_point.position)
        )

        # BARCAPs should not commit further than halfway to the closest enemy
        # airfield (with some breathing room) to avoid those missions becoming
        # offensive. For dissimilar doctrines we could weight this so that, as
        # an example, modern US goes no closer than 70% of the way to the WW2
        # German base, and the Germans go no closer than 30% of the way to the
        # US base, but for now equal weighting is fine.
        max_distance = airfield_distance * 0.45
        return min(cap_threat_range, max_distance)

    @classmethod
    def for_faction(cls, game: Game, player: bool) -> ThreatZones:
        """Generates the threat zones projected by the given coalition.

        Args:
            game: The game to generate the threat zone for.
            player: True if the coalition projecting the threat zone belongs to
            the player.

        Returns:
            The threat zones projected by the given coalition. If the threat
            zone belongs to the player, it is the zone that will be avoided by
            the enemy and vice versa.
        """
        air_threats = []
        air_defenses = []
        radar_sam_threats = []
        for control_point in game.theater.controlpoints:
            if control_point.captured != player:
                continue
            if control_point.runway_is_operational():
                point = ShapelyPoint(control_point.position.x, control_point.position.y)
                cap_threat_range = cls.barcap_threat_range(game, control_point)
                air_threats.append(point.buffer(cap_threat_range.meters))

            for tgo in control_point.ground_objects:
                for group in tgo.groups:
                    threat_range = tgo.threat_range(group)
                    # Any system with a shorter range than this is not worth
                    # even avoiding.
                    if threat_range > nautical_miles(3):
                        point = ShapelyPoint(tgo.position.x, tgo.position.y)
                        threat_zone = point.buffer(threat_range.meters)
                        air_defenses.append(threat_zone)
                    radar_threat_range = tgo.threat_range(group, radar_only=True)
                    if radar_threat_range > nautical_miles(3):
                        point = ShapelyPoint(tgo.position.x, tgo.position.y)
                        threat_zone = point.buffer(threat_range.meters)
                        radar_sam_threats.append(threat_zone)

        return cls(
            airbases=unary_union(air_threats),
            air_defenses=unary_union(air_defenses),
            radar_sam_threats=unary_union(radar_sam_threats),
        )

    @staticmethod
    def dcs_to_shapely_point(point: DcsPoint) -> ShapelyPoint:
        return ShapelyPoint(point.x, point.y)
