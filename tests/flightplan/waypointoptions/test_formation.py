from datetime import datetime

from dcs.task import OptFormation

from game.flightplan.waypointactions.taskcontext import TaskContext
from game.flightplan.waypointoptions.formation import Formation


def test_formation() -> None:
    tasks = list(Formation.LINE_ABREAST_OPEN.iter_tasks(TaskContext(datetime.now())))
    assert len(tasks) == 1
    task = tasks[0]
    assert task.dict() == OptFormation.line_abreast_open().dict()
