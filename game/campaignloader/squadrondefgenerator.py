from __future__ import annotations

import itertools
import random
from typing import Optional, TYPE_CHECKING

from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType
from game.squadrons.operatingbases import OperatingBases
from game.squadrons.squadrondef import SquadronDef
from game.theater import ControlPoint
from game.ato.ai_flight_planner_db import aircraft_for_task, tasks_for_aircraft

if TYPE_CHECKING:
    from game.factions.faction import Faction


class SquadronDefGenerator:
    def __init__(self, faction: Faction) -> None:
        self.faction = faction
        self.count = itertools.count(1)
        self.used_nicknames: set[str] = set()

    def generate_for_task(
        self, task: FlightType, control_point: ControlPoint
    ) -> Optional[SquadronDef]:
        aircraft_choice: Optional[AircraftType] = None
        for aircraft in aircraft_for_task(task):
            if aircraft not in self.faction.aircrafts:
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
            country=self.faction.country,
            role="Flying Squadron",
            aircraft=aircraft,
            livery=None,
            mission_types=tuple(tasks_for_aircraft(aircraft)),
            operating_bases=OperatingBases.default_for_aircraft(aircraft),
            female_pilot_percentage=6,
            pilot_pool=[],
        )

    @staticmethod
    def _make_random_nickname() -> str:
        from game.naming import ANIMALS

        animal = random.choice(ANIMALS)
        adjective = random.choice(
            (
                None,
                "Aggressive",
                "Alpha",
                "Ancient",
                "Angelic",
                "Angry",
                "Apoplectic",
                "Aquamarine",
                "Astral",
                "Avenging",
                "Azure",
                "Badass",
                "Barbaric",
                "Battle",
                "Battling",
                "Bellicose",
                "Belligerent",
                "Big",
                "Bionic",
                "Black",
                "Bladed",
                "Blazoned",
                "Blood",
                "Bloody",
                "Blue",
                "Bold",
                "Boxing",
                "Brash",
                "Brass",
                "Brave",
                "Brazen",
                "Bronze",
                "Brown",
                "Brutal",
                "Burning",
                "Buzzing",
                "Celestial",
                "Clever",
                "Cloud",
                "Cobalt",
                "Copper",
                "Coral",
                "Crazy",
                "Crimson",
                "Crouching",
                "Cursed",
                "Cyan",
                "Danger",
                "Dangerous",
                "Dapper",
                "Daring",
                "Dark",
                "Dawn",
                "Day",
                "Deadly",
                "Death",
                "Defiant",
                "Demon",
                "Desert",
                "Devil",
                "Devil's",
                "Diabolical",
                "Diamond",
                "Dire",
                "Dirty",
                "Doom",
                "Doomed",
                "Double",
                "Drunken",
                "Dusk",
                "Dusty",
                "Eager",
                "Ebony",
                "Electric",
                "Emerald",
                "Eternal",
                "Evil",
                "Faithful",
                "Famous",
                "Fanged",
                "Fearless",
                "Feisty",
                "Ferocious",
                "Fierce",
                "Fiery",
                "Fighting",
                "Fire",
                "First",
                "Flame",
                "Flaming",
                "Flying",
                "Forest",
                "Frenzied",
                "Frosty",
                "Frozen",
                "Furious",
                "Gallant",
                "Ghost",
                "Giant",
                "Gigantic",
                "Glaring",
                "Global",
                "Gold",
                "Golden",
                "Green",
                "Grey",
                "Grim",
                "Grizzly",
                "Growling",
                "Grumpy",
                "Hammer",
                "Hard",
                "Hardy",
                "Heavy",
                "Hell",
                "Hell's",
                "Hidden",
                "Homicidal",
                "Hostile",
                "Howling",
                "Hyper",
                "Ice",
                "Icy",
                "Immortal",
                "Indignant",
                "Infamous",
                "Invincible",
                "Iron",
                "Jolly",
                "Laser",
                "Lava",
                "Lavender",
                "Lethal",
                "Light",
                "Lightning",
                "Livid",
                "Lucky",
                "Mad",
                "Magenta",
                "Magma",
                "Maroon",
                "Menacing",
                "Merciless",
                "Metal",
                "Midnight",
                "Mighty",
                "Mithril",
                "Mocking",
                "Moon",
                "Mountain",
                "Muddy",
                "Nasty",
                "Naughty",
                "Night",
                "Nova",
                "Nutty",
                "Obsidian",
                "Ocean",
                "Oddball",
                "Old",
                "Omega",
                "Onyx",
                "Orange",
                "Perky",
                "Pink",
                "Power",
                "Prickly",
                "Proud",
                "Puckered",
                "Pugnacious",
                "Puking",
                "Purple",
                "Ragged",
                "Raging",
                "Rainbow",
                "Rampant",
                "Razor",
                "Ready",
                "Reaper",
                "Reckless",
                "Red",
                "Roaring",
                "Rocky",
                "Rolling",
                "Royal",
                "Rusty",
                "Sable",
                "Salty",
                "Sand",
                "Sarcastic",
                "Saucy",
                "Scarlet",
                "Scarred",
                "Scary",
                "Screaming",
                "Scythed",
                "Shadow",
                "Shiny",
                "Shocking",
                "Silver",
                "Sky",
                "Smoke",
                "Smokin'",
                "Snapping",
                "Snappy",
                "Snarling",
                "Snow",
                "Soaring",
                "Space",
                "Spiky",
                "Spiny",
                "Star",
                "Steady",
                "Steel",
                "Stone",
                "Storm",
                "Striking",
                "Strong",
                "Stubborn",
                "Sun",
                "Super",
                "Terrible",
                "Thorny",
                "Thunder",
                "Top",
                "Tough",
                "Toxic",
                "Tricky",
                "Turquoise",
                "Typhoon",
                "Ultimate",
                "Ultra",
                "Ultramarine",
                "Vengeful",
                "Venom",
                "Vermillion",
                "Vicious",
                "Victorious",
                "Vigilant",
                "Violent",
                "Violet",
                "War",
                "Water",
                "Whistling",
                "White",
                "Wicked",
                "Wild",
                "Wizard",
                "Wrathful",
                "Yellow",
                "Young",
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
