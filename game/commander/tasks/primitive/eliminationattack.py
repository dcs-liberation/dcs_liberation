from __future__ import annotations

from game.commander.tasks.frontlinestancetask import FrontLineStanceTask
from game.ground_forces.combat_stance import CombatStance


class EliminationAttack(FrontLineStanceTask):
    @property
    def stance(self) -> CombatStance:
        return CombatStance.ELIMINATION

    @property
    def have_sufficient_front_line_advantage(self) -> bool:
        return self.ground_force_balance >= 1.5
