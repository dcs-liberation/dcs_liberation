from collections.abc import Iterator
from datetime import datetime, timedelta

import dcs.task
from dcs.task import Task

from game.ato.flightstate.actionstate import ActionState
from game.utils import Distance
from .taskcontext import TaskContext
from .waypointaction import WaypointAction


class EngageTargets(WaypointAction):
    def __init__(
        self,
        max_distance_from_flight: Distance,
        target_types: list[type[dcs.task.TargetType]],
    ) -> None:
        self._max_distance_from_flight = max_distance_from_flight
        self._target_types = target_types

    def update_state(
        self, state: ActionState, time: datetime, duration: timedelta
    ) -> timedelta:
        state.finish()
        return duration

    def describe(self) -> str:
        return "Searching for targets"

    def iter_tasks(self, ctx: TaskContext) -> Iterator[Task]:
        yield dcs.task.EngageTargets(
            max_distance=int(self._max_distance_from_flight.meters),
            targets=self._target_types,
        )
