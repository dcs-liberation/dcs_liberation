from game import Game
from qt_ui.models import GameModel


class GameContext:
    _game_model: GameModel

    @classmethod
    def set_model(cls, game_model: GameModel) -> None:
        cls._game_model = game_model

    @classmethod
    def get(cls) -> Game:
        if cls._game_model.game is None:
            raise RuntimeError("GameContext has no Game set")
        return cls._game_model.game

    @classmethod
    def get_model(cls) -> GameModel:
        return cls._game_model
