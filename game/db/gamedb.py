from typing import TYPE_CHECKING

from .database import Database

if TYPE_CHECKING:
    from game.ato import Flight
    from game.theater import FrontLine, TheaterGroundObject


class GameDb:
    def __init__(self) -> None:
        self.flights: Database[Flight] = Database()
        self.front_lines: Database[FrontLine] = Database()
        self.tgos: Database[TheaterGroundObject] = Database()
