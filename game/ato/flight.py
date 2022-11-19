from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any, List, Optional, TYPE_CHECKING

from dcs import Point
from dcs.planes import C_101CC, C_101EB, Su_33

from .flightroster import FlightRoster
from .flightstate import FlightState, Navigating, Uninitialized
from .flightstate.killed import Killed
from .loadouts import Loadout
from ..sidc import (
    Entity,
    SidcDescribable,
    StandardIdentity,
    Status,
    SymbolSet,
)

if TYPE_CHECKING:
    from game.dcs.aircrafttype import AircraftType
    from game.sim.gameupdateevents import GameUpdateEvents
    from game.sim.simulationresults import SimulationResults
    from game.squadrons import Squadron, Pilot
    from game.theater import ControlPoint
    from game.transfers import TransferOrder
    from .flightplans.flightplan import FlightPlan
    from .flighttype import FlightType
    from .flightwaypoint import FlightWaypoint
    from .package import Package
    from .starttype import StartType


class Flight(SidcDescribable):
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
        self.id = uuid.uuid4()
        self.package = package
        self.country = country
        self.coalition = squadron.coalition
        self.squadron = squadron
        self.squadron.claim_inventory(count)
        if roster is None:
            self.roster = FlightRoster(self.squadron, initial_size=count)
        else:
            self.roster = roster
        self.divert = divert
        self.flight_type = flight_type
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

        # Will be replaced with a more appropriate FlightPlan later, but start with a
        # cheaply constructed one since adding more flights to the package may affect
        # the optimal layout.
        from .flightplans.flightplanbuildertypes import FlightPlanBuilderTypes

        self._flight_plan_builder = FlightPlanBuilderTypes.for_flight(self)(self)

    @property
    def flight_plan(self) -> FlightPlan[Any]:
        return self._flight_plan_builder.get_or_build()

    def degrade_to_custom_flight_plan(self) -> None:
        from .flightplans.custom import Builder as CustomBuilder

        self._flight_plan_builder = CustomBuilder(self, self.flight_plan.waypoints[1:])
        self.recreate_flight_plan()

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        # Avoid persisting the flight state since that's not (currently) used outside
        # mission generation. This is a bit of a hack for the moment and in the future
        # we will need to persist the flight state, but for now keep it out of save
        # compat (it also contains a generator that cannot be pickled).
        del state["state"]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        state["state"] = Uninitialized(self, state["squadron"].settings)
        self.__dict__.update(state)

    @property
    def blue(self) -> bool:
        return self.squadron.player

    @property
    def standard_identity(self) -> StandardIdentity:
        return StandardIdentity.FRIEND if self.blue else StandardIdentity.HOSTILE_FAKER

    @property
    def sidc_status(self) -> Status:
        return Status.PRESENT if self.alive else Status.PRESENT_DESTROYED

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.AIR, self.flight_type.entity_type

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
    def is_helo(self) -> bool:
        return self.unit_type.dcs_unit_type.helicopter

    @property
    def from_cp(self) -> ControlPoint:
        return self.departure

    @property
    def points(self) -> List[FlightWaypoint]:
        return self.flight_plan.waypoints[1:]

    def position(self) -> Point:
        return self.state.estimate_position()

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

    def abort(self) -> None:
        from .flightplans.rtb import RtbFlightPlan

        self._flight_plan_builder = RtbFlightPlan.builder_type()(self)
        plan = self._flight_plan_builder.get_or_build()

        self.set_state(
            Navigating(
                self,
                self.squadron.settings,
                plan.abort_index,
                has_aborted=True,
            )
        )

    def set_state(self, state: FlightState) -> None:
        self.state = state

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        self.state.on_game_tick(events, time, duration)

    def should_halt_sim(self) -> bool:
        return self.state.should_halt_sim()

    @property
    def alive(self) -> bool:
        return self.state.alive

    def kill(self, results: SimulationResults, events: GameUpdateEvents) -> None:
        # This is a bit messy while we're in transition from turn-based to turnless
        # because we want the simulation to have minimal impact on the save game while
        # turns exist so that loading a game is essentially a way to reset the
        # simulation to the start of the turn. As such, we don't actually want to mark
        # pilots killed or reduce squadron aircraft availability, but we do still need
        # the UI to reflect that aircraft were lost and avoid generating those flights
        # when the mission is generated.
        #
        # For now we do this by logging the kill in the SimulationResults, which is
        # similar to the Debriefing. We also set the flight's state to Killed, which
        # will prevent it from being spawned in the mission and updates the SIDC.
        # This does leave an opportunity for players to cheat since the UI won't stop
        # them from cancelling a dead flight, returning the aircraft to the pool. Not a
        # big deal for now.
        # TODO: Support partial kills.
        self.set_state(
            Killed(self.state.estimate_position(), self, self.squadron.settings)
        )
        events.update_flight(self)
        for pilot in self.roster.pilots:
            if pilot is not None:
                results.kill_pilot(self, pilot)

    def recreate_flight_plan(self) -> None:
        self._flight_plan_builder.regenerate()
