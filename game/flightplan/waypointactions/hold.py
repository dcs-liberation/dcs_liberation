from collections.abc import Iterator
from datetime import datetime, timedelta

from dcs.task import Task, OrbitAction, ControlledTask

from game.ato.flightstate.actionstate import ActionState
from game.provider import Provider
from game.utils import Distance, Speed
from .taskcontext import TaskContext
from .waypointaction import WaypointAction


class Hold(WaypointAction):
    """Loiter at a location until a push time to synchronize with other flights.

    Taxi behavior is extremely unpredictable, so we cannot reliably predict ETAs for
    waypoints without first fixing a time for one waypoint by holding until a sync time.
    This is typically done with a dedicated hold point. If the flight reaches the hold
    point before their push time, they will loiter at that location rather than fly to
    their next waypoint as a speed that's often dangerously slow.
    """

    def __init__(
        self, push_time_provider: Provider[datetime], altitude: Distance, speed: Speed
    ) -> None:
        self._push_time_provider = push_time_provider
        self._altitude = altitude
        self._speed = speed

    def describe(self) -> str:
        return self._push_time_provider().strftime("Holding until %H:%M:%S")

    def update_state(
        self, state: ActionState, time: datetime, duration: timedelta
    ) -> timedelta:
        push_time = self._push_time_provider()
        if push_time <= time:
            state.finish()
            return time - push_time
        return timedelta()

    def iter_tasks(self, ctx: TaskContext) -> Iterator[Task]:
        remaining_time = self._push_time_provider() - ctx.mission_start_time
        if remaining_time <= timedelta():
            return

        loiter = ControlledTask(
            OrbitAction(
                altitude=int(self._altitude.meters),
                pattern=OrbitAction.OrbitPattern.Circle,
                speed=self._speed.kph,
            )
        )
        # The DCS task is serialized using the time from mission start, not the actual
        # time.
        loiter.stop_after_time(int(remaining_time.total_seconds()))
        yield loiter
