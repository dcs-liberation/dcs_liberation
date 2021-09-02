from __future__ import annotations

import random
import time
from typing import List, Any, TYPE_CHECKING

from dcs.country import Country

from game.dcs.aircrafttype import AircraftType
from game.dcs.unittype import UnitType

if TYPE_CHECKING:
    from gen.flights.flight import Flight

ALPHA_MILITARY = [
    "Alpha",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliet",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whisky",
    "XRay",
    "Yankee",
    "Zulu",
    "Zero",
]

ANIMALS: tuple[str, ...] = (
    "AARDWOLF",
    "ALBATROSS",
    "ALLIGATOR",
    "ALPACA",
    "ANACONDA",
    "ANTELOPE",
    "ARGALI",
    "ARMADILLO",
    "BABOON",
    "BADGER",
    "BANDICOOT",
    "BARRACUDA",
    "BASILISK",
    "BAT",
    "BEAR",
    "BISON",
    "BOBCAT",
    "BONGO",
    "BUFFALO",
    "BULLDOG",
    "BUMBLEBEE",
    "BUNNY",
    "BUTTERFLY",
    "CAIMAN",
    "CAMEL",
    "CANARY",
    "CAPYBARA",
    "CARACAL",
    "CASTOR",
    "CAT",
    "CATERPILLAR",
    "CATFISH",
    "CENTIPEDE",
    "CHAMELEON",
    "CHEETAH",
    "CHICKEN",
    "COBRA",
    "COLT",
    "CORAL",
    "CORGI",
    "COTTONMOUTH",
    "COW",
    "COYOTE",
    "CRAB",
    "CROW",
    "DACHSHUND",
    "DEER",
    "DINGO",
    "DODO",
    "DOG",
    "DOLPHIN",
    "DONKEY",
    "DOVE",
    "DRAGON",
    "DUCK",
    "ELEPHANT",
    "ELK",
    "FALCON",
    "FAWN",
    "FENNEC",
    "FERRET",
    "FINCH",
    "FISH",
    "FLAMINGO",
    "FOX",
    "FROG",
    "GAZELLE",
    "GECKO",
    "GIRAFFE",
    "GOOSE",
    "GOPHER",
    "GORILLA",
    "GRASSHOPPER",
    "GREYHOUND",
    "GRIZZLY",
    "GUANACO",
    "GULL",
    "HAMSTER",
    "HARAMBE",
    "HARE",
    "HARRIER",
    "HAWK",
    "HEDGEHOG",
    "HIPPO",
    "HORSE",
    "HUSKY",
    "IGUANA",
    "IMPALA",
    "INSECT",
    "JACKAL",
    "JAGUAR",
    "JELLYFISH",
    "JERBOA",
    "KANGAROO",
    "KITTEN",
    "KIWI",
    "KOALA",
    "KOMODO",
    "LADYBUG",
    "LEOPARD",
    "LIGHTFOOT",
    "LION",
    "LIZARD",
    "LLAMA",
    "LOBSTER",
    "LOCUST",
    "LYNX",
    "MACAW",
    "MAGPIE",
    "MAMBA",
    "MAMMOTH",
    "MANATEE",
    "MARE",
    "MAVERICK",
    "MEERKAT",
    "MINK",
    "MOCKINGBIRD",
    "MOLE",
    "MOLLY",
    "MONGOOSE",
    "MONKEY",
    "MONSTER",
    "MOOSE",
    "MOSQUITO",
    "MOTH",
    "MOUSE",
    "MULE",
    "MUSK",
    "OCELOT",
    "OCTOPUS",
    "ORCA",
    "ORYX",
    "OSTRICH",
    "OTTER",
    "OWL",
    "OX",
    "OYSTER",
    "PANDA",
    "PANGOLIN",
    "PANTHER",
    "PARROT",
    "PEACOCK",
    "PELICAN",
    "PENGUIN",
    "PHEASANT",
    "PIGLET",
    "PIKE",
    "PIRANHA",
    "PLATYPUS",
    "POODLE",
    "PORCUPINE",
    "PRONGHORN",
    "PUG",
    "PUMA",
    "PYTHON",
    "RACOON",
    "RAGDOLL",
    "RAT",
    "RAVEN",
    "REINDEER",
    "RHINO",
    "ROBIN",
    "SCORPIO",
    "SEAL",
    "SHARK",
    "SHEEP",
    "SHRIMP",
    "SKATE",
    "SKUNK",
    "SLUG",
    "SNAIL",
    "SNAKE",
    "SQUIRREL",
    "STARFISH",
    "SWAN",
    "TAMARIN",
    "TAPIR",
    "TAURUS",
    "TERMITE",
    "TETRA",
    "TIGER",
    "TOAD",
    "TORTOISE",
    "TOUCAN",
    "TURKEY",
    "URCHIN",
    "VIPER",
    "VULTURE",
    "WALLABY",
    "WALRUS",
    "WARTHOG",
    "WATERBUCK",
    "WEASEL",
    "WHALE",
    "WOLF",
    "WOLVERINE",
    "WOMBAT",
    "WOODCHUCK",
    "WOODPECKER",
    "WORM",
    "YAK",
    "ZEBRA",
    "ZEBU",
)


class NameGenerator:
    number = 0
    infantry_number = 0
    aircraft_number = 0
    convoy_number = 0
    cargo_ship_number = 0

    animals: list[str] = list(ANIMALS)
    existing_alphas: List[str] = []

    @classmethod
    def reset(cls) -> None:
        cls.number = 0
        cls.infantry_number = 0
        cls.convoy_number = 0
        cls.cargo_ship_number = 0
        cls.animals = list(ANIMALS)
        cls.existing_alphas = []

    @classmethod
    def reset_numbers(cls) -> None:
        cls.number = 0
        cls.infantry_number = 0
        cls.aircraft_number = 0
        cls.convoy_number = 0
        cls.cargo_ship_number = 0

    @classmethod
    def next_aircraft_name(
        cls, country: Country, parent_base_id: int, flight: Flight
    ) -> str:
        cls.aircraft_number += 1
        try:
            if flight.custom_name:
                name_str = flight.custom_name
            else:
                name_str = "{} {}".format(
                    flight.package.target.name, flight.flight_type
                )
        except AttributeError:  # Here to maintain save compatibility with 2.3
            name_str = "{} {}".format(flight.package.target.name, flight.flight_type)
        return "{}|{}|{}|{}|{}|".format(
            name_str,
            country.id,
            cls.aircraft_number,
            parent_base_id,
            flight.unit_type.name,
        )

    @classmethod
    def next_unit_name(
        cls, country: Country, parent_base_id: int, unit_type: UnitType[Any]
    ) -> str:
        cls.number += 1
        return "unit|{}|{}|{}|{}|".format(
            country.id, cls.number, parent_base_id, unit_type.name
        )

    @classmethod
    def next_infantry_name(
        cls, country: Country, parent_base_id: int, unit_type: UnitType[Any]
    ) -> str:
        cls.infantry_number += 1
        return "infantry|{}|{}|{}|{}|".format(
            country.id,
            cls.infantry_number,
            parent_base_id,
            unit_type.name,
        )

    @classmethod
    def next_awacs_name(cls, country: Country) -> str:
        cls.number += 1
        return "awacs|{}|{}|0|".format(country.id, cls.number)

    @classmethod
    def next_tanker_name(cls, country: Country, unit_type: AircraftType) -> str:
        cls.number += 1
        return "tanker|{}|{}|0|{}".format(country.id, cls.number, unit_type.name)

    @classmethod
    def next_carrier_name(cls, country: Country) -> str:
        cls.number += 1
        return "carrier|{}|{}|0|".format(country.id, cls.number)

    @classmethod
    def next_convoy_name(cls) -> str:
        cls.convoy_number += 1
        return f"Convoy {cls.convoy_number:03}"

    @classmethod
    def next_cargo_ship_name(cls) -> str:
        cls.cargo_ship_number += 1
        return f"Cargo Ship {cls.cargo_ship_number:03}"

    @classmethod
    def random_objective_name(cls) -> str:
        if cls.animals:
            animal = random.choice(cls.animals)
            cls.animals.remove(animal)
            return animal

        for _ in range(10):
            alpha = random.choice(ALPHA_MILITARY).upper()
            number = random.randint(0, 100)
            alpha_mil_name = f"{alpha} #{number:02}"
            if alpha_mil_name not in cls.existing_alphas:
                cls.existing_alphas.append(alpha_mil_name)
                return alpha_mil_name

        # At this point, give up trying - something has gone wrong and we haven't been
        # able to make a new name in 10 tries. We'll just make a longer name using the
        # current unix epoch in nanoseconds. That should be unique... right?
        last_chance_name = alpha_mil_name + str(time.time_ns())
        cls.existing_alphas.append(last_chance_name)
        return last_chance_name


namegen = NameGenerator
