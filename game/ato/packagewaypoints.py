from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.flightplan import JoinZoneGeometry
from game.flightplan.ipsolver import IpSolver
from game.flightplan.refuelzonegeometry import RefuelZoneGeometry
from game.utils import dcs_to_shapely_point

if TYPE_CHECKING:
    from game.ato import Package
    from game.coalition import Coalition


@dataclass(frozen=True)
class PackageWaypoints:
    join: Point
    ingress: Point
    split: Point
    refuel: Point

    @staticmethod
    def create(package: Package, coalition: Coalition) -> PackageWaypoints:
        origin = package.departure_closest_to_target()

        # Start by picking the best IP for the attack.
        ingress_point_shapely = IpSolver(
            dcs_to_shapely_point(origin.position),
            dcs_to_shapely_point(package.target.position),
            coalition.doctrine,
            coalition.opponent.threat_zone.all,
        ).solve()
        ingress_point = origin.position.new_in_same_map(
            ingress_point_shapely.x, ingress_point_shapely.y
        )

        join_point = JoinZoneGeometry(
            package.target.position,
            origin.position,
            ingress_point,
            coalition,
        ).find_best_join_point()

        refuel_point = RefuelZoneGeometry(
            origin.position,
            join_point,
            coalition,
        ).find_best_refuel_point()

        # And the split point based on the best route from the IP. Since that's no
        # different than the best route *to* the IP, this is the same as the join point.
        # TODO: Estimate attack completion point based on the IP and split from there?
        return PackageWaypoints(
            WaypointBuilder.perturb(join_point),
            ingress_point,
            WaypointBuilder.perturb(join_point),
            refuel_point,
        )
