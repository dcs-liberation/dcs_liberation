from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox

import qt_ui.uiconstants as CONST


class QBudgetBox(QGroupBox):
    """
    UI Component to display current budget and player's money
    """

    def __init__(self):
        super(QBudgetBox, self).__init__("Budget")

        self.money_icon = QLabel()
        self.money_icon.setPixmap(CONST.ICONS["Money"])
        self.money_amount = QLabel()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.money_icon)
        self.layout.addWidget(self.money_amount)
        self.setLayout(self.layout)

    def setBudget(self, budget, reward):
        """
        Set the money amount to display
        :param budget: Current money available
        :param reward: Planned reward for next turn
        """
        self.money_amount.setText(str(budget) + "M (+" + str(reward) + "M)")