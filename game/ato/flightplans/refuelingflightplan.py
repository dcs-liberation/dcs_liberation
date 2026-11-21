from __future__ import annotations

from abc import ABC
from collections.abc import Iterable
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from game.utils import Distance, Speed, knots, meters
from .patrolling import PatrollingFlightPlan, PatrollingLayout

if TYPE_CHECKING:
    from game.ato.package import Package


class RefuelingFlightPlan(PatrollingFlightPlan[PatrollingLayout], ABC):
    PRE_MISSION_AAR_TANKER_LEAD_TIME = timedelta(minutes=5)

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

    def pre_mission_aar_packages(self) -> Iterable[Package]:
        return [self.package]

    @property
    def first_pre_mission_aar_time(self) -> datetime | None:
        if getattr(self, "_checking_pre_mission_aar_time", False):
            self._pre_mission_aar_time_reentered = True
            return None

        self._checking_pre_mission_aar_time = True
        first_pre_refuel: datetime | None = None
        try:
            for package in self.pre_mission_aar_packages():
                for flight in package.flights:
                    if flight == self.flight:
                        continue
                    flight_plan = getattr(flight, "flight_plan", None)
                    if flight_plan is None:
                        continue
                    pre_refuel = getattr(flight_plan.layout, "pre_refuel", None)
                    if pre_refuel is None:
                        continue
                    self._pre_mission_aar_time_reentered = False
                    arrival_time = flight_plan.tot_for_waypoint(pre_refuel)
                    if self._pre_mission_aar_time_reentered:
                        continue
                    if arrival_time is None:
                        continue
                    if first_pre_refuel is None or arrival_time < first_pre_refuel:
                        first_pre_refuel = arrival_time
            return first_pre_refuel
        finally:
            self._checking_pre_mission_aar_time = False

    @property
    def pre_mission_aar_tanker_start_time(self) -> datetime | None:
        first_pre_refuel = self.first_pre_mission_aar_time
        if first_pre_refuel is None:
            return None
        return first_pre_refuel - self.PRE_MISSION_AAR_TANKER_LEAD_TIME
