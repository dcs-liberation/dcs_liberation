from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, List, Optional, TYPE_CHECKING

from dcs.planes import C_101CC, C_101EB, Su_33

from gen.flights.loadouts import Loadout
from .flightroster import FlightRoster
from .flightstate import FlightState, Uninitialized
from ..savecompat import has_save_compat_for

if TYPE_CHECKING:
    from game.dcs.aircrafttype import AircraftType
    from game.sim.gameupdateevents import GameUpdateEvents
    from game.squadrons import Squadron, Pilot
    from game.theater import ControlPoint, MissionTarget
    from game.transfers import TransferOrder
    from .flighttype import FlightType
    from .flightwaypoint import FlightWaypoint
    from .package import Package
    from .starttype import StartType


class Flight:
    def __init__(
        self,
        package: Package,
        country: str,
        squadron: Squadron,
        count: int,
        flight_type: FlightType,
        start_type: StartType,
        divert: Optional[ControlPoint],
        custom_name: Optional[str] = None,
        cargo: Optional[TransferOrder] = None,
        roster: Optional[FlightRoster] = None,
    ) -> None:
        self.package = package
        self.country = country
        self.squadron = squadron
        self.squadron.claim_inventory(count)
        if roster is None:
            self.roster = FlightRoster(self.squadron, initial_size=count)
        else:
            self.roster = roster
        self.divert = divert
        self.flight_type = flight_type
        # TODO: Replace with FlightPlan.
        self.targets: List[MissionTarget] = []
        self.loadout = Loadout.default_for(self)
        self.start_type = start_type
        self.use_custom_loadout = False
        self.custom_name = custom_name

        # Only used by transport missions.
        self.cargo = cargo

        # Flight properties that can be set in the mission editor. This is used for
        # things like HMD selection, ripple quantity, etc. Any values set here will take
        # the place of the defaults defined by DCS.
        #
        # This is a part of the Flight rather than the Loadout because DCS does not
        # associate these choices with the loadout, and we don't want to reset these
        # options when players switch loadouts.
        self.props: dict[str, Any] = {}

        # Used for simulating the travel to first contact.
        self.state: FlightState = Uninitialized(self, squadron.settings)

        # Will be replaced with a more appropriate FlightPlan by
        # FlightPlanBuilder, but an empty flight plan the flight begins with an
        # empty flight plan.
        from gen.flights.flightplan import FlightPlan, CustomFlightPlan

        self.flight_plan: FlightPlan = CustomFlightPlan(
            package=package, flight=self, custom_waypoints=[]
        )

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        # Avoid persisting the flight state since that's not (currently) used outside
        # mission generation. This is a bit of a hack for the moment and in the future
        # we will need to persist the flight state, but for now keep it out of save
        # compat (it also contains a generator that cannot be pickled).
        del state["state"]
        return state

    @has_save_compat_for(6)
    def __setstate__(self, state: dict[str, Any]) -> None:
        state["state"] = Uninitialized(self, state["squadron"].settings)
        if "props" not in state:
            state["props"] = {}
        self.__dict__.update(state)

    @property
    def departure(self) -> ControlPoint:
        return self.squadron.location

    @property
    def arrival(self) -> ControlPoint:
        return self.squadron.arrival

    @property
    def count(self) -> int:
        return self.roster.max_size

    @property
    def client_count(self) -> int:
        return self.roster.player_count

    @property
    def unit_type(self) -> AircraftType:
        return self.squadron.aircraft

    @property
    def from_cp(self) -> ControlPoint:
        return self.departure

    @property
    def points(self) -> List[FlightWaypoint]:
        return self.flight_plan.waypoints[1:]

    def resize(self, new_size: int) -> None:
        self.squadron.claim_inventory(new_size - self.count)
        self.roster.resize(new_size)

    def set_pilot(self, index: int, pilot: Optional[Pilot]) -> None:
        self.roster.set_pilot(index, pilot)

    @property
    def missing_pilots(self) -> int:
        return self.roster.missing_pilots

    def return_pilots_and_aircraft(self) -> None:
        self.roster.clear()
        self.squadron.claim_inventory(-self.count)

    def max_takeoff_fuel(self) -> Optional[float]:
        # Special case so Su 33 and C101 can take off
        unit_type = self.unit_type.dcs_unit_type
        if unit_type == Su_33:
            if self.flight_type.is_air_to_air:
                return Su_33.fuel_max / 2.2
            else:
                return Su_33.fuel_max * 0.8
        elif unit_type in {C_101EB, C_101CC}:
            return unit_type.fuel_max * 0.5
        return None

    def __repr__(self) -> str:
        if self.custom_name:
            return f"{self.custom_name} {self.count} x {self.unit_type}"
        return f"[{self.flight_type}] {self.count} x {self.unit_type}"

    def __str__(self) -> str:
        if self.custom_name:
            return f"{self.custom_name} {self.count} x {self.unit_type}"
        return f"[{self.flight_type}] {self.count} x {self.unit_type}"

    def set_state(self, state: FlightState) -> None:
        self.state = state

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        self.state.on_game_tick(events, time, duration)

    def should_halt_sim(self) -> bool:
        return self.state.should_halt_sim()
