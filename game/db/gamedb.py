from typing import TYPE_CHECKING

from .database import Database

if TYPE_CHECKING:
    from game.ato import Flight


class GameDb:
    def __init__(self) -> None:
        self.flights: Database[Flight] = Database()
