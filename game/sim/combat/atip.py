from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

from .frozencombat import FrozenCombat
from .. import GameUpdateEvents
from ...ato.flightstate import InCombat, InFlight, FlightState
from ...ato.flightplans.formationattack import FormationAttackFlightPlan
from game.settings.settings import CombatResolutionMethod

if TYPE_CHECKING:
    from game.ato import Flight
    from ..simulationresults import SimulationResults


class AtIp(FrozenCombat):
    def __init__(self, freeze_duration: timedelta, flight: Flight) -> None:
        freeze_duration_ = freeze_duration
        if isinstance(flight.flight_plan, FormationAttackFlightPlan) and isinstance(
            flight.state, InFlight
        ):
            # If flight is a type with an IP and is currently in-flight, we can set a more informative freeze duration.

            # If we entered IP combat and other elements of the package are also in IP combat, set the freeze
            # duration to the same as the other elements of the package so that the package stays together.
            match_package_freeze_duration = self._freeze_duration_to_match_package(
                flight
            )
            if match_package_freeze_duration is not None:
                freeze_duration_ = match_package_freeze_duration
            else:
                # No other elements of the package are in Ip combat so this must be the first flight to reach the Ip.
                # Set the freeze duration to the expected time to reach the split point i.e. when the flight is planned
                # to be disengaging.
                split_waypoint_freeze_duration = (
                    self._freeze_duration_to_reach_split_point(flight)
                )
                if (
                    split_waypoint_freeze_duration is not None
                ):  # Can find the split waypoint
                    freeze_duration_ = split_waypoint_freeze_duration

        super().__init__(freeze_duration_)
        self.flight = flight

    def because(self) -> str:
        return f"{self.flight} is at its IP"

    def describe(self) -> str:
        return "at IP"

    def iter_flights(self) -> Iterator[Flight]:
        yield self.flight

    def resolve(
        self,
        results: SimulationResults,
        events: GameUpdateEvents,
        time: datetime,
        elapsed_time: timedelta,
        resolution_method: CombatResolutionMethod,
    ) -> None:
        logging.debug(
            f"{self.flight} attack on {self.flight.package.target} auto-resolved with "
            "mission failure but no losses"
        )
        assert isinstance(self.flight.state, InCombat)
        self.flight.state.exit_combat(
            events, time, elapsed_time, avoid_further_combat=True
        )

    @staticmethod
    def _freeze_duration_to_reach_split_point(flight: Flight) -> Optional[timedelta]:
        flight_state = flight.state
        while (
            isinstance(flight_state, InFlight)
            and flight_state.current_waypoint != flight.flight_plan.layout.split
        ):
            flight_state = flight_state.next_waypoint_state()
        if not isinstance(flight_state, InFlight):
            return None

        split_waypoint_tot = flight.flight_plan.tot_for_waypoint(
            flight_state.current_waypoint
        )
        current_waypoint_tot = flight.flight_plan.tot_for_waypoint(
            flight.state.current_waypoint  # type: ignore
        )
        if split_waypoint_tot is None or current_waypoint_tot is None:
            return None
        return split_waypoint_tot - current_waypoint_tot

    @staticmethod
    def _freeze_duration_to_match_package(flight: Flight) -> Optional[timedelta]:
        for package_flight in flight.package.flights:
            if (
                package_flight.state.in_combat
                and isinstance(package_flight.state, InCombat)
                and isinstance(package_flight.state.combat, AtIp)
            ):
                return package_flight.state.combat.freeze_duration
        return None
