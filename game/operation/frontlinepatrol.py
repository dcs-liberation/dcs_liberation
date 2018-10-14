from game.db import assigned_units_split

from .operation import *


MAX_DISTANCE_BETWEEN_GROUPS = 12000


class FrontlinePatrolOperation(Operation):
    cas = None  # type: db.AssignedUnitsDict
    escort = None  # type: db.AssignedUnitsDict
    interceptors = None  # type: db.AssignedUnitsDict

    armor_attackers = None  # type: db.ArmorDict
    armor_defenders = None  # type: db.ArmorDict

    def setup(self,
              cas: db.AssignedUnitsDict,
              escort: db.AssignedUnitsDict,
              interceptors: db.AssignedUnitsDict,
              armor_attackers: db.ArmorDict,
              armor_defenders: db.ArmorDict):
        self.cas = cas
        self.escort = escort
        self.interceptors = interceptors

        self.armor_attackers = armor_attackers
        self.armor_defenders = armor_defenders

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(FrontlinePatrolOperation, self).prepare(terrain, is_quick)
        self.defenders_starting_position = None

        conflict = Conflict.frontline_cap_conflict(
            attacker=self.current_mission.country(self.attacker_name),
            defender=self.current_mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.current_mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_defenders_cas(*assigned_units_split(self.cas), at=self.defenders_starting_position)
        self.airgen.generate_defenders_escort(*assigned_units_split(self.escort), at=self.defenders_starting_position)
        self.airgen.generate_migcap(*assigned_units_split(self.interceptors), at=self.attackers_starting_position)

        self.armorgen.generate_vec(self.armor_attackers, self.armor_defenders)

        self.briefinggen.title = "Frontline CAP"
        self.briefinggen.description = "Providing CAP support for ground units attacking enemy lines. Enemy will scramble its CAS and your task is to intercept it. Operation will be considered successful if total number of friendly units will be lower than enemy by at least a factor of 0.8 (i.e. with 12 units from both sides, there should be at least 8 friendly units alive), lowering targets strength as a result."
        self.briefinggen.append_waypoint("CAP AREA IP")
        self.briefinggen.append_waypoint("CAP AREA EGRESS")
        super(FrontlinePatrolOperation, self).generate()
