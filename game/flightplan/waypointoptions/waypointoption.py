from __future__ import annotations

from collections.abc import Iterator

from dcs.task import Task

from game.flightplan.waypointactions.taskcontext import TaskContext


# Not explicitly an ABC because that prevents subclasses from deriving Enum.
class WaypointOption:
    def id(self) -> str:
        raise RuntimeError

    def iter_tasks(self, ctx: TaskContext) -> Iterator[Task]:
        raise RuntimeError
