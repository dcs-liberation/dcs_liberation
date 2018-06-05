import typing
import pdb
import dcs

from random import randint

import globals

from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.vehicles import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.mapping import *
from dcs.point import *
from dcs.task import *


class ShipGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, position: Point):
        self.m = mission
        self.conflict = conflict
        self.position = position

    def generate(self):
        self.m.ship_group(
            country=self.conflict.attackers_side,
            name=namegen.next_transport_group_name(),
            _type=dcs.ships.CVN_74_John_C__Stennis,
            position=self.position)
