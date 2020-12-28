import random

from dcs.country import Country
from dcs.unittype import UnitType

from game import db

from gen.flights.flight import Flight

ALPHA_MILITARY = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot",
                  "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike",
                  "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra",
                  "Tango", "Uniform", "Victor", "Whisky", "XRay", "Yankee",
                  "Zulu", "Zero"]

ANIMALS = [
        "SHARK", "TORTOISE", "BAT", "PANGOLIN", "AARDWOLF",
        "MONKEY", "BUFFALO", "DOG", "BOBCAT", "LYNX", "PANTHER", "TIGER",
        "LION", "OWL", "BUTTERFLY", "BISON", "DUCK", "COBRA", "MAMBA",
        "DOLPHIN", "PHEASANT", "ARMADILLLO", "RACOON", "ZEBRA", "COW", "COYOTE", "FOX",
        "LIGHTFOOT", "COTTONMOUTH", "TAURUS", "VIPER", "CASTOR", "GIRAFFE", "SNAKE",
        "MONSTER", "ALBATROSS", "HAWK", "DOVE", "MOCKINGBIRD", "GECKO", "ORYX", "GORILLA",
        "HARAMBE", "GOOSE", "MAVERICK", "HARE", "JACKAL", "LEOPARD", "CAT", "MUSK", "ORCA",
        "OCELOT", "BEAR", "PANDA", "GULL", "PENGUIN", "PYTHON", "RAVEN", "DEER", "MOOSE",
        "REINDEER", "SHEEP", "GAZELLE", "INSECT", "VULTURE", "WALLABY", "KANGAROO", "KOALA",
        "KIWI", "WHALE", "FISH", "RHINO", "HIPPO", "RAT", "WOODPECKER", "WORM", "BABOON",
        "YAK", "SCORPIO", "HORSE", "POODLE", "CENTIPEDE", "CHICKEN", "CHEETAH", "CHAMELEON",
        "CATFISH", "CATERPILLAR", "CARACAL", "CAMEL", "CAIMAN", "BARRACUDA", "BANDICOOT",
        "ALLIGATOR", "BONGO", "CORAL", "ELEPHANT", "ANTELOPE", "CRAB", "DACHSHUND", "DODO",
        "FLAMINGO", "FERRET", "FALCON", "BULLDOG", "DONKEY", "IGUANA", "TAMARIN", "HARRIER",
        "GRIZZLY", "GREYHOUND", "GRASSHOPPER", "JAGUAR", "LADYBUG", "KOMODO", "DRAGON", "LIZARD",
        "LLAMA", "LOBSTER", "OCTOPUS", "MANATEE", "MAGPIE", "MACAW", "OSTRICH", "OYSTER",
        "MOLE", "MULE", "MOTH", "MONGOOSE", "MOLLY", "MEERKAT", "MOUSE", "PEACOCK", "PIKE", "ROBIN",
        "RAGDOLL", "PLATYPUS", "PELICAN", "PARROT", "PORCUPINE", "PIRANHA", "PUMA", "PUG", "TAPIR",
        "TERMITE", "URCHIN", "SHRIMP", "TURKEY", "TOUCAN", "TETRA", "HUSKY", "STARFISH", "SWAN",
        "FROG", "SQUIRREL", "WALRUS", "WARTHOG", "CORGI", "WEASEL", "WOMBAT", "WOLVERINE", "MAMMOTH",
        "TOAD", "WOLF", "ZEBU", "SEAL", "SKATE", "JELLYFISH", "MOSQUITO", "LOCUST", "SLUG", "SNAIL",
        "HEDGEHOG", "PIGLET", "FENNEC", "BADGER", "ALPACA", "DINGO", "COLT", "SKUNK", "BUNNY", "IMPALA",
        "GUANACO", "CAPYBARA", "ELK", "MINK", "PRONGHORN", "CROW", "BUMBLEBEE", "FAWN", "OTTER", "WATERBUCK",
        "JERBOA", "KITTEN", "ARGALI", "OX", "MARE", "FINCH", "BASILISK", "GOPHER", "HAMSTER", "CANARY", "WOODCHUCK",
        "ANACONDA"
    ]

class NameGenerator:
    number = 0
    infantry_number = 0

    ANIMALS = ANIMALS

    @classmethod
    def reset(cls):
        cls.number = 0
        cls.infantry_number = 0
        cls.ANIMALS = ANIMALS

    @classmethod
    def reset_numbers(cls):
        cls.number = 0
        cls.infantry_number = 0

    @classmethod
    def next_aircraft_name(cls, country: Country, parent_base_id: int, flight: Flight):
        cls.number += 1
        try:
            if flight.custom_name:
                name_str = flight.custom_name
            else:
                name_str = "{} {}".format(
                    flight.package.target.name, flight.flight_type)
        except AttributeError:  # Here to maintain save compatibility with 2.3
            name_str = "{} {}".format(
                flight.package.target.name, flight.flight_type)
        return "{}|{}|{}|{}|{}|".format(name_str, country.id, cls.number, parent_base_id, db.unit_type_name(flight.unit_type))

    @classmethod
    def next_unit_name(cls, country: Country, parent_base_id: int, unit_type: UnitType):
        cls.number += 1
        return "unit|{}|{}|{}|{}|".format(country.id, cls.number, parent_base_id, db.unit_type_name(unit_type))

    @classmethod
    def next_infantry_name(cls, country: Country, parent_base_id: int, unit_type: UnitType):
        cls.infantry_number += 1
        return "infantry|{}|{}|{}|{}|".format(country.id, cls.infantry_number, parent_base_id, db.unit_type_name(unit_type))

    @staticmethod
    def next_basedefense_name():
        return "basedefense_aa|0|0|"

    @classmethod
    def next_awacs_name(cls, country: Country):
        cls.number += 1
        return "awacs|{}|{}|0|".format(country.id, cls.number)

    @classmethod
    def next_tanker_name(cls, country: Country, unit_type: UnitType):
        cls.number += 1
        return "tanker|{}|{}|0|{}".format(country.id, cls.number, db.unit_type_name(unit_type))

    @classmethod
    def next_carrier_name(cls, country: Country):
        cls.number += 1
        return "carrier|{}|{}|0|".format(country.id, cls.number)

    @classmethod
    def random_objective_name(cls):
        if len(cls.ANIMALS) == 0:
            return random.choice(ALPHA_MILITARY).upper() + "#" + str(random.randint(0, 100))
        else:
            animal = random.choice(cls.ANIMALS)
            cls.ANIMALS.remove(animal)
            return animal


namegen = NameGenerator
