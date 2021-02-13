from PySide2.QtWidgets import QComboBox

from game.theater import CombatStance, ControlPoint


class QGroundForcesStrategySelector(QComboBox):
    def __init__(self, cp: ControlPoint, enemy_cp: ControlPoint):
        super(QGroundForcesStrategySelector, self).__init__()
        self.cp = cp
        self.enemy_cp = enemy_cp

        if enemy_cp.id not in self.cp.stances:
            self.cp.stances[enemy_cp.id] = CombatStance.DEFENSIVE

        for i, stance in enumerate(CombatStance):
            self.addItem(stance.name, userData=stance)
            if self.cp.stances[enemy_cp.id] == stance:
                self.setCurrentIndex(i)

        self.currentTextChanged.connect(self.on_change)

    def on_change(self):
        print(self.currentData())
        self.cp.stances[self.enemy_cp.id] = self.currentData()
