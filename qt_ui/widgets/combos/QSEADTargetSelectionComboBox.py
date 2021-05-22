from PySide2.QtGui import QStandardItem, QStandardItemModel

from game import Game
from gen import db
from qt_ui.widgets.combos.QFilteredComboBox import QFilteredComboBox


class SEADTargetInfo:
    def __init__(self):
        self.name = ""
        self.location = None
        self.radars = []
        self.threat_range = 0
        self.detection_range = 0


class QSEADTargetSelectionComboBox(QFilteredComboBox):
    def __init__(self, game: Game, parent=None):
        super(QSEADTargetSelectionComboBox, self).__init__(parent)
        self.game = game
        self.find_possible_sead_targets()

    def get_selected_target(self) -> SEADTargetInfo:
        n = self.currentText()
        for target in self.targets:
            if target.name == n:
                return target

    def find_possible_sead_targets(self):

        self.targets = []
        i = 0
        model = QStandardItemModel()

        def add_model_item(i, model, target):
            item = QStandardItem(target.name)
            model.setItem(i, 0, item)
            self.targets.append(target)
            return i + 1

        for cp in self.game.theater.controlpoints:
            if cp.captured:
                continue
            for g in cp.ground_objects:

                radars = []
                max_detection_range = 0
                threat_range = 0
                if g.dcs_identifier == "AA":
                    for group in g.groups:
                        for u in group.units:
                            utype = db.unit_type_from_name(u.type)
                            detection_range = getattr(utype, "detection_range", 0)
                            if detection_range > 1000:
                                max_detection_range = max(
                                    detection_range, max_detection_range
                                )
                            radars.append(u)

                            if hasattr(utype, "threat_range"):
                                if utype.threat_range > threat_range:
                                    threat_range = utype.threat_range
                    if len(radars) > 0:
                        tgt_info = SEADTargetInfo()
                        tgt_info.name = (
                            g.obj_name
                            + " ["
                            + ",".join(
                                [db.unit_type_from_name(u.type).id for u in radars]
                            )
                            + " ]"
                        )
                        if len(tgt_info.name) > 25:
                            tgt_info.name = (
                                g.obj_name + " [" + str(len(radars)) + " units]"
                            )
                        tgt_info.radars = radars
                        tgt_info.location = g
                        tgt_info.threat_range = threat_range
                        tgt_info.detection_range = max_detection_range
                        i = add_model_item(i, model, tgt_info)

        self.setModel(model)
