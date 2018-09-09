from dcs.terrain import Terrain

from game import db
from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.triggergen import *
from gen.airsupportgen import *
from gen.visualgen import *
from gen.conflictgen import Conflict

from .operation import Operation


class StrikeOperation(Operation):
    strikegroup = None  # type: db.PlaneDict
    escort = None  # type: db.PlaneDict
    interceptors = None  # type: db.PlaneDict

    def setup(self,
              strikegroup: db.PlaneDict,
              escort: db.PlaneDict,
              interceptors: db.PlaneDict):
        self.strikegroup = strikegroup
        self.escort = escort
        self.interceptors = interceptors

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(StrikeOperation, self).prepare(terrain, is_quick)

        self.defenders_starting_position = None
        if self.game.player == self.defender_name:
            self.attackers_starting_position = None

        conflict = Conflict.capture_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        targets = []  # type: typing.List[typing.Tuple[str, Point]]
        category_counters = {}  # type: typing.Dict[str, int]
        processed_groups = []
        for object in self.to_cp.ground_objects:
            if object.group_id in processed_groups:
                continue

            processed_groups.append(object.group_id)

            category_counters[object.category] = category_counters.get(object.category, 0) + 1
            markpoint_name = "{}{}".format(object.name_abbrev, category_counters[object.category])
            targets.append((markpoint_name, object.position))
            self.briefinggen.append_target(str(object), markpoint_name)

        targets.sort(key=lambda x: self.from_cp.position.distance_to_point(x[1]))

        self.airgen.generate_ground_attack_strikegroup(strikegroup=self.strikegroup,
                                                       targets=targets,
                                                       clients=self.attacker_clients,
                                                       at=self.attackers_starting_position)

        self.airgen.generate_attackers_escort(self.escort,
                                              clients=self.attacker_clients,
                                              at=self.attackers_starting_position)

        self.airgen.generate_barcap(patrol=self.interceptors,
                                    clients={},
                                    at=self.defenders_starting_position)

        self.briefinggen.title = "Strike"
        self.briefinggen.description = "Destroy infrastructure assets and military supplies in the region. Each building destroyed will lower targets strength."
        super(StrikeOperation, self).generate()
