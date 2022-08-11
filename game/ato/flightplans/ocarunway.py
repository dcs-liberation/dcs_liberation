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
from ..flightwaypointtype import FlightWaypointType


class OcaRunwayFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[OcaRunwayFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        location = self.package.target

        if not isinstance(location, Airfield):
            logging.exception(
                f"Invalid Objective Location for OCA/Runway flight "
                f"{self.flight=} at {location=}."
            )
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_OCA_RUNWAY)

    def build(self) -> OcaRunwayFlightPlan:
        return OcaRunwayFlightPlan(self.flight, self.layout())
