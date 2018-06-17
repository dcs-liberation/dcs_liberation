from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.task import *
from dcs.terrain.terrain import NoParkingSlotError

SPREAD_DISTANCE_FACTOR = 1, 2
ESCORT_MAX_DIST = 30000
WORKAROUND_WAYP_DIST = 1000

WARM_START_ALTITUDE = 3600
WARM_START_AIRSPEED = 600
INTERCEPTION_AIRSPEED = 1200

TRANSPORT_LANDING_ALT = 500

INTERCEPTION_ALT = 3600
CAS_ALTITUDE = 1000
RTB_ALTITUDE = 1000

INTERCEPT_MAX_DISTANCE = 80000

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

    def _split_to_groups(self, dict: db.PlaneDict, clients: db.PlaneDict = None) -> typing.Collection[typing.Tuple[FlyingType, int, int]]:
        for flying_type, count in dict.items():
            if clients:
                client_count = clients.get(flying_type, 0)
            else:
                client_count = 0

            while count > 0:
                group_size = min(count, 4)
                client_size = max(min(client_count, 4), 0)

                yield (flying_type, group_size, client_size)
                count -= group_size
                client_count -= client_size

    def _setup_group(self, group: FlyingGroup, for_task: Task, clients: db.PlaneDict):
        did_load_loadout = False
        unit_type = group.units[0].unit_type
        if unit_type in db.PLANE_PAYLOAD_OVERRIDES:
            override_loadout = db.PLANE_PAYLOAD_OVERRIDES[unit_type]
            if type(override_loadout) == dict:
                if for_task in db.PLANE_PAYLOAD_OVERRIDES[unit_type]:
                    group.load_loadout(db.PLANE_PAYLOAD_OVERRIDES[unit_type][for_task])
                    did_load_loadout = True
                elif "*" in db.PLANE_PAYLOAD_OVERRIDES[unit_type]:
                    group.load_loadout(db.PLANE_PAYLOAD_OVERRIDES[unit_type]["*"])
                    did_load_loadout = True
            elif issubclass(override_loadout, MainTask):
                group.load_task_default_loadout(override_loadout)
                did_load_loadout = True

        if not did_load_loadout:
            group.load_task_default_loadout(for_task)

        if unit_type in db.PLANE_LIVERY_OVERRIDES:
            for unit_instance in group.units:
                unit_instance.livery_id = db.PLANE_LIVERY_OVERRIDES[unit_type]

        single_client = sum(clients.values()) == 1
        client_count = clients.get(unit_type, 0)
        for idx in range(min(client_count, len(group.units))):
            if single_client:
                group.units[idx].set_player()
            else:
                group.units[idx].set_client()

    def _generate_at_airport(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, airport: Airport = None) -> FlyingGroup:
        assert count > 0
        assert unit is not None

        return self.m.flight_group_from_airport(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=self.m.terrain.airport_by_id(airport.id),
            maintask=None,
            start_type=StartType.Warm,
            group_size=count,
            parking_slots=None)

    def _generate_inflight(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, at: Point) -> FlyingGroup:
        assert count > 0
        assert unit is not None

        return self.m.flight_group(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=None,
            position=at,
            altitude=WARM_START_ALTITUDE,
            speed=WARM_START_AIRSPEED,
            maintask=None,
            start_type=StartType.Warm,
            group_size=count)

    def _generate_at_carrier(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, at: ShipGroup) -> FlyingGroup:
        assert count > 0
        assert unit is not None

        return self.m.flight_group_from_unit(
            country=side,
            name=name,
            aircraft_type=unit_type,
            pad_group=at,
            maintask=None,
            start_type=StartType.Warm,
            group_size=count)

    def _generate_group(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, at: db.StartingPosition):
        if isinstance(at, Point):
            return self._generate_inflight(name, side, unit_type, count, client_count, at)
        elif isinstance(at, ShipGroup):
            return self._generate_at_carrier(name, side, unit_type, count, client_count, at)
        elif issubclass(at, Airport):
            try:
                return self._generate_at_airport(name, side, unit_type, count, client_count, at)
            except NoParkingSlotError:
                return self._generate_inflight(name, side, unit_type, count, client_count, at.position)
        else:
            assert False

    def _at_position(self, at) -> Point:
        if isinstance(at, Point):
            return at
        elif isinstance(at, ShipGroup):
            return at.position
        elif issubclass(at, Airport):
            return at.position
        else:
            assert False

    def _generate_escort(self, side: Country, units: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition):
        groups = []
        for flying_type, count, client_count in self._split_to_groups(units, clients):
            group = self._generate_group(
                name=namegen.next_escort_group_name(),
                side=side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at)

            group.task = Escort.name

            heading = group.position.heading_between_point(self.conflict.position)
            position = group.position  # type: Point
            wayp = group.add_waypoint(position.point_from_heading(heading, WORKAROUND_WAYP_DIST), CAS_ALTITUDE, WARM_START_AIRSPEED)

            self._setup_group(group, CAP, clients)

            for group in self.escort_targets:
                wayp.tasks.append(EscortTaskAction(group.id, engagement_max_dist=ESCORT_MAX_DIST))

            groups.append(group)
        return groups

    def generate_cas(self, attackers: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        assert len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(attackers, clients):
            group = self._generate_group(
                    name=namegen.next_cas_group_name(),
                    side=self.conflict.attackers_side,
                    unit_type=flying_type,
                    count=count,
                    client_count=client_count,
                    at=at and at or self._group_point(self.conflict.air_attackers_location))
            self.escort_targets.append(group)

            group.add_waypoint(self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            group.task = CAS.name
            self._setup_group(group, CAS, clients)

            group.add_waypoint(self.conflict.from_cp.position, RTB_ALTITUDE)

    def generate_cas_escort(self, attackers: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for g in self._generate_escort(
                side=self.conflict.attackers_side,
                units=attackers,
                clients=clients,
                at=at and at or self._group_point(self.conflict.air_attackers_location)):
            g.add_waypoint(self.conflict.from_cp.position, RTB_ALTITUDE)

    def generate_transport_escort(self, escort: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for g in self._generate_escort(
                side=self.conflict.defenders_side,
                units=escort,
                clients=clients,
                at=at and at or self._group_point(self.conflict.air_defenders_location)):
            g.add_waypoint(self.conflict.to_cp.position, RTB_ALTITUDE)

    def generate_defense(self, defenders: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(defenders, clients):
            group = self._generate_group(
                name=namegen.next_intercept_group_name(),
                side=self.conflict.defenders_side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_defenders_location))

            group.task = CAP.name
            wayp = group.add_waypoint(self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            wayp.tasks.append(dcs.task.EngageTargets(max_distance=INTERCEPT_MAX_DISTANCE))
            wayp.tasks.append(dcs.task.OrbitAction())
            self._setup_group(group, CAP, clients)

            group.add_waypoint(self.conflict.to_cp.position, RTB_ALTITUDE)

    def generate_transport(self, transport: db.PlaneDict, destination: Airport):
        assert len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(transport):
            group = self._generate_group(
                name=namegen.next_transport_group_name(),
                side=self.conflict.defenders_side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=self._group_point(self.conflict.air_defenders_location))

            group.task = Transport.name

            self.escort_targets.append(group)
            group.add_waypoint(destination.position.random_point_within(0, 0), TRANSPORT_LANDING_ALT)
            group.land_at(destination)

    def generate_interception(self, interceptors: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(interceptors, clients):
            group = self._generate_group(
                name=namegen.next_intercept_group_name(),
                side=self.conflict.attackers_side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            group.task = CAP.name

            heading = group.position.heading_between_point(self.conflict.position)
            initial_wayp = group.add_waypoint(group.position.point_from_heading(heading, WORKAROUND_WAYP_DIST), INTERCEPTION_ALT, INTERCEPTION_AIRSPEED)
            initial_wayp.tasks.append(EngageTargets(max_distance=INTERCEPT_MAX_DISTANCE))

            wayp = group.add_waypoint(self.conflict.position, 0)
            wayp.tasks.append(EngageTargets(max_distance=INTERCEPT_MAX_DISTANCE))
            self._setup_group(group, CAP, clients)

            group.add_waypoint(self.conflict.from_cp.position, RTB_ALTITUDE)
