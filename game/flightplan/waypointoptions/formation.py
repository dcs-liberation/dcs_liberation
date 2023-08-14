from collections.abc import Iterator
from enum import Enum

from dcs.task import OptFormation, Task

from game.flightplan.waypointactions.taskcontext import TaskContext
from game.flightplan.waypointoptions.waypointoption import WaypointOption


class Formation(WaypointOption, Enum):
    FINGER_FOUR_CLOSE = OptFormation.finger_four_close()
    FINGER_FOUR_OPEN = OptFormation.finger_four_open()
    LINE_ABREAST_OPEN = OptFormation.line_abreast_open()
    SPREAD_FOUR_OPEN = OptFormation.spread_four_open()
    TRAIL_OPEN = OptFormation.trail_open()

    def id(self) -> str:
        return "formation"

    def iter_tasks(self, ctx: TaskContext) -> Iterator[Task]:
        yield self.value
