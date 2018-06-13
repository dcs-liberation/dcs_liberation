from game import db

from theater.conflicttheater import ConflictTheater
from .conflictgen import *
from .naming import *

from dcs.mission import *

DISTANCE_FACTOR = 4, 5
EXTRA_AA_MIN_DISTANCE = 70000

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


class ExtraAAConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, theater: ConflictTheater, player_name: Country, enemy_name: Country):
        self.mission = mission
        self.theater = theater
        self.conflict = conflict
        self.player_name = player_name
        self.enemy_name = enemy_name

    def generate(self):
        for cp in self.theater.controlpoints:
            if cp.position.distance_to_point(self.conflict.position) > EXTRA_AA_MIN_DISTANCE:
                country_name = cp.captured and self.player_name or self.enemy_name

                self.mission.vehicle_group(
                    country=self.mission.country(country_name),
                    name=namegen.next_ground_group_name(),
                    _type=random.choice(db.find_unittype(AirDefence, country_name)),
                    position=cp.position,
                    group_size=2
                )

