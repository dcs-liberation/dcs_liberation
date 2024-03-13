from __future__ import annotations

import itertools
import logging
from collections.abc import Iterator
from datetime import timedelta
from typing import Optional, TYPE_CHECKING

from .aircombat import AirCombat
from .aircraftengagementzones import AircraftEngagementZones
from .atip import AtIp
from .defendingsam import DefendingSam
from .joinablecombat import JoinableCombat
from .samengagementzones import SamEngagementZones
from ..gameupdateevents import GameUpdateEvents

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight
    from .frozencombat import FrozenCombat


class CombatInitiator:
    def __init__(
        self, game: Game, combats: list[FrozenCombat], events: GameUpdateEvents
    ) -> None:
        self.game = game
        self.combats = combats
        self.events = events

    def update_active_combats(self) -> None:
        blue_a2a = AircraftEngagementZones.from_ato(self.game.blue.ato)
        red_a2a = AircraftEngagementZones.from_ato(self.game.red.ato)
        blue_sam = SamEngagementZones.from_theater(self.game.theater, player=True)
        red_sam = SamEngagementZones.from_theater(self.game.theater, player=False)

        # Check each vulnerable flight to see if it has initiated combat. If any flight
        # initiates combat, a single FrozenCombat will be created for all involved
        # flights and the FlightState of each flight will be updated accordingly.
        #
        # There's some nuance to this behavior. Duplicate combats are avoided because
        # InCombat flight states are not considered vulnerable. That means that once an
        # aircraft has entered combat it will not be rechecked later in the loop or on
        # another tick.
        for flight in self.iter_flights():
            if flight.state.in_combat:
                return

            if flight.squadron.player:
                a2a = red_a2a
                own_a2a = blue_a2a
                sam = red_sam
            else:
                a2a = blue_a2a
                own_a2a = red_a2a
                sam = blue_sam
            self.check_flight_for_combat(flight, a2a, own_a2a, sam)

    def check_flight_for_combat(
        self,
        flight: Flight,
        a2a: AircraftEngagementZones,
        own_a2a: AircraftEngagementZones,
        sam: SamEngagementZones,
    ) -> None:
        if (joined := self.check_flight_for_joined_combat(flight)) is not None:
            logging.info(f"{flight} is joining existing combat {joined}")
            joined.join(flight)
            own_a2a.remove_flight(flight)
            self.events.update_combat(joined)
        elif (combat := self.check_flight_for_new_combat(flight, a2a, sam)) is not None:
            logging.info(f"Creating new combat because {combat.because()}")
            combat.update_flight_states()
            # Remove any preoccupied flights from the list of potential air-to-air
            # threats. This prevents BARCAPs (and other air-to-air types) from getting
            # involved in multiple combats simultaneously. Additional air-to-air
            # aircraft may join existing combats, but they will not create new combats.
            a2a.update_for_combat(combat)
            own_a2a.update_for_combat(combat)
            self.combats.append(combat)
            self.events.new_combat(combat)

    def check_flight_for_joined_combat(
        self, flight: Flight
    ) -> Optional[JoinableCombat]:
        for combat in self.combats:
            if isinstance(combat, JoinableCombat) and combat.joinable_by(flight):
                return combat
        return None

    @staticmethod
    def check_flight_for_new_combat(
        flight: Flight, a2a: AircraftEngagementZones, sam: SamEngagementZones
    ) -> Optional[FrozenCombat]:
        if not flight.state.in_flight:
            return None

        if flight.state.is_at_ip and not flight.state.avoid_further_combat:
            return AtIp(timedelta(minutes=1), flight)

        position = flight.state.estimate_position()

        if flight.state.vulnerable_to_intercept and a2a.covers(position):
            flights = [flight]
            flights.extend(a2a.iter_intercepting_flights(position))
            return AirCombat(timedelta(minutes=1), flights)

        if flight.state.vulnerable_to_sam and sam.covers(position):
            return DefendingSam(
                timedelta(minutes=1), flight, list(sam.iter_threatening_sams(position))
            )

        return None

    def iter_flights(self) -> Iterator[Flight]:
        packages = itertools.chain(
            self.game.blue.ato.packages, self.game.red.ato.packages
        )
        for package in packages:
            yield from package.flights
