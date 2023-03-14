import datetime
from typing import cast

import pytest

from game import Game
from game.persistence import SaveManager


class StubGame:
    def __init__(self) -> None:
        self.date = datetime.date.min
        self.save_manager = SaveManager(cast(Game, self))


@pytest.fixture
def game() -> Game:
    return cast(Game, StubGame())
