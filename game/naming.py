from __future__ import annotations

import random
import time
from typing import Any, List, TYPE_CHECKING

from dcs.country import Country

from game.dcs.aircrafttype import AircraftType
from game.dcs.unittype import UnitType

if TYPE_CHECKING:
    from game.ato.flight import Flight

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
    "AARDVARK",
    "AARDWOLF",
    "ADDER",
    "ALBACORE",
    "ALBATROSS",
    "ALLIGATOR",
    "ALPACA",
    "ANACONDA",
    "ANOLE",
    "ANTEATER",
    "ANTELOPE",
    "ANTLION",
    "ARAPAIMA",
    "ARCHERFISH",
    "ARGALI",
    "ARMADILLO",
    "ASP",
    "AUROCHS",
    "AXOLOTL",
    "BABIRUSA",
    "BABOON",
    "BADGER",
    "BANDICOOT",
    "BARRACUDA",
    "BARRAMUNDI",
    "BASILISK",
    "BASS",
    "BAT",
    "BEAR",
    "BEAVER",
    "BEETLE",
    "BELUGA",
    "BETTONG",
    "BINTURONG",
    "BISON",
    "BLOODHOUND",
    "BOA",
    "BOBCAT",
    "BONGO",
    "BONITO",
    "BUFFALO",
    "BULLDOG",
    "BULLFROG",
    "BULLSHARK",
    "BUMBLEBEE",
    "BUNNY",
    "BUTTERFLY",
    "CAIMAN",
    "CAMEL",
    "CANARY",
    "CAPYBARA",
    "CARACAL",
    "CARP",
    "CASTOR",
    "CAT",
    "CATERPILLAR",
    "CATFISH",
    "CENTIPEDE",
    "CHAMELEON",
    "CHEETAH",
    "CHICKEN",
    "CHIMAERA",
    "CICADA",
    "CICHLID",
    "CIVET",
    "COBIA",
    "COBRA",
    "COCKATOO",
    "COD",
    "COELACANTH",
    "COLT",
    "CONDOR",
    "COPPERHEAD",
    "CORAL",
    "CORGI",
    "COTTONMOUTH",
    "COUGAR",
    "COW",
    "COYOTE",
    "CRAB",
    "CRANE",
    "CRICKET",
    "CROCODILE",
    "CROW",
    "CUTTLEFISH",
    "DACHSHUND",
    "DEER",
    "DINGO",
    "DIREWOLF",
    "DODO",
    "DOG",
    "DOLPHIN",
    "DONKEY",
    "DOVE",
    "DRACO",
    "DRAGON",
    "DRAGONFLY",
    "DUCK",
    "DUGONG",
    "EAGLE",
    "EARWIG",
    "ECHIDNA",
    "EEL",
    "ELEPHANT",
    "ELK",
    "EMU",
    "ERMINE",
    "FALCON",
    "FANGTOOTH",
    "FAWN",
    "FENNEC",
    "FERRET",
    "FINCH",
    "FIREFLY",
    "FISH",
    "FLAMINGO",
    "FLEA",
    "FLOUNDER",
    "FOX",
    "FRINGEHEAD",
    "FROG",
    "FROGMOUTH",
    "GAR",
    "GAZELLE",
    "GECKO",
    "GENET",
    "GERBIL",
    "GHARIAL",
    "GIBBON",
    "GIRAFFE",
    "GOOSE",
    "GOPHER",
    "GORILLA",
    "GOSHAWK",
    "GRASSHOPPER",
    "GREYHOUND",
    "GRIZZLY",
    "GROUPER",
    "GROUSE",
    "GRYPHON",
    "GUANACO",
    "GULL",
    "GUPPY",
    "HADDOCK",
    "HAGFISH",
    "HALIBUT",
    "HAMSTER",
    "HARAMBE",
    "HARE",
    "HARRIER",
    "HAWK",
    "HEDGEHOG",
    "HERMITCRAB",
    "HERON",
    "HERRING",
    "HIPPO",
    "HORNBILL",
    "HORNET",
    "HORSE",
    "HUNTSMAN",
    "HUSKY",
    "HYENA",
    "IBEX",
    "IBIS",
    "IGUANA",
    "IMPALA",
    "INSECT",
    "IRUKANDJI",
    "ISOPOD",
    "JACKAL",
    "JAGUAR",
    "JELLYFISH",
    "JERBOA",
    "KAKAPO",
    "KANGAROO",
    "KATYDID",
    "KEA",
    "KINGFISHER",
    "KITTEN",
    "KIWI",
    "KOALA",
    "KOMODO",
    "KRAIT",
    "LADYBUG",
    "LAMPREY",
    "LEMUR",
    "LEOPARD",
    "LIGHTFOOT",
    "LION",
    "LIONFISH",
    "LIZARD",
    "LLAMA",
    "LOACH",
    "LOBSTER",
    "LOCUST",
    "LORIKEET",
    "LUNGFISH",
    "LYNX",
    "MACAW",
    "MAGPIE",
    "MALLARD",
    "MAMBA",
    "MAMMOTH",
    "MANATEE",
    "MANDRILL",
    "MANTA",
    "MANTIS",
    "MARE",
    "MARLIN",
    "MARMOT",
    "MARTEN",
    "MASTIFF",
    "MASTODON",
    "MAVERICK",
    "MAYFLY",
    "MEERKAT",
    "MILLIPEDE",
    "MINK",
    "MOA",
    "MOCKINGBIRD",
    "MOLE",
    "MOLERAT",
    "MOLLY",
    "MONGOOSE",
    "MONKEY",
    "MONKFISH",
    "MONSTER",
    "MOOSE",
    "MORAY",
    "MOSQUITO",
    "MOTH",
    "MOUSE",
    "MUDSKIPPER",
    "MULE",
    "MUSK",
    "MYNA",
    "NARWHAL",
    "NAUTILUS",
    "NEWT",
    "NIGHTINGALE",
    "NUMBAT",
    "OCELOT",
    "OCTOPUS",
    "OKAPI",
    "OLM",
    "OPAH",
    "OPOSSUM",
    "ORCA",
    "ORYX",
    "OSPREY",
    "OSTRICH",
    "OTTER",
    "OWL",
    "OX",
    "OYSTER",
    "PADDLEFISH",
    "PADEMELON",
    "PANDA",
    "PANGOLIN",
    "PANTHER",
    "PARAKEET",
    "PARROT",
    "PEACOCK",
    "PELICAN",
    "PENGUIN",
    "PERCH",
    "PEREGRINE",
    "PETRAL",
    "PHEASANT",
    "PIG",
    "PIGEON",
    "PIGLET",
    "PIKE",
    "PIRANHA",
    "PLATYPUS",
    "POODLE",
    "PORCUPINE",
    "PORPOISE",
    "POSSUM",
    "POTOROO",
    "PRONGHORN",
    "PUFFERFISH",
    "PUFFIN",
    "PUG",
    "PUMA",
    "PYTHON",
    "QUAGGA",
    "QUAIL",
    "QUOKKA",
    "QUOLL",
    "RABBIT",
    "RACOON",
    "RAGDOLL",
    "RAT",
    "RATTLESNAKE",
    "RAVEN",
    "REINDEER",
    "RHINO",
    "ROACH",
    "ROBIN",
    "SABERTOOTH",
    "SAILFISH",
    "SALAMANDER",
    "SALMON",
    "SANDFLY",
    "SARDINE",
    "SAWFISH",
    "SCARAB",
    "SCORPION",
    "SEAHORSE",
    "SEAL",
    "SEALION",
    "SERVAL",
    "SHARK",
    "SHEEP",
    "SHOEBILL",
    "SHRIKE",
    "SHRIMP",
    "SIDEWINDER",
    "SILKWORM",
    "SKATE",
    "SKINK",
    "SKUNK",
    "SLOTH",
    "SLUG",
    "SNAIL",
    "SNAKE",
    "SNAPPER",
    "SNOOK",
    "SPARROW",
    "SPIDER",
    "SPRINGBOK",
    "SQUID",
    "SQUIRREL",
    "STAGHORN",
    "STARFISH",
    "STINGRAY",
    "STINKBUG",
    "STOUT",
    "STURGEON",
    "SUGARGLIDER",
    "SUNBEAR",
    "SWALLOW",
    "SWAN",
    "SWIFT",
    "SWORDFISH",
    "TAIPAN",
    "TAKAHE",
    "TAMARIN",
    "TANG",
    "TAPIR",
    "TARANTULA",
    "TARPON",
    "TARSIER",
    "TAURUS",
    "TERMITE",
    "TERRIER",
    "TETRA",
    "THRUSH",
    "THYLACINE",
    "TIGER",
    "TOAD",
    "TORTOISE",
    "TOUCAN",
    "TREADFIN",
    "TREVALLY",
    "TRIGGERFISH",
    "TROUT",
    "TUATARA",
    "TUNA",
    "TURKEY",
    "TURTLE",
    "URCHIN",
    "VIPER",
    "VULTURE",
    "WALLABY",
    "WALLAROO",
    "WALLEYE",
    "WALRUS",
    "WARTHOG",
    "WASP",
    "WATERBUCK",
    "WEASEL",
    "WEEVIL",
    "WEKA",
    "WHALE",
    "WILDCAT",
    "WILDEBEEST",
    "WOLF",
    "WOLFHOUND",
    "WOLVERINE",
    "WOMBAT",
    "WOODCHUCK",
    "WOODPECKER",
    "WORM",
    "WRASSE",
    "WYVERN",
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
    jtac_number = 0

    animals: list[str] = list(ANIMALS)
    existing_alphas: List[str] = []

    @classmethod
    def reset(cls) -> None:
        cls.number = 0
        cls.infantry_number = 0
        cls.convoy_number = 0
        cls.cargo_ship_number = 0
        cls.jtac_number = 0
        cls.animals = list(ANIMALS)
        cls.existing_alphas = []

    @classmethod
    def reset_numbers(cls) -> None:
        cls.number = 0
        cls.infantry_number = 0
        cls.aircraft_number = 0
        cls.convoy_number = 0
        cls.cargo_ship_number = 0
        cls.jtac_number = 0

    @classmethod
    def next_aircraft_name(cls, country: Country, flight: Flight) -> str:
        cls.aircraft_number += 1
        if flight.custom_name:
            name_str = flight.custom_name
        else:
            name_str = "{} {}".format(flight.package.target.name, flight.flight_type)
        return "{}|{}|{}|{}|".format(
            name_str, country.id, cls.aircraft_number, flight.unit_type.name
        )

    @classmethod
    def next_unit_name(cls, country: Country, unit_type: UnitType[Any]) -> str:
        cls.number += 1
        return "unit|{}|{}|{}|".format(country.id, cls.number, unit_type.name)

    @classmethod
    def next_infantry_name(cls, country: Country, unit_type: UnitType[Any]) -> str:
        cls.infantry_number += 1
        return "infantry|{}|{}|{}|".format(
            country.id,
            cls.infantry_number,
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
    def next_jtac_name(cls) -> str:
        name = (
            ALPHA_MILITARY[cls.jtac_number]
            if cls.jtac_number < len(ALPHA_MILITARY)
            else str(cls.jtac_number + 1)
        )
        cls.jtac_number += 1
        return f"JTAC {name}"

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
