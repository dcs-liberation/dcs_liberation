from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint, LeafletPoly, ShapelyUtil
from game.sim.combat import FrozenCombat
from game.sim.combat.aircombat import AirCombat
from game.sim.combat.atip import AtIp
from game.sim.combat.defendingsam import DefendingSam
from game.theater import ConflictTheater


class FrozenCombatJs(BaseModel):
    id: UUID
    flight_position: LeafletPoint | None
    target_positions: list[LeafletPoint] | None
    footprint: list[LeafletPoly] | None

    class Config:
        title = "FrozenCombat"

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
                flight_position=combat.flight.position().latlng(),
                target_positions=[combat.flight.package.target.position.latlng()],
                footprint=None,
            )
        if isinstance(combat, DefendingSam):
            return FrozenCombatJs(
                id=combat.id,
                flight_position=combat.flight.position().latlng(),
                target_positions=[sam.position.latlng() for sam in combat.air_defenses],
                footprint=None,
            )
        raise NotImplementedError(f"Unhandled FrozenCombat type: {combat.__class__}")
