import random

from gen.sam.group_generator import GroupGenerator
from dcs import unitgroup
from dcs.point import PointAction
from dcs.unit import Ship
from dcs.ships import *


class DDGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction, ddtype):
        self.game = game
        self.go = ground_object
        self.position = ground_object.position
        self.heading = random.randint(0, 359)
        self.faction = faction
        self.vg = unitgroup.ShipGroup(self.game.next_group_id(), self.groupNamePrefix + self.go.group_identifier)
        wp = self.vg.add_waypoint(self.position, 0)
        wp.ETA_locked = True
        self.ddtype = ddtype

    def generate(self):
        self.add_unit(self.ddtype, "DD1", self.position.x + 500, self.position.y + 900, self.heading)
        self.add_unit(self.ddtype, "DD2", self.position.x + 500, self.position.y - 900, self.heading)
        self.get_generated_group().points[0].speed = 20
    
    def add_unit(self, unit_type, name, pos_x, pos_y, heading):
        nn = "cgroup|" + str(self.go.cp_id) + '|' + str(self.go.group_id) + '|' + str(self.go.group_identifier) + "|" + name

        unit = Ship(self.game.next_unit_id(),
                       nn, unit_type)
        unit.position.x = pos_x
        unit.position.y = pos_y
        unit.heading = heading
        self.vg.add_unit(unit)
        return unit



class OliverHazardPerryGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(OliverHazardPerryGroupGenerator, self).__init__(game, ground_object, faction, Oliver_Hazzard_Perry_class)


class ArleighBurkeGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(ArleighBurkeGroupGenerator, self).__init__(game, ground_object, faction, USS_Arleigh_Burke_IIa)
