from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.unitgroup import *
from dcs.task import *


class ShipGenerator:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def generate(self, type: ShipType, country: str, at: Point) -> ShipGroup:
        return self.m.ship_group(
            country=self.m.country(country),
            name=namegen.next_transport_group_name(),
            _type=type,
            position=at)
