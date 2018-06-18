from game import db

from gen.conflictgen import Conflict
from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.settingsgen import *
from gen.awacsgen import *
from gen.visualgen import *

from .operation import Operation

class CaptureOperation(Operation):
    cas = None  # type: db.PlaneDict
    escort = None  # type: db.PlaneDict
    intercept = None  # type: db.PlaneDict
    attack = None  # type: db.ArmorDict
    defense = None  # type: db.ArmorDict
    aa = None  # type: db.AirDefenseDict

    def setup(self,
              cas: db.PlaneDict,
              escort: db.PlaneDict,
              attack: db.ArmorDict,
              intercept: db.PlaneDict,
              defense: db.ArmorDict,
              aa: db.AirDefenseDict):
        self.cas = cas
        self.escort = escort
        self.intercept = intercept
        self.attack = attack
        self.defense = defense
        self.aa = aa

    def prepare(self, terrain: dcs.terrain.Terrain, is_quick: bool):
        super(CaptureOperation, self).prepare(terrain, is_quick)

        self.defenders_starting_position = None
        if self.game.player == self.defender_name:
            self.attackers_starting_position = None

        conflict = Conflict.capture_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )
        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.armorgen.generate(self.attack, self.defense)
        self.aagen.generate(self.aa)

        self.airgen.generate_defense(self.intercept, clients=self.defender_clients, at=self.defenders_starting_position)

        self.airgen.generate_cas_strikegroup(self.cas, clients=self.attacker_clients, at=self.attackers_starting_position)
        self.airgen.generate_strikegroup_escort(self.escort, clients=self.attacker_clients, at=self.attackers_starting_position)

        self.visualgen.generate_target_smokes(self.to_cp)
        super(CaptureOperation, self).generate()

