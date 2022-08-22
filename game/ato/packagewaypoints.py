from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.flightplan import IpZoneGeometry, JoinZoneGeometry
from game.flightplan.refuelzonegeometry import RefuelZoneGeometry

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
        ingress_point = IpZoneGeometry(
            package.target.position,
            origin.position,
            coalition,
        ).find_best_ip()

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
