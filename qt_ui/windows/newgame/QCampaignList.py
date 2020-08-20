from PySide2 import QtGui
from PySide2.QtCore import QSize, QItemSelectionModel
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QListView, QAbstractItemView

from theater import caucasus, nevada, persiangulf, normandy, thechannel, syria
import qt_ui.uiconstants as CONST

CAMPAIGNS = [
    ("Caucasus - Western Georgia", caucasus.WesternGeorgia, "Terrain_Caucasus"),
    ("Caucasus - Russia Small", caucasus.RussiaSmall, "Terrain_Caucasus"),
    ("Caucasus - North Caucasus", caucasus.NorthCaucasus, "Terrain_Caucasus"),
    ("Caucasus - Full Map", caucasus.CaucasusTheater, "Terrain_Caucasus"),
    ("Nevada - North Nevada", nevada.NevadaTheater, "Terrain_Nevada"),
    ("Persian Gulf - Invasion of Iran", persiangulf.IranianCampaign, "Terrain_Persian_Gulf"),
    ("Persian Gulf - Invasion of Iran [Lite]", persiangulf.IranInvasionLite, "Terrain_Persian_Gulf"),
    ("Persian Gulf - Emirates", persiangulf.Emirates, "Terrain_Persian_Gulf"),
    ("Persian Gulf - Desert War", persiangulf.DesertWar, "Terrain_Persian_Gulf"),
    ("Persian Gulf - Full Map", persiangulf.PersianGulfTheater, "Terrain_Persian_Gulf"),

    ("Syria - Golan heights battle", syria.GolanHeights, "Terrain_Syria"),
    ("Syria - Invasion from Turkey", persiangulf.PersianGulfTheater, "Terrain_Syria"),
    ("Syria - Syrian Civil War", persiangulf.PersianGulfTheater, "Terrain_Syria"),
    ("Syria - War on Insurgents", persiangulf.PersianGulfTheater, "Terrain_Syria"),
    ("Syria - Full Map", persiangulf.PersianGulfTheater, "Terrain_Syria"),

    ("Normandy - Normandy", normandy.NormandyTheater, "Terrain_Normandy"),
    ("Normandy - Normandy Small", normandy.NormandySmall, "Terrain_Normandy"),
    ("The Channel - Battle of Britain", thechannel.BattleOfBritain, "Terrain_Channel"),
    ("The Channel - Dunkirk", thechannel.Dunkirk, "Terrain_Channel"),
]


class QCampaignItem(QStandardItem):

    def __init__(self, text, theater, icon):
        super(QCampaignItem, self).__init__()
        self.theater = theater
        self.setIcon(QtGui.QIcon(CONST.ICONS[icon]))
        self.setEditable(False)
        self.setText(text)

class QCampaignList(QListView):

    def __init__(self):
        super(QCampaignList, self).__init__()
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.setMinimumWidth(250)
        self.setMinimumHeight(350)
        self.campaigns = []
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setup_content()

    def setup_content(self):
        for i, campaign in enumerate(CAMPAIGNS):
            self.campaigns.append(campaign)
            item = QCampaignItem(*campaign)
            self.model.appendRow(item)
        self.setSelectedCampaign(0)
        self.repaint()

    def setSelectedCampaign(self, row):
        self.selectionModel().clearSelection()
        index = self.model.index(row, 0)
        if not index.isValid():
            index = self.model.index(0, 0)
        self.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select)
        self.repaint()

    def clear_layout(self):
        self.model.removeRows(0, self.model.rowCount())