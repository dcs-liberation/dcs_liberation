from PySide2.QtGui import QStandardItem, QStandardItemModel

from game import Game
from qt_ui.widgets.combos.QFilteredComboBox import QFilteredComboBox


class StrikeTargetInfo:

    def __init__(self):
        self.name = ""
        self.location = None
        self.units = []
        self.buildings = []


class QStrikeTargetSelectionComboBox(QFilteredComboBox):

    def __init__(self, game: Game, parent=None):
        super(QStrikeTargetSelectionComboBox, self).__init__(parent)
        self.game = game
        self.find_possible_strike_targets()


        for t in self.targets:
            print(t.name + " - " + str(len(t.units)) + " " + str(len(t.buildings)))


    def get_selected_target(self) -> StrikeTargetInfo:
        n = self.currentText()
        for target in self.targets:
            if target.name == n:
                return target

    def find_possible_strike_targets(self):

        self.targets = []
        i = 0
        model = QStandardItemModel()

        def add_model_item(i, model, target):
            item = QStandardItem(target.name)
            model.setItem(i, 0, item)
            self.targets.append(target)
            return i + 1

        for cp in self.game.theater.controlpoints:
            if cp.captured: continue

            added_obj_names = []

            for g in cp.ground_objects:
                if g.obj_name in added_obj_names: continue

                target = StrikeTargetInfo()
                target.location = g
                target.name = g.obj_name

                if g.dcs_identifier == "AA":
                    target.name = g.obj_name + " [units]"
                    for group in g.groups:
                        for u in group.units:
                            target.units.append(u)
                else:
                    target.name = g.obj_name + " [" + g.category + "]"
                    for g2 in cp.ground_objects:
                        if g2 is not g and g2.obj_name == g.obj_name:
                            target.buildings.append(g2)

                i = add_model_item(i, model, target)
                added_obj_names.append(g.obj_name)

        self.setModel(model)


