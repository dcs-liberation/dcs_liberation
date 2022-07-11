from __future__ import annotations

from datetime import timedelta
from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .ischeduler import IScheduler
from .. import ScheduledFlight
from ..flightwaypointtype import FlightWaypointType


class Scheduler(IScheduler[FormationAttackLayout]):
    def schedule(self) -> SeadFlightPlan:
        return SeadFlightPlan(self.flight, self.layout)


class SeadFlightPlan(FormationAttackFlightPlan):
    def __init__(self, flight: ScheduledFlight, layout: FormationAttackLayout) -> None:
        super().__init__(flight, layout)

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @staticmethod
    def scheduler_type() -> Type[Scheduler]:
        return Scheduler

    @property
    def lead_time(self) -> timedelta:
        return timedelta(minutes=1)


class Builder(FormationAttackBuilder[FormationAttackLayout]):
    def build(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_SEAD)
