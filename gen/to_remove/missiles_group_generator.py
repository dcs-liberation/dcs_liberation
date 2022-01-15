import logging
import random
from typing import Optional

from dcs.unitgroup import VehicleGroup

from game import db, Game
from game.theater.theatergroundobject import MissileSiteGroundObject
from gen.to_remove.scud_site import ScudGenerator
from gen.to_remove.v1_group import V1GroupGenerator

MISSILES_MAP = {"V1GroupGenerator": V1GroupGenerator, "ScudGenerator": ScudGenerator}
