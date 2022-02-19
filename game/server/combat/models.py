from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletLatLon, LeafletPoly, ShapelyUtil
from game.sim.combat import FrozenCombat
from game.sim.combat.aircombat import AirCombat
from game.sim.combat.atip import AtIp
from game.sim.combat.defendingsam import DefendingSam
from game.theater import ConflictTheater


class FrozenCombatJs(BaseModel):
    id: UUID
    flight_position: LeafletLatLon | None
    target_positions: list[LeafletLatLon] | None
    footprint: list[LeafletPoly] | None

    @staticmethod
    def for_combat(combat: FrozenCombat, theater: ConflictTheater) -> FrozenCombatJs:
        if isinstance(combat, AirCombat):
            return FrozenCombatJs(
                id=combat.id,
                flight_position=None,
                target_positions=None,
                footprint=ShapelyUtil.polys_to_leaflet(combat.footprint, theater),
            )
        if isinstance(combat, AtIp):
            return FrozenCombatJs(
                id=combat.id,
                flight_position=theater.point_to_ll(combat.flight.position()).as_list(),
                target_positions=[
                    theater.point_to_ll(combat.flight.package.target.position).as_list()
                ],
                footprint=None,
            )
        if isinstance(combat, DefendingSam):
            return FrozenCombatJs(
                id=combat.id,
                flight_position=theater.point_to_ll(combat.flight.position()).as_list(),
                target_positions=[
                    theater.point_to_ll(sam.position).as_list()
                    for sam in combat.air_defenses
                ],
                footprint=None,
            )
        raise NotImplementedError(f"Unhandled FrozenCombat type: {combat.__class__}")
