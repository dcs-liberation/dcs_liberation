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


class OcaAircraftFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[OcaAircraftFlightPlan, FormationAttackLayout]):
    def layout(self, dump_debug_info: bool) -> FormationAttackLayout:
        location = self.package.target

        if not isinstance(location, Airfield):
            logging.exception(
                f"Invalid Objective Location for OCA/Aircraft flight "
                f"{self.flight=} at {location=}."
            )
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_OCA_AIRCRAFT, dump_debug_info)

    def build(self, dump_debug_info: bool = False) -> OcaAircraftFlightPlan:
        return OcaAircraftFlightPlan(self.flight, self.layout(dump_debug_info))
