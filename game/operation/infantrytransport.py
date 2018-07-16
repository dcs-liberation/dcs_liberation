from dcs.terrain import Terrain

from game import db
from gen.armor import *
from gen.aircraft import *
from gen.aaa import *
from gen.shipgen import *
from gen.triggergen import *
from gen.airsupportgen import *
from gen.visualgen import *
from gen.conflictgen import Conflict

from .operation import Operation


class InfantryTransportOperation(Operation):
    transport = None  # type: db.HeliDict
    aa = None  # type: db.AirDefenseDict

    def setup(self, transport: db.HeliDict, aa: db.AirDefenseDict):
        self.transport = transport
        self.aa = aa

    def prepare(self, terrain: Terrain, is_quick: bool):
        super(InfantryTransportOperation, self).prepare(terrain, is_quick)

        conflict = Conflict.transport_conflict(
            attacker=self.mission.country(self.attacker_name),
            defender=self.mission.country(self.defender_name),
            from_cp=self.from_cp,
            to_cp=self.to_cp,
            theater=self.game.theater
        )

        self.initialize(mission=self.mission,
                        conflict=conflict)

    def generate(self):
        self.airgen.generate_passenger_transport(
            helis=self.transport,
            clients=self.attacker_clients,
            at=self.attackers_starting_position
        )

        self.armorgen.generate_passengers(count=6)
        self.aagen.generate_at_defenders_location(self.aa)

        self.visualgen.generate_transportation_marker(self.conflict.ground_attackers_location)
        self.visualgen.generate_transportation_destination(self.conflict.position)

        # TODO: horrible, horrible hack
        # this will disable vehicle activation triggers,
        # which aren't needed on this type of missions
        self.is_quick = True
        super(InfantryTransportOperation, self).generate()
        self.is_quick = False
