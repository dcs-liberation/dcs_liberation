from __future__ import annotations

import logging
from typing import Type

from game.theater.theatergroundobject import (
    EwrGroundObject,
    SamGroundObject,
)
from .formationattack import FormationAttackBuilder, FormationAttackFlightPlan
from .invalidobjectivelocation import InvalidObjectiveLocation
from ..flightwaypointtype import FlightWaypointType


class DeadFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[DeadFlightPlan]):
    def build(self) -> FormationAttackFlightPlan:
        location = self.package.target

        is_ewr = isinstance(location, EwrGroundObject)
        is_sam = isinstance(location, SamGroundObject)
        if not is_ewr and not is_sam:
            logging.exception(
                f"Invalid Objective Location for DEAD flight {self.flight=} at "
                f"{location=}"
            )
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(DeadFlightPlan, FlightWaypointType.INGRESS_DEAD)
