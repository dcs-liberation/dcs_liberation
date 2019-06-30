import logging

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

    def generate_carrier(self, for_units: typing.Collection[UnitType], country: str, at: Point) -> ShipGroup:
        type = db.find_unittype(Carriage, country)[0]
        for unit_type in for_units:
            if unit_type in db.CARRIER_TYPE_BY_PLANE:
                type = db.CARRIER_TYPE_BY_PLANE[unit_type]
                break

        group = self.m.ship_group(
            country=self.m.country(country),
            name=namegen.next_carrier_name(self.m.country(country)),
            _type=type,
            position=at)

        group.points[0].tasks.append(ActivateBeaconCommand(unit_id=group.id, channel=20, callsign="SHDW", aa=False))
        group.points[0].tasks.append(ActivateICLSCommand(unit_id=group.id, channel=1))
        return group

    def generate_cargo(self, units: db.ShipDict) -> typing.Collection[ShipGroup]:
        groups = []
        offset = 0
        for unit_type, unit_count in units.items():
            for _ in range(unit_count):
                offset += 1
                logging.info("shipgen: {} ({}) for {}".format(unit_type, unit_count, self.conflict.defenders_side))
                group = self.m.ship_group(
                    country=self.conflict.defenders_country,
                    name=namegen.next_unit_name(self.conflict.defenders_country, unit_type),
                    _type=unit_type,
                    position=self.conflict.ground_defenders_location.random_point_within(SHIP_RANDOM_SPREAD, SHIP_RANDOM_SPREAD).point_from_heading(0, offset * SHIP_RANDOM_SPREAD)
                )

                group.add_waypoint(self.conflict.to_cp.position)
                groups.append(group)

        return groups
