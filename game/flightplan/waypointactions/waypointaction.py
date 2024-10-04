from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs.task import Task

from .taskcontext import TaskContext

if TYPE_CHECKING:
    from game.ato.flightstate.actionstate import ActionState


class WaypointAction(ABC):
    @abstractmethod
    def describe(self) -> str: ...

    @abstractmethod
    def update_state(
        self, state: ActionState, time: datetime, duration: timedelta
    ) -> timedelta: ...

    @abstractmethod
    def iter_tasks(self, ctx: TaskContext) -> Iterator[Task]: ...
