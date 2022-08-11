from __future__ import annotations

from typing import Type

from game.theater.theatergroundobject import TheaterGroundObject
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
    def schedule(self) -> BaiFlightPlan:
        return BaiFlightPlan(self.flight, self.layout)


class BaiFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @staticmethod
    def scheduler_type() -> Type[Scheduler]:
        return Scheduler


class Builder(FormationAttackBuilder[FormationAttackLayout]):
    def build(self) -> FormationAttackLayout:
        location = self.package.target

        from game.transfers import Convoy

        targets: list[StrikeTarget] = []
        if isinstance(location, TheaterGroundObject):
            for group in location.groups:
                if group.units:
                    targets.append(
                        StrikeTarget(f"{group.group_name} at {location.name}", group)
                    )
        elif isinstance(location, Convoy):
            targets.append(StrikeTarget(location.name, location))
        else:
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_BAI, targets)
