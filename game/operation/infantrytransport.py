from game.db import assigned_units_split

from .operation import *


class InfantryTransportOperation(Operation):
    transport = None  # type: db.AssignedUnitsDict
    aa = None  # type: db.AirDefenseDict

    def setup(self, transport: db.AssignedUnitsDict, aa: db.AirDefenseDict):
        self.transport = transport
        self.aa = aa

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(InfantryTransportOperation, self).prepare(terrain, is_quick)

        conflict = Conflict.transport_conflict(
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            attacker=self.current_mission.country(self.attacker_country),
            defender=self.current_mission.country(self.defender_country),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.current_mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_passenger_transport(*assigned_units_split(self.transport), at=self.attackers_starting_position)

        self.armorgen.generate_passengers(count=6)
        self.aagen.generate_at_defenders_location(self.aa)

        self.visualgen.generate_transportation_marker(self.conflict.ground_attackers_location)
        self.visualgen.generate_transportation_destination(self.conflict.position)

        self.briefinggen.title = "Infantry transport"
        self.briefinggen.description = "Helicopter operation to transport infantry troops from the base to the front line. Lowers target strength"
        self.briefinggen.append_waypoint("DROP POINT")

        # TODO: horrible, horrible hack
        # this will disable vehicle activation triggers,
        # which aren't needed on this type of missions
        self.is_quick = True
        super(InfantryTransportOperation, self).generate()
        self.is_quick = False
