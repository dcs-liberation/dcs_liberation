from PySide2.QtCore import QObject, Signal
from game import Game


class GameUpdateSignal(QObject):

    instance = None
    gameupdated = Signal(Game)

    def __init__(self):
        super(GameUpdateSignal, self).__init__()
        GameUpdateSignal.instance = self

    def updateGame(self, game: Game):
        self.gameupdated.emit(game)

    @staticmethod
    def get_instance():
        return GameUpdateSignal.instance
