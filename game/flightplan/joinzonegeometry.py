from __future__ import annotations

from typing import TYPE_CHECKING

import shapely.ops
from dcs import Point
from shapely.geometry import (
    MultiLineString,
    MultiPolygon,
    Point as ShapelyPoint,
    Polygon,
)

from game.utils import nautical_miles

if TYPE_CHECKING:
    from game.coalition import Coalition


class JoinZoneGeometry:
    """Defines the zones used for finding optimal join point placement.

    The zones themselves are stored in the class rather than just the resulting join
    point so that the zones can be drawn in the map for debugging purposes.
    """

    def __init__(
        self, target: Point, home: Point, ip: Point, coalition: Coalition
    ) -> None:
        self._target = target
        # Normal join placement is based on the path from home to the IP. If no path is
        # found it means that the target is on a direct path. In that case we instead
        # want to enforce that the join point is:
        #
        # * Not closer to the target than the IP.
        # * Not too close to the home airfield.
        # * Not threatened.
        # * A minimum distance from the IP.
        # * Not too sharp a turn at the ingress point.
        self.ip = ShapelyPoint(ip.x, ip.y)
        self.threat_zone = coalition.opponent.threat_zone.all
        self.home = ShapelyPoint(home.x, home.y)

        self.ip_bubble = self.ip.buffer(coalition.doctrine.join_distance.meters)

        ip_distance = ip.distance_to_point(target)
        self.target_bubble = ShapelyPoint(target.x, target.y).buffer(ip_distance)

        # The minimum distance between the home location and the IP.
        min_distance_from_home = nautical_miles(5)

        self.home_bubble = self.home.buffer(min_distance_from_home.meters)

        excluded_zones = shapely.ops.unary_union(
            [self.ip_bubble, self.target_bubble, self.threat_zone]
        )

        if not isinstance(excluded_zones, MultiPolygon):
            excluded_zones = MultiPolygon([excluded_zones])
        self.excluded_zones = excluded_zones

        ip_heading = target.heading_between_point(ip)

        # Arbitrarily large since this is later constrained by the map boundary, and
        # we'll be picking a location close to the IP anyway. Just used to avoid real
        # distance calculations to project to the map edge.
        large_distance = nautical_miles(400).meters
        turn_limit = 40
        ip_limit_ccw = ip.point_from_heading(ip_heading - turn_limit, large_distance)
        ip_limit_cw = ip.point_from_heading(ip_heading + turn_limit, large_distance)

        ip_direction_limit_wedge = Polygon(
            [
                (ip.x, ip.y),
                (ip_limit_ccw.x, ip_limit_ccw.y),
                (ip_limit_cw.x, ip_limit_cw.y),
            ]
        )

        permissible_zones = ip_direction_limit_wedge.difference(
            self.excluded_zones
        ).difference(self.home_bubble)
        if permissible_zones.is_empty:
            permissible_zones = MultiPolygon([])
        if not isinstance(permissible_zones, MultiPolygon):
            permissible_zones = MultiPolygon([permissible_zones])
        self.permissible_zones = permissible_zones

        preferred_lines = ip_direction_limit_wedge.intersection(
            self.excluded_zones.boundary
        ).difference(self.home_bubble)

        if preferred_lines.is_empty:
            preferred_lines = MultiLineString([])
        if not isinstance(preferred_lines, MultiLineString):
            preferred_lines = MultiLineString([preferred_lines])
        self.preferred_lines = preferred_lines

    def find_best_join_point(self) -> Point:
        if self.preferred_lines.is_empty:
            join, _ = shapely.ops.nearest_points(self.permissible_zones, self.ip)
        else:
            join, _ = shapely.ops.nearest_points(self.preferred_lines, self.ip)
        return self._target.new_in_same_map(join.x, join.y)
