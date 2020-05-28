from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QFrame, QSizePolicy

import qt_ui.uiconstants as CONST
from game.db import REWARDS, PLAYER_BUDGET_BASE
from game.game import Game


class QHorizontalSeparationLine(QFrame):

  def __init__(self):
    super().__init__()
    self.setMinimumWidth(1)
    self.setFixedHeight(20)
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

class QFinancesMenu(QDialog):

    def __init__(self, game: Game):
        super(QFinancesMenu, self).__init__()

        self.game = game
        self.setModal(True)
        self.setWindowTitle("Finances")
        self.setWindowIcon(CONST.ICONS["Money"])
        self.setMinimumSize(450, 200)

        reward = PLAYER_BUDGET_BASE * len(self.game.theater.player_points())
        layout = QGridLayout()
        layout.addWidget(QLabel("<b>Control Points</b>"), 0, 0)
        layout.addWidget(QLabel(str(len(self.game.theater.player_points())) + " bases x " + str(PLAYER_BUDGET_BASE) + "M"), 0, 1)
        layout.addWidget(QLabel(str(reward) + "M"), 0, 2)

        layout.addWidget(QHorizontalSeparationLine(), 1, 0, 1, 3)

        i = 2
        for cp in self.game.theater.player_points():
            obj_names = []
            [obj_names.append(ground_object.obj_name) for ground_object in cp.ground_objects if ground_object.obj_name not in obj_names]
            for obj_name in obj_names:
                reward = 0
                g = None
                cat = None
                number = 0
                for ground_object in cp.ground_objects:
                    if ground_object.obj_name != obj_name or ground_object.is_dead:
                        continue
                    else:
                        if g is None:
                            g = ground_object
                            cat = g.category
                        if cat in REWARDS.keys():
                            number = number + 1
                            reward += REWARDS[cat]

                if g is not None and cat in REWARDS.keys():
                    layout.addWidget(QLabel("<b>" + g.category.upper() + " [" + obj_name + "]</b>"), i, 0)
                    layout.addWidget(QLabel(str(number) + " buildings x " + str(REWARDS[cat]) + "M"), i, 1)
                    rlabel = QLabel(str(reward) + "M")
                    rlabel.setProperty("style", "green")
                    layout.addWidget(rlabel, i, 2)
                    i = i + 1

        self.setLayout(layout)

        layout.addWidget(QHorizontalSeparationLine(), i+1, 0, 1, 3)

        layout.addWidget(QLabel("<b>" + str(self.game.budget_reward_amount) + "M </b>"), i+2, 2)

