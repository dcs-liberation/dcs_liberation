from dataclasses import dataclass

from game.ato import FlightType


@dataclass(frozen=True)
class Task:
    """The main task of a flight or package."""

    #: The type of task.
    task_type: FlightType

    #: The location of the objective.
    location: str
