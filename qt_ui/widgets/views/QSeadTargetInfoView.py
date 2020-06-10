from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QListView, QAbstractItemView

from qt_ui.widgets.combos.QSEADTargetSelectionComboBox import SEADTargetInfo


class QSeadTargetInfoView(QGroupBox):
    """
    UI Component to display info about a sead target
    """

    def __init__(self, sead_target_infos: SEADTargetInfo):
        if sead_target_infos is None:
            sead_target_infos = SEADTargetInfo()
        super(QSeadTargetInfoView, self).__init__("Target : " + sead_target_infos.name)
        self.sead_target_infos = sead_target_infos
        self.radar_list = QListView()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.radar_list)
        self.setLayout(layout)

    def setTarget(self, target: SEADTargetInfo):
        self.setTitle(target.name)
        self.sead_target_infos = target
        radar_list_model = QStandardItemModel()
        self.radar_list.setSelectionMode(QAbstractItemView.NoSelection)
        for r in self.sead_target_infos.radars:
            radar_list_model.appendRow(QStandardItem(r.type))
        self.radar_list.setModel(radar_list_model)









