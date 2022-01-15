import logging
import random
from typing import Optional

from dcs.unitgroup import VehicleGroup

from game import db, Game
from game.theater.theatergroundobject import CoastalSiteGroundObject
from gen.to_remove.silkworm import SilkwormGenerator

COASTAL_MAP = {
    "SilkwormGenerator": SilkwormGenerator,
}
