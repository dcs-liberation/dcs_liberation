from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path
from typing import Iterator, Tuple, TYPE_CHECKING

from game.dcs.aircrafttype import AircraftType
from .squadrondef import SquadronDef

if TYPE_CHECKING:
    from game import Game
    from ..factions.faction import Faction


class SquadronDefLoader:
    def __init__(self, game: Game, faction: Faction) -> None:
        self.game = game
        self.faction = faction

    @staticmethod
    def squadron_directories() -> Iterator[Path]:
        from game import persistency

        yield Path(persistency.base_path()) / "Liberation/Squadrons"
        yield Path("resources/squadrons")

    def load(self) -> dict[AircraftType, list[SquadronDef]]:
        squadrons: dict[AircraftType, list[SquadronDef]] = defaultdict(list)
        country = self.faction.country
        faction = self.faction
        any_country = country.startswith("Combined Joint Task Forces ")
        for directory in self.squadron_directories():
            for path, squadron_def in self.load_squadrons_from(directory):
                if not any_country and squadron_def.country != country:
                    logging.debug(
                        "Not using squadron for non-matching country (is "
                        f"{squadron_def.country}, need {country}: {path}"
                    )
                    continue
                if squadron_def.aircraft not in faction.aircrafts:
                    logging.debug(
                        f"Not using squadron because {faction.name} cannot use "
                        f"{squadron_def.aircraft}: {path}"
                    )
                    continue
                logging.debug(
                    f"Found {squadron_def.name} {squadron_def.aircraft} "
                    f"{squadron_def.role} compatible with {faction.name}"
                )

                squadrons[squadron_def.aircraft].append(squadron_def)
        return squadrons

    @staticmethod
    def load_squadrons_from(directory: Path) -> Iterator[Tuple[Path, SquadronDef]]:
        logging.debug(f"Looking for factions in {directory}")
        # First directory level is the aircraft type so that historical squadrons that
        # have flown multiple airframes can be defined as many times as needed. The main
        # load() method is responsible for filtering out squadrons that aren't
        # compatible with the faction.
        for squadron_path in directory.glob("*/*.yaml"):
            try:
                yield squadron_path, SquadronDef.from_yaml(squadron_path)
            except Exception as ex:
                raise RuntimeError(
                    f"Failed to load squadron defined by {squadron_path}"
                ) from ex
