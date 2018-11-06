from game.db import assigned_units_split

from .operation import *


class InterceptOperation(Operation):
    location = None  # type: Point
    escort = None  # type: db.AssignedUnitsDict
    transport = None  # type: db.PlaneDict
    interceptors = None  # type: db.AssignedUnitsDict
    airdefense = None  # type: db.AirDefenseDict

    trigger_radius = TRIGGER_RADIUS_LARGE

    def setup(self,
              location: Point,
              escort: db.AssignedUnitsDict,
              transport: db.PlaneDict,
              airdefense: db.AirDefenseDict,
              interceptors: db.AssignedUnitsDict):
        self.location = location
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
            attacker=self.current_mission.country(self.attacker_name),
            defender=self.current_mission.country(self.defender_name),
            position=self.location,
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.current_mission,
                        conflict=conflict)

    def generate(self):
        if self.is_player_attack:
            self.prepare_carriers(db.unitdict_from(self.interceptors))

        self.airgen.generate_transport(self.transport, self.to_cp.at)
        self.airgen.generate_defenders_escort(*assigned_units_split(self.escort), at=self.defenders_starting_position)

        self.airgen.generate_interception(*assigned_units_split(self.interceptors), at=self.attackers_starting_position)

        self.briefinggen.title = "Air Intercept"

        if self.game.player == self.attacker_name:
            self.briefinggen.description = "Intercept enemy supply transport aircraft. Escort will also be present if there are available planes on the base. Operation will be considered successful if most of the targets are destroyed, lowering targets strength as a result"
            self.briefinggen.append_waypoint("TARGET")
            for unit_type, count in self.transport.items():
                self.briefinggen.append_target("{} ({})".format(db.unit_type_name(unit_type), count))
        else:
            self.briefinggen.description = "Escort friendly supply transport aircraft. Operation will be considered failed if most of the targets are destroyed, lowering CP strength as a result"

        super(InterceptOperation, self).generate()

