import datetime
from typing import cast

import pytest

from game import Game


class StubGame:
    def __init__(self) -> None:
        self.date = datetime.date.min


@pytest.fixture
def game() -> Game:
    return cast(Game, StubGame())
