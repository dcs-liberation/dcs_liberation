import logging

from dcs.helicopters import UH_1H

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


class AircraftConflictGenerator:
    escort_targets = [] # type: typing.List[typing.Tuple[FlyingGroup, int]]

    def __init__(self, mission: Mission, conflict: Conflict, settings: Settings):
        self.m = mission
        self.settings = settings
        self.conflict = conflict
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

        print("SETUP GROUP : " + str(for_task) + " -- " + str(group.name))

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

            # Do not generate player group with late activation.
            if group.late_activation:
                group.late_activation = False

            # Set up F-14 Client to have pre-stored alignement
            if unit_type is F_14B:
                group.units[idx].set_property(F_14B.Properties.INSAlignmentStored.id, True)

        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))

        if unit_type in helicopters.helicopter_map.values() and unit_type not in [UH_1H]:
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

        if unit_type in helicopters.helicopter_map.values():
            alt = WARM_START_HELI_ALT
            speed = WARM_START_HELI_AIRSPEED
        else:
            alt = WARM_START_ALTITUDE
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

    def _setup_custom_payload(self, flight, group:FlyingGroup):
        if flight.use_custom_loadout:

            logging.info("Custom loadout for flight : " + flight.__repr__())
            for p in group.units:
                p.pylons.clear()

            for key in flight.loadout.keys():
                if "Pylon" + key in flight.unit_type.__dict__.keys():
                    print(flight.loadout)
                    weapon_dict = flight.unit_type.__dict__["Pylon" + key].__dict__
                    if flight.loadout[key] in weapon_dict.keys():
                        weapon = weapon_dict[flight.loadout[key]]
                        group.load_pylon(weapon, int(key))
                else:
                    logging.warning("Pylon not found ! => Pylon" + key + " on " + str(flight.unit_type))


    def generate_flights(self, cp, country, flight_planner:FlightPlanner):

        for flight in flight_planner.interceptor_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_intercept_flight(group, flight)
            self._setup_custom_payload(flight, group)

        for flight in flight_planner.cap_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_cap_flight(group, flight)
            self._setup_custom_payload(flight, group)

        for flight in flight_planner.cas_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_cas_flight(group, flight)
            self._setup_custom_payload(flight, group)

        for flight in flight_planner.sead_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_sead_flight(group, flight)
            self._setup_custom_payload(flight, group)

        for flight in flight_planner.strike_flights:
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_group_as_strike_flight(group, flight)
            self._setup_custom_payload(flight, group)

        for flight in flight_planner.custom_flights:
            group = self.generate_planned_flight(cp, country, flight)
            if flight.flight_type == FlightType.INTERCEPTION:
                self.setup_group_as_intercept_flight(group, flight)
            elif flight.flight_type in [FlightType.CAP, FlightType.TARCAP, FlightType.BARCAP]:
                self.setup_group_as_cap_flight(group, flight)
            elif flight.flight_type in [FlightType.CAS, FlightType.BAI]:
                self.setup_group_as_cas_flight(group, flight)
            elif flight.flight_type in [FlightType.STRIKE]:
                self.setup_group_as_strike_flight(group, flight)
            elif flight.flight_type in [FlightType.ANTISHIP]:
                self.setup_group_as_antiship_flight(group, flight)
            elif flight.flight_type in [FlightType.SEAD, FlightType.DEAD]:
                self.setup_group_as_sead_flight(group, flight)
            else:
                self.setup_group_as_cap_flight(group, flight)
            self._setup_custom_payload(flight, group)

    def generate_planned_flight(self, cp, country, flight:Flight):
        try:
            if flight.start_type == "In Flight" or flight.client_count == 0:
                group = self._generate_group(
                    name=namegen.next_unit_name(country, cp.id, flight.unit_type),
                    side=country,
                    unit_type=flight.unit_type,
                    count=flight.count,
                    client_count=0,
                    at=cp.position)
            else:

                st = StartType.Runway
                if flight.start_type == "Cold":
                    st = StartType.Cold
                elif flight.start_type == "Warm":
                    st = StartType.Warm

                if cp.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]:
                    group_name = cp.get_carrier_group_name()
                    group = self._generate_at_group(
                        name=namegen.next_unit_name(country, cp.id, flight.unit_type),
                        side=country,
                        unit_type=flight.unit_type,
                        count=flight.count,
                        client_count=0,
                        at=self.m.find_group(group_name),)
                else:
                    group = self._generate_at_airport(
                        name=namegen.next_unit_name(country, cp.id, flight.unit_type),
                        side=country,
                        unit_type=flight.unit_type,
                        count=flight.count,
                        client_count=0,
                        airport=self.m.terrain.airport_by_id(cp.at.id),
                        start_type=st)
        except Exception:
            # Generated when there is no place on Runway or on Parking Slots
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

    def setup_group_as_intercept_flight(self, group, flight):
        group.points[0].ETA = 0
        group.late_activation = True
        self._setup_group(group, Intercept, flight.client_count)
        for point in flight.points:
            group.add_waypoint(Point(point.x,point.y), point.alt)


    def setup_group_as_cap_flight(self, group, flight):
        self._setup_group(group, CAP, flight.client_count)
        for point in flight.points:
            group.add_waypoint(Point(point.x,point.y), point.alt)

    def setup_group_as_cas_flight(self, group, flight):
        group.task = CAS.name
        self._setup_group(group, CAS, flight.client_count)

        group.points[0].tasks.clear()
        group.points[0].tasks.append(CASTaskAction())
        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
        group.points[0].tasks.append(OptROE(OptROE.Values.OpenFireWeaponFree))
        group.points[0].tasks.append(OptRestrictJettison(True))

        for point in flight.points:
            group.add_waypoint(Point(point.x,point.y), point.alt)

    def setup_group_as_sead_flight(self, group, flight):
        group.task = SEAD.name
        self._setup_group(group, SEAD, flight.client_count)

        group.points[0].tasks.clear()
        group.points[0].tasks.append(SEADTaskAction())
        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
        group.points[0].tasks.append(OptROE(OptROE.Values.OpenFireWeaponFree))
        group.points[0].tasks.append(OptRestrictJettison(True))

        i = 1
        for point in flight.points:
            group.add_waypoint(Point(point.x,point.y), point.alt)
            group.points[i].tasks.clear()
            group.points[i].tasks.append(SEADTaskAction())
            i = i + 1

    def setup_group_as_strike_flight(self, group, flight):
        group.task = PinpointStrike.name
        self._setup_group(group, GroundAttack, flight.client_count)

        group.points[0].tasks.clear()
        group.points[0].tasks.append(CASTaskAction())
        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
        group.points[0].tasks.append(OptROE(OptROE.Values.OpenFire))
        group.points[0].tasks.append(OptRestrictJettison(True))

        i = 1
        for point in flight.points:
            group.add_waypoint(Point(point.x,point.y), point.alt)
            for t in point.targets:
                group.points[i].tasks.append(Bombing(t.position))
            i = i + 1


    def setup_group_as_antiship_flight(self, group, flight):
        group.task = AntishipStrike.name
        self._setup_group(group, AntishipStrike, flight.client_count)

        group.points[0].tasks.clear()
        group.points[0].tasks.append(AntishipStrikeTaskAction())
        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
        group.points[0].tasks.append(OptROE(OptROE.Values.OpenFireWeaponFree))
        group.points[0].tasks.append(OptRestrictJettison(True))

        for point in flight.points:
            group.add_waypoint(Point(point.x,point.y), point.alt)


