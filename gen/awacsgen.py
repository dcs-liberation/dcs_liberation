from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.task import *
from dcs.terrain.terrain import NoParkingSlotError

AWACS_DISTANCE = 150000
AWACS_ALT = 10000


class AWACSConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def generate(self):
        plane = db.find_unittype(AWACS, self.conflict.attackers_side.name)[0]

        self.mission.awacs_flight(
            country=self.conflict.attackers_side,
            name=namegen.next_awacs_group_name(),
            plane_type=plane,
            altitude=AWACS_ALT,
            airport=None,
            position=self.conflict.position.random_point_within(AWACS_DISTANCE, AWACS_DISTANCE))
