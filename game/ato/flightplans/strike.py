from __future__ import annotations

from typing import Type

from game.theater import TheaterGroundObject
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .ischeduler import IScheduler
from .waypointbuilder import StrikeTarget
from ..flightwaypointtype import FlightWaypointType


class Scheduler(IScheduler[FormationAttackLayout]):
    def schedule(self) -> StrikeFlightPlan:
        return StrikeFlightPlan(self.flight, self.layout)


class StrikeFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @staticmethod
    def scheduler_type() -> Type[Scheduler]:
        return Scheduler


class Builder(FormationAttackBuilder[FormationAttackLayout]):
    def build(self) -> FormationAttackLayout:
        location = self.package.target

        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        targets: list[StrikeTarget] = []
        for idx, unit in enumerate(location.strike_targets):
            targets.append(StrikeTarget(f"{unit.type.id} #{idx}", unit))

        return self._build(FlightWaypointType.INGRESS_STRIKE, targets)
