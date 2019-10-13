from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.mission import *

from .conflictgen import *
from .naming import *

DISTANCE_FACTOR = 0.5, 1
EXTRA_AA_MIN_DISTANCE = 50000
EXTRA_AA_MAX_DISTANCE = 150000
EXTRA_AA_POSITION_FROM_CP = 550

class ExtraAAConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game, player_country: Country, enemy_country: Country):
        self.mission = mission
        self.game = game
        self.conflict = conflict
        self.player_country = player_country
        self.enemy_country = enemy_country

    def generate(self):

        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue

            if cp.position.distance_to_point(self.conflict.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            if cp.position.distance_to_point(self.conflict.from_cp.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            if cp.position.distance_to_point(self.conflict.to_cp.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            if cp.position.distance_to_point(self.conflict.position) > EXTRA_AA_MAX_DISTANCE:
                continue

            country_name = cp.captured and self.player_country or self.enemy_country
            position = cp.position.point_from_heading(0, EXTRA_AA_POSITION_FROM_CP)

            self.mission.vehicle_group(
                country=self.mission.country(country_name),
                name=namegen.next_basedefense_name(),
                _type=db.EXTRA_AA[country_name],
                position=position,
                group_size=1
            )

