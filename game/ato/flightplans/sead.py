from __future__ import annotations

from datetime import timedelta
from typing import Type

from .formationattack import FormationAttackBuilder, FormationAttackFlightPlan
from ..flightwaypointtype import FlightWaypointType


class SeadFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[SeadFlightPlan]):
    def build(self) -> FormationAttackFlightPlan:
        return self._build(
            SeadFlightPlan,
            FlightWaypointType.INGRESS_SEAD,
            lead_time=timedelta(minutes=1),
        )
