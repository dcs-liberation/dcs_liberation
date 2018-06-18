from dcs.terrain import Terrain

from gen import *
from .operation import Operation


class InterceptOperation(Operation):
    escort = None  # type: db.PlaneDict
    transport = None  # type: db.PlaneDict
    interceptors = None  # type: db.PlaneDict
    airdefense = None  # type: db.AirDefenseDict

    def setup(self,
              escort: db.PlaneDict,
              transport: db.PlaneDict,
              airdefense: db.AirDefenseDict,
              interceptors: db.PlaneDict):
        self.escort = escort
        self.transport = transport
        self.airdefense = airdefense
        self.interceptors = interceptors

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(InterceptOperation, self).prepare(terrain, is_quick)
        self.defenders_starting_position = None
        if self.defender_name == self.game.player:
            self.attackers_starting_position = None

        conflict = Conflict.intercept_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_transport(self.transport, self.to_cp.at)
        self.airgen.generate_transport_escort(self.escort, clients=self.defender_clients)

        if self.from_cp.is_global:
            super(InterceptOperation, self).generate()
            self.airgen.generate_interception(self.interceptors, clients=self.attacker_clients, at=self.attackers_starting_position)
        else:
            self.airgen.generate_interception(self.interceptors, clients=self.attacker_clients, at=self.attackers_starting_position)
            super(InterceptOperation, self).generate()

