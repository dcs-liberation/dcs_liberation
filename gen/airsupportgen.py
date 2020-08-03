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

        CALLSIGNS = ["TKR", "TEX", "FUL", "FUE", ""]
        for i, tanker_unit_type in enumerate(db.find_unittype(Refueling, self.conflict.attackers_side)):
            self.generated_tankers.append(db.unit_type_name(tanker_unit_type))
            tanker_heading = self.conflict.to_cp.position.heading_between_point(self.conflict.from_cp.position) + TANKER_HEADING_OFFSET * i
            tanker_position = player_cp.position.point_from_heading(tanker_heading, TANKER_DISTANCE)
            tanker_group = self.mission.refuel_flight(
                country=self.mission.country(self.game.player_country),
                name=namegen.next_tanker_name(self.mission.country(self.game.player_country)),
                airport=None,
                plane_type=tanker_unit_type,
                position=tanker_position,
                altitude=TANKER_ALT,
                race_distance=58000,
                frequency=130 + i,
                start_type=StartType.Warm,
                speed=574,
                tacanchannel="{}X".format(60 + i),
            )

            tanker_group.points[0].tasks.pop() # Override PyDCS tacan channel
            tanker_group.points[0].tasks.append(ActivateBeaconCommand(97+1, "X", CALLSIGNS[i], True, tanker_group.units[0].id, True))

            tanker_group.points[0].tasks.append(SetInvisibleCommand(True))
            tanker_group.points[0].tasks.append(SetImmortalCommand(True))

        if is_awacs_enabled:
            try:
                awacs_unit = db.find_unittype(AWACS, self.conflict.attackers_side)[0]
                awacs_flight = self.mission.awacs_flight(
                    country=self.mission.country(self.game.player_country),
                    name=namegen.next_awacs_name(self.mission.country(self.game.player_country)),
                    plane_type=awacs_unit,
                    altitude=AWACS_ALT,
                    airport=None,
                    position=self.conflict.position.random_point_within(AWACS_DISTANCE, AWACS_DISTANCE),
                    frequency=133,
                    start_type=StartType.Warm,
                )
                awacs_flight.points[0].tasks.append(SetInvisibleCommand(True))
                awacs_flight.points[0].tasks.append(SetImmortalCommand(True))
            except:
                print("No AWACS for faction")

