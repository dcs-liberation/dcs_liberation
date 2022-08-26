from __future__ import annotations

from typing import Type

from game.theater import TheaterGroundObject
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .waypointbuilder import StrikeTarget
from ..flightwaypointtype import FlightWaypointType


class StrikeFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[StrikeFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        location = self.package.target

        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        targets: list[StrikeTarget] = []
        for idx, unit in enumerate(location.strike_targets):
            targets.append(StrikeTarget(f"{unit.type.id} #{idx}", unit))

        return self._build(FlightWaypointType.INGRESS_STRIKE, targets)

    def build(self) -> StrikeFlightPlan:
        return StrikeFlightPlan(self.flight, self.layout())
