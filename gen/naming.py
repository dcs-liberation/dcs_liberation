from game import db
import random

ALPHA_MILITARY = ["Alpha","Bravo","Charlie","Delta","Echo","Foxtrot",
                  "Golf","Hotel","India","Juliet","Kilo","Lima","Mike",
                  "November","Oscar","Papa","Quebec","Romeo","Sierra",
                  "Tango","Uniform","Victor","Whisky","XRay","Yankee",
                  "Zulu","Zero"]

class NameGenerator:
    number = 0

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

    def __init__(self):
        self.number = 0
        self.ANIMALS = NameGenerator.ANIMALS.copy()

    def reset(self):
        self.number = 0
        self.ANIMALS = NameGenerator.ANIMALS.copy()

    def next_unit_name(self, country, parent_base_id, unit_type):
        self.number += 1
        return "unit|{}|{}|{}|{}|".format(country.id, self.number, parent_base_id, db.unit_type_name(unit_type))

    def next_infantry_name(self, country, parent_base_id, unit_type):
        self.number += 1
        return "infantry|{}|{}|{}|{}|".format(country.id, self.number, parent_base_id, db.unit_type_name(unit_type))

    def next_basedefense_name(self):
        return "basedefense_aa|0|0|"

    def next_awacs_name(self, country):
        self.number += 1
        return "awacs|{}|{}|0|".format(country.id, self.number)

    def next_tanker_name(self, country, unit_type):
        self.number += 1
        return "tanker|{}|{}|0|{}".format(country.id, self.number, db.unit_type_name(unit_type))

    def next_carrier_name(self, country):
        self.number += 1
        return "carrier|{}|{}|0|".format(country.id, self.number)

    def random_objective_name(self):
        if len(self.ANIMALS) == 0:
            return random.choice(ALPHA_MILITARY).upper() + "#" + str(random.randint(0, 100))
        else:
            animal = random.choice(self.ANIMALS)
            self.ANIMALS.remove(animal)
            return animal


namegen = NameGenerator()



