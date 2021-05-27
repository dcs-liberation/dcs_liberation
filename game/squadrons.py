from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Type, Tuple, List, TYPE_CHECKING, Optional, Iterable, Iterator

import yaml
from dcs.unittype import FlyingType
from faker import Faker

from game.db import flying_type_from_name

if TYPE_CHECKING:
    from game import Game
    from gen.flights.flight import FlightType


@dataclass
class PilotRecord:
    missions_flown: int = field(default=0)


@dataclass
class Pilot:
    name: str
    player: bool = field(default=False)
    alive: bool = field(default=True)
    record: PilotRecord = field(default_factory=PilotRecord)

    @classmethod
    def random(cls, faker: Faker) -> Pilot:
        return Pilot(faker.name())


@dataclass
class Squadron:
    name: str
    nickname: str
    country: str
    role: str
    aircraft: Type[FlyingType]
    mission_types: Tuple[FlightType, ...]
    pilots: List[Pilot]
    available_pilots: List[Pilot] = field(init=False, hash=False, compare=False)

    # We need a reference to the Game so that we can access the Faker without needing to
    # persist it to the save game, or having to reconstruct it (it's not cheap) each
    # time we create or load a squadron.
    game: Game = field(hash=False, compare=False)
    player: bool

    def __post_init__(self) -> None:
        self.available_pilots = list(self.pilots)

    def claim_available_pilot(self) -> Optional[Pilot]:
        if not self.available_pilots:
            self.enlist_new_pilots(1)
        return self.available_pilots.pop()

    def claim_pilot(self, pilot: Pilot) -> None:
        if pilot not in self.available_pilots:
            raise ValueError(
                f"Cannot assign {pilot} to {self} because they are not available"
            )
        self.available_pilots.remove(pilot)

    def return_pilot(self, pilot: Pilot) -> None:
        self.available_pilots.append(pilot)

    def return_pilots(self, pilots: Iterable[Pilot]) -> None:
        self.available_pilots.extend(pilots)

    def enlist_new_pilots(self, count: int) -> None:
        new_pilots = [Pilot(self.faker.name()) for _ in range(count)]
        self.pilots.extend(new_pilots)
        self.available_pilots.extend(new_pilots)

    def return_all_pilots(self) -> None:
        self.available_pilots = self.pilots

    @property
    def faker(self) -> Faker:
        return self.game.faker_for(self.player)

    @property
    def active_pilots(self) -> list[Pilot]:
        return [p for p in self.pilots if p.alive]

    @property
    def size(self) -> int:
        return len(self.active_pilots)

    def pilot_at_index(self, index: int) -> Pilot:
        return self.pilots[index]

    @classmethod
    def from_yaml(cls, path: Path, game: Game, player: bool) -> Squadron:
        from gen.flights.flight import FlightType

        with path.open() as squadron_file:
            data = yaml.load(squadron_file)

        unit_type = flying_type_from_name(data["aircraft"])
        if unit_type is None:
            raise KeyError(f"Could not find any aircraft with the ID {unit_type}")

        return Squadron(
            name=data["name"],
            nickname=data["nickname"],
            country=game.country_for(player),
            role=data["role"],
            aircraft=unit_type,
            mission_types=tuple(FlightType.from_name(n) for n in data["mission_types"]),
            pilots=[Pilot(n) for n in data.get("pilots", [])],
            game=game,
            player=player,
        )


class AirWing:
    def __init__(self, game: Game, player: bool) -> None:
        from gen.flights.flight import FlightType

        self.game = game
        self.player = player
        self.squadrons: dict[Type[FlyingType], list[Squadron]] = {
            aircraft: [] for aircraft in game.faction_for(player).aircrafts
        }
        for num, (aircraft, squadrons) in enumerate(self.squadrons.items()):
            squadrons.append(
                Squadron(
                    name=f"Squadron {num + 1:03}",
                    nickname=self.random_nickname(),
                    country=game.country_for(player),
                    role="Flying Squadron",
                    aircraft=aircraft,
                    mission_types=tuple(FlightType),
                    pilots=[],
                    game=game,
                    player=player,
                )
            )

    def squadron_for(self, aircraft: Type[FlyingType]) -> Squadron:
        return self.squadrons[aircraft][0]

    def iter_squadrons(self) -> Iterator[Squadron]:
        return itertools.chain.from_iterable(self.squadrons.values())

    def squadron_at_index(self, index: int) -> Squadron:
        return list(self.iter_squadrons())[index]

    @property
    def size(self) -> int:
        return sum(len(s) for s in self.squadrons.values())

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
            for squadron in self.iter_squadrons():
                if squadron.nickname == nickname:
                    break
            else:
                return nickname
