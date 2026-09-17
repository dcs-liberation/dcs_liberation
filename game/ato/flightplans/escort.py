from __future__ import annotations

from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .waypointbuilder import WaypointBuilder


class EscortFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[EscortFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        assert self.package.waypoints is not None

        builder = WaypointBuilder(self.flight, self.coalition)
        ingress, target = builder.escort(
            self.package.waypoints.ingress, self.package.target
        )
        hold = builder.hold(self._hold_point())
        join = builder.join(self.package.waypoints.join)
        split = builder.split(self.package.waypoints.split)
        refuel = builder.refuel(self.package.waypoints.refuel)
        nav_to = builder.nav_path(
            hold.position, join.position, self.doctrine.combat_altitude
        )
        pre_refuel = None
        nav_from_pre_refuel = []
        if self.flight.pre_mission_aar:
            pre_refuel = builder.pre_mission_aar(self.package.waypoints.refuel)
            nav_to = builder.nav_path(
                hold.position,
                pre_refuel.position,
                self.doctrine.combat_altitude,
            )
            nav_from_pre_refuel = builder.nav_path(
                pre_refuel.position,
                join.position,
                self.doctrine.combat_altitude,
            )

        return FormationAttackLayout(
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
            nav_to=nav_to,
            pre_refuel=pre_refuel,
            join=join,
            ingress=ingress,
            targets=[target],
            nav_from_pre_refuel=nav_from_pre_refuel,
            split=split,
            refuel=refuel,
            nav_from=builder.nav_path(
                refuel.position,
                self.flight.arrival.position,
                self.doctrine.combat_altitude,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self, dump_debug_info: bool = False) -> EscortFlightPlan:
        return EscortFlightPlan(self.flight, self.layout())
