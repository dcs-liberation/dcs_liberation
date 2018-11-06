from game.db import assigned_units_split

from .operation import *


MAX_DISTANCE_BETWEEN_GROUPS = 12000


class FrontlineAttackOperation(Operation):
    strikegroup = None  # type: db.AssignedUnitsDict
    attackers = None  # type: db.ArmorDict
    target = None  # type: db.ArmorDict

    def setup(self,
              target: db.ArmorDict,
              attackers: db.ArmorDict,
              strikegroup: db.AssignedUnitsDict):
        self.strikegroup = strikegroup
        self.target = target
        self.attackers = attackers

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(FrontlineAttackOperation, self).prepare(terrain, is_quick)
        if self.defender_name == self.game.player:
            self.attackers_starting_position = None
            self.defenders_starting_position = None

        conflict = Conflict.frontline_cas_conflict(
            attacker=self.current_mission.country(self.attacker_name),
            defender=self.current_mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.current_mission,
                        conflict=conflict)

    def generate(self):
        if self.is_player_attack:
            self.prepare_carriers(db.unitdict_from(self.strikegroup))

        self.armorgen.generate_vec(self.attackers, self.target)

        planes_flights = {k: v for k, v in self.strikegroup.items() if k in plane_map.values()}
        self.airgen.generate_cas_strikegroup(*assigned_units_split(planes_flights), at=self.attackers_starting_position)

        heli_flights = {k: v for k, v in self.strikegroup.items() if k in helicopters.helicopter_map.values()}
        if heli_flights:
            self.briefinggen.append_frequency("FARP + Heli flights", "127.5 MHz AM")
            for farp, dict in zip(self.groundobjectgen.generate_farps(sum([x[0] for x in heli_flights.values()])),
                                  db.assignedunits_split_to_count(heli_flights, self.groundobjectgen.FARP_CAPACITY)):
                self.airgen.generate_cas_strikegroup(*assigned_units_split(dict),
                                                     at=farp,
                                                     escort=len(planes_flights) == 0)

        self.briefinggen.title = "Frontline CAS"
        self.briefinggen.description = "Provide CAS for the ground forces attacking enemy lines. Operation will be considered successful if total number of enemy units will be lower than your own by a factor of 1.5 (i.e. with 12 units from both sides, enemy forces need to be reduced to at least 8), meaning that you (and, probably, your wingmans) should concentrate on destroying the enemy units. Target base strength will be lowered as a result. Be advised that your flight will not attack anything until you explicitly tell them so by comms menu."
        self.briefinggen.append_waypoint("CAS AREA IP")
        self.briefinggen.append_waypoint("CAS AREA EGRESS")
        super(FrontlineAttackOperation, self).generate()
