from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from dcs.mission import Mission

if TYPE_CHECKING:
    from game.game import Game


class Labels(IntEnum):
    Off = 0
    Full = 1
    Abbreviated = 2
    Dot = 3


class ForcedOptionsGenerator:
    def __init__(self, mission: Mission, game: Game) -> None:
        self.mission = mission
        self.game = game

    def _set_options_view(self) -> None:
        self.mission.forced_options.options_view = self.game.settings.map_coalition_visibility

    def _set_external_views(self) -> None:
        if not self.game.settings.external_views_allowed:
            self.mission.forced_options.external_views = self.game.settings.external_views_allowed

    def _set_labels(self) -> None:
        if self.game.settings.labels == "Abbreviated":
            self.mission.forced_options.labels = int(Labels.Abbreviated)
        elif self.game.settings.labels == "Dot Only":
            self.mission.forced_options.labels = int(Labels.Dot)
        elif self.game.settings.labels == "Off":
            self.mission.forced_options.labels = int(Labels.Off)

    def generate(self):
        self._set_options_view()
        self._set_external_views()
        self._set_labels()


        