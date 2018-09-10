from game.db import assigned_units_split

from gen.triggergen import *

from .operation import *


class BaseAttackOperation(Operation):
    cas = None  # type: db.AssignedUnitsDict
    escort = None  # type: db.AssignedUnitsDict
    intercept = None  # type: db.AssignedUnitsDict
    attack = None  # type: db.ArmorDict
    defense = None  # type: db.ArmorDict
    aa = None  # type: db.AirDefenseDict

    trigger_radius = TRIGGER_RADIUS_SMALL

    def setup(self,
              cas: db.AssignedUnitsDict,
              escort: db.AssignedUnitsDict,
              attack: db.AssignedUnitsDict,
              intercept: db.AssignedUnitsDict,
              defense: db.ArmorDict,
              aa: db.AirDefenseDict):
        self.cas = cas
        self.escort = escort
        self.intercept = intercept
        self.attack = attack
        self.defense = defense
        self.aa = aa

    def prepare(self, terrain: dcs.terrain.Terrain, is_quick: bool):
        super(BaseAttackOperation, self).prepare(terrain, is_quick)

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
        self.armorgen.generate(self.attack, self.defense)
        self.aagen.generate(self.aa)

        self.airgen.generate_defense(*assigned_units_split(self.intercept), at=self.defenders_starting_position)

        self.airgen.generate_cas_strikegroup(*assigned_units_split(self.cas), at=self.attackers_starting_position)
        self.airgen.generate_attackers_escort(*assigned_units_split(self.escort), at=self.attackers_starting_position)

        self.visualgen.generate_target_smokes(self.to_cp)

        self.briefinggen.title = "Base attack"
        self.briefinggen.description = "The goal of an attacker is to lower defender presence by destroying their armor and aircraft. Base will be considered captured if attackers on the ground overrun the defenders. Be advised that your flight will not attack anything until you explicitly tell them so by comms menu."
        super(BaseAttackOperation, self).generate()

