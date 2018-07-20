from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.task import *
from dcs.terrain.terrain import NoParkingSlotError

TANKER_DISTANCE = 15000
TANKER_ALT = 10000

AWACS_DISTANCE = 150000
AWACS_ALT = 10000


class AirSupportConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def generate(self, is_awacs_enabled):
        tanker_unit = db.find_unittype(Refueling, self.conflict.attackers_side.name)[0]
        tanker_heading = self.conflict.to_cp.position.heading_between_point(self.conflict.from_cp.position)
        tanker_position = self.conflict.from_cp.position.point_from_heading(tanker_heading, TANKER_DISTANCE)
        tanker_group = self.mission.refuel_flight(
            country=self.mission.country(self.game.player),
            name=namegen.next_tanker_name(self.mission.country(self.game.player)),
            airport=None,
            plane_type=tanker_unit,
            position=tanker_position,
            altitude=TANKER_ALT,
            frequency=140,
            start_type=StartType.Warm,
            tacanchannel="99X",
        )

        tanker_group.points[0].tasks.append(ActivateBeaconCommand(channel=10, unit_id=tanker_group.id, aa=False))

        if is_awacs_enabled:
            awacs_unit = db.find_unittype(AWACS, self.conflict.attackers_side.name)[0]
            self.mission.awacs_flight(
                country=self.mission.country(self.game.player),
                name=namegen.next_awacs_name(self.mission.country(self.game.player),),
                plane_type=awacs_unit,
                altitude=AWACS_ALT,
                airport=None,
                position=self.conflict.position.random_point_within(AWACS_DISTANCE, AWACS_DISTANCE),
                frequency=180,
                start_type=StartType.Warm,
            )
