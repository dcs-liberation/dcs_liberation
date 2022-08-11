from __future__ import annotations

from datetime import timedelta
from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .. import Flight
from ..flightwaypointtype import FlightWaypointType


class SeadFlightPlan(FormationAttackFlightPlan):
    def __init__(self, flight: Flight, layout: FormationAttackLayout) -> None:
        super().__init__(flight, layout)

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def lead_time(self) -> timedelta:
        return timedelta(minutes=1)


class Builder(FormationAttackBuilder[SeadFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_SEAD)

    def build(self) -> SeadFlightPlan:
        return SeadFlightPlan(self.flight, self.layout())
