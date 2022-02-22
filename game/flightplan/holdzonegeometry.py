from __future__ import annotations

from typing import TYPE_CHECKING

import shapely.ops
from dcs import Point
from shapely.geometry import MultiPolygon, Point as ShapelyPoint, Polygon

from game.utils import nautical_miles

if TYPE_CHECKING:
    from game.coalition import Coalition
    from game.theater import ConflictTheater


class HoldZoneGeometry:
    """Defines the zones used for finding optimal hold point placement.

    The zones themselves are stored in the class rather than just the resulting hold
    point so that the zones can be drawn in the map for debugging purposes.
    """

    def __init__(
        self,
        target: Point,
        home: Point,
        ip: Point,
        join: Point,
        coalition: Coalition,
        theater: ConflictTheater,
    ) -> None:
        self._target = target
        # Hold points are placed one of two ways. Either approach guarantees:
        #
        # * Safe hold point.
        # * Minimum distance to the join point.
        # * Not closer to the target than the join point.
        #
        # 1. As near the join point as possible with a specific distance from the
        #    departure airfield. This prevents loitering directly above the airfield but
        #    also keeps the hold point close to the departure airfield.
        #
        # 2. Alternatively, if the entire home zone is excluded by the above criteria,
        #    as neat the departure airfield as possible within a minimum distance from
        #    the join point, with a restricted turn angle at the join point. This
        #    handles the case where we need to backtrack from the departure airfield and
        #    the join point to place the hold point, but the turn angle limit restricts
        #    the maximum distance of the backtrack while maintaining the direction of
        #    the flight plan.
        self.threat_zone = coalition.opponent.threat_zone.all
        self.home = ShapelyPoint(home.x, home.y)

        self.join = ShapelyPoint(join.x, join.y)

        self.join_bubble = self.join.buffer(coalition.doctrine.push_distance.meters)

        join_to_target_distance = join.distance_to_point(target)
        self.target_bubble = ShapelyPoint(target.x, target.y).buffer(
            join_to_target_distance
        )

        self.home_bubble = self.home.buffer(coalition.doctrine.hold_distance.meters)

        excluded_zones = shapely.ops.unary_union(
            [self.join_bubble, self.target_bubble, self.threat_zone]
        )
        if not isinstance(excluded_zones, MultiPolygon):
            excluded_zones = MultiPolygon([excluded_zones])
        self.excluded_zones = excluded_zones

        join_heading = ip.heading_between_point(join)

        # Arbitrarily large since this is later constrained by the map boundary, and
        # we'll be picking a location close to the IP anyway. Just used to avoid real
        # distance calculations to project to the map edge.
        large_distance = nautical_miles(400).meters
        turn_limit = 40
        join_limit_ccw = join.point_from_heading(
            join_heading - turn_limit, large_distance
        )
        join_limit_cw = join.point_from_heading(
            join_heading + turn_limit, large_distance
        )

        join_direction_limit_wedge = Polygon(
            [
                (join.x, join.y),
                (join_limit_ccw.x, join_limit_ccw.y),
                (join_limit_cw.x, join_limit_cw.y),
            ]
        )

        permissible_zones = (
            coalition.nav_mesh.map_bounds(theater)
            .intersection(join_direction_limit_wedge)
            .difference(self.excluded_zones)
            .difference(self.home_bubble)
        )
        if not isinstance(permissible_zones, MultiPolygon):
            permissible_zones = MultiPolygon([permissible_zones])
        self.permissible_zones = permissible_zones
        self.preferred_lines = self.home_bubble.boundary.difference(self.excluded_zones)

    def find_best_hold_point(self) -> Point:
        if self.preferred_lines.is_empty:
            hold, _ = shapely.ops.nearest_points(self.permissible_zones, self.home)
        else:
            hold, _ = shapely.ops.nearest_points(self.preferred_lines, self.join)
        return self._target.new_in_same_map(hold.x, hold.y)
