from __future__ import annotations

import itertools
import logging
import random
from collections import defaultdict
from dataclasses import dataclass, field
from enum import unique, Enum
from pathlib import Path
from typing import (
    Tuple,
    TYPE_CHECKING,
    Optional,
    Iterator,
    Sequence,
)

import yaml
from faker import Faker

from game.dcs.aircrafttype import AircraftType
from game.settings import AutoAtoBehavior

if TYPE_CHECKING:
    from game import Game
    from gen.flights.flight import FlightType


@dataclass
class PilotRecord:
    missions_flown: int = field(default=0)


@unique
class PilotStatus(Enum):
    Active = "Active"
    OnLeave = "On leave"
    Dead = "Dead"


@dataclass
class Pilot:
    name: str
    player: bool = field(default=False)
    status: PilotStatus = field(default=PilotStatus.Active)
    record: PilotRecord = field(default_factory=PilotRecord)

    @property
    def alive(self) -> bool:
        return self.status is not PilotStatus.Dead

    @property
    def on_leave(self) -> bool:
        return self.status is PilotStatus.OnLeave

    def send_on_leave(self) -> None:
        if self.status is not PilotStatus.Active:
            raise RuntimeError("Only active pilots may be sent on leave")
        self.status = PilotStatus.OnLeave

    def return_from_leave(self) -> None:
        if self.status is not PilotStatus.OnLeave:
            raise RuntimeError("Only pilots on leave may be returned from leave")
        self.status = PilotStatus.Active

    def kill(self) -> None:
        self.status = PilotStatus.Dead

    @classmethod
    def random(cls, faker: Faker) -> Pilot:
        return Pilot(faker.name())


@dataclass
class Squadron:
    name: str
    nickname: Optional[str]
    country: str
    role: str
    aircraft: AircraftType
    livery: Optional[str]
    mission_types: tuple[FlightType, ...]

    #: The pool of pilots that have not yet been assigned to the squadron. This only
    #: happens when a preset squadron defines more preset pilots than the squadron limit
    #: allows. This pool will be consumed before random pilots are generated.
    pilot_pool: list[Pilot]

    current_roster: list[Pilot] = field(default_factory=list, init=False, hash=False)
    available_pilots: list[Pilot] = field(
        default_factory=list, init=False, hash=False, compare=False
    )

    auto_assignable_mission_types: set[FlightType] = field(
        init=False, hash=False, compare=False
    )

    # We need a reference to the Game so that we can access the Faker without needing to
    # persist it to the save game, or having to reconstruct it (it's not cheap) each
    # time we create or load a squadron.
    game: Game = field(hash=False, compare=False)
    player: bool

    def __post_init__(self) -> None:
        if any(p.status is not PilotStatus.Active for p in self.pilot_pool):
            raise ValueError("Squadrons can only be created with active pilots.")
        self._recruit_pilots(self.game.settings.squadron_pilot_limit)
        self.auto_assignable_mission_types = set(self.mission_types)

    def __str__(self) -> str:
        if self.nickname is None:
            return self.name
        return f'{self.name} "{self.nickname}"'

    def claim_available_pilot(self) -> Optional[Pilot]:
        if not self.available_pilots:
            return None

        # For opfor, so player/AI option is irrelevant.
        if not self.player:
            return self.available_pilots.pop()

        preference = self.game.settings.auto_ato_behavior

        # No preference, so the first pilot is fine.
        if preference is AutoAtoBehavior.Default:
            return self.available_pilots.pop()

        prefer_players = preference is AutoAtoBehavior.Prefer
        for pilot in self.available_pilots:
            if pilot.player == prefer_players:
                self.available_pilots.remove(pilot)
                return pilot

        # No pilot was found that matched the user's preference.
        #
        # If they chose to *never* assign players and only players remain in the pool,
        # we cannot fill the slot with the available pilots.
        #
        # If they only *prefer* players and we're out of players, just return an AI
        # pilot.
        if not prefer_players:
            return None
        return self.available_pilots.pop()

    def claim_pilot(self, pilot: Pilot) -> None:
        if pilot not in self.available_pilots:
            raise ValueError(
                f"Cannot assign {pilot} to {self} because they are not available"
            )
        self.available_pilots.remove(pilot)

    def return_pilot(self, pilot: Pilot) -> None:
        self.available_pilots.append(pilot)

    def return_pilots(self, pilots: Sequence[Pilot]) -> None:
        # Return in reverse so that returning two pilots and then getting two more
        # results in the same ordering. This happens commonly when resetting rosters in
        # the UI, when we clear the roster because the UI is updating, then end up
        # repopulating the same size flight from the same squadron.
        self.available_pilots.extend(reversed(pilots))

    def _recruit_pilots(self, count: int) -> None:
        new_pilots = self.pilot_pool[:count]
        self.pilot_pool = self.pilot_pool[count:]
        count -= len(new_pilots)
        new_pilots.extend([Pilot(self.faker.name()) for _ in range(count)])
        self.current_roster.extend(new_pilots)
        self.available_pilots.extend(new_pilots)

    def replenish_lost_pilots(self) -> None:
        replenish_count = min(
            self.game.settings.squadron_replenishment_rate,
            self.number_of_unfilled_pilot_slots,
        )
        if replenish_count > 0:
            self._recruit_pilots(replenish_count)

    def return_all_pilots(self) -> None:
        self.available_pilots = list(self.active_pilots)

    @staticmethod
    def send_on_leave(pilot: Pilot) -> None:
        pilot.send_on_leave()

    def return_from_leave(self, pilot: Pilot):
        if not self.has_unfilled_pilot_slots:
            raise RuntimeError(
                f"Cannot return {pilot} from leave because {self} is full"
            )
        pilot.return_from_leave()

    @property
    def faker(self) -> Faker:
        return self.game.faker_for(self.player)

    def _pilots_with_status(self, status: PilotStatus) -> list[Pilot]:
        return [p for p in self.current_roster if p.status == status]

    def _pilots_without_status(self, status: PilotStatus) -> list[Pilot]:
        return [p for p in self.current_roster if p.status != status]

    @property
    def active_pilots(self) -> list[Pilot]:
        return self._pilots_with_status(PilotStatus.Active)

    @property
    def pilots_on_leave(self) -> list[Pilot]:
        return self._pilots_with_status(PilotStatus.OnLeave)

    @property
    def number_of_pilots_including_inactive(self) -> int:
        return len(self.current_roster)

    @property
    def number_of_unfilled_pilot_slots(self) -> int:
        return self.game.settings.squadron_pilot_limit - len(self.active_pilots)

    @property
    def number_of_available_pilots(self) -> int:
        return len(self.available_pilots)

    @property
    def has_available_pilots(self) -> bool:
        return bool(self.available_pilots)

    @property
    def has_unfilled_pilot_slots(self) -> bool:
        return self.number_of_unfilled_pilot_slots > 0

    def can_auto_assign(self, task: FlightType) -> bool:
        return task in self.auto_assignable_mission_types

    def pilot_at_index(self, index: int) -> Pilot:
        return self.current_roster[index]

    @classmethod
    def from_yaml(cls, path: Path, game: Game, player: bool) -> Squadron:
        from gen.flights.ai_flight_planner_db import tasks_for_aircraft
        from gen.flights.flight import FlightType

        with path.open(encoding="utf8") as squadron_file:
            data = yaml.safe_load(squadron_file)

        name = data["aircraft"]
        try:
            unit_type = AircraftType.named(name)
        except KeyError as ex:
            raise KeyError(f"Could not find any aircraft named {name}") from ex

        pilots = [Pilot(n, player=False) for n in data.get("pilots", [])]
        pilots.extend([Pilot(n, player=True) for n in data.get("players", [])])

        mission_types = [FlightType.from_name(n) for n in data["mission_types"]]
        tasks = tasks_for_aircraft(unit_type)
        for mission_type in list(mission_types):
            if mission_type not in tasks:
                logging.error(
                    f"Squadron has mission type {mission_type} but {unit_type} is not "
                    f"capable of that task: {path}"
                )
                mission_types.remove(mission_type)

        return Squadron(
            name=data["name"],
            nickname=data.get("nickname"),
            country=data["country"],
            role=data["role"],
            aircraft=unit_type,
            livery=data.get("livery"),
            mission_types=tuple(mission_types),
            pilot_pool=pilots,
            game=game,
            player=player,
        )

    def __setstate__(self, state) -> None:
        # TODO: Remove save compat.
        if "auto_assignable_mission_types" not in state:
            state["auto_assignable_mission_types"] = set(state["mission_types"])
        self.__dict__.update(state)


class SquadronLoader:
    def __init__(self, game: Game, player: bool) -> None:
        self.game = game
        self.player = player

    @staticmethod
    def squadron_directories() -> Iterator[Path]:
        from game import persistency

        yield Path(persistency.base_path()) / "Liberation/Squadrons"
        yield Path("resources/squadrons")

    def load(self) -> dict[AircraftType, list[Squadron]]:
        squadrons: dict[AircraftType, list[Squadron]] = defaultdict(list)
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
        from gen.flights.ai_flight_planner_db import tasks_for_aircraft

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
                    livery=None,
                    mission_types=tuple(tasks_for_aircraft(aircraft)),
                    pilot_pool=[],
                    game=game,
                    player=player,
                )
            ]

    def squadrons_for(self, aircraft: AircraftType) -> Sequence[Squadron]:
        return self.squadrons[aircraft]

    def squadrons_for_task(self, task: FlightType) -> Iterator[Squadron]:
        for squadron in self.iter_squadrons():
            if task in squadron.mission_types:
                yield squadron

    def auto_assignable_for_task_with_type(
        self, aircraft: AircraftType, task: FlightType
    ) -> Iterator[Squadron]:
        for squadron in self.squadrons_for(aircraft):
            if squadron.can_auto_assign(task) and squadron.has_available_pilots:
                yield squadron

    def squadron_for(self, aircraft: AircraftType) -> Squadron:
        return self.squadrons_for(aircraft)[0]

    def iter_squadrons(self) -> Iterator[Squadron]:
        return itertools.chain.from_iterable(self.squadrons.values())

    def squadron_at_index(self, index: int) -> Squadron:
        return list(self.iter_squadrons())[index]

    def replenish(self) -> None:
        for squadron in self.iter_squadrons():
            squadron.replenish_lost_pilots()

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
