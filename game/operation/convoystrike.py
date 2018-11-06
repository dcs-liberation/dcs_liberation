from game.db import assigned_units_split

from .operation import *


class ConvoyStrikeOperation(Operation):
    strikegroup = None  # type: db.AssignedUnitsDict
    target = None  # type: db.ArmorDict

    def setup(self,
              target: db.ArmorDict,
              strikegroup: db.AssignedUnitsDict):
        self.strikegroup = strikegroup
        self.target = target

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(ConvoyStrikeOperation, self).prepare(terrain, is_quick)

        conflict = Conflict.convoy_strike_conflict(
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

        self.armorgen.generate_convoy(self.target)

        self.briefinggen.append_waypoint("TARGET")
        super(ConvoyStrikeOperation, self).generate()
