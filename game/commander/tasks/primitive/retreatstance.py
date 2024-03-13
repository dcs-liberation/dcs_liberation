from __future__ import annotations

from game.commander.tasks.frontlinestancetask import FrontLineStanceTask
from game.ground_forces.combat_stance import CombatStance


class RetreatStance(FrontLineStanceTask):
    @property
    def stance(self) -> CombatStance:
        return CombatStance.RETREAT

    @property
    def have_sufficient_front_line_advantage(self) -> bool:
        return True
