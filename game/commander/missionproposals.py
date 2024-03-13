from dataclasses import field, dataclass
from enum import Enum, auto
from typing import Optional

from game.theater import MissionTarget
from game.ato.flighttype import FlightType


class EscortType(Enum):
    AirToAir = auto()
    Sead = auto()


@dataclass(frozen=True)
class ProposedFlight:
    """A flight outline proposed by the mission planner.

    Proposed flights haven't been assigned specific aircraft yet. They have only
    a task, a required number of aircraft, and a maximum distance allowed
    between the objective and the departure airfield.
    """

    #: The flight's role.
    task: FlightType

    #: The number of aircraft required.
    num_aircraft: int

    #: The type of threat this flight defends against if it is an escort. Escort
    #: flights will be pruned if the rest of the package is not threatened by
    #: the threat they defend against. If this flight is not an escort, this
    #: field is None.
    escort_type: Optional[EscortType] = field(default=None)

    def __str__(self) -> str:
        return f"{self.task} {self.num_aircraft} ship"


@dataclass(frozen=True)
class ProposedMission:
    """A mission outline proposed by the mission planner.

    Proposed missions haven't been assigned aircraft yet. They have only an
    objective location and a list of proposed flights that are required for the
    mission.
    """

    #: The mission objective.
    location: MissionTarget

    #: The proposed flights that are required for the mission.
    flights: list[ProposedFlight]

    asap: bool = field(default=False)

    def __str__(self) -> str:
        flights = ", ".join([str(f) for f in self.flights])
        return f"{self.location.name}: {flights}"
