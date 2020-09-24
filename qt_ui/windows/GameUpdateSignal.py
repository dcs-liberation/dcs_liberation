from PySide2.QtCore import QObject, Signal

from game import Game
from game.event import Event, Debriefing


class DebriefingSignal:

    def __init__(self, game, gameEvent, debriefing):
        self.game = game
        self.gameEvent = gameEvent
        self.debriefing = debriefing


class GameUpdateSignal(QObject):

    instance = None
    gameupdated = Signal(Game)
    budgetupdated = Signal(Game)
    debriefingReceived = Signal(DebriefingSignal)

    def __init__(self):
        super(GameUpdateSignal, self).__init__()
        GameUpdateSignal.instance = self

    def updateGame(self, game: Game):
        self.gameupdated.emit(game)

    def updateBudget(self, game: Game):
        self.budgetupdated.emit(game)

    def sendDebriefing(self, game: Game, gameEvent: Event, debriefing: Debriefing):
        sig = DebriefingSignal(game, gameEvent, debriefing)
        self.gameupdated.emit(game)
        self.debriefingReceived.emit(sig)

    @staticmethod
    def get_instance():
        return GameUpdateSignal.instance
