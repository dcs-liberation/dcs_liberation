from game.db import assigned_units_split

from .operation import *


class NavalInterceptionOperation(Operation):
    strikegroup = None  # type: db.AssignedUnitsDict
    interceptors = None  # type: db.AssignedUnitsDict
    targets = None  # type: db.ShipDict
    trigger_radius = TRIGGER_RADIUS_LARGE

    def setup(self,
              strikegroup: db.AssignedUnitsDict,
              interceptors: db.AssignedUnitsDict,
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
        self.prepare_carriers(db.unitdict_from(self.strikegroup))

        target_groups = self.shipgen.generate_cargo(units=self.targets)

        self.airgen.generate_ship_strikegroup(
            *assigned_units_split(self.strikegroup),
            target_groups=target_groups,
            at=self.attackers_starting_position
        )

        if self.interceptors:
            self.airgen.generate_defense(
                *assigned_units_split(self.interceptors),
                at=self.defenders_starting_position
            )

        self.briefinggen.title = "Naval Intercept"
        if self.game.player == self.attacker_name:
            self.briefinggen.description = "Destroy supply transport ships. Lowers target strength. Be advised that your flight will not attack anything until you explicitly tell them so by comms menu."
            for unit_type, count in self.targets.items():
                self.briefinggen.append_target("{} ({})".format(db.unit_type_name(unit_type), count))
        else:
            self.briefinggen.description = "Protect supply transport ships."
        self.briefinggen.append_waypoint("TARGET")

        super(NavalInterceptionOperation, self).generate()

