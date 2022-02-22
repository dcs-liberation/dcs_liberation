from __future__ import annotations

from typing import TYPE_CHECKING

import shapely.ops
from dcs import Point
from shapely.geometry import MultiPolygon, Point as ShapelyPoint

from game.utils import meters, nautical_miles

if TYPE_CHECKING:
    from game.coalition import Coalition


class IpZoneGeometry:
    """Defines the zones used for finding optimal IP placement.

    The zones themselves are stored in the class rather than just the resulting IP so
    that the zones can be drawn in the map for debugging purposes.
    """

    def __init__(
        self,
        target: Point,
        home: Point,
        coalition: Coalition,
    ) -> None:
        self._target = target
        self.threat_zone = coalition.opponent.threat_zone.all
        self.home = ShapelyPoint(home.x, home.y)

        max_ip_distance = coalition.doctrine.max_ingress_distance
        min_ip_distance = coalition.doctrine.min_ingress_distance

        # The minimum distance between the home location and the IP.
        min_distance_from_home = nautical_miles(5)

        # The distance that is expected to be needed between the beginning of the attack
        # and weapon release. This buffers the threat zone to give a 5nm window between
        # the edge of the "safe" zone and the actual threat so that "safe" IPs are less
        # likely to end up with the attacker entering a threatened area.
        attack_distance_buffer = nautical_miles(5)

        home_threatened = coalition.opponent.threat_zone.threatened(home)

        shapely_target = ShapelyPoint(target.x, target.y)
        home_to_target_distance = meters(home.distance_to_point(target))

        self.home_bubble = self.home.buffer(home_to_target_distance.meters).difference(
            self.home.buffer(min_distance_from_home.meters)
        )

        # If the home zone is not threatened and home is within LAR, constrain the max
        # range to the home-to-target distance to prevent excessive backtracking.
        #
        # If the home zone *is* threatened, we need to back out of the zone to
        # rendezvous anyway.
        if not home_threatened and (
            min_ip_distance < home_to_target_distance < max_ip_distance
        ):
            max_ip_distance = home_to_target_distance
        max_ip_bubble = shapely_target.buffer(max_ip_distance.meters)
        min_ip_bubble = shapely_target.buffer(min_ip_distance.meters)
        self.ip_bubble = max_ip_bubble.difference(min_ip_bubble)

        # The intersection of the home bubble and IP bubble will be all the points that
        # are within the valid IP range that are not farther from home than the target
        # is. However, if the origin airfield is threatened but there are safe
        # placements for the IP, we should not constrain to the home zone. In this case
        # we'll either end up with a safe zone outside the home zone and pick the
        # closest point in to to home (minimizing backtracking), or we'll have no safe
        # IP anywhere within range of the target, and we'll later pick the IP nearest
        # the edge of the threat zone.
        if home_threatened:
            self.permissible_zone = self.ip_bubble
        else:
            self.permissible_zone = self.ip_bubble.intersection(self.home_bubble)

        if self.permissible_zone.is_empty:
            # If home is closer to the target than the min range, there will not be an
            # IP solution that's close enough to home, in which case we need to ignore
            # the home bubble.
            self.permissible_zone = self.ip_bubble

        safe_zones = self.permissible_zone.difference(
            self.threat_zone.buffer(attack_distance_buffer.meters)
        )

        if not isinstance(safe_zones, MultiPolygon):
            safe_zones = MultiPolygon([safe_zones])
        self.safe_zones = safe_zones

    def _unsafe_ip(self) -> ShapelyPoint:
        unthreatened_home_zone = self.home_bubble.difference(self.threat_zone)
        if unthreatened_home_zone.is_empty:
            # Nowhere in our home zone is safe. The package will need to exit the
            # threatened area to hold and rendezvous. Pick the IP closest to the
            # edge of the threat zone.
            return shapely.ops.nearest_points(
                self.permissible_zone, self.threat_zone.boundary
            )[0]

        # No safe point in the IP zone, but the home zone is safe. Pick the max-
        # distance IP that's closest to the untreatened home zone.
        return shapely.ops.nearest_points(
            self.permissible_zone, unthreatened_home_zone
        )[0]

    def _safe_ip(self) -> ShapelyPoint:
        # We have a zone of possible IPs that are safe, close enough, and in range. Pick
        # the IP in the zone that's closest to the target.
        return shapely.ops.nearest_points(self.safe_zones, self.home)[0]

    def find_best_ip(self) -> Point:
        if self.safe_zones.is_empty:
            ip = self._unsafe_ip()
        else:
            ip = self._safe_ip()
        return self._target.new_in_same_map(ip.x, ip.y)
