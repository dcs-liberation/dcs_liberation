from __future__ import annotations

from game.commander.tasks.frontlinestancetask import FrontLineStanceTask
from game.commander.theaterstate import TheaterState
from game.ground_forces.combat_stance import CombatStance


class BreakthroughAttack(FrontLineStanceTask):
    @property
    def stance(self) -> CombatStance:
        return CombatStance.BREAKTHROUGH

    @property
    def have_sufficient_front_line_advantage(self) -> bool:
        return self.ground_force_balance >= 2.0

    def opposing_battle_positions_eliminated(self, state: TheaterState) -> bool:
        battle_positions = state.enemy_battle_positions[self.enemy_cp]
        return not bool(battle_positions.blocking_capture)

    def preconditions_met(self, state: TheaterState) -> bool:
        if not super().preconditions_met(state):
            return False
        return self.opposing_battle_positions_eliminated(state)

    def apply_effects(self, state: TheaterState) -> None:
        super().apply_effects(state)
        state.active_front_lines.remove(self.front_line)
