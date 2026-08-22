from abc import ABC
from datetime import datetime

from game.utils import Distance, Speed, knots, meters
from .patrolling import PatrollingFlightPlan, PatrollingLayout


class RefuelingFlightPlan(PatrollingFlightPlan[PatrollingLayout], ABC):
    @property
    def patrol_speed(self) -> Speed:
        # TODO: Could use self.flight.unit_type.preferred_patrol_speed(altitude).
        if self.flight.unit_type.patrol_speed is not None:
            return self.flight.unit_type.patrol_speed
        # ~280 knots IAS at 21000.
        return knots(400)

    @property
    def engagement_distance(self) -> Distance:
        # TODO: Factor out a common base of the combat and non-combat race-tracks.
        # No harm in setting this, but we ought to clean up a bit.
        return meters(0)

    @property
    def first_pre_mission_aar_time(self) -> datetime | None:
        coalition = getattr(self.flight, "coalition", None)
        ato = getattr(coalition, "ato", None)
        packages = getattr(ato, "packages", [self.package])

        first_pre_refuel: datetime | None = None
        for package in packages:
            for flight in package.flights:
                if flight == self.flight:
                    continue
                flight_plan = getattr(flight, "flight_plan", None)
                if flight_plan is None:
                    continue
                pre_refuel = getattr(flight_plan.layout, "pre_refuel", None)
                if pre_refuel is None:
                    continue
                arrival_time = flight_plan.tot_for_waypoint(pre_refuel)
                if arrival_time is None:
                    continue
                if first_pre_refuel is None or arrival_time < first_pre_refuel:
                    first_pre_refuel = arrival_time
        return first_pre_refuel
