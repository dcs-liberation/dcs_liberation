from __future__ import annotations

from typing import TYPE_CHECKING

from dcs.forcedoptions import ForcedOptions
from dcs.mission import Mission

if TYPE_CHECKING:
    from game.game import Game


class ForcedOptionsGenerator:
    def __init__(self, mission: Mission, game: Game) -> None:
        self.mission = mission
        self.game = game

    def _set_options_view(self) -> None:
        self.mission.forced_options.options_view = (
            self.game.settings.map_coalition_visibility
        )

    def _set_external_views(self) -> None:
        if not self.game.settings.external_views_allowed:
            self.mission.forced_options.external_views = (
                self.game.settings.external_views_allowed
            )

    def _set_easy_communication(self) -> None:
        self.mission.forced_options.easy_communication = (
            self.game.settings.easy_communication
        )

    def _set_labels(self) -> None:
        # TODO: Fix settings to use the real type.
        # TODO: Allow forcing "full" and have default do nothing.
        if self.game.settings.labels == "Abbreviated":
            self.mission.forced_options.labels = ForcedOptions.Labels.Abbreviate
        elif self.game.settings.labels == "Dot Only":
            self.mission.forced_options.labels = ForcedOptions.Labels.DotOnly
        elif self.game.settings.labels == "Neutral Dot":
            self.mission.forced_options.labels = ForcedOptions.Labels.NeutralDot
        elif self.game.settings.labels == "Off":
            self.mission.forced_options.labels = ForcedOptions.Labels.None_

    def _set_unrestricted_satnav(self) -> None:
        blue = self.game.blue.faction
        red = self.game.red.faction
        if blue.unrestricted_satnav or red.unrestricted_satnav:
            self.mission.forced_options.unrestricted_satnav = True

    def _set_battle_damage_assessment(self) -> None:
        self.mission.forced_options.battle_damage_assessment = (
            self.game.settings.battle_damage_assessment
        )

    def generate(self) -> None:
        self._set_options_view()
        self._set_external_views()
        self._set_easy_communication()
        self._set_labels()
        self._set_unrestricted_satnav()
        self._set_battle_damage_assessment()
