import copy
import logging

from dcs.planes import B_17G, B_52H, Tu_22M3
from dcs.point import MovingPoint
from dcs.task import Bombing, OptFormation, WeaponType

from .pydcswaypointbuilder import PydcsWaypointBuilder


class StrikeIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if self.group.units[0].unit_type in [B_17G, B_52H, Tu_22M3]:
            self.add_bombing_tasks(waypoint)
        else:
            self.add_strike_tasks(waypoint)

        waypoint.tasks.append(OptFormation.trail_open())

    def add_bombing_tasks(self, waypoint: MovingPoint) -> None:
        targets = self.waypoint.targets
        if not targets:
            return

        center = copy.copy(targets[0].position)
        for target in targets[1:]:
            center += target.position
        center /= len(targets)
        bombing = Bombing(center, weapon_type=WeaponType.Bombs)
        bombing.params["expend"] = "All"
        bombing.params["attackQtyLimit"] = False
        bombing.params["directionEnabled"] = False
        bombing.params["altitudeEnabled"] = False
        bombing.params["groupAttack"] = True
        waypoint.tasks.append(bombing)

    def add_strike_tasks(self, waypoint: MovingPoint) -> None:

        # logic to try and spread out the targets within a strike target
        # for example, if there is one strike ahead of this flights strike, then shift it's bombing targets by two (arbitrary number, ideally it'd be based on number of planes/bombs per flight and knowing how many bombs per target the user wants)
        strike_flights_ahead = 0
        waypoint_index = [
            i
            for i, w in enumerate(self.flight.points)
            if w.x == self.waypoint.x and w.y == self.waypoint.y
        ][0]
        logging.debug(f"waypoint index: {waypoint_index}")
        for flight in self.package.flights:

            # found a flight with the same target (aka ingress) waypoint
            if (
                flight.points[waypoint_index].x == self.waypoint.x
                and flight.points[waypoint_index].y == self.waypoint.y
            ):
                strike_flights_ahead += 1

            # found self's flight
            if self.flight == flight:
                strike_flights_ahead -= 1
                break

        logging.debug(f"strike_flights_ahead: {strike_flights_ahead}")
        logging.debug(f"targets: {len(self.waypoint.targets)}")

        if strike_flights_ahead > 0:
            # ex. shifts [0, 1, 2] to [2, 0, 1]
            start_index = strike_flights_ahead * 2
            targets = [self.waypoint.targets[start_index]]
            targets += self.waypoint.targets[start_index + 1 :]
            targets += self.waypoint.targets[:start_index]
            logging.info(
                f"Shifting strike targets to {[self.waypoint.targets.index(t) + 1 for t in targets]}"
            )
        else:
            # not shifting if no strike flights counted ahead of this flight
            targets = [t for t in self.waypoint.targets]

        for target in targets:
            bombing = Bombing(target.position, weapon_type=WeaponType.Auto)
            # If there is only one target, drop all ordnance in one pass.
            if len(self.waypoint.targets) == 1:
                bombing.params["expend"] = "All"
            bombing.params["groupAttack"] = True
            waypoint.tasks.append(bombing)

            # Register special waypoints
            self.register_special_waypoints(self.waypoint.targets)
