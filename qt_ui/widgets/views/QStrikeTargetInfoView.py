import random

from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import (
    QGroupBox,
    QLabel,
    QWidget,
    QVBoxLayout,
    QListView,
    QAbstractItemView,
)

from qt_ui.widgets.combos.QStrikeTargetSelectionComboBox import StrikeTargetInfo


class QStrikeTargetInfoView(QGroupBox):
    """
    UI Component to display info about a strike target
    """

    def __init__(self, strike_target_infos: StrikeTargetInfo):

        if strike_target_infos is None:
            strike_target_infos = StrikeTargetInfo()

        super(QStrikeTargetInfoView, self).__init__(
            "Target : " + strike_target_infos.name
        )

        self.strike_target_infos = strike_target_infos

        self.listView = QListView()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.listView)
        self.setLayout(layout)

    def setTarget(self, target):

        self.setTitle(target.name)
        self.strike_target_infos = target
        model = QStandardItemModel()
        self.listView.setSelectionMode(QAbstractItemView.NoSelection)

        if len(self.strike_target_infos.units) > 0:
            dic = {}
            for u in self.strike_target_infos.units:
                if u.type in dic.keys():
                    dic[u.type] = dic[u.type] + 1
                else:
                    dic[u.type] = 1
            for k, v in dic.items():
                model.appendRow(QStandardItem(k + " x " + str(v)))
                print(k + " x " + str(v))
        else:
            dic = {}
            for b in self.strike_target_infos.buildings:
                id = b.dcs_identifier
                if b.is_dead:
                    id = id + "[Destroyed]"
                if id in dic.keys():
                    dic[id] = dic[id] + 1
                else:
                    dic[id] = 1
            for k, v in dic.items():
                model.appendRow(QStandardItem(k + " x " + str(v)))
                print(k + " x " + str(v))

        self.listView.setModel(model)
