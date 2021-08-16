from __future__ import annotations

from typing import Optional

from PySide2 import QtGui
from PySide2.QtCore import QItemSelectionModel, QModelIndex, Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QAbstractItemView, QListView

import qt_ui.uiconstants as CONST
from game.campaignloader.campaign import Campaign


class QCampaignItem(QStandardItem):
    def __init__(self, campaign: Campaign) -> None:
        super(QCampaignItem, self).__init__()
        self.setData(campaign, QCampaignList.CampaignRole)
        self.setIcon(QtGui.QIcon(CONST.ICONS[campaign.icon_name]))
        self.setEditable(False)
        if campaign.is_compatible:
            name = campaign.name
        else:
            name = f"[INCOMPATIBLE] {campaign.name}"
        self.setText(name)


class QCampaignList(QListView):
    CampaignRole = Qt.UserRole

    def __init__(self, campaigns: list[Campaign], show_incompatible: bool) -> None:
        super(QCampaignList, self).__init__()
        self.campaign_model = QStandardItemModel(self)
        self.setModel(self.campaign_model)
        self.setMinimumWidth(250)
        self.setMinimumHeight(350)
        self.campaigns = campaigns
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setup_content(show_incompatible)

    @property
    def selected_campaign(self) -> Optional[Campaign]:
        return self.currentIndex().data(QCampaignList.CampaignRole)

    def setup_content(self, show_incompatible: bool) -> None:
        self.selectionModel().blockSignals(True)
        try:
            self.campaign_model.clear()
            for campaign in self.campaigns:
                if show_incompatible or campaign.is_compatible:
                    item = QCampaignItem(campaign)
                    self.campaign_model.appendRow(item)
        finally:
            self.selectionModel().blockSignals(False)

        self.selectionModel().setCurrentIndex(
            self.campaign_model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
        )
