from __future__ import annotations

from typing import Type

from game.theater import NavalControlPoint
from game.theater.theatergroundobject import NavalGroundObject
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .waypointbuilder import StrikeTarget
from ..flightwaypointtype import FlightWaypointType


class AntiShipFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[AntiShipFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        location = self.package.target

        from game.transfers import CargoShip

        if isinstance(location, NavalControlPoint):
            targets = self.anti_ship_targets_for_tgo(location.find_main_tgo())
        elif isinstance(location, NavalGroundObject):
            targets = self.anti_ship_targets_for_tgo(location)
        elif isinstance(location, CargoShip):
            targets = [StrikeTarget(location.name, location)]
        else:
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_BAI, targets)

    @staticmethod
    def anti_ship_targets_for_tgo(tgo: NavalGroundObject) -> list[StrikeTarget]:
        return [StrikeTarget(f"{g.group_name} at {tgo.name}", g) for g in tgo.groups]

    def build(self) -> AntiShipFlightPlan:
        return AntiShipFlightPlan(self.flight, self.layout())
