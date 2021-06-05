from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Union, Tuple

import packaging.version
from PySide2 import QtGui
from PySide2.QtCore import QItemSelectionModel, QModelIndex, Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QAbstractItemView, QListView

import qt_ui.uiconstants as CONST
from game.theater import ConflictTheater
from game.version import CAMPAIGN_FORMAT_VERSION

PERF_FRIENDLY = 0
PERF_MEDIUM = 1
PERF_HARD = 2
PERF_NASA = 3


@dataclass(frozen=True)
class Campaign:
    name: str
    icon_name: str
    authors: str
    description: str

    #: The revision of the campaign format the campaign was built for. We do not attempt
    #: to migrate old campaigns, but this is used to show a warning in the UI when
    #: selecting a campaign that is not up to date.
    version: Tuple[int, int]

    recommended_player_faction: str
    recommended_enemy_faction: str
    performance: Union[PERF_FRIENDLY, PERF_MEDIUM, PERF_HARD, PERF_NASA]
    data: Dict[str, Any]
    path: Path

    @classmethod
    def from_json(cls, path: Path) -> Campaign:
        with path.open() as campaign_file:
            data = json.load(campaign_file)

        sanitized_theater = data["theater"].replace(" ", "")
        version_field = data.get("version", "0")
        try:
            version = packaging.version.parse(version_field)
        except TypeError:
            logging.warning(
                f"Non-string campaign version in {path}. Parse may be incorrect."
            )
            version = packaging.version.parse(str(version_field))
        return cls(
            data["name"],
            f"Terrain_{sanitized_theater}",
            data.get("authors", "???"),
            data.get("description", ""),
            (version.major, version.minor),
            data.get("recommended_player_faction", "USA 2005"),
            data.get("recommended_enemy_faction", "Russia 1990"),
            data.get("performance", 0),
            data,
            path,
        )

    def load_theater(self) -> ConflictTheater:
        return ConflictTheater.from_json(self.path.parent, self.data)

    @property
    def is_out_of_date(self) -> bool:
        """Returns True if this campaign is not up to date with the latest format.

        This is more permissive than is_from_future, which is sensitive to minor version
        bumps (the old game definitely doesn't support the minor features added in the
        new version, and the campaign may require them. However, the minor version only
        indicates *optional* new features, so we do not need to mark out of date
        campaigns as incompatible if they are within the same major version.
        """
        return self.version[0] < CAMPAIGN_FORMAT_VERSION[0]

    @property
    def is_from_future(self) -> bool:
        """Returns True if this campaign is newer than the supported format."""
        return self.version > CAMPAIGN_FORMAT_VERSION

    @property
    def is_compatible(self) -> bool:
        """Returns True is this campaign was built for this version of the game."""
        if not self.version:
            return False
        if self.is_out_of_date:
            return False
        if self.is_from_future:
            return False
        return True


def load_campaigns() -> List[Campaign]:
    campaign_dir = Path("resources\\campaigns")
    campaigns = []
    for path in campaign_dir.glob("*.json"):
        try:
            logging.debug(f"Loading campaign from {path}...")
            campaign = Campaign.from_json(path)
            campaigns.append(campaign)
        except RuntimeError:
            logging.exception(f"Unable to load campaign from {path}")

    return sorted(campaigns, key=lambda x: x.name)


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
    def selected_campaign(self) -> Campaign:
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
