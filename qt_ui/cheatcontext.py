from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING

from game.server import EventStream
from game.turnstate import TurnState
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.gameoverdialog import GameOverDialog

if TYPE_CHECKING:
    from game import Game
    from game.sim import GameUpdateEvents


@contextmanager
def game_state_modifying_cheat_context(game: Game) -> Iterator[GameUpdateEvents]:
    with EventStream.event_context() as events:
        yield events

        state = game.check_win_loss()
        if state is not TurnState.CONTINUE:
            dialog = GameOverDialog(won=state is TurnState.WIN)
            dialog.exec()
        else:
            game.initialize_turn(events)
            GameUpdateSignal.get_instance().updateGame(game)
