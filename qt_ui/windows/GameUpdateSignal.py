from __future__ import annotations

from typing import Optional

from PySide2.QtCore import QObject, Signal

from game import Game
from game.debriefing import Debriefing


class GameUpdateSignal(QObject):

    instance = None
    gameupdated = Signal(Game)
    budgetupdated = Signal(Game)
    debriefingReceived = Signal(Debriefing)

    game_loaded = Signal(Game)

    flight_paths_changed = Signal()
    package_selection_changed = Signal(int)  # -1 indicates no selection.
    flight_selection_changed = Signal(int)  # -1 indicates no selection.

    def __init__(self):
        super(GameUpdateSignal, self).__init__()
        GameUpdateSignal.instance = self

        self.game_loaded.connect(self.updateGame)

    def select_package(self, index: Optional[int]) -> None:
        # noinspection PyUnresolvedReferences
        self.package_selection_changed.emit(-1 if index is None else index)

    def select_flight(self, index: Optional[int]) -> None:
        # noinspection PyUnresolvedReferences
        self.flight_selection_changed.emit(-1 if index is None else index)

    def redraw_flight_paths(self) -> None:
        # noinspection PyUnresolvedReferences
        self.flight_paths_changed.emit()

    def updateGame(self, game: Optional[Game]):
        # noinspection PyUnresolvedReferences
        self.gameupdated.emit(game)

    def updateBudget(self, game: Game):
        # noinspection PyUnresolvedReferences
        self.budgetupdated.emit(game)

    def sendDebriefing(self, debriefing: Debriefing) -> None:
        # noinspection PyUnresolvedReferences
        self.debriefingReceived.emit(debriefing)

    @staticmethod
    def get_instance() -> GameUpdateSignal:
        return GameUpdateSignal.instance
