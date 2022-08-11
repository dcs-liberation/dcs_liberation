from __future__ import annotations

import logging
from typing import Type

from game.theater import Airfield
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .ischeduler import IScheduler
from ..flightwaypointtype import FlightWaypointType


class Scheduler(IScheduler[FormationAttackLayout]):
    def schedule(self) -> OcaRunwayFlightPlan:
        return OcaRunwayFlightPlan(self.flight, self.layout)


class OcaRunwayFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @staticmethod
    def scheduler_type() -> Type[Scheduler]:
        return Scheduler


class Builder(FormationAttackBuilder[FormationAttackLayout]):
    def build(self) -> FormationAttackLayout:
        location = self.package.target

        if not isinstance(location, Airfield):
            logging.exception(
                f"Invalid Objective Location for OCA/Runway flight "
                f"{self.flight=} at {location=}."
            )
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_OCA_RUNWAY)
