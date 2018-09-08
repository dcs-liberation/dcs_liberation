from dcs.terrain import Terrain

from gen import *
from .operation import Operation


class NavalInterceptionOperation(Operation):
    strikegroup = None  # type: db.PlaneDict
    interceptors = None  # type: db.PlaneDict
    targets = None  # type: db.ShipDict
    trigger_radius = TRIGGER_RADIUS_LARGE

    def setup(self,
              strikegroup: db.PlaneDict,
              interceptors: db.PlaneDict,
              targets: db.ShipDict):
        self.strikegroup = strikegroup
        self.interceptors = interceptors
        self.targets = targets

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(NavalInterceptionOperation, self).prepare(terrain, is_quick)
        if self.defender_name == self.game.player:
            self.attackers_starting_position = None

        conflict = Conflict.naval_intercept_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(self.mission, conflict)

    def generate(self):
        target_groups = self.shipgen.generate_cargo(units=self.targets)

        self.airgen.generate_ship_strikegroup(
            attackers=self.strikegroup,
            clients=self.attacker_clients,
            target_groups=target_groups,
            at=self.attackers_starting_position
        )

        if self.interceptors:
            self.airgen.generate_defense(
                defenders=self.interceptors,
                clients=self.defender_clients,
                at=self.defenders_starting_position
            )

        self.briefinggen.title = "Naval Intercept"
        self.briefinggen.description = "Destroy supply transport ships. Lowers target strength. Be advised that your flight will not attack anything until you explicitly tell them so by comms menu."

        super(NavalInterceptionOperation, self).generate()

