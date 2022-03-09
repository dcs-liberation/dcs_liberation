from __future__ import annotations

import logging
from typing import Type

from game.theater import Airfield
from .formationattack import FormationAttackBuilder, FormationAttackFlightPlan
from .invalidobjectivelocation import InvalidObjectiveLocation
from ..flightwaypointtype import FlightWaypointType


class OcaAircraftFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[OcaAircraftFlightPlan]):
    def build(self) -> FormationAttackFlightPlan:
        location = self.package.target

        if not isinstance(location, Airfield):
            logging.exception(
                f"Invalid Objective Location for OCA/Aircraft flight "
                f"{self.flight=} at {location=}."
            )
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(
            OcaAircraftFlightPlan, FlightWaypointType.INGRESS_OCA_AIRCRAFT
        )
