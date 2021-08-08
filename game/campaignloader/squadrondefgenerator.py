from __future__ import annotations

import itertools
import random
from typing import TYPE_CHECKING, Optional

from game.dcs.aircrafttype import AircraftType
from game.squadrons.operatingbases import OperatingBases
from game.squadrons.squadrondef import SquadronDef
from game.theater import ControlPoint
from gen.flights.ai_flight_planner_db import aircraft_for_task, tasks_for_aircraft
from gen.flights.flight import FlightType

if TYPE_CHECKING:
    from game.coalition import Coalition


class SquadronDefGenerator:
    def __init__(self, coalition: Coalition) -> None:
        self.coalition = coalition
        self.count = itertools.count(1)
        self.used_nicknames: set[str] = set()

    def generate_for_task(
        self, task: FlightType, control_point: ControlPoint
    ) -> Optional[SquadronDef]:
        aircraft_choice: Optional[AircraftType] = None
        for aircraft in aircraft_for_task(task):
            if aircraft not in self.coalition.faction.aircrafts:
                continue
            if not control_point.can_operate(aircraft):
                continue
            aircraft_choice = aircraft
            # 50/50 chance to keep looking for an aircraft that isn't as far up the
            # priority list to maintain some unit variety.
            if random.choice([True, False]):
                break

        if aircraft_choice is None:
            return None
        return self.generate_for_aircraft(aircraft_choice)

    def generate_for_aircraft(self, aircraft: AircraftType) -> SquadronDef:
        return SquadronDef(
            name=f"Squadron {next(self.count):03}",
            nickname=self.random_nickname(),
            country=self.coalition.country_name,
            role="Flying Squadron",
            aircraft=aircraft,
            livery=None,
            mission_types=tuple(tasks_for_aircraft(aircraft)),
            operating_bases=OperatingBases.default_for_aircraft(aircraft),
            pilot_pool=[],
        )

    @staticmethod
    def _make_random_nickname() -> str:
        from gen.naming import ANIMALS

        animal = random.choice(ANIMALS)
        adjective = random.choice(
            (
                None,
                "Red",
                "Blue",
                "Green",
                "Golden",
                "Black",
                "Fighting",
                "Flying",
            )
        )
        if adjective is None:
            return animal.title()
        return f"{adjective} {animal}".title()

    def random_nickname(self) -> str:
        while True:
            nickname = self._make_random_nickname()
            if nickname not in self.used_nicknames:
                self.used_nicknames.add(nickname)
                return nickname
