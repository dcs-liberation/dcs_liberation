from game import db
from game.settings import Settings
from .conflictgen import *
from .naming import *
from .triggergen import TRIGGER_WAYPOINT_OFFSET

from dcs.mission import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.task import *
from dcs.terrain.terrain import NoParkingSlotError

SPREAD_DISTANCE_FACTOR = 1, 2
ESCORT_ENGAGEMENT_MAX_DIST = 100000
WORKAROUND_WAYP_DIST = 1000

WARM_START_HELI_AIRSPEED = 200
WARM_START_HELI_ALT = 1000

WARM_START_ALTITUDE = 3000
WARM_START_AIRSPEED = 550

INTERCEPTION_ALT = 3000
INTERCEPTION_AIRSPEED = 1000

ATTACK_CIRCLE_ALT = 5000
ATTACK_CIRCLE_DURATION = 15

CAS_ALTITUDE = 1000
RTB_ALTITUDE = 1000
HELI_ALT = 900

TRANSPORT_LANDING_ALT = 1000

DEFENCE_ENGAGEMENT_MAX_DISTANCE = 60000
INTERCEPT_MAX_DISTANCE = 200000


class AircraftConflictGenerator:
    escort_targets = [] # type: typing.List[typing.Tuple[PlaneGroup, int]]

    def __init__(self, mission: Mission, conflict: Conflict, settings: Settings):
        self.m = mission
        self.settings = settings
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

    def _setup_group(self, group: FlyingGroup, for_task: Task, client_count: int):
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

        single_client = client_count == 1
        for idx in range(0, min(len(group.units), client_count)):
            if single_client:
                group.units[idx].set_player()
            else:
                group.units[idx].set_client()

        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))

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

        if unit_type in helicopters.helicopter_map:
            alt = WARM_START_HELI_ALT + random.randint(50, 200)
            speed = WARM_START_HELI_AIRSPEED
        else:
            alt = WARM_START_ALTITUDE + random.randint(50, 200)
            speed = WARM_START_AIRSPEED

        pos = Point(at.x + random.randint(100, 200), at.y + random.randint(100, 200))

        return self.m.flight_group(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=None,
            position=pos,
            altitude=alt,
            speed=speed,
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
            takeoff_ban = unit_type in db.CARRIER_TAKEOFF_BAN
            if not takeoff_ban:
                return self._generate_at_carrier(name, side, unit_type, count, client_count, at)
            else:
                return self._generate_inflight(name, side, unit_type, count, client_count, at.position)
        elif issubclass(at, Airport):
            takeoff_ban = unit_type in db.TAKEOFF_BAN
            ai_ban = client_count == 0 and self.settings.only_player_takeoff

            if not takeoff_ban and not ai_ban:
                try:
                    return self._generate_at_airport(name, side, unit_type, count, client_count, at)
                except NoParkingSlotError:
                    pass
            return self._generate_inflight(name, side, unit_type, count, client_count, at.position)
        else:
            assert False

    def _rtb_for(self, group: FlyingGroup, cp: ControlPoint, at: db.StartingPosition = None):
        group.add_waypoint(cp.position, RTB_ALTITUDE)

        if isinstance(cp.at, Point):
            pass
        elif isinstance(cp.at, ShipGroup):
            pass
        elif issubclass(cp.at, Airport):
            group.land_at(cp.at)

    def _at_position(self, at) -> Point:
        if isinstance(at, Point):
            return at
        elif isinstance(at, ShipGroup):
            return at.position
        elif issubclass(at, Airport):
            return at.position
        else:
            assert False

    def _generate_escort(self, side: Country, units: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition, is_quick=False, should_orbit=False):
        groups = []
        for flying_type, count, client_count in self._split_to_groups(units, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(side, flying_type),
                side=side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at)

            group.task = Escort.name

            heading = group.position.heading_between_point(self.conflict.position)
            position = group.position  # type: Point
            wayp = group.add_waypoint(position.point_from_heading(heading, WORKAROUND_WAYP_DIST), CAS_ALTITUDE, WARM_START_AIRSPEED)
            self._setup_group(group, CAP, client_count)

            for escorted_group, waypoint_index in self.escort_targets:
                waypoint_index += 1
                if not is_quick:
                    waypoint_index += TRIGGER_WAYPOINT_OFFSET

                wayp.tasks.append(EscortTaskAction(escorted_group.id, engagement_max_dist=ESCORT_ENGAGEMENT_MAX_DIST, lastwpt=waypoint_index))

            if should_orbit:
                orbit_task = ControlledTask(OrbitAction(ATTACK_CIRCLE_ALT, pattern=OrbitAction.OrbitPattern.Circle))
                orbit_task.stop_after_duration(ATTACK_CIRCLE_DURATION * 60)

                orbit_waypoint = group.add_waypoint(self.conflict.position, CAS_ALTITUDE)
                orbit_waypoint.tasks.append(orbit_task)
                orbit_waypoint.tasks.append(EngageTargets(max_distance=DEFENCE_ENGAGEMENT_MAX_DISTANCE))

            groups.append(group)
        return groups

    def generate_cas_strikegroup(self, attackers: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        assert len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(attackers, clients):
            group = self._generate_group(
                    name=namegen.next_unit_name(self.conflict.attackers_side, flying_type),
                    side=self.conflict.attackers_side,
                    unit_type=flying_type,
                    count=count,
                    client_count=client_count,
                    at=at and at or self._group_point(self.conflict.air_attackers_location))

            waypoint = group.add_waypoint(self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            group.task = CAS.name
            self._setup_group(group, CAS, client_count)
            self.escort_targets.append((group, group.points.index(waypoint)))
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_ship_strikegroup(self, attackers: db.PlaneDict, clients: db.PlaneDict, target_groups: typing.Collection[ShipGroup], at: db.StartingPosition = None):
        assert len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(attackers, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_side, flying_type),
                side=self.conflict.attackers_side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            wayp = group.add_waypoint(self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            for target_group in target_groups:
                wayp.tasks.append(AttackGroup(target_group.id))

            group.task = AntishipStrike.name
            self._setup_group(group, AntishipStrike, client_count)
            self.escort_targets.append((group, group.points.index(wayp)))
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_strikegroup_escort(self, attackers: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for g in self._generate_escort(
                side=self.conflict.attackers_side,
                units=attackers,
                clients=clients,
                at=at and at or self._group_point(self.conflict.air_attackers_location),
                is_quick=at is None,
                should_orbit=True):
            self._rtb_for(g, self.conflict.from_cp, at)

    def generate_transport_escort(self, escort: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for g in self._generate_escort(
                side=self.conflict.defenders_side,
                units=escort,
                clients=clients,
                at=at and at or self._group_point(self.conflict.air_defenders_location),
                is_quick=at is None,
                should_orbit=False):
            self._rtb_for(g, self.conflict.to_cp, at)

    def generate_defense(self, defenders: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(defenders, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.defenders_side, flying_type),
                side=self.conflict.defenders_side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_defenders_location))

            group.task = CAP.name
            wayp = group.add_waypoint(self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            wayp.tasks.append(dcs.task.EngageTargets(max_distance=DEFENCE_ENGAGEMENT_MAX_DISTANCE))
            wayp.tasks.append(dcs.task.OrbitAction(ATTACK_CIRCLE_ALT, pattern=OrbitAction.OrbitPattern.Circle))
            self._setup_group(group, CAP, client_count)
            self._rtb_for(group, self.conflict.to_cp, at)

    def generate_transport(self, transport: db.PlaneDict, destination: Airport):
        assert len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(transport):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.defenders_side, flying_type),
                side=self.conflict.defenders_side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=self._group_point(self.conflict.air_defenders_location))

            waypoint = group.add_waypoint(destination.position.random_point_within(0, 0), TRANSPORT_LANDING_ALT)
            self.escort_targets.append((group, group.points.index(waypoint)))

            group.task = Transport.name
            group.land_at(destination)

    def generate_interception(self, interceptors: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(interceptors, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_side, flying_type),
                side=self.conflict.attackers_side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            group.task = CAP.name

            heading = group.position.heading_between_point(self.conflict.position)
            initial_wayp = group.add_waypoint(group.position.point_from_heading(heading, WORKAROUND_WAYP_DIST), INTERCEPTION_ALT, INTERCEPTION_AIRSPEED)
            initial_wayp.tasks.append(EngageTargets(max_distance=INTERCEPT_MAX_DISTANCE))

            wayp = group.add_waypoint(self.conflict.position, WARM_START_ALTITUDE, INTERCEPTION_AIRSPEED)
            wayp.tasks.append(EngageTargets(max_distance=INTERCEPT_MAX_DISTANCE))
            self._setup_group(group, CAP, client_count)
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_passenger_transport(self, helis: db.HeliDict, clients: db.HeliDict, at: db.StartingPosition):
        for heli_type, count, client_count in self._split_to_groups(helis, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_side, heli_type),
                side=self.conflict.attackers_side,
                unit_type=heli_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location)
            )

            group.add_waypoint(
                pos=self.conflict.position,
                altitude=HELI_ALT,
            )

            self._setup_group(group, Transport, client_count)
