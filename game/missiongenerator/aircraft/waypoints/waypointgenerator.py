import itertools
import random
from datetime import timedelta
from typing import Any

from dcs import Mission
from dcs.action import AITaskPush, ActivateGroup
from dcs.condition import CoalitionHasAirdrome, TimeAfter
from dcs.planes import AJS37
from dcs.task import StartCommand
from dcs.triggers import Event, TriggerOnce, TriggerRule
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.missiongenerator.airsupport import AirSupport
from game.settings import Settings
from game.theater import ControlPointType
from game.utils import meters, pairwise
from gen.flights.traveltime import TotEstimator

from .pydcswaypointbuilder import PydcsWaypointBuilder, TARGET_WAYPOINTS
from .baiingress import BaiIngressBuilder
from .cargostop import CargoStopBuilder
from .casingress import CasIngressBuilder
from .deadingress import DeadIngressBuilder
from .default import DefaultWaypointBuilder
from .holdpoint import HoldPointBuilder
from .joinpoint import JoinPointBuilder
from .landingpoint import LandingPointBuilder
from .ocaaircraftingress import OcaAircraftIngressBuilder
from .ocarunwayingress import OcaRunwayIngressBuilder
from .racetrack import RaceTrackBuilder
from .racetrackend import RaceTrackEndBuilder
from .seadingress import SeadIngressBuilder
from .strikeingress import StrikeIngressBuilder
from .sweepingress import SweepIngressBuilder


class WaypointGenerator:
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        mission: Mission,
        settings: Settings,
        air_support: AirSupport,
    ) -> None:
        self.flight = flight
        self.group = group
        self.mission = mission
        self.settings = settings
        self.air_support = air_support

    def create_waypoints(self) -> tuple[timedelta, list[FlightWaypoint]]:
        for waypoint in self.flight.points:
            waypoint.tot = None

        takeoff_point = FlightWaypoint.from_pydcs(
            self.group.points[0], self.flight.from_cp
        )
        mission_start_time = self.set_takeoff_time(takeoff_point)

        filtered_points: list[FlightWaypoint] = []

        for point in self.flight.points:
            if point.only_for_player and not self.flight.client_count:
                continue
            filtered_points.append(point)
        # Only add 1 target waypoint for Viggens.  This only affects player flights, the
        # Viggen can't have more than 9 waypoints which leaves us with two target point
        # under the current flight plans.
        # TODO: Make this smarter. It currently targets a random unit in the group.
        # This could be updated to make it pick the "best" two targets in the group.
        if self.flight.unit_type.dcs_unit_type is AJS37 and self.flight.client_count:
            viggen_target_points = [
                (idx, point)
                for idx, point in enumerate(filtered_points)
                if point.waypoint_type in TARGET_WAYPOINTS
            ]
            if viggen_target_points:
                keep_target = viggen_target_points[
                    random.randint(0, len(viggen_target_points) - 1)
                ]
                filtered_points = [
                    point
                    for idx, point in enumerate(filtered_points)
                    if (
                        point.waypoint_type not in TARGET_WAYPOINTS
                        or idx == keep_target[0]
                    )
                ]

        for idx, point in enumerate(filtered_points):
            self.builder_for_waypoint(point).build()

        # Set here rather than when the FlightData is created so they waypoints
        # have their TOTs and fuel minimums set. Once we're more confident in our fuel
        # estimation ability the minimum fuel amounts will be calculated during flight
        # plan construction, but for now it's only used by the kneeboard so is generated
        # late.
        waypoints = [takeoff_point] + self.flight.points
        self._estimate_min_fuel_for(waypoints)
        return mission_start_time, waypoints

    def builder_for_waypoint(self, waypoint: FlightWaypoint) -> PydcsWaypointBuilder:
        builders = {
            FlightWaypointType.DROP_OFF: CargoStopBuilder,
            FlightWaypointType.INGRESS_BAI: BaiIngressBuilder,
            FlightWaypointType.INGRESS_CAS: CasIngressBuilder,
            FlightWaypointType.INGRESS_DEAD: DeadIngressBuilder,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT: OcaAircraftIngressBuilder,
            FlightWaypointType.INGRESS_OCA_RUNWAY: OcaRunwayIngressBuilder,
            FlightWaypointType.INGRESS_SEAD: SeadIngressBuilder,
            FlightWaypointType.INGRESS_STRIKE: StrikeIngressBuilder,
            FlightWaypointType.INGRESS_SWEEP: SweepIngressBuilder,
            FlightWaypointType.JOIN: JoinPointBuilder,
            FlightWaypointType.LANDING_POINT: LandingPointBuilder,
            FlightWaypointType.LOITER: HoldPointBuilder,
            FlightWaypointType.PATROL: RaceTrackEndBuilder,
            FlightWaypointType.PATROL_TRACK: RaceTrackBuilder,
            FlightWaypointType.PICKUP: CargoStopBuilder,
        }
        builder = builders.get(waypoint.waypoint_type, DefaultWaypointBuilder)
        return builder(
            waypoint, self.group, self.flight, self.mission, self.air_support
        )

    def _estimate_min_fuel_for(self, waypoints: list[FlightWaypoint]) -> None:
        if self.flight.unit_type.fuel_consumption is None:
            return

        combat_speed_types = {
            FlightWaypointType.INGRESS_BAI,
            FlightWaypointType.INGRESS_CAS,
            FlightWaypointType.INGRESS_DEAD,
            FlightWaypointType.INGRESS_ESCORT,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT,
            FlightWaypointType.INGRESS_OCA_RUNWAY,
            FlightWaypointType.INGRESS_SEAD,
            FlightWaypointType.INGRESS_STRIKE,
            FlightWaypointType.INGRESS_SWEEP,
            FlightWaypointType.SPLIT,
        } | set(TARGET_WAYPOINTS)

        consumption = self.flight.unit_type.fuel_consumption
        min_fuel: float = consumption.min_safe

        # The flight plan (in reverse) up to and including the arrival point.
        main_flight_plan = reversed(waypoints)
        try:
            while waypoint := next(main_flight_plan):
                if waypoint.waypoint_type is FlightWaypointType.LANDING_POINT:
                    waypoint.min_fuel = min_fuel
                    main_flight_plan = itertools.chain([waypoint], main_flight_plan)
                    break
        except StopIteration:
            # Some custom flight plan without a landing point. Skip it.
            return

        for b, a in pairwise(main_flight_plan):
            distance = meters(a.position.distance_to_point(b.position))
            if a.waypoint_type is FlightWaypointType.TAKEOFF:
                ppm = consumption.climb
            elif b.waypoint_type in combat_speed_types:
                ppm = consumption.combat
            else:
                ppm = consumption.cruise
            min_fuel += distance.nautical_miles * ppm
            a.min_fuel = min_fuel

    def set_takeoff_time(self, waypoint: FlightWaypoint) -> timedelta:
        estimator = TotEstimator(self.flight.package)
        start_time = estimator.mission_start_time(self.flight)

        if self.should_delay_flight(start_time):
            if self.should_activate_late():
                # Late activation causes the aircraft to not be spawned
                # until triggered.
                self.set_activation_time(start_time)
            elif self.flight.get_start_type is StartType.COLD:
                # Setting the start time causes the AI to wait until the
                # specified time to begin their startup sequence.
                self.set_startup_time(start_time)

        # And setting *our* waypoint TOT causes the takeoff time to show up in
        # the player's kneeboard.
        waypoint.tot = self.flight.flight_plan.takeoff_time()
        return start_time

    def set_activation_time(self, delay: timedelta) -> None:
        # Note: Late activation causes the waypoint TOTs to look *weird* in the
        # mission editor. Waypoint times will be relative to the group
        # activation time rather than in absolute local time. A flight delayed
        # until 09:10 when the overall mission start time is 09:00, with a join
        # time of 09:30 will show the join time as 00:30, not 09:30.
        self.group.late_activation = True

        activation_trigger = TriggerOnce(
            Event.NoEvent, f"FlightLateActivationTrigger{self.group.id}"
        )
        activation_trigger.add_condition(TimeAfter(seconds=int(delay.total_seconds())))

        self.prevent_spawn_at_hostile_airbase(activation_trigger)
        activation_trigger.add_action(ActivateGroup(self.group.id))
        self.mission.triggerrules.triggers.append(activation_trigger)

    def prevent_spawn_at_hostile_airbase(self, trigger: TriggerRule) -> None:
        # Prevent delayed flights from spawning at airbases if they were
        # captured before they've spawned.
        if self.flight.from_cp.cptype != ControlPointType.AIRBASE:
            return

        trigger.add_condition(
            CoalitionHasAirdrome(
                self.flight.squadron.coalition.coalition_id, self.flight.from_cp.id
            )
        )

    def set_startup_time(self, delay: timedelta) -> None:
        # Uncontrolled causes the AI unit to spawn, but not begin startup.
        self.group.uncontrolled = True

        activation_trigger = TriggerOnce(
            Event.NoEvent, f"FlightStartTrigger{self.group.id}"
        )
        activation_trigger.add_condition(TimeAfter(seconds=int(delay.total_seconds())))

        self.prevent_spawn_at_hostile_airbase(activation_trigger)
        self.group.add_trigger_action(StartCommand())
        activation_trigger.add_action(AITaskPush(self.group.id, len(self.group.tasks)))
        self.mission.triggerrules.triggers.append(activation_trigger)

    def should_delay_flight(self, start_time: timedelta) -> bool:
        if start_time.total_seconds() <= 0:
            return False

        if not self.flight.client_count:
            return True

        if start_time < timedelta(minutes=10):
            # Don't bother delaying client flights with short start delays. Much
            # more than ten minutes starts to eat into fuel a bit more
            # (espeicially for something fuel limited like a Harrier).
            return False

        return not self.settings.never_delay_player_flights

    def should_activate_late(self) -> bool:
        if self.flight.get_start_type is StartType.COLD:
            # Avoid spawning aircraft in the air or on the runway until it's
            # time for their mission. Also avoid burning through gas spawning
            # hot aircraft hours before their takeoff time.
            return True

        if self.flight.from_cp.is_fleet:
            # Carrier spawns will crowd the carrier deck, especially without
            # super carrier.
            # TODO: Is there enough parking on the supercarrier?
            return True

        return False
