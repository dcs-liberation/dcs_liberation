import logging

from game import db
from game.settings import Settings
from gen.flights.ai_flight_planner import FlightPlanner
from gen.flights.flight import Flight, FlightType
from .conflictgen import *
from .naming import *
from .triggergen import TRIGGER_WAYPOINT_OFFSET

from dcs.mission import *
from dcs.unitgroup import *
from dcs.unittype import *
from dcs.task import *
from dcs.terrain.terrain import NoParkingSlotError, RunwayOccupiedError

SPREAD_DISTANCE_FACTOR = 1, 2
ESCORT_ENGAGEMENT_MAX_DIST = 100000
WORKAROUND_WAYP_DIST = 1000

WARM_START_HELI_AIRSPEED = 120
WARM_START_HELI_ALT = 500

WARM_START_ALTITUDE = 3000
WARM_START_AIRSPEED = 550

INTERCEPTION_AIRSPEED = 1000
BARCAP_RACETRACK_DISTANCE = 20000

ATTACK_CIRCLE_ALT = 1000
ATTACK_CIRCLE_DURATION = 15

CAS_ALTITUDE = 800
RTB_ALTITUDE = 800
RTB_DISTANCE = 5000
HELI_ALT = 500

TRANSPORT_LANDING_ALT = 2000

DEFENCE_ENGAGEMENT_MAX_DISTANCE = 60000
INTERCEPT_MAX_DISTANCE = 200000

GROUP_VERTICAL_OFFSET = 300


class AircraftConflictGenerator:
    escort_targets = [] # type: typing.List[typing.Tuple[FlyingGroup, int]]
    vertical_offset = None  # type: int

    def __init__(self, mission: Mission, conflict: Conflict, settings: Settings):
        self.m = mission
        self.settings = settings
        self.conflict = conflict
        self.vertical_offset = 0
        self.escort_targets = []

    def _start_type(self) -> StartType:
        return self.settings.cold_start and StartType.Cold or StartType.Warm

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

            if flying_type == F_14B:
                # workaround since 2 and 3 tomcat collide on carrier
                group_size = 2
            else:
                group_size = 4

            while count > 0:
                group_size = min(count, group_size)
                client_size = max(min(client_count, group_size), 0)

                yield (flying_type, group_size, client_size)
                count -= group_size
                client_count -= client_size

    def _setup_group(self, group: FlyingGroup, for_task: typing.Type[Task], client_count: int):
        did_load_loadout = False
        unit_type = group.units[0].unit_type

        if unit_type in db.PLANE_PAYLOAD_OVERRIDES:
            override_loadout = db.PLANE_PAYLOAD_OVERRIDES[unit_type]
            if type(override_loadout) == dict:
                if for_task in db.PLANE_PAYLOAD_OVERRIDES[unit_type]:
                    payload_name = db.PLANE_PAYLOAD_OVERRIDES[unit_type][for_task]
                    group.load_loadout(payload_name)
                    did_load_loadout = True
                    logging.info("Loaded overridden payload for {} - {} for task {}".format(unit_type, payload_name, for_task))
                elif "*" in db.PLANE_PAYLOAD_OVERRIDES[unit_type]:
                    payload_name = db.PLANE_PAYLOAD_OVERRIDES[unit_type]["*"]
                    group.load_loadout(payload_name)
                    did_load_loadout = True
                    logging.info("Loaded overridden payload for {} - {} for task {}".format(unit_type, payload_name, for_task))
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

            # Set up F-14 Client to have pre-stored alignement
            if unit_type is F_14B:
                group.units[idx].set_property(F_14B.Properties.INSAlignmentStored.id, True)

        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))

        if unit_type in helicopters.helicopter_map.values():
            group.set_frequency(127.5)
        else:
            if unit_type not in [P_51D_30_NA, P_51D, SpitfireLFMkIX, SpitfireLFMkIXCW, FW_190A8, FW_190D9, Bf_109K_4]:
                group.set_frequency(251.0)
            else:
                # WW2
                group.set_frequency(124.0)

    def _generate_at_airport(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, airport: Airport = None, start_type = None) -> FlyingGroup:
        assert count > 0
        assert unit is not None

        if start_type is None:
            start_type = self._start_type()

        logging.info("airgen: {} for {} at {}".format(unit_type, side.id, airport))
        return self.m.flight_group_from_airport(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=self.m.terrain.airport_by_id(airport.id),
            maintask=None,
            start_type=start_type,
            group_size=count,
            parking_slots=None)

    def _generate_inflight(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, at: Point) -> FlyingGroup:
        assert count > 0
        assert unit is not None

        self.vertical_offset += GROUP_VERTICAL_OFFSET
        if unit_type in helicopters.helicopter_map.values():
            alt = WARM_START_HELI_ALT + self.vertical_offset
            speed = WARM_START_HELI_AIRSPEED
        else:
            alt = WARM_START_ALTITUDE + self.vertical_offset
            speed = WARM_START_AIRSPEED

        pos = Point(at.x + random.randint(100, 1000), at.y + random.randint(100, 1000))

        logging.info("airgen: {} for {} at {} at {}".format(unit_type, side.id, alt, speed))
        group = self.m.flight_group(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=None,
            position=pos,
            altitude=alt,
            speed=speed,
            maintask=None,
            start_type=self._start_type(),
            group_size=count)

        group.points[0].alt_type = "RADIO"
        return group

    def _generate_at_group(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, at: typing.Union[ShipGroup, StaticGroup]) -> FlyingGroup:
        assert count > 0
        assert unit is not None

        logging.info("airgen: {} for {} at unit {}".format(unit_type, side.id, at))
        return self.m.flight_group_from_unit(
            country=side,
            name=name,
            aircraft_type=unit_type,
            pad_group=at,
            maintask=None,
            start_type=self._start_type(),
            group_size=count)

    def _generate_group(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, at: db.StartingPosition):
        if isinstance(at, Point):
            return self._generate_inflight(name, side, unit_type, count, client_count, at)
        elif isinstance(at, Group):
            takeoff_ban = unit_type in db.CARRIER_TAKEOFF_BAN
            ai_ban = client_count == 0 and self.settings.only_player_takeoff

            if not takeoff_ban and not ai_ban:
                return self._generate_at_group(name, side, unit_type, count, client_count, at)
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

    def _add_radio_waypoint(self, group: FlyingGroup, position, altitude: int, airspeed: int = 600):
        point = group.add_waypoint(position, altitude, airspeed)
        point.alt_type = "RADIO"
        return point

    def _rtb_for(self, group: FlyingGroup, cp: ControlPoint, at: db.StartingPosition = None):
        if not at:
            at = cp.at
        position = at if isinstance(at, Point) else at.position

        last_waypoint = group.points[-1]
        if last_waypoint is not None:
            heading = position.heading_between_point(last_waypoint.position)
            tod_location = position.point_from_heading(heading, RTB_DISTANCE)
            self._add_radio_waypoint(group, tod_location, last_waypoint.alt)

        destination_waypoint = self._add_radio_waypoint(group, position, RTB_ALTITUDE)
        if isinstance(at, Airport):
            group.land_at(at)
        return destination_waypoint

    def _at_position(self, at) -> Point:
        if isinstance(at, Point):
            return at
        elif isinstance(at, ShipGroup):
            return at.position
        elif issubclass(at, Airport):
            return at.position
        else:
            assert False

    def _generate_escort(self, side: Country, units: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition, cp, is_quick=False, should_orbit=False):
        groups = []
        for flying_type, count, client_count in self._split_to_groups(units, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(side, cp.id, flying_type),
                side=side,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at)

            group.task = Escort.name
            self._setup_group(group, CAP, client_count)

            for escorted_group, waypoint_index in self.escort_targets:
                waypoint_index += 1
                if not is_quick:
                    waypoint_index += TRIGGER_WAYPOINT_OFFSET

                group.points[0].tasks.append(EscortTaskAction(escorted_group.id, engagement_max_dist=ESCORT_ENGAGEMENT_MAX_DIST, lastwpt=waypoint_index))

            if should_orbit:
                orbit_task = ControlledTask(OrbitAction(ATTACK_CIRCLE_ALT, pattern=OrbitAction.OrbitPattern.Circle))
                orbit_task.stop_after_duration(ATTACK_CIRCLE_DURATION * 60)

                orbit_waypoint = self._add_radio_waypoint(group, self.conflict.position, CAS_ALTITUDE)
                orbit_waypoint.tasks.append(orbit_task)
                orbit_waypoint.tasks.append(EngageTargets(max_distance=DEFENCE_ENGAGEMENT_MAX_DISTANCE))

            groups.append(group)
        return groups


    def generate_flights(self, cp, country, flight_planner:FlightPlanner):

        for flight in flight_planner.cap_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_cap_flight(group, flight)

        for flight in flight_planner.cas_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_cas_flight(group, flight)

        for flight in flight_planner.sead_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_sead_flight(group, flight)

    def generate_planned_flight(self, cp, country, flight:Flight):
        try:
            group = self._generate_at_airport(
                name=namegen.next_unit_name(country, cp.id, flight.unit_type),
                side=country,
                unit_type=flight.unit_type,
                count=flight.count,
                client_count=0,
                airport=self.m.terrain.airport_by_id(cp.at.id),
                start_type=StartType.Runway)
        except Exception:
            group = self._generate_group(
                name=namegen.next_unit_name(country, cp.id, flight.unit_type),
                side=country,
                unit_type=flight.unit_type,
                count=flight.count,
                client_count=0,
                at=cp.position)
            group.points[0].alt = 1500
        group.points[0].ETA = flight.scheduled_in * 60
        return group

    def setup_group_as_cap_flight(self, group, flight):
        self._setup_group(group, CAP, flight.client_count)
        for point in flight.points:
            group.add_waypoint(Point(point[0],point[1]), point[2])

    def setup_group_as_cas_flight(self, group, flight):
        group.task = CAS.name
        self._setup_group(group, CAS, flight.client_count)

        group.points[0].tasks.clear()
        group.points[0].tasks.append(CASTaskAction())
        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
        group.points[0].tasks.append(OptROE(OptROE.Values.OpenFireWeaponFree))

        for location in flight.points:
            group.add_waypoint(Point(location[0], location[1]), location[2])

    def setup_group_as_sead_flight(self, group, flight):
        self._setup_group(group, SEAD, flight.client_count)

        group.points[0].tasks.clear()
        group.points[0].tasks.append(SEADTaskAction())
        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
        group.points[0].tasks.append(OptROE(OptROE.Values.WeaponFree))

        for point in flight.points:
            group.add_waypoint(Point(point[0], point[1]), point[2])

    def generate_cas_strikegroup(self, attackers: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None, escort=True):
        assert not escort or len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(attackers, clients):
            group = self._generate_group(
                    name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                    side=self.conflict.attackers_country,
                    unit_type=flying_type,
                    count=count,
                    client_count=client_count,
                    at=at and at or self._group_point(self.conflict.air_attackers_location))

            waypoint = self._add_radio_waypoint(group, self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            if self.conflict.is_vector:
                self._add_radio_waypoint(group, self.conflict.tail, CAS_ALTITUDE, WARM_START_AIRSPEED)

            group.task = CAS.name
            self._setup_group(group, CAS, client_count)
            if escort:
                self.escort_targets.append((group, group.points.index(waypoint)))
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_ground_attack_strikegroup(self, strikegroup: db.PlaneDict, clients: db.PlaneDict, targets: typing.List[typing.Tuple[str, Point]], at: db.StartingPosition = None, escort=True):
        assert not escort or len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(strikegroup, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                side=self.conflict.attackers_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            escort_until_waypoint = None

            for name, pos in targets:
                waypoint = group.add_waypoint(pos, 0, WARM_START_AIRSPEED, self.m.translation.create_string(name))
                waypoint.tasks.append(Bombing(pos, attack_qty=2))
                if escort_until_waypoint is None:
                    escort_until_waypoint = waypoint

            group.task = GroundAttack.name
            self._setup_group(group, GroundAttack, client_count)
            if escort:
                self.escort_targets.append((group, group.points.index(escort_until_waypoint)))
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_sead_strikegroup(self, strikegroup: db.PlaneDict, clients: db.PlaneDict, targets: typing.List[typing.Tuple[str, Point]], at: db.StartingPosition, escort=True):
        assert not escort or len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(strikegroup, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                side=self.conflict.attackers_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            escort_until_waypoint = None

            for name, pos in targets:
                waypoint = group.add_waypoint(pos, 0, WARM_START_AIRSPEED, self.m.translation.create_string(name))
                if escort_until_waypoint is None:
                    escort_until_waypoint = waypoint

            group.task = SEAD.name
            self._setup_group(group, SEAD, client_count)
            if escort:
                self.escort_targets.append((group, group.points.index(escort_until_waypoint)))

            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_defenders_cas(self, defenders: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None, escort=True):
        assert not escort or len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(defenders, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.defenders_country, self.conflict.to_cp.id, flying_type),
                side=self.conflict.defenders_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_defenders_location))

            location = self._group_point(self.conflict.air_defenders_location)
            insertion_point = self.conflict.find_insertion_point(location)
            waypoint = self._add_radio_waypoint(group, insertion_point, CAS_ALTITUDE, WARM_START_AIRSPEED)

            if self.conflict.is_vector:
                destination_tail = self.conflict.tail.distance_to_point(insertion_point) > self.conflict.position.distance_to_point(insertion_point)
                self._add_radio_waypoint(group, destination_tail and self.conflict.tail or self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)

            group.task = CAS.name
            self._setup_group(group, CAS, client_count)
            if escort:
                self.escort_targets.append((group, group.points.index(waypoint)))
            self._rtb_for(group, self.conflict.to_cp, at)

    def generate_ship_strikegroup(self, attackers: db.PlaneDict, clients: db.PlaneDict, target_groups: typing.Collection[ShipGroup], at: db.StartingPosition = None, escort=True):
        assert not escort or len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(attackers, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                side=self.conflict.attackers_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            wayp = self._add_radio_waypoint(group, self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            for target_group in target_groups:
                wayp.tasks.append(AttackGroup(target_group.id))

            group.task = AntishipStrike.name
            self._setup_group(group, AntishipStrike, client_count)
            if escort:
                self.escort_targets.append((group, group.points.index(wayp)))
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_attackers_escort(self, attackers: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for g in self._generate_escort(
                side=self.conflict.attackers_country,
                units=attackers,
                clients=clients,
                at=at and at or self._group_point(self.conflict.air_attackers_location),
                is_quick=at is None,
                cp=self.conflict.from_cp,
                should_orbit=True):
            self._rtb_for(g, self.conflict.from_cp, at)

    def generate_defenders_escort(self, escort: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for g in self._generate_escort(
                side=self.conflict.defenders_country,
                units=escort,
                clients=clients,
                at=at and at or self._group_point(self.conflict.air_defenders_location),
                is_quick=at is None,
                cp=self.conflict.to_cp,
                should_orbit=False):
            self._rtb_for(g, self.conflict.to_cp, at)

    def generate_defense(self, defenders: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(defenders, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.to_cp.id, flying_type),
                side=self.conflict.defenders_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_defenders_location))

            group.task = CAP.name
            wayp = self._add_radio_waypoint(group, self.conflict.position, CAS_ALTITUDE, WARM_START_AIRSPEED)
            wayp.tasks.append(dcs.task.EngageTargets(max_distance=DEFENCE_ENGAGEMENT_MAX_DISTANCE))
            wayp.tasks.append(dcs.task.OrbitAction(ATTACK_CIRCLE_ALT, pattern=OrbitAction.OrbitPattern.Circle))
            self._setup_group(group, CAP, client_count)
            self._rtb_for(group, self.conflict.to_cp, at)

    def generate_migcap(self, patrol: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(patrol, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                side=self.conflict.attackers_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            waypoint = self._add_radio_waypoint(group, self.conflict.position, WARM_START_ALTITUDE, WARM_START_AIRSPEED)
            if self.conflict.is_vector:
                self._add_radio_waypoint(group, self.conflict.tail, WARM_START_ALTITUDE, WARM_START_AIRSPEED)

            group.task = CAP.name
            self._setup_group(group, CAP, client_count)
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_barcap(self, patrol: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(patrol, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                side=self.conflict.defenders_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_defenders_location))

            waypoint = self._add_radio_waypoint(group, self.conflict.position, WARM_START_ALTITUDE, WARM_START_AIRSPEED)
            if self.conflict.is_vector:
                self._add_radio_waypoint(group, self.conflict.tail, WARM_START_ALTITUDE, WARM_START_AIRSPEED)
            else:
                heading = group.position.heading_between_point(self.conflict.position)
                waypoint = self._add_radio_waypoint(group, self.conflict.position.point_from_heading(heading, BARCAP_RACETRACK_DISTANCE),
                                                    WARM_START_ALTITUDE,
                                                    WARM_START_AIRSPEED)
                waypoint.tasks.append(OrbitAction(WARM_START_ALTITUDE, WARM_START_AIRSPEED))

            group.task = CAP.name
            self._setup_group(group, CAP, client_count)
            self._rtb_for(group, self.conflict.to_cp, at)

    def generate_transport(self, transport: db.PlaneDict, destination: Airport, escort=True):
        assert not escort or len(self.escort_targets) == 0

        for flying_type, count, client_count in self._split_to_groups(transport):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                side=self.conflict.defenders_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=self._group_point(self.conflict.air_defenders_location))

            waypoint = self._rtb_for(group, self.conflict.to_cp)
            if escort:
                self.escort_targets.append((group, group.points.index(waypoint)))

            self._add_radio_waypoint(group, destination.position, RTB_ALTITUDE)
            group.task = Transport.name
            group.land_at(destination)

    def generate_interception(self, interceptors: db.PlaneDict, clients: db.PlaneDict, at: db.StartingPosition = None):
        for flying_type, count, client_count in self._split_to_groups(interceptors, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, flying_type),
                side=self.conflict.attackers_country,
                unit_type=flying_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location))

            group.task = CAP.name
            group.points[0].tasks.append(EngageTargets(max_distance=INTERCEPT_MAX_DISTANCE))

            wayp = self._add_radio_waypoint(group, self.conflict.position, WARM_START_ALTITUDE, INTERCEPTION_AIRSPEED)
            wayp.tasks.append(EngageTargets(max_distance=INTERCEPT_MAX_DISTANCE))
            
            if self.conflict.is_vector:
                self._add_radio_waypoint(group, self.conflict.tail, CAS_ALTITUDE, WARM_START_ALTITUDE)

            self._setup_group(group, CAP, client_count)
            self._rtb_for(group, self.conflict.from_cp, at)

    def generate_passenger_transport(self, helis: db.HeliDict, clients: db.HeliDict, at: db.StartingPosition):
        for heli_type, count, client_count in self._split_to_groups(helis, clients):
            group = self._generate_group(
                name=namegen.next_unit_name(self.conflict.attackers_country, self.conflict.from_cp.id, heli_type),
                side=self.conflict.attackers_country,
                unit_type=heli_type,
                count=count,
                client_count=client_count,
                at=at and at or self._group_point(self.conflict.air_attackers_location)
            )

            self._add_radio_waypoint(group, self.conflict.position, HELI_ALT)
            self._setup_group(group, Transport, client_count)


