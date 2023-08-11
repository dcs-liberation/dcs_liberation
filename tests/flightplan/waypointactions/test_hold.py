from datetime import datetime, timedelta

from game.ato.flightstate.actionstate import ActionState
from game.flightplan.waypointactions.hold import Hold
from game.flightplan.waypointactions.taskcontext import TaskContext
from game.utils import meters, kph


def test_hold_tasks() -> None:
    t0 = datetime(1999, 3, 28)
    tasks = list(
        Hold(lambda: t0 + timedelta(minutes=5), meters(8000), kph(400)).iter_tasks(
            TaskContext(t0 + timedelta(minutes=1))
        )
    )
    assert len(tasks) == 1
    task = tasks[0]
    assert task.id == "ControlledTask"
    assert task.params["stopCondition"]["time"] == 4 * 60
    assert task.params["task"]["id"] == "Orbit"
    assert task.params["task"]["params"]["altitude"] == 8000
    assert task.params["task"]["params"]["pattern"] == "Circle"
    assert task.params["task"]["params"]["speed"] == kph(400).meters_per_second


def test_hold_task_at_or_after_push() -> None:
    t0 = datetime(1999, 3, 28)
    assert not list(
        Hold(lambda: t0, meters(8000), kph(400)).iter_tasks(TaskContext(t0))
    )
    assert not list(
        Hold(lambda: t0, meters(8000), kph(400)).iter_tasks(
            TaskContext(t0 + timedelta(minutes=1))
        )
    )


def test_hold_tick() -> None:
    t0 = datetime(1999, 3, 28)
    task = Hold(lambda: t0 + timedelta(minutes=5), meters(8000), kph(400))
    state = ActionState(task)
    task.update_state(state, t0, timedelta())
    assert not state.is_finished()
    task.update_state(state, t0 + timedelta(minutes=1), timedelta(minutes=1))
    assert not state.is_finished()
    task.update_state(state, t0 + timedelta(minutes=2), timedelta(minutes=1))
    assert not state.is_finished()
    task.update_state(state, t0 + timedelta(minutes=3), timedelta(minutes=1))
    assert not state.is_finished()
    task.update_state(state, t0 + timedelta(minutes=4), timedelta(minutes=1))
    assert not state.is_finished()
    task.update_state(state, t0 + timedelta(minutes=5), timedelta(minutes=1))
    assert state.is_finished()
    task.update_state(state, t0 + timedelta(minutes=6), timedelta(minutes=1))
    assert state.is_finished()


def test_hold_description() -> None:
    assert (
        Hold(
            lambda: datetime(1999, 3, 28) + timedelta(minutes=5), meters(8000), kph(400)
        ).describe()
        == "Holding until 00:05:00"
    )
