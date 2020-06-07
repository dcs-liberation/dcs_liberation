import logging
import typing
from enum import IntEnum

from dcs.mission import Mission
from dcs.forcedoptions import ForcedOptions

from .conflictgen import *


class Labels(IntEnum):
    Off = 0
    Full = 1
    Abbreviated = 2
    Dot = 3


class ForcedOptionsGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def _set_options_view(self):

        if self.game.settings.map_coalition_visibility == ForcedOptions.Views.All:
            self.mission.forced_options.options_view = ForcedOptions.Views.All
        elif self.game.settings.map_coalition_visibility == ForcedOptions.Views.Allies:
            self.mission.forced_options.options_view = ForcedOptions.Views.Allies
        elif self.game.settings.map_coalition_visibility == ForcedOptions.Views.OnlyAllies:
            self.mission.forced_options.options_view = ForcedOptions.Views.OnlyAllies
        elif self.game.settings.map_coalition_visibility == ForcedOptions.Views.MyAircraft:
            self.mission.forced_options.options_view = ForcedOptions.Views.MyAircraft
        elif self.game.settings.map_coalition_visibility == ForcedOptions.Views.OnlyMap:
            self.mission.forced_options.options_view = ForcedOptions.Views.OnlyMap

    def _set_external_views(self):
        if not self.game.settings.external_views_allowed:
            self.mission.forced_options.external_views = self.game.settings.external_views_allowed

    def _set_labels(self):
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


        