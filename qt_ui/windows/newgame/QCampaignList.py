import json
import logging
import os

from PySide2 import QtGui
from PySide2.QtCore import QSize, QItemSelectionModel
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QListView, QAbstractItemView

from theater import caucasus, nevada, persiangulf, normandy, thechannel, syria, ConflictTheater
import qt_ui.uiconstants as CONST

CAMPAIGN_DIR = ".\\resources\\campaigns"
CAMPAIGNS = []

# Load the campaigns files from the directory
campaign_files = os.listdir(CAMPAIGN_DIR)
for f in campaign_files:
    try:
        ff = os.path.join(CAMPAIGN_DIR, f)
        with open(ff, "r") as campaign_data:
            data = json.load(campaign_data)
            choice = (data["name"], ff, "Terrain_" + data["theater"].replace(" ", ""))
            logging.info("Loaded campaign : " + data["name"])
            CAMPAIGNS.append(choice)
            ConflictTheater.from_file(choice[1])
            logging.info("Loaded campaign :" + ff)
    except Exception as e:
        logging.info("Unable to load campaign :" + f)

class QCampaignItem(QStandardItem):

    def __init__(self, text, filename, icon):
        super(QCampaignItem, self).__init__()
        self.filename = filename
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