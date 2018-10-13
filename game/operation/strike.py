from game.db import assigned_units_split

from .operation import *


class StrikeOperation(Operation):
    strikegroup = None  # type: db.AssignedUnitsDict
    escort = None  # type: db.AssignedUnitsDict
    interceptors = None  # type: db.AssignedUnitsDict

    def setup(self,
              strikegroup: db.AssignedUnitsDict,
              escort: db.AssignedUnitsDict,
              interceptors: db.AssignedUnitsDict):
        self.strikegroup = strikegroup
        self.escort = escort
        self.interceptors = interceptors

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(StrikeOperation, self).prepare(terrain, is_quick)

        self.defenders_starting_position = None
        if self.game.player == self.defender_name:
            self.attackers_starting_position = None

        conflict = Conflict.strike_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        for global_cp in self.game.theater.controlpoints:
            if not global_cp.is_global:
                continue

            ship = self.shipgen.generate_carrier(type=db.find_unittype(Carriage, self.game.player)[0],
                                                 country=self.game.player,
                                                 at=global_cp.at)

            if global_cp == self.from_cp and not self.is_quick:
                self.attackers_starting_position = ship

        targets = []  # type: typing.List[typing.Tuple[str, str, Point]]
        category_counters = {}  # type: typing.Dict[str, int]
        processed_groups = []
        for object in self.to_cp.ground_objects:
            if object.group_identifier in processed_groups:
                continue

            processed_groups.append(object.group_identifier)
            category_counters[object.category] = category_counters.get(object.category, 0) + 1
            markpoint_name = "{}{}".format(object.name_abbrev, category_counters[object.category])
            targets.append((str(object), markpoint_name, object.position))

        targets.sort(key=lambda x: self.from_cp.position.distance_to_point(x[2]))

        for (name, markpoint_name, _) in targets:
            self.briefinggen.append_waypoint("TARGET {} (TP {})".format(str(name), markpoint_name))

        planes_flights = {k: v for k, v in self.strikegroup.items() if k in plane_map.values()}
        self.airgen.generate_ground_attack_strikegroup(*assigned_units_split(planes_flights),
                                                       targets=[(mp, pos) for (n, mp, pos) in targets],
                                                       at=self.attackers_starting_position)

        heli_flights = {k: v for k, v in self.strikegroup.items() if k in helicopters.helicopter_map.values()}
        if heli_flights:
            self.briefinggen.append_frequency("FARP", "127.5 MHz AM")
            for farp, dict in zip(self.groundobjectgen.generate_farps(sum([x[0] for x in heli_flights.values()])),
                                  db.assignedunits_split_to_count(heli_flights, self.groundobjectgen.FARP_CAPACITY)):
                self.airgen.generate_ground_attack_strikegroup(*assigned_units_split(dict),
                                                               targets=[(mp, pos) for (n, mp, pos) in targets],
                                                               at=farp,
                                                               escort=len(planes_flights) == 0)

        self.airgen.generate_attackers_escort(*assigned_units_split(self.escort), at=self.attackers_starting_position)
        self.airgen.generate_barcap(*assigned_units_split(self.interceptors), at=self.defenders_starting_position)

        self.briefinggen.title = "Strike"
        self.briefinggen.description = "Destroy infrastructure assets and military supplies in the region. Each building destroyed will lower targets strength."
        super(StrikeOperation, self).generate()
