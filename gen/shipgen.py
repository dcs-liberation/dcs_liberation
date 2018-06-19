from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.unitgroup import *
from dcs.task import *

SHIP_RANDOM_SPREAD = 300


class ShipGenerator:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def generate_carrier(self, type: ShipType, country: str, at: Point) -> ShipGroup:
        return self.m.ship_group(
            country=self.m.country(country),
            name=namegen.next_transport_group_name(),
            _type=type,
            position=at)

    def generate_cargo(self, units: db.ShipDict) -> typing.Collection[ShipGroup]:
        groups = []
        for unit_type, unit_count in units.items():
            group = self.m.ship_group(
                country=self.conflict.defenders_side,
                name=namegen.next_transport_group_name(),
                _type=unit_type,
                position=self.conflict.ground_defenders_location.random_point_within(SHIP_RANDOM_SPREAD, SHIP_RANDOM_SPREAD),
                group_size=unit_count,
            )

            group.add_waypoint(self.conflict.to_cp.position)
            groups.append(group)

        return groups
