from collections.abc import Iterator
from datetime import timedelta, datetime

from dcs.task import Task

from game.ato.flightstate.actionstate import ActionState
from game.flightplan.waypointactions.taskcontext import TaskContext
from game.flightplan.waypointactions.waypointaction import WaypointAction


class TestAction(WaypointAction):
    def describe(self) -> str:
        return ""

    def update_state(
        self, state: ActionState, time: datetime, duration: timedelta
    ) -> timedelta:
        return timedelta()

    def iter_tasks(self, ctx: TaskContext) -> Iterator[Task]:
        yield from []


def test_actionstate() -> None:
    action = TestAction()
    state = ActionState(action)
    assert not state.is_finished()
    state.finish()
    assert state.is_finished()
