from __future__ import annotations

import itertools
import logging
import random
from collections import defaultdict
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
        self.available_pilots = list(self.active_pilots)

    def __str__(self) -> str:
        return f'{self.name} "{self.nickname}"'

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
        self.available_pilots = list(self.active_pilots)

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
            data = yaml.safe_load(squadron_file)

        unit_type = flying_type_from_name(data["aircraft"])
        if unit_type is None:
            raise KeyError(f"Could not find any aircraft with the ID {unit_type}")

        return Squadron(
            name=data["name"],
            nickname=data["nickname"],
            country=data["country"],
            role=data["role"],
            aircraft=unit_type,
            mission_types=tuple(FlightType.from_name(n) for n in data["mission_types"]),
            pilots=[Pilot(n) for n in data.get("pilots", [])],
            game=game,
            player=player,
        )


class SquadronLoader:
    def __init__(self, game: Game, player: bool) -> None:
        self.game = game
        self.player = player

    @staticmethod
    def squadron_directories() -> Iterator[Path]:
        from game import persistency

        yield Path(persistency.base_path()) / "Liberation/Squadrons"
        yield Path("resources/squadrons")

    def load(self) -> dict[Type[FlyingType], list[Squadron]]:
        squadrons: dict[Type[FlyingType], list[Squadron]] = defaultdict(list)
        country = self.game.country_for(self.player)
        faction = self.game.faction_for(self.player)
        any_country = country.startswith("Combined Joint Task Forces ")
        for directory in self.squadron_directories():
            for path, squadron in self.load_squadrons_from(directory):
                if not any_country and squadron.country != country:
                    logging.debug(
                        "Not using squadron for non-matching country (is "
                        f"{squadron.country}, need {country}: {path}"
                    )
                    continue
                if squadron.aircraft not in faction.aircrafts:
                    logging.debug(
                        f"Not using squadron because {faction.name} cannot use "
                        f"{squadron.aircraft}: {path}"
                    )
                    continue
                logging.debug(
                    f"Found {squadron.name} {squadron.aircraft} {squadron.role} "
                    f"compatible with {faction.name}"
                )
                squadrons[squadron.aircraft].append(squadron)
        # Convert away from defaultdict because defaultdict doesn't unpickle so we don't
        # want it in the save state.
        return dict(squadrons)

    def load_squadrons_from(self, directory: Path) -> Iterator[Tuple[Path, Squadron]]:
        logging.debug(f"Looking for factions in {directory}")
        # First directory level is the aircraft type so that historical squadrons that
        # have flown multiple airframes can be defined as many times as needed. The main
        # load() method is responsible for filtering out squadrons that aren't
        # compatible with the faction.
        for squadron_path in directory.glob("*/*.yaml"):
            try:
                yield squadron_path, Squadron.from_yaml(
                    squadron_path, self.game, self.player
                )
            except Exception as ex:
                raise RuntimeError(
                    f"Failed to load squadron defined by {squadron_path}"
                ) from ex


class AirWing:
    def __init__(self, game: Game, player: bool) -> None:
        from gen.flights.flight import FlightType

        self.game = game
        self.player = player
        self.squadrons = SquadronLoader(game, player).load()

        count = itertools.count(1)
        for aircraft in game.faction_for(player).aircrafts:
            if aircraft in self.squadrons:
                continue
            self.squadrons[aircraft] = [
                Squadron(
                    name=f"Squadron {next(count):03}",
                    nickname=self.random_nickname(),
                    country=game.country_for(player),
                    role="Flying Squadron",
                    aircraft=aircraft,
                    mission_types=tuple(FlightType),
                    pilots=[],
                    game=game,
                    player=player,
                )
            ]

    def squadron_for(self, aircraft: Type[FlyingType]) -> Squadron:
        return self.squadrons[aircraft][0]

    def iter_squadrons(self) -> Iterator[Squadron]:
        return itertools.chain.from_iterable(self.squadrons.values())

    def squadron_at_index(self, index: int) -> Squadron:
        return list(self.iter_squadrons())[index]

    def reset(self) -> None:
        for squadron in self.iter_squadrons():
            squadron.return_all_pilots()

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
