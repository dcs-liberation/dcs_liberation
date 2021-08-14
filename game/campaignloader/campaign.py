from __future__ import annotations

import json
import logging
from collections import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, Any

from packaging.version import Version
import yaml

from game.campaignloader.mizcampaignloader import MizCampaignLoader
from game.profiling import logged_duration
from game.theater import (
    ConflictTheater,
    CaucasusTheater,
    NevadaTheater,
    PersianGulfTheater,
    NormandyTheater,
    TheChannelTheater,
    SyriaTheater,
    MarianaIslandsTheater,
)
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
    performance: int
    data: Dict[str, Any]
    path: Path

    @classmethod
    def from_file(cls, path: Path) -> Campaign:
        with path.open() as campaign_file:
            if path.suffix == ".yaml":
                data = yaml.safe_load(campaign_file)
            else:
                data = json.load(campaign_file)

        sanitized_theater = data["theater"].replace(" ", "")
        version_field = data.get("version", "0")
        try:
            version = Version(version_field)
        except TypeError:
            logging.warning(
                f"Non-string campaign version in {path}. Parse may be incorrect."
            )
            version = Version(str(version_field))
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
        theaters = {
            "Caucasus": CaucasusTheater,
            "Nevada": NevadaTheater,
            "Persian Gulf": PersianGulfTheater,
            "Normandy": NormandyTheater,
            "The Channel": TheChannelTheater,
            "Syria": SyriaTheater,
            "MarianaIslands": MarianaIslandsTheater,
        }
        theater = theaters[self.data["theater"]]
        t = theater()

        try:
            miz = self.data["miz"]
        except KeyError as ex:
            raise RuntimeError(
                "Old format (non-miz) campaigns are no longer supported."
            ) from ex

        with logged_duration("Importing miz data"):
            MizCampaignLoader(self.path.parent / miz, t).populate_theater()
        return t

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
        if self.version == (0, 0):
            return False
        if self.is_out_of_date:
            return False
        if self.is_from_future:
            return False
        return True

    @staticmethod
    def iter_campaign_defs() -> Iterator[Path]:
        campaign_dir = Path("resources/campaigns")
        yield from campaign_dir.glob("*.json")
        yield from campaign_dir.glob("*.yaml")

    @classmethod
    def load_each(cls) -> Iterator[Campaign]:
        for path in cls.iter_campaign_defs():
            try:
                logging.debug(f"Loading campaign from {path}...")
                campaign = Campaign.from_file(path)
                yield campaign
            except RuntimeError:
                logging.exception(f"Unable to load campaign from {path}")
