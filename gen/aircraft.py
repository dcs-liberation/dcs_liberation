from dcs.action import ActivateGroup, AITaskPush, MessageToCoalition, MessageToAll
from dcs.condition import TimeAfter, CoalitionHasAirdrome, PartOfCoalitionInZone
from dcs.helicopters import UH_1H
from dcs.terrain.terrain import NoParkingSlotError
from dcs.triggers import TriggerOnce, Event

from game.data.cap_capabilities_db import GUNFIGHTERS
from game.settings import Settings
from game.utils import nm_to_meter
from gen.flights.ai_flight_planner import FlightPlanner
from gen.flights.flight import Flight, FlightType, FlightWaypointType
from .conflictgen import *
from .naming import *

WARM_START_HELI_AIRSPEED = 120
WARM_START_HELI_ALT = 500
WARM_START_ALTITUDE = 3000
WARM_START_AIRSPEED = 550

CAP_DURATION = 30 # minutes

RTB_ALTITUDE = 800
RTB_DISTANCE = 5000
HELI_ALT = 500


class AircraftConflictGenerator:
    escort_targets = [] # type: typing.List[typing.Tuple[FlyingGroup, int]]

    def __init__(self, mission: Mission, conflict: Conflict, settings: Settings, game):
        self.m = mission
        self.game = game
        self.settings = settings
        self.conflict = conflict
        self.escort_targets = []

    def _start_type(self) -> StartType:
        return self.settings.cold_start and StartType.Cold or StartType.Warm


    def _setup_group(self, group: FlyingGroup, for_task: typing.Type[Task], flight: Flight):
        did_load_loadout = False
        unit_type = group.units[0].unit_type

        if unit_type in db.PLANE_PAYLOAD_OVERRIDES:
            override_loadout = db.PLANE_PAYLOAD_OVERRIDES[unit_type]
            if type(override_loadout) == dict:

                # Clear pylons
                for p in group.units:
                    p.pylons.clear()

                # Now load loadout
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

        single_client = flight.client_count == 1
        for idx in range(0, min(len(group.units), flight.client_count)):
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

        # TODO : refactor this following bad specific special case code :(

        if unit_type in helicopters.helicopter_map.values() and unit_type not in [UH_1H]:
            group.set_frequency(127.5)
        else:
            if unit_type not in [P_51D_30_NA, P_51D, SpitfireLFMkIX, SpitfireLFMkIXCW, P_47D_30, I_16, FW_190A8, FW_190D9, Bf_109K_4]:
                group.set_frequency(251.0)
            else:
                # WW2
                if unit_type in [FW_190A8, FW_190D9, Bf_109K_4, Ju_88A4]:
                    group.set_frequency(40)
                else:
                    group.set_frequency(124.0)

        # Special case so Su 33 carrier take off
        if unit_type is Su_33:
            if task is not CAP:
                for unit in group.units:
                    unit.fuel = Su_33.fuel_max / 2.2
            else:
                for unit in group.units:
                    unit.fuel = Su_33.fuel_max * 0.8


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
            airport=airport,
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

    def _generate_at_group(self, name: str, side: Country, unit_type: FlyingType, count: int, client_count: int, at: typing.Union[ShipGroup, StaticGroup], start_type=None) -> FlyingGroup:
        assert count > 0
        assert unit is not None

        if start_type is None:
            start_type = self._start_type()

        logging.info("airgen: {} for {} at unit {}".format(unit_type, side.id, at))
        return self.m.flight_group_from_unit(
            country=side,
            name=name,
            aircraft_type=unit_type,
            pad_group=at,
            maintask=None,
            start_type=start_type,
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
                    logging.info("No parking slot found at " + at.name + ", switching to air start.")
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

        # Clear pydcs parking slots
        if cp.airport is not None:
            logging.info("CLEARING SLOTS @ " + cp.airport.name)
            logging.info("===============")
            if cp.airport is not None:
                for ps in cp.airport.parking_slots:
                    logging.info("SLOT : " + str(ps.unit_id))
                    ps.unit_id = None
                logging.info("----------------")
            logging.info("===============")

        for flight in flight_planner.flights:

            if flight.client_count == 0 and self.game.position_culled(flight.from_cp.position):
                logging.info("Flight not generated : culled")
                continue
            logging.info("Generating flight : " + str(flight.unit_type))
            group = self.generate_planned_flight(cp, country, flight)
            self.setup_flight_group(group, flight, flight.flight_type)
            self.setup_group_activation_trigger(flight, group)


    def setup_group_activation_trigger(self, flight, group):
        if flight.scheduled_in > 0 and flight.client_count == 0:

            if flight.start_type != "In Flight" and flight.from_cp.cptype not in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]:
                group.late_activation = False
                group.uncontrolled = True

                activation_trigger = TriggerOnce(Event.NoEvent, "FlightStartTrigger" + str(group.id))
                activation_trigger.add_condition(TimeAfter(seconds=flight.scheduled_in * 60))
                if (flight.from_cp.cptype == ControlPointType.AIRBASE):
                    if flight.from_cp.captured:
                        activation_trigger.add_condition(
                            CoalitionHasAirdrome(self.game.get_player_coalition_id(), flight.from_cp.id))
                    else:
                        activation_trigger.add_condition(
                            CoalitionHasAirdrome(self.game.get_enemy_coalition_id(), flight.from_cp.id))

                if flight.flight_type == FlightType.INTERCEPTION:
                    self.setup_interceptor_triggers(group, flight, activation_trigger)

                group.add_trigger_action(StartCommand())
                activation_trigger.add_action(AITaskPush(group.id, len(group.tasks)))

                self.m.triggerrules.triggers.append(activation_trigger)
            else:
                group.late_activation = True
                activation_trigger = TriggerOnce(Event.NoEvent, "FlightLateActivationTrigger" + str(group.id))
                activation_trigger.add_condition(TimeAfter(seconds=flight.scheduled_in*60))

                if(flight.from_cp.cptype == ControlPointType.AIRBASE):
                    if flight.from_cp.captured:
                        activation_trigger.add_condition(CoalitionHasAirdrome(self.game.get_player_coalition_id(), flight.from_cp.id))
                    else:
                        activation_trigger.add_condition(CoalitionHasAirdrome(self.game.get_enemy_coalition_id(), flight.from_cp.id))

                if flight.flight_type == FlightType.INTERCEPTION:
                    self.setup_interceptor_triggers(group, flight, activation_trigger)

                activation_trigger.add_action(ActivateGroup(group.id))
                self.m.triggerrules.triggers.append(activation_trigger)

    def setup_interceptor_triggers(self, group, flight, activation_trigger):

        detection_zone = self.m.triggers.add_triggerzone(flight.from_cp.position, radius=25000, hidden=False, name="ITZ")
        if flight.from_cp.captured:
            activation_trigger.add_condition(PartOfCoalitionInZone(self.game.get_enemy_color(), detection_zone.id)) # TODO : support unit type in part of coalition
            activation_trigger.add_action(MessageToAll(String("WARNING : Enemy aircraft have been detected in the vicinity of " + flight.from_cp.name + ". Interceptors are taking off."), 20))
        else:
            activation_trigger.add_condition(PartOfCoalitionInZone(self.game.get_player_color(), detection_zone.id))
            activation_trigger.add_action(MessageToAll(String("WARNING : We have detected that enemy aircraft are scrambling for an interception on " + flight.from_cp.name + " airbase."), 20))

    def generate_planned_flight(self, cp, country, flight:Flight):
        try:
            if flight.client_count == 0 and self.game.settings.perf_ai_parking_start:
                flight.start_type = "Cold"

            if flight.start_type == "In Flight":
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
                        at=self.m.find_group(group_name),
                        start_type=st)
                else:
                    group = self._generate_at_airport(
                        name=namegen.next_unit_name(country, cp.id, flight.unit_type),
                        side=country,
                        unit_type=flight.unit_type,
                        count=flight.count,
                        client_count=0,
                        airport=cp.airport,
                        start_type=st)
        except Exception as e:
            # Generated when there is no place on Runway or on Parking Slots
            logging.error(e)
            logging.warning("No room on runway or parking slots. Starting from the air.")
            flight.start_type = "In Flight"
            group = self._generate_group(
                name=namegen.next_unit_name(country, cp.id, flight.unit_type),
                side=country,
                unit_type=flight.unit_type,
                count=flight.count,
                client_count=0,
                at=cp.position)
            group.points[0].alt = 1500

        flight.group = group
        return group

    def setup_group_as_intercept_flight(self, group, flight):
        group.points[0].ETA = 0
        group.late_activation = True
        self._setup_group(group, Intercept, flight)
        for point in flight.points:
            group.add_waypoint(Point(point.x,point.y), point.alt)


    def setup_flight_group(self, group, flight, flight_type):

        if flight_type in [FlightType.CAP, FlightType.BARCAP, FlightType.TARCAP, FlightType.INTERCEPTION]:
            group.task = CAP.name
            self._setup_group(group, CAP, flight)
            # group.points[0].tasks.clear()
            group.points[0].tasks.clear()
            group.points[0].tasks.append(EngageTargets(max_distance=nm_to_meter(50), targets=[Targets.All.Air]))
            # group.tasks.append(EngageTargets(max_distance=nm_to_meter(120), targets=[Targets.All.Air]))
            if flight.unit_type not in GUNFIGHTERS:
                group.points[0].tasks.append(OptRTBOnOutOfAmmo(OptRTBOnOutOfAmmo.Values.AAM))
            else:
                group.points[0].tasks.append(OptRTBOnOutOfAmmo(OptRTBOnOutOfAmmo.Values.Cannon))

        elif flight_type in [FlightType.CAS, FlightType.BAI]:
            group.task = CAS.name
            self._setup_group(group, CAS, flight)
            group.points[0].tasks.clear()
            group.points[0].tasks.append(EngageTargets(max_distance=nm_to_meter(10), targets=[Targets.All.GroundUnits.GroundVehicles]))
            group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
            group.points[0].tasks.append(OptROE(OptROE.Values.OpenFireWeaponFree))
            group.points[0].tasks.append(OptRTBOnOutOfAmmo(OptRTBOnOutOfAmmo.Values.Unguided))
            group.points[0].tasks.append(OptRestrictJettison(True))
        elif flight_type in [FlightType.SEAD, FlightType.DEAD]:
            group.task = SEAD.name
            self._setup_group(group, SEAD, flight)
            group.points[0].tasks.clear()
            group.points[0].tasks.append(NoTask())
            group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
            group.points[0].tasks.append(OptROE(OptROE.Values.OpenFire))
            group.points[0].tasks.append(OptRestrictJettison(True))
            group.points[0].tasks.append(OptRTBOnOutOfAmmo(OptRTBOnOutOfAmmo.Values.ASM))
        elif flight_type in [FlightType.STRIKE]:
            group.task = PinpointStrike.name
            self._setup_group(group, GroundAttack, flight)
            group.points[0].tasks.clear()
            group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
            group.points[0].tasks.append(OptROE(OptROE.Values.OpenFire))
            group.points[0].tasks.append(OptRestrictJettison(True))
        elif flight_type in [FlightType.ANTISHIP]:
            group.task = AntishipStrike.name
            self._setup_group(group, AntishipStrike, flight)
            group.points[0].tasks.clear()
            group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
            group.points[0].tasks.append(OptROE(OptROE.Values.OpenFire))
            group.points[0].tasks.append(OptRestrictJettison(True))

        group.points[0].tasks.append(OptRTBOnBingoFuel(True))
        group.points[0].tasks.append(OptRestrictAfterburner(True))

        if hasattr(flight.unit_type, 'eplrs'):
            if flight.unit_type.eplrs:
                group.points[0].tasks.append(EPLRS(group.id))

        for i, point in enumerate(flight.points):
            if not point.only_for_player or (point.only_for_player and flight.client_count > 0):
                pt = group.add_waypoint(Point(point.x, point.y), point.alt)
                if point.waypoint_type == FlightWaypointType.PATROL_TRACK:
                    action = ControlledTask(OrbitAction(altitude=pt.alt, pattern=OrbitAction.OrbitPattern.RaceTrack))
                    action.stop_after_duration(CAP_DURATION * 60)
                    #for tgt in point.targets:
                    #    if hasattr(tgt, "position"):
                    #        engagetgt = EngageTargetsInZone(tgt.position, radius=CAP_DEFAULT_ENGAGE_DISTANCE, targets=[Targets.All.Air])
                    #        pt.tasks.append(engagetgt)
                elif point.waypoint_type == FlightWaypointType.LANDING_POINT:
                    pt.type = "Land"
                elif point.waypoint_type == FlightWaypointType.INGRESS_STRIKE:

                    if group.units[0].unit_type == B_17G:
                        if len(point.targets) > 0:
                            bcenter = Point(0,0)
                            for j, t in enumerate(point.targets):
                                bcenter.x += t.position.x
                                bcenter.y += t.position.y
                            bcenter.x = bcenter.x / len(point.targets)
                            bcenter.y = bcenter.y / len(point.targets)
                            bombing = Bombing(bcenter)
                            bombing.params["expend"] = "All"
                            bombing.params["attackQtyLimit"] = False
                            bombing.params["directionEnabled"] = False
                            bombing.params["altitudeEnabled"] = False
                            bombing.params["weaponType"] = 2032
                            bombing.params["groupAttack"] = True
                            pt.tasks.append(bombing)
                    else:
                        for j, t in enumerate(point.targets):
                            print(t.position)
                            pt.tasks.append(Bombing(t.position))
                            if group.units[0].unit_type == JF_17 and j < 4:
                                group.add_nav_target_point(t.position, "PP" + str(j + 1))
                            if group.units[0].unit_type == F_14B and j == 0:
                                group.add_nav_target_point(t.position, "ST")
                            if group.units[0].unit_type == AJS37 and j < 9:
                                group.add_nav_target_point(t.position, "M" + str(j + 1))
                elif point.waypoint_type == FlightWaypointType.INGRESS_SEAD:

                    tgroup = self.m.find_group(point.targetGroup.group_identifier)
                    if tgroup is not None:
                        task = AttackGroup(tgroup.id)
                        task.params["expend"] = "All"
                        task.params["attackQtyLimit"] = False
                        task.params["directionEnabled"] = False
                        task.params["altitudeEnabled"] = False
                        task.params["weaponType"] = 268402702 # Guided Weapons
                        task.params["groupAttack"] = True
                        pt.tasks.append(task)

                    for j, t in enumerate(point.targets):
                        if group.units[0].unit_type == JF_17 and j < 4:
                            group.add_nav_target_point(t.position, "PP" + str(j + 1))
                        if group.units[0].unit_type == F_14B and j == 0:
                            group.add_nav_target_point(t.position, "ST")
                        if group.units[0].unit_type == AJS37 and j < 9:
                            group.add_nav_target_point(t.position, "M" + str(j + 1))

                if pt is not None:
                    pt.alt_type = point.alt_type
                    pt.name = String(point.name)

        self._setup_custom_payload(flight, group)


    def setup_group_as_antiship_flight(self, group, flight):
        group.task = AntishipStrike.name
        self._setup_group(group, AntishipStrike, flight)

        group.points[0].tasks.clear()
        group.points[0].tasks.append(AntishipStrikeTaskAction())
        group.points[0].tasks.append(OptReactOnThreat(OptReactOnThreat.Values.EvadeFire))
        group.points[0].tasks.append(OptROE(OptROE.Values.OpenFireWeaponFree))
        group.points[0].tasks.append(OptRestrictJettison(True))

        for point in flight.points:
            group.add_waypoint(Point(point.x, point.y), point.alt)


    def setup_radio_preset(self, flight, group):
        pass


