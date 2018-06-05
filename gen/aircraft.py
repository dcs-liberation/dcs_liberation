import typing
import pdb
import dcs

from random import randint

import globals

from shop import db
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
WORKAROUND_WAYP_DIST = 1000

WARM_START_ALTITUDE = 6000
WARM_START_AIRSPEED = 300

INTERCEPT_ALT = 15000
CAS_ALTITUDE = 3000

INTERCEPT_MAX_DISTANCE_FACTOR = 15

class AircraftConflictGenerator:
    escort_targets = [] # type: typing.List[PlaneGroup]

    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict
        self.escort_targets = []

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
            unit: PlaneType,
            count: int,
            client_count: int,
            at: Point = None,
            airport: Airport = None) -> FlyingGroup:
        starttype = airport is None and StartType.Warm or StartType.Cold
        assert count > 0

        group = self.m.flight_group(
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

        for idx in range(client_count):
            group.units[idx].set_client()

        return group

    def _generate_escort(self, units: db.PlaneDict, clients: db.PlaneDict, airport: Airport, side: Country, location: Point):
        if len(self.escort_targets) == 0:
            return

        for type, count in units.items():
            group = self._generate_group(
                name=namegen.next_escort_group_name(),
                side=side,
                unit=type,
                count=count,
                client_count=clients.get(type, 0),
                at=location,
                airport=airport)

            group.task = Escort.name
            group.load_task_default_loadout(dcs.task.Escort)

            heading = group.position.heading_between_point(self.conflict.position)
            position = group.position  # type: Point
            wayp = group.add_waypoint(position.point_from_heading(heading, WORKAROUND_WAYP_DIST), CAS_ALTITUDE)

            for group in self.escort_targets:
                wayp.tasks.append(EscortTaskAction(group.id, engagement_max_dist=ESCORT_MAX_DIST))

    def generate_cas(self, attackers: db.PlaneDict, clients: db.PlaneDict, airport: Airport = None):
        assert len(self.escort_targets) == 0

        for type, count in attackers.items():
            group = self._generate_group(
                    name=namegen.next_cas_group_name(),
                    side=self.conflict.attackers_side,
                    unit=type,
                    count=count,
                    client_count=clients.get(type, 0),
                    at=airport is None and self._group_point(self.conflict.air_attackers_location) or None,
                    airport=airport)
            self.escort_targets.append(group)

            group.add_waypoint(self.conflict.position, CAS_ALTITUDE)
            group.task = CAS.name
            group.load_task_default_loadout(CAS)

    def generate_cas_escort(self, attackers: db.PlaneDict, clients: db.PlaneDict, airport: Airport = None):
        self._generate_escort(
            units=attackers,
            clients=clients,
            airport=airport,
            side=self.conflict.attackers_side,
            location=airport is None and self._group_point(self.conflict.air_attackers_location) or None
        )

    def generate_transport_escort(self, escort: db.PlaneDict, clients: db.PlaneDict, airport: Airport = None):
        self._generate_escort(
            units=escort,
            clients=clients,
            airport=airport,
            side=self.conflict.defenders_side,
            location=airport is None and self._group_point(self.conflict.air_defenders_location) or None
        )

    def generate_defense(self, defenders: db.PlaneDict, clients: db.PlaneDict, airport: Airport = None):
        for type, count in defenders.items():
            group = self._generate_group(
                    name=namegen.next_intercept_group_name(),
                    side=self.conflict.defenders_side,
                    unit=type,
                    count=count,
                    client_count=clients.get(type, 0),
                    at=airport is None and self._group_point(self.conflict.air_defenders_location) or None,
                    airport=airport)

            group.task = FighterSweep.name
            group.load_task_default_loadout(FighterSweep)
            wayp = group.add_waypoint(self.conflict.position, CAS_ALTITUDE)
            wayp.tasks.append(dcs.task.EngageTargets(max_distance=self.conflict.size * INTERCEPT_MAX_DISTANCE_FACTOR))
            wayp.tasks.append(dcs.task.OrbitAction())

    def generate_transport(self, transport: db.PlaneDict, destination: Airport):
        assert len(self.escort_targets) == 0

        for type, count in transport.items():
            group = self._generate_group(
                name=namegen.next_transport_group_name(),
                side=self.conflict.defenders_side,
                unit=type,
                count=count,
                client_count=0,
                at=self._group_point(self.conflict.air_defenders_location),
                airport=None
            )

            group.task = Transport.name

            self.escort_targets.append(group)
            group.land_at(destination)

    def generate_interception(self, interceptors: db.PlaneDict, clients: db.PlaneDict, airport: Airport = None):
        for type, count in interceptors.items():
            group = self._generate_group(
                name=namegen.next_intercept_group_name(),
                side=self.conflict.attackers_side,
                unit=type,
                count=count,
                client_count=clients.get(type, 0),
                at=airport is None and self._group_point(self.conflict.air_attackers_location) or None,
                airport=airport
            )

            group.task = FighterSweep.name
            group.load_task_default_loadout(FighterSweep)

            heading = group.position.heading_between_point(self.conflict.position)
            initial_wayp = group.add_waypoint(group.position.point_from_heading(heading, WORKAROUND_WAYP_DIST), INTERCEPT_ALT)
            initial_wayp.tasks.append(EngageTargets())

            wayp = group.add_waypoint(self.conflict.position, 0)
            wayp.tasks.append(EngageTargets())
