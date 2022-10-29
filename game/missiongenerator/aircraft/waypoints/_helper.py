from dcs import Mission
from dcs.action import SetFlag
from dcs.condition import TimeAfter
from dcs.task import ControlledTask
from dcs.triggers import TriggerOnce, Event

from game.ato import Package


def create_stop_orbit_trigger(
    orbit: ControlledTask, package: Package, mission: Mission, elapsed: int
) -> None:
    orbit.stop_if_user_flag(id(package), True)
    orbits = [
        x
        for x in mission.triggerrules.triggers
        if x.comment == f"StopOrbit{id(package)}"
    ]
    if not any(orbits):
        stop_trigger = TriggerOnce(Event.NoEvent, f"StopOrbit{id(package)}")
        stop_condition = TimeAfter(elapsed)
        stop_action = SetFlag(id(package))
        stop_trigger.add_condition(stop_condition)
        stop_trigger.add_action(stop_action)
        mission.triggerrules.triggers.append(stop_trigger)
