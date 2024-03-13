from __future__ import annotations

from typing import Callable, TYPE_CHECKING

from game.theater import ControlPoint, MissionTarget, TheaterGroundObject

if TYPE_CHECKING:
    from game import Game
    from qt_ui.models import GameModel


class GameContext:
    _game_model: GameModel

    @classmethod
    def set_model(cls, game_model: GameModel) -> None:
        cls._game_model = game_model

    @classmethod
    def get(cls) -> Game | None:
        return cls._game_model.game

    @classmethod
    def require(cls) -> Game:
        if cls._game_model.game is None:
            raise RuntimeError("GameContext has no Game set")
        return cls._game_model.game

    @classmethod
    def get_model(cls) -> GameModel:
        return cls._game_model


class QtCallbacks:
    def __init__(
        self,
        create_new_package: Callable[[MissionTarget], None],
        show_tgo_info: Callable[[TheaterGroundObject], None],
        show_control_point_info: Callable[[ControlPoint], None],
    ) -> None:
        self.create_new_package = create_new_package
        self.show_tgo_info = show_tgo_info
        self.show_control_point_info = show_control_point_info


class QtContext:
    _callbacks: QtCallbacks

    @classmethod
    def set_callbacks(cls, callbacks: QtCallbacks) -> None:
        cls._callbacks = callbacks

    @classmethod
    def get(cls) -> QtCallbacks:
        if cls._callbacks is None:
            raise RuntimeError("QtContext has no callbacks set")
        return cls._callbacks
