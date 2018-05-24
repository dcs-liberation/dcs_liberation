import typing
import pdb
import dcs

from random import randint

import globals

from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.vehicles import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.mapping import *
from dcs.point import *
from dcs.task import *

SPREAD_DISTANCE_FACTOR = 1, 2
ESCORT_MAX_DIST = 30000

WARM_START_ALTITUDE = 6000
WARM_START_AIRSPEED = 300
CAS_ALTITUDE = 3000

INTERCEPT_MAX_DISTANCE_FACTOR = 15

class AircraftConflictGenerator:
    escort_targets = [] # type: typing.List[PlaneGroup]

    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def _group_point(self, point) -> Point:
        distance = randint(
                int(self.conflict.size * SPREAD_DISTANCE_FACTOR[0]),
                int(self.conflict.size * SPREAD_DISTANCE_FACTOR[1]),
                )
        return point.random_point_within(distance, self.conflict.size * SPREAD_DISTANCE_FACTOR[0])

    def _generate_group(
            self,
            name: str,
            side: Country,
            unit: UnitType,
            count: int,
            at: Point = None,
            airport: Airport = None) -> PlaneGroup:
        starttype = airport == None and StartType.Warm or StartType.Cold
        return self.m.flight_group(
                country=side,
                name=name,
                aircraft_type=unit,
                airport=airport,
                position=at,
                altitude=WARM_START_ALTITUDE,
                speed=WARM_START_AIRSPEED,
                maintask=None,
                start_type=starttype,
                group_size=count)

    def generate_cas(self, attackers: typing.Dict[PlaneType, int], airport: Airport = None):
        for type, count in attackers.items():
            group = self._generate_group(
                    name=namegen.next_cas_group_name(),
                    side=self.conflict.attackers_side,
                    unit=type,
                    count=count,
                    at=airport == None and self._group_point(self.conflict.air_attackers_location) or None,
                    airport=airport)
            self.escort_targets.append(group)

            group.add_waypoint(self.conflict.point, CAS_ALTITUDE)
            group.task = CAS.name

    def generate_escort(self, attackers: typing.Dict[PlaneType, int], airport: Airport = None):
        for type, count in attackers.items():
            group = self._generate_group(
                    name=namegen.next_escort_group_name(),
                    side=self.conflict.attackers_side,
                    unit=type,
                    count=count,
                    at=airport == None and self._group_point(self.conflict.air_attackers_location) or None,
                    airport=airport)

            group.task = Escort.name
            group.load_task_default_loadout(dcs.task.Escort.name)

            heading = group.position.heading_between_point(self.conflict.point)
            position = group.position # type: Point
            wayp = group.add_waypoint(position.point_from_heading(heading, 3000), CAS_ALTITUDE)

            for group in self.escort_targets:
                wayp.tasks.append(EscortTaskAction(group.id, engagement_max_dist=ESCORT_MAX_DIST))

    def generate_interceptors(self, defenders: typing.Dict[PlaneType, int], airport: Airport = None):
        for type, count in defenders.items():
            group = self._generate_group(
                    name=namegen.next_intercept_group_name(),
                    side=self.conflict.defenders_side,
                    unit=type,
                    count=count,
                    at=airport == None and self._group_point(self.conflict.air_defenders_location) or None,
                    airport=airport)

            group.task = FighterSweep.name
            group.load_task_default_loadout(dcs.task.FighterSweep())
            wayp = group.add_waypoint(self.conflict.point, CAS_ALTITUDE)
            wayp.tasks.append(dcs.task.EngageTargets(max_distance=self.conflict.size * INTERCEPT_MAX_DISTANCE_FACTOR))
            wayp.tasks.append(dcs.task.OrbitAction())
