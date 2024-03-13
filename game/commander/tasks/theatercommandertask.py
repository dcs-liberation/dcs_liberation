from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from game.commander.theaterstate import TheaterState
from game.htn import PrimitiveTask

if TYPE_CHECKING:
    from game.coalition import Coalition


class TheaterCommanderTask(PrimitiveTask[TheaterState]):
    @abstractmethod
    def execute(self, coalition: Coalition) -> None:
        ...
