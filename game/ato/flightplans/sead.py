from __future__ import annotations

from datetime import timedelta
from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from ..flightwaypointtype import FlightWaypointType


class SeadFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def default_tot_offset(self) -> timedelta:
        return -timedelta(minutes=1)


class Builder(FormationAttackBuilder[SeadFlightPlan, FormationAttackLayout]):
    def layout(self,dump_debug_info: bool) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_SEAD, dump_debug_info)

    def build(self, dump_debug_info: bool = False) -> SeadFlightPlan:
        return SeadFlightPlan(self.flight, self.layout(dump_debug_info))
