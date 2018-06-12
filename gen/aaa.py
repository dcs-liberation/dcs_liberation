from game import db

from .conflictgen import *
from .naming import *

from dcs.mission import *

DISTANCE_FACTOR = 4, 5

class AAConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def generate(self, units: db.AirDefenseDict):
        for type, count in units.items():
            for _, radial in zip(range(count), self.conflict.radials):
                distance = randint(self.conflict.size * DISTANCE_FACTOR[0], self.conflict.size * DISTANCE_FACTOR[1])
                p = self.conflict.position.point_from_heading(radial, distance)

                self.m.vehicle_group(
                        country=self.conflict.defenders_side,
                        name=namegen.next_ground_group_name(),
                        _type=type,
                        position=p,
                        group_size=1)

