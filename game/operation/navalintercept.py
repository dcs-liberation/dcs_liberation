from dcs.terrain import Terrain

from gen import *
from .operation import Operation


class NavalInterceptionOperation(Operation):
    strikegroup = None  # type: db.PlaneDict
    interceptors = None  # type: db.PlaneDict
    targets = None  # type: db.ShipDict

    def setup(self,
              strikegroup: db.PlaneDict,
              interceptors: db.PlaneDict,
              targets: db.ShipDict):
        self.strikegroup = strikegroup
        self.interceptors = interceptors
        self.targets = targets

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(NavalInterceptionOperation, self).prepare(terrain, is_quick)

        conflict = Conflict.naval_intercept_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            theater=self.game.theater,
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        self.initialize(self.mission, conflict)

    def generate(self):
        super(NavalInterceptionOperation, self).generate()

        self.airgen.generate_ship_strikegroup(
            attackers= self.strikegroup,
            clients=self.attacker_clients,
            at=self.attackers_starting_position
        )

        self.airgen.generate_interception(
            interceptors=self.interceptors,
            clients=self.defender_clients,
            at=self.defenders_starting_position
        )

        self.shipgen.generate_cargo(units=self.targets)

