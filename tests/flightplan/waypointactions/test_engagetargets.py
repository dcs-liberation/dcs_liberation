from datetime import datetime, timedelta

from dcs.task import Targets

from game.ato.flightstate.actionstate import ActionState
from game.flightplan.waypointactions.engagetargets import EngageTargets
from game.flightplan.waypointactions.taskcontext import TaskContext
from game.utils import meters


def test_engage_targets() -> None:
    tasks = list(
        EngageTargets(
            meters(100), [Targets.All.Air.Planes, Targets.All.Air.Helicopters]
        ).iter_tasks(TaskContext(datetime.now()))
    )
    assert len(tasks) == 1
    task = tasks[0]
    assert task.id == "EngageTargets"
    assert task.params["targetTypes"] == {
        1: Targets.All.Air.Planes,
        2: Targets.All.Air.Helicopters,
    }
    assert task.params["value"] == "Planes;Helicopters"
    assert task.params["maxDist"] == 100


def test_engage_targets_update_state() -> None:
    task = EngageTargets(meters(100), [Targets.All])
    state = ActionState(task)
    assert not task.update_state(state, datetime.now(), timedelta())
    assert state.is_finished()


def test_engage_targets_description() -> None:
    assert (
        EngageTargets(meters(100), [Targets.All]).describe() == "Searching for targets"
    )
