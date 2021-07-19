from __future__ import annotations

from game.commander.tasks.frontlinestancetask import FrontLineStanceTask
from game.commander.theaterstate import TheaterState
from gen.ground_forces.combat_stance import CombatStance


class BreakthroughAttack(FrontLineStanceTask):
    @property
    def stance(self) -> CombatStance:
        return CombatStance.BREAKTHROUGH

    @property
    def have_sufficient_front_line_advantage(self) -> bool:
        return self.ground_force_balance >= 2.0

    def opposing_garrisons_eliminated(self, state: TheaterState) -> bool:
        garrisons = state.enemy_garrisons[self.enemy_cp]
        return not bool(garrisons.blocking_capture)

    def preconditions_met(self, state: TheaterState) -> bool:
        if not super().preconditions_met(state):
            return False
        return self.opposing_garrisons_eliminated(state)

    def apply_effects(self, state: TheaterState) -> None:
        super().apply_effects(state)
        state.active_front_lines.remove(self.front_line)
