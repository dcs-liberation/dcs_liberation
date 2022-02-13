from game import Game


class GameContext:
    _game: Game | None

    @classmethod
    def set(cls, game: Game | None) -> None:
        cls._game = game

    @classmethod
    def get(cls) -> Game:
        if cls._game is None:
            raise RuntimeError("GameContext has no Game set")
        return cls._game
