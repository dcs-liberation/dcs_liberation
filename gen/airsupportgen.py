from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.task import *
from dcs.terrain.terrain import NoParkingSlotError

TANKER_DISTANCE = 15000
TANKER_ALT = 4572
TANKER_HEADING_OFFSET = 45

AWACS_DISTANCE = 150000
AWACS_ALT = 13000


class AirSupportConflictGenerator:
    generated_tankers = None  # type: typing.List[str]

    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game
        self.generated_tankers = []

    @classmethod
    def support_tasks(cls) -> typing.Collection[typing.Type[MainTask]]:
        return [Refueling, AWACS]

    def generate(self, is_awacs_enabled):
        player_cp = self.conflict.from_cp if self.conflict.from_cp.captured else self.conflict.to_cp

        for i, tanker_unit_type in enumerate(db.find_unittype(Refueling, self.conflict.attackers_side.name)):
            self.generated_tankers.append(db.unit_type_name(tanker_unit_type))
            tanker_heading = self.conflict.to_cp.position.heading_between_point(self.conflict.from_cp.position) + TANKER_HEADING_OFFSET * i
            tanker_position = player_cp.position.point_from_heading(tanker_heading, TANKER_DISTANCE)
            tanker_group = self.mission.refuel_flight(
                country=self.mission.country(self.game.player),
                name=namegen.next_tanker_name(self.mission.country(self.game.player)),
                airport=None,
                plane_type=tanker_unit_type,
                position=tanker_position,
                altitude=TANKER_ALT,
                frequency=130 + i,
                start_type=StartType.Warm,
                tacanchannel="{}X".format(97 + i),
            )

            tanker_group.points[0].tasks.append(ActivateBeaconCommand(channel=97 + i, unit_id=tanker_group.id, aa=False))
            tanker_group.points[0].tasks.append(SetInvisibleCommand(True))
            tanker_group.points[0].tasks.append(SetImmortalCommand(True))

        if is_awacs_enabled:
            awacs_unit = db.find_unittype(AWACS, self.conflict.attackers_side.name)[0]
            awacs_flight = self.mission.awacs_flight(
                country=self.mission.country(self.game.player),
                name=namegen.next_awacs_name(self.mission.country(self.game.player)),
                plane_type=awacs_unit,
                altitude=AWACS_ALT,
                airport=None,
                position=self.conflict.position.random_point_within(AWACS_DISTANCE, AWACS_DISTANCE),
                frequency=133,
                start_type=StartType.Warm,
            )

            awacs_flight.points[0].tasks.append(SetInvisibleCommand(True))
            awacs_flight.points[0].tasks.append(SetImmortalCommand(True))
