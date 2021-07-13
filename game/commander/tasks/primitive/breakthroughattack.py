from __future__ import annotations

from game.commander.tasks.frontlinestancetask import FrontLineStanceTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint
from game.theater.theatergroundobject import VehicleGroupGroundObject
from game.utils import meters
from gen.ground_forces.combat_stance import CombatStance


class BreakthroughAttack(FrontLineStanceTask):
    @property
    def stance(self) -> CombatStance:
        return CombatStance.BREAKTHROUGH

    @property
    def have_sufficient_front_line_advantage(self) -> bool:
        return self.ground_force_balance >= 1.2

    @property
    def opposing_garrisons_eliminated(self) -> bool:
        # TODO: Should operate on TheaterState to account for BAIs planned this turn.
        for tgo in self.enemy_cp.ground_objects:
            if not isinstance(tgo, VehicleGroupGroundObject):
                continue
            if meters(tgo.distance_to(self.enemy_cp)) < ControlPoint.CAPTURE_DISTANCE:
                return False
        return True

    def preconditions_met(self, state: TheaterState) -> bool:
        if not super().preconditions_met(state):
            return False
        return self.opposing_garrisons_eliminated

    def apply_effects(self, state: TheaterState) -> None:
        super().apply_effects(state)
        state.active_front_lines.remove(self.front_line)
