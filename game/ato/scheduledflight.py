from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, TYPE_CHECKING

from dcs import Point

from game.sidc import Entity, SidcDescribable, StandardIdentity, Status, SymbolSet
from .flight import Flight
from .flightstate import FlightState, Killed, Navigating, Uninitialized

if TYPE_CHECKING:
    from game.sim import GameUpdateEvents
    from game.sim.simulationresults import SimulationResults
    from game.squadrons.squadron import Squadron
    from game.theater.controlpoint import ControlPoint
    from game.transfers import TransferOrder
    from .flightplans.flightplan import FlightPlan
    from .flightroster import FlightRoster
    from .flighttype import FlightType
    from .flightwaypoint import FlightWaypoint
    from .package import Package
    from .starttype import StartType


class ScheduledFlight(Flight, SidcDescribable):
    def __init__(
        self,
        package: Package,
        country: str,
        squadron: Squadron,
        count: int,
        flight_type: FlightType,
        start_type: StartType,
        divert: ControlPoint | None,
        custom_name: str | None = None,
        cargo: TransferOrder | None = None,
        roster: FlightRoster | None = None,
    ) -> None:
        super().__init__(
            package,
            country,
            squadron,
            count,
            flight_type,
            start_type,
            divert,
            custom_name,
            cargo,
            roster,
        )

        # Used for simulating the travel to first contact.
        self.state: FlightState = Uninitialized(self, squadron.settings)

        # Will be replaced with a more appropriate FlightPlan by
        # FlightPlanBuilder, but an empty flight plan the flight begins with an
        # empty flight plan.
        from .flightplans.custom import CustomFlightPlan, CustomLayout

        self.flight_plan: FlightPlan[Any] = CustomFlightPlan(
            self, CustomLayout(custom_waypoints=[])
        )

    @staticmethod
    def schedule(flight: Flight) -> ScheduledFlight:
        pass

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
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.AIR, self.flight_type.entity_type

    @property
    def standard_identity(self) -> StandardIdentity:
        return StandardIdentity.FRIEND if self.blue else StandardIdentity.HOSTILE_FAKER

    @property
    def sidc_status(self) -> Status:
        return Status.PRESENT if self.alive else Status.PRESENT_DESTROYED

    def position(self) -> Point:
        return self.state.estimate_position()

    def set_state(self, state: FlightState) -> None:
        self.state = state

    def abort(self) -> None:
        from .flightplans.rtb import RtbFlightPlan

        layout = RtbFlightPlan.builder_type()(self, self.coalition.game.theater).build()
        self.flight_plan = RtbFlightPlan(self, layout)

        self.set_state(
            Navigating(
                self,
                self.squadron.settings,
                self.flight_plan.abort_index,
                has_aborted=True,
            )
        )

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        self.state.on_game_tick(events, time, duration)

    def should_halt_sim(self) -> bool:
        return self.state.should_halt_sim()

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

    @property
    def alive(self) -> bool:
        return self.state.alive

    @property
    def points(self) -> list[FlightWaypoint]:
        return self.flight_plan.waypoints[1:]
