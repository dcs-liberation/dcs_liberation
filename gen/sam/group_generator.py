import math
import random

from dcs import unitgroup
from dcs.point import PointAction
from dcs.unit import Vehicle


class GroupGenerator():

    def __init__(self, game, ground_object, faction = None): # faction is not mandatory because some subclasses do not use it
        self.game = game
        self.go = ground_object
        self.position = ground_object.position
        self.heading = random.randint(0, 359)
        self.faction = faction
        self.vg = unitgroup.VehicleGroup(self.game.next_group_id(), self.groupNamePrefix + self.go.group_identifier)
        wp = self.vg.add_waypoint(self.position, PointAction.OffRoad, 0)
        wp.ETA_locked = True

    @property
    def groupNamePrefix(self):
        return ""

    def generate(self):
        raise NotImplementedError

    def get_generated_group(self):
        return self.vg

    def add_unit(self, unit_type, name, pos_x, pos_y, heading):

        nn = "cgroup|" + str(self.go.cp_id) + '|' + str(self.go.group_id) + '|' + str(self.go.group_identifier) + "|" + name

        unit = Vehicle(self.game.next_unit_id(),
                       nn, unit_type.id)
        unit.position.x = pos_x
        unit.position.y = pos_y
        unit.heading = heading
        self.vg.add_unit(unit)
        return unit

    def get_circular_position(self, num_units, launcher_distance, coverage=90):
        """
        Given a position on the map, array a group of units in a circle a uniform distance from the unit
        :param num_units:
            number of units to play on the circle
        :param launcher_distance:
            distance the units should be from the center unit
        :param coverage:
            0-360
        :return:
            list of tuples representing each unit location
                [(pos_x, pos_y, heading), ...]
        """
        if coverage == 360:
            # one of the positions is shared :'(
            outer_offset = coverage / num_units
        else:
            outer_offset = coverage / (num_units - 1)

        positions = []

        if num_units % 2 == 0:
            current_offset = self.heading - ((coverage / (num_units - 1)) / 2)
        else:
            current_offset = self.heading
        current_offset -= outer_offset * (math.ceil(num_units / 2) - 1)
        for x in range(1, num_units + 1):
            positions.append((
                self.position.x + launcher_distance * math.cos(math.radians(current_offset)),
                self.position.y + launcher_distance * math.sin(math.radians(current_offset)),
                current_offset,
            ))
            current_offset += outer_offset
        return positions

