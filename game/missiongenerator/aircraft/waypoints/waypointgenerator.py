import itertools
import random
from collections.abc import Iterator
from datetime import datetime, timedelta
from typing import Any

from dcs import Mission
from dcs.action import AITaskPush, ActivateGroup
from dcs.condition import CoalitionHasAirdrome, TimeAfter
from dcs.planes import AJS37
from dcs.task import StartCommand
from dcs.triggers import Event, TriggerOnce, TriggerRule
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightWaypoint
from game.ato.flightstate import InFlight, WaitingForStart
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.missiongenerator.aircraft.waypoints.cargostop import CargoStopBuilder
from game.missiongenerator.aircraft.waypoints.recoverytanker import (
    RecoveryTankerBuilder,
)
from game.missiongenerator.missiondata import MissionData
from game.settings import Settings
from game.unitmap import UnitMap
from game.utils import pairwise
from .baiingress import BaiIngressBuilder
from .landingzone import LandingZoneBuilder
from .casingress import CasIngressBuilder
from .deadingress import DeadIngressBuilder
from .default import DefaultWaypointBuilder
from .holdpoint import HoldPointBuilder
from .joinpoint import JoinPointBuilder
from .landingpoint import LandingPointBuilder
from .ocaaircraftingress import OcaAircraftIngressBuilder
from .ocarunwayingress import OcaRunwayIngressBuilder
from .pydcswaypointbuilder import PydcsWaypointBuilder, TARGET_WAYPOINTS
from .racetrack import RaceTrackBuilder
from .racetrackend import RaceTrackEndBuilder
from .refuel import RefuelPointBuilder
from .seadingress import SeadIngressBuilder
from .splitpoint import SplitPointBuilder
from .strikeingress import StrikeIngressBuilder
from .sweepingress import SweepIngressBuilder


class WaypointGenerator:
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        mission: Mission,
        turn_start_time: datetime,
        time: datetime,
        settings: Settings,
        mission_data: MissionData,
        unit_map: UnitMap,
    ) -> None:
        self.flight = flight
        self.group = group
        self.mission = mission
        self.elapsed_mission_time = time - turn_start_time
        self.time = time
        self.settings = settings
        self.mission_data = mission_data
        self.unit_map = unit_map

    def create_waypoints(self) -> tuple[timedelta, list[FlightWaypoint]]:
        for waypoint in self.flight.points:
            waypoint.tot = None

        waypoints = self.flight.flight_plan.waypoints
        mission_start_time = self.set_takeoff_time(waypoints[0])

        filtered_points: list[FlightWaypoint] = []
        for point in self.flight.points:
            if point.only_for_player and not self.flight.client_count:
                continue
            if isinstance(self.flight.state, InFlight):
                if point == self.flight.state.current_waypoint:
                    # We don't need to build this waypoint because pydcs did that for
                    # us, but we do need to configure the tasks for it so that mid-
                    # mission aircraft starting at a waypoint with tasks behave
                    # correctly.
                    self.builder_for_waypoint(point).add_tasks(self.group.points[0])
                if not self.flight.state.has_passed_waypoint(point):
                    filtered_points.append(point)
            else:
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
        self._estimate_min_fuel_for(waypoints)
        return mission_start_time, waypoints

    def builder_for_waypoint(self, waypoint: FlightWaypoint) -> PydcsWaypointBuilder:
        builders = {
            FlightWaypointType.INGRESS_BAI: BaiIngressBuilder,
            FlightWaypointType.INGRESS_CAS: CasIngressBuilder,
            FlightWaypointType.INGRESS_DEAD: DeadIngressBuilder,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT: OcaAircraftIngressBuilder,
            FlightWaypointType.INGRESS_OCA_RUNWAY: OcaRunwayIngressBuilder,
            FlightWaypointType.INGRESS_SEAD: SeadIngressBuilder,
            FlightWaypointType.INGRESS_STRIKE: StrikeIngressBuilder,
            FlightWaypointType.INGRESS_SWEEP: SweepIngressBuilder,
            FlightWaypointType.JOIN: JoinPointBuilder,
            FlightWaypointType.SPLIT: SplitPointBuilder,
            FlightWaypointType.LANDING_POINT: LandingPointBuilder,
            FlightWaypointType.LOITER: HoldPointBuilder,
            FlightWaypointType.PATROL: RaceTrackEndBuilder,
            FlightWaypointType.PATROL_TRACK: RaceTrackBuilder,
            FlightWaypointType.PICKUP_ZONE: LandingZoneBuilder,
            FlightWaypointType.DROPOFF_ZONE: LandingZoneBuilder,
            FlightWaypointType.REFUEL: RefuelPointBuilder,
            FlightWaypointType.RECOVERY_TANKER: RecoveryTankerBuilder,
            FlightWaypointType.CARGO_STOP: CargoStopBuilder,
        }
        builder = builders.get(waypoint.waypoint_type, DefaultWaypointBuilder)
        return builder(
            waypoint,
            self.group,
            self.flight,
            self.mission,
            self.elapsed_mission_time,
            self.mission_data,
            self.unit_map,
        )

    def _estimate_min_fuel_for(self, waypoints: list[FlightWaypoint]) -> None:
        if self.flight.unit_type.fuel_consumption is None:
            return

        consumption = self.flight.unit_type.fuel_consumption
        min_fuel: float = consumption.min_safe

        # The flight plan (in reverse) up to and including the arrival point.
        main_flight_plan: Iterator[FlightWaypoint] = reversed(waypoints)
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
            for_leg = self.flight.flight_plan.fuel_consumption_between_points(a, b)
            if for_leg is None:
                continue
            min_fuel += for_leg
            a.min_fuel = min_fuel

    def set_takeoff_time(self, waypoint: FlightWaypoint) -> timedelta:
        if isinstance(self.flight.state, WaitingForStart):
            delay = self.flight.state.time_remaining(self.time)
        else:
            delay = timedelta()

        if self.should_delay_flight():
            if self.should_activate_late():
                # Late activation causes the aircraft to not be spawned
                # until triggered.
                self.set_activation_time(delay)
            elif self.flight.start_type is StartType.COLD:
                # Setting the start time causes the AI to wait until the
                # specified time to begin their startup sequence.
                self.set_startup_time(delay)

        # And setting *our* waypoint TOT causes the takeoff time to show up in
        # the player's kneeboard.
        waypoint.tot = self.flight.flight_plan.takeoff_time()
        return delay

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
        if (airport := self.flight.departure.dcs_airport) is not None:
            trigger.add_condition(
                CoalitionHasAirdrome(
                    self.flight.squadron.coalition.coalition_id, airport.id
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

    def should_delay_flight(self) -> bool:
        if not isinstance(self.flight.state, WaitingForStart):
            return False

        if not self.flight.client_count:
            return True

        if self.flight.state.time_remaining(self.time) < timedelta(minutes=10):
            # Don't bother delaying client flights with short start delays. Much more
            # than ten minutes starts to eat into fuel a bit more (especially for
            # something fuel limited like a Harrier).
            return False

        return not self.settings.never_delay_player_flights

    def should_activate_late(self) -> bool:
        if self.flight.start_type is not StartType.COLD:
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
