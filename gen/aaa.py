from game import *

from theater.conflicttheater import ConflictTheater
from .conflictgen import *
from .naming import *

from dcs.mission import *

DISTANCE_FACTOR = 0.5, 1
EXTRA_AA_MIN_DISTANCE = 35000
EXTRA_AA_POSITION_FROM_CP = 550


class AAConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def generate_at_defenders_location(self, units: db.AirDefenseDict):
        for unit_type, count in units.items():
            for _ in range(count):
                self.m.vehicle_group(
                    country=self.conflict.defenders_side,
                    name=namegen.next_ground_group_name(),
                    _type=unit_type,
                    position=self.conflict.ground_defenders_location.random_point_within(100, 100),
                    group_size=1)

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
    def __init__(self, mission: Mission, conflict: Conflict, game, player_name: Country, enemy_name: Country):
        self.mission = mission
        self.game = game
        self.conflict = conflict
        self.player_name = player_name
        self.enemy_name = enemy_name

    def generate(self):
        from theater.conflicttheater import ControlPoint

        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue

            if cp.position.distance_to_point(self.conflict.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            if cp.position.distance_to_point(self.conflict.from_cp.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            country_name = cp.captured and self.player_name or self.enemy_name
            position = cp.position.point_from_heading(0, EXTRA_AA_POSITION_FROM_CP)

            self.mission.vehicle_group(
                country=self.mission.country(country_name),
                name=namegen.next_ground_group_name(),
                _type=db.EXTRA_AA[country_name],
                position=position,
                group_size=2
            )

