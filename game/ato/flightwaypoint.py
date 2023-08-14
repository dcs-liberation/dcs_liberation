from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, TYPE_CHECKING

from dcs import Point

from game.ato.flightwaypointtype import FlightWaypointType
from game.flightplan.waypointactions.waypointaction import WaypointAction
from game.flightplan.waypointoptions.waypointoption import WaypointOption
from game.theater.theatergroup import TheaterUnit
from game.utils import Distance, meters

if TYPE_CHECKING:
    from game.theater import ControlPoint

AltitudeReference = Literal["BARO", "RADIO"]


@dataclass
class FlightWaypoint:
    name: str
    waypoint_type: FlightWaypointType
    position: Point
    alt: Distance = meters(0)
    alt_type: AltitudeReference = "BARO"
    control_point: ControlPoint | None = None

    # TODO: Merge with pretty_name.
    # Only used in the waypoint list in the flight edit page. No sense
    # having three names. A short and long form is enough.
    description: str = ""

    targets: list[TheaterUnit] = field(default_factory=list)
    obj_name: str = ""
    pretty_name: str = ""
    only_for_player: bool = False
    flyover: bool = False

    # The minimum amount of fuel remaining at this waypoint in pounds.
    min_fuel: float | None = None

    actions: list[WaypointAction] = field(default_factory=list)
    options: dict[str, WaypointOption] = field(default_factory=dict)

    # These are set very late by the air conflict generator (part of mission
    # generation). We do it late so that we don't need to propagate changes
    # to waypoint times whenever the player alters the package TOT or the
    # flight's offset in the UI.
    tot: datetime | None = None
    departure_time: datetime | None = None

    def add_action(self, action: WaypointAction) -> None:
        self.actions.append(action)

    def set_option(self, option: WaypointOption) -> None:
        self.options[option.id()] = option

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    def __hash__(self) -> int:
        return hash(id(self))
