from __future__ import annotations

import itertools
import logging
import random
from dataclasses import dataclass, field
from datetime import timedelta
from functools import cached_property
from typing import Dict, List, Optional, TYPE_CHECKING, Type, Union, Iterable, Any

from dcs import helicopters
from dcs.action import AITaskPush, ActivateGroup
from dcs.condition import CoalitionHasAirdrome, TimeAfter
from dcs.country import Country
from dcs.flyingunit import FlyingUnit
from dcs.mapping import Point
from dcs.mission import Mission, StartType
from dcs.planes import (
    AJS37,
    B_17G,
    B_52H,
    C_101CC,
    C_101EB,
    F_14B,
    JF_17,
    Su_33,
    Tu_22M3,
)
from dcs.point import MovingPoint, PointAction
from dcs.task import (
    AWACS,
    AWACSTaskAction,
    ActivateBeaconCommand,
    AntishipStrike,
    AttackGroup,
    Bombing,
    BombingRunway,
    CAP,
    CAS,
    ControlledTask,
    EPLRS,
    EngageTargets,
    EngageTargetsInZone,
    FighterSweep,
    GroundAttack,
    OptROE,
    OptRTBOnBingoFuel,
    OptRTBOnOutOfAmmo,
    OptReactOnThreat,
    OptRestrictJettison,
    OrbitAction,
    Refueling,
    RunwayAttack,
    StartCommand,
    Tanker,
    Targets,
    Transport,
    WeaponType,
    TargetType,
)
from dcs.terrain.terrain import Airport, NoParkingSlotError
from dcs.triggers import Event, TriggerOnce, TriggerRule
from dcs.unit import Unit, Skill
from dcs.unitgroup import FlyingGroup, ShipGroup, StaticGroup
from dcs.unittype import FlyingType

from game import db
from game.data.weapons import Pylon, WeaponType as WeaponTypeEnum
from game.dcs.aircrafttype import AircraftType
from game.factions.faction import Faction
from game.settings import Settings
from game.squadrons import Pilot
from game.theater.controlpoint import (
    Airfield,
    ControlPoint,
    ControlPointType,
    NavalControlPoint,
    OffMapSpawn,
)
from game.theater.missiontarget import MissionTarget
from game.theater.theatergroundobject import TheaterGroundObject
from game.transfers import MultiGroupTransport
from game.unitmap import UnitMap
from game.utils import Distance, meters, nautical_miles, pairwise
from gen.ato import AirTaskingOrder, Package
from gen.callsigns import create_group_callsign_from_unit
from gen.flights.flight import (
    Flight,
    FlightType,
    FlightWaypoint,
    FlightWaypointType,
)
from gen.lasercoderegistry import LaserCodeRegistry
from gen.radios import RadioFrequency, RadioRegistry
from gen.runways import RunwayData
from gen.tacan import TacanBand, TacanRegistry
from .airsupport import AirSupport, AwacsInfo, TankerInfo
from .callsigns import callsign_for_support_unit
from .flights.flightplan import (
    AwacsFlightPlan,
    CasFlightPlan,
    LoiterFlightPlan,
    PatrollingFlightPlan,
    RefuelingFlightPlan,
    SweepFlightPlan,
)
from .flights.traveltime import GroundSpeed, TotEstimator
from .naming import namegen

if TYPE_CHECKING:
    from game import Game

WARM_START_HELI_ALT = meters(500)
WARM_START_ALTITUDE = meters(3000)

RTB_ALTITUDE = meters(800)
RTB_DISTANCE = 5000
HELI_ALT = 500

TARGET_WAYPOINTS = (
    FlightWaypointType.TARGET_GROUP_LOC,
    FlightWaypointType.TARGET_POINT,
    FlightWaypointType.TARGET_SHIP,
)


@dataclass(frozen=True)
class ChannelAssignment:
    radio_id: int
    channel: int


@dataclass
class FlightData:
    """Details of a planned flight."""

    #: The package that the flight belongs to.
    package: Package

    flight_type: FlightType

    aircraft_type: AircraftType

    #: All units in the flight.
    units: List[FlyingUnit]

    #: Total number of aircraft in the flight.
    size: int

    #: True if this flight belongs to the player's coalition.
    friendly: bool

    #: Number of seconds after mission start the flight is set to depart.
    departure_delay: timedelta

    #: Arrival airport.
    arrival: RunwayData

    #: Departure airport.
    departure: RunwayData

    #: Diver airport.
    divert: Optional[RunwayData]

    #: Waypoints of the flight plan.
    waypoints: List[FlightWaypoint]

    #: Radio frequency for intra-flight communications.
    intra_flight_channel: RadioFrequency

    #: Bingo fuel value in lbs.
    bingo_fuel: Optional[int]

    joker_fuel: Optional[int]

    laser_codes: list[Optional[int]]

    custom_name: Optional[str]

    callsign: str = field(init=False)

    #: Map of radio frequencies to their assigned radio and channel, if any.
    frequency_to_channel_map: Dict[RadioFrequency, ChannelAssignment] = field(
        init=False, default_factory=dict
    )

    def __post_init__(self) -> None:
        self.callsign = create_group_callsign_from_unit(self.units[0])

    @property
    def client_units(self) -> List[FlyingUnit]:
        """List of playable units in the flight."""
        return [u for u in self.units if u.is_human()]

    def num_radio_channels(self, radio_id: int) -> int:
        """Returns the number of preset channels for the given radio."""
        # Note: pydcs only initializes the radio presets for client slots.
        return self.client_units[0].num_radio_channels(radio_id)

    def channel_for(self, frequency: RadioFrequency) -> Optional[ChannelAssignment]:
        """Returns the radio and channel number for the given frequency."""
        return self.frequency_to_channel_map.get(frequency, None)

    def assign_channel(
        self, radio_id: int, channel_id: int, frequency: RadioFrequency
    ) -> None:
        """Assigns a preset radio channel to the given frequency."""
        for unit in self.client_units:
            unit.set_radio_channel_preset(radio_id, channel_id, frequency.mhz)

        # One frequency could be bound to multiple channels. Prefer the first,
        # since with the current implementation it will be the lowest numbered
        # channel.
        if frequency not in self.frequency_to_channel_map:
            self.frequency_to_channel_map[frequency] = ChannelAssignment(
                radio_id, channel_id
            )


class AircraftConflictGenerator:
    def __init__(
        self,
        mission: Mission,
        settings: Settings,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        laser_code_registry: LaserCodeRegistry,
        unit_map: UnitMap,
        air_support: AirSupport,
        helipads: dict[ControlPoint, list[StaticGroup]],
    ) -> None:
        self.m = mission
        self.game = game
        self.settings = settings
        self.radio_registry = radio_registry
        self.tacan_registy = tacan_registry
        self.laser_code_registry = laser_code_registry
        self.unit_map = unit_map
        self.flights: List[FlightData] = []
        self.air_support = air_support
        self.helipads = helipads

    @cached_property
    def use_client(self) -> bool:
        """True if Client should be used instead of Player."""
        blue_clients = self.client_slots_in_ato(self.game.blue.ato)
        red_clients = self.client_slots_in_ato(self.game.red.ato)
        return blue_clients + red_clients > 1

    @staticmethod
    def client_slots_in_ato(ato: AirTaskingOrder) -> int:
        total = 0
        for package in ato.packages:
            for flight in package.flights:
                total += flight.client_count
        return total

    @staticmethod
    def _start_type(start_type: str) -> StartType:
        if start_type == "Runway":
            return StartType.Runway
        elif start_type == "Cold":
            return StartType.Cold
        return StartType.Warm

    def skill_level_for(
        self, unit: FlyingUnit, pilot: Optional[Pilot], blue: bool
    ) -> Skill:
        if blue:
            base_skill = Skill(self.game.settings.player_skill)
        else:
            base_skill = Skill(self.game.settings.enemy_skill)

        if pilot is None:
            logging.error(f"Cannot determine skill level: {unit.name} has not pilot")
            return base_skill

        levels = [
            Skill.Average,
            Skill.Good,
            Skill.High,
            Skill.Excellent,
        ]
        current_level = levels.index(base_skill)
        missions_for_skill_increase = 4
        increase = pilot.record.missions_flown // missions_for_skill_increase
        capped_increase = min(current_level + increase, len(levels) - 1)
        new_level = (capped_increase, current_level)[
            self.game.settings.ai_pilot_levelling
        ]
        return levels[new_level]

    def set_skill(self, unit: FlyingUnit, pilot: Optional[Pilot], blue: bool) -> None:
        if pilot is None or not pilot.player:
            unit.skill = self.skill_level_for(unit, pilot, blue)
            return

        if self.use_client:
            unit.set_client()
        else:
            unit.set_player()

    @staticmethod
    def livery_from_db(flight: Flight) -> Optional[str]:
        return db.PLANE_LIVERY_OVERRIDES.get(flight.unit_type.dcs_unit_type)

    def livery_from_faction(self, flight: Flight) -> Optional[str]:
        faction = self.game.faction_for(player=flight.departure.captured)
        if (choices := faction.liveries_overrides.get(flight.unit_type)) is not None:
            return random.choice(choices)
        return None

    @staticmethod
    def livery_from_squadron(flight: Flight) -> Optional[str]:
        return flight.squadron.livery

    def livery_for(self, flight: Flight) -> Optional[str]:
        if (livery := self.livery_from_squadron(flight)) is not None:
            return livery
        if (livery := self.livery_from_faction(flight)) is not None:
            return livery
        if (livery := self.livery_from_db(flight)) is not None:
            return livery
        return None

    def _setup_livery(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        livery = self.livery_for(flight)
        if livery is None:
            return
        for unit in group.units:
            unit.livery_id = livery

    def _setup_group(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        unit_type = group.units[0].unit_type

        self._setup_payload(flight, group)
        self._setup_livery(flight, group)

        laser_codes = []
        for unit, pilot in zip(group.units, flight.roster.pilots):
            player = pilot is not None and pilot.player
            self.set_skill(unit, pilot, blue=flight.departure.captured)
            # Do not generate player group with late activation.
            if player and group.late_activation:
                group.late_activation = False

            code: Optional[int] = None
            if flight.loadout.has_weapon_of_type(WeaponTypeEnum.TGP) and player:
                code = self.laser_code_registry.get_next_laser_code()
            laser_codes.append(code)

            # Set up F-14 Client to have pre-stored alignment
            if unit_type is F_14B:
                unit.set_property(F_14B.Properties.INSAlignmentStored.id, True)

        group.points[0].tasks.append(
            OptReactOnThreat(OptReactOnThreat.Values.EvadeFire)
        )

        if (
            flight.flight_type == FlightType.AEWC
            or flight.flight_type == FlightType.REFUELING
        ):
            channel = self.radio_registry.alloc_uhf()
        else:
            channel = flight.unit_type.alloc_flight_radio(self.radio_registry)

        try:
            group.set_frequency(channel.mhz)
        except TypeError:
            # TODO: Remote try/except when pydcs bug is fixed.
            # https://github.com/pydcs/dcs/issues/175
            # pydcs now emits an error when attempting to set a preset channel for an
            # aircraft that doesn't support them. We're not choosing to set a preset
            # here, we're just trying to set the AI's frequency. pydcs automatically
            # tries to set channel 1 when it does that and doesn't suppress this new
            # error.
            pass

        divert = None
        if flight.divert is not None:
            divert = flight.divert.active_runway(self.game.conditions, dynamic_runways)

        self.flights.append(
            FlightData(
                package=package,
                aircraft_type=flight.unit_type,
                flight_type=flight.flight_type,
                units=group.units,
                size=len(group.units),
                friendly=flight.from_cp.captured,
                # Set later.
                departure_delay=timedelta(),
                departure=flight.departure.active_runway(
                    self.game.conditions, dynamic_runways
                ),
                arrival=flight.arrival.active_runway(
                    self.game.conditions, dynamic_runways
                ),
                divert=divert,
                # Waypoints are added later, after they've had their TOTs set.
                waypoints=[],
                intra_flight_channel=channel,
                bingo_fuel=flight.flight_plan.bingo_fuel,
                joker_fuel=flight.flight_plan.joker_fuel,
                custom_name=flight.custom_name,
                laser_codes=laser_codes,
            )
        )

        # Special case so Su 33 and C101 can take off
        if unit_type in [Su_33, C_101EB, C_101CC]:
            self.set_reduced_fuel(flight, group, unit_type)

        if isinstance(flight.flight_plan, AwacsFlightPlan):
            callsign = callsign_for_support_unit(group)

            self.air_support.awacs.append(
                AwacsInfo(
                    group_name=str(group.name),
                    callsign=callsign,
                    freq=channel,
                    depature_location=flight.departure.name,
                    end_time=flight.flight_plan.mission_departure_time,
                    start_time=flight.flight_plan.mission_start_time,
                    blue=flight.departure.captured,
                )
            )

        if isinstance(flight.flight_plan, RefuelingFlightPlan):
            callsign = callsign_for_support_unit(group)

            tacan = self.tacan_registy.alloc_for_band(TacanBand.Y)
            self.air_support.tankers.append(
                TankerInfo(
                    group_name=str(group.name),
                    callsign=callsign,
                    variant=flight.unit_type.name,
                    freq=channel,
                    tacan=tacan,
                    start_time=flight.flight_plan.patrol_start_time,
                    end_time=flight.flight_plan.patrol_end_time,
                    blue=flight.departure.captured,
                )
            )

    def _generate_at_airport(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        airport: Airport,
    ) -> FlyingGroup[Any]:
        assert count > 0

        logging.info("airgen: {} for {} at {}".format(unit_type, side.id, airport))
        return self.m.flight_group_from_airport(
            country=side,
            name=name,
            aircraft_type=unit_type,
            airport=airport,
            maintask=None,
            start_type=self._start_type(start_type),
            group_size=count,
            parking_slots=None,
        )

    def _generate_inflight(
        self, name: str, side: Country, flight: Flight, origin: ControlPoint
    ) -> FlyingGroup[Any]:
        assert flight.count > 0
        at = origin.position

        alt_type = "RADIO"
        if isinstance(origin, OffMapSpawn):
            alt = flight.flight_plan.waypoints[0].alt
            alt_type = flight.flight_plan.waypoints[0].alt_type
        elif flight.unit_type in helicopters.helicopter_map.values():
            alt = WARM_START_HELI_ALT
        else:
            alt = WARM_START_ALTITUDE

        speed = GroundSpeed.for_flight(flight, alt)

        pos = Point(at.x + random.randint(100, 1000), at.y + random.randint(100, 1000))

        logging.info(
            "airgen: {} for {} at {} at {}".format(
                flight.unit_type, side.id, alt, int(speed.kph)
            )
        )
        group = self.m.flight_group(
            country=side,
            name=name,
            aircraft_type=flight.unit_type.dcs_unit_type,
            airport=None,
            position=pos,
            altitude=alt.meters,
            speed=speed.kph,
            maintask=None,
            group_size=flight.count,
        )

        group.points[0].alt_type = alt_type
        return group

    def _generate_at_group(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        at: Union[ShipGroup, StaticGroup],
    ) -> FlyingGroup[Any]:
        assert count > 0

        logging.info("airgen: {} for {} at unit {}".format(unit_type, side.id, at))
        return self.m.flight_group_from_unit(
            country=side,
            name=name,
            aircraft_type=unit_type,
            pad_group=at,
            maintask=None,
            start_type=self._start_type(start_type),
            group_size=count,
        )

    def _generate_at_cp_helipad(
        self,
        name: str,
        side: Country,
        unit_type: Type[FlyingType],
        count: int,
        start_type: str,
        cp: ControlPoint,
    ) -> FlyingGroup[Any]:
        assert count > 0

        logging.info(
            "airgen at cp's helipads : {} for {} at {}".format(
                unit_type, side.id, cp.name
            )
        )

        try:
            helipad = self.helipads[cp].pop()
        except IndexError as ex:
            raise RuntimeError(f"Not enough helipads available at {cp}") from ex

        group = self._generate_at_group(
            name=name,
            side=side,
            unit_type=unit_type,
            count=count,
            start_type=start_type,
            at=helipad,
        )

        # Note : A bit dirty, need better support in pydcs
        group.points[0].action = PointAction.FromGroundArea
        group.points[0].type = "TakeOffGround"
        group.units[0].heading = helipad.units[0].heading
        if start_type != "Cold":
            group.points[0].action = PointAction.FromGroundAreaHot
            group.points[0].type = "TakeOffGroundHot"

        for i in range(count - 1):
            try:
                helipad = self.helipads[cp].pop()
                group.units[1 + i].position = Point(helipad.x, helipad.y)
                group.units[1 + i].heading = helipad.units[0].heading
            except IndexError as ex:
                raise RuntimeError(f"Not enough helipads available at {cp}") from ex
        return group

    def _add_radio_waypoint(
        self,
        group: FlyingGroup[Any],
        position: Point,
        altitude: Distance,
        airspeed: int = 600,
    ) -> MovingPoint:
        point = group.add_waypoint(position, altitude.meters, airspeed)
        point.alt_type = "RADIO"
        return point

    @staticmethod
    def _at_position(at: Union[Point, ShipGroup, Type[Airport]]) -> Point:
        if isinstance(at, Point):
            return at
        elif isinstance(at, ShipGroup):
            return at.position
        elif issubclass(at, Airport):
            return at.position
        else:
            assert False

    def _setup_payload(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        for p in group.units:
            p.pylons.clear()

        loadout = flight.loadout
        if self.game.settings.restrict_weapons_by_date:
            loadout = loadout.degrade_for_date(flight.unit_type, self.game.date)

        for pylon_number, weapon in loadout.pylons.items():
            if weapon is None:
                continue
            pylon = Pylon.for_aircraft(flight.unit_type, pylon_number)
            pylon.equip(group, weapon)

    def clear_parking_slots(self) -> None:
        for cp in self.game.theater.controlpoints:
            for parking_slot in cp.parking_slots:
                parking_slot.unit_id = None

    def generate_flights(
        self,
        country: Country,
        ato: AirTaskingOrder,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:

        for package in ato.packages:
            if not package.flights:
                continue
            for flight in package.flights:
                logging.info(f"Generating flight: {flight.unit_type}")
                group = self.generate_planned_flight(flight.from_cp, country, flight)
                self.unit_map.add_aircraft(group, flight)
                self.setup_flight_group(group, package, flight, dynamic_runways)
                self.create_waypoints(group, package, flight)

    def spawn_unused_aircraft(
        self, player_country: Country, enemy_country: Country
    ) -> None:
        inventories = self.game.aircraft_inventory.inventories
        for control_point, inventory in inventories.items():
            if not isinstance(control_point, Airfield):
                continue

            faction = self.game.coalition_for(control_point.captured).faction
            if control_point.captured:
                country = player_country
            else:
                country = enemy_country

            for aircraft, available in inventory.all_aircraft:
                try:
                    self._spawn_unused_at(
                        control_point, country, faction, aircraft, available
                    )
                except NoParkingSlotError:
                    # If we run out of parking, stop spawning aircraft.
                    return

    def _spawn_unused_at(
        self,
        control_point: Airfield,
        country: Country,
        faction: Faction,
        aircraft: AircraftType,
        number: int,
    ) -> None:
        for _ in range(number):
            # Creating a flight even those this isn't a fragged mission lets us
            # reuse the existing debriefing code.
            # TODO: Special flight type?
            flight = Flight(
                Package(control_point),
                faction.country,
                self.game.air_wing_for(control_point.captured).squadron_for(aircraft),
                1,
                FlightType.BARCAP,
                "Cold",
                departure=control_point,
                arrival=control_point,
                divert=None,
            )

            group = self._generate_at_airport(
                name=namegen.next_aircraft_name(country, control_point.id, flight),
                side=country,
                unit_type=aircraft.dcs_unit_type,
                count=1,
                start_type="Cold",
                airport=control_point.airport,
            )

            if aircraft in faction.liveries_overrides:
                livery = random.choice(faction.liveries_overrides[aircraft])
                for unit in group.units:
                    unit.livery_id = livery

            group.uncontrolled = True
            self.unit_map.add_aircraft(group, flight)

    def set_activation_time(
        self, flight: Flight, group: FlyingGroup[Any], delay: timedelta
    ) -> None:
        # Note: Late activation causes the waypoint TOTs to look *weird* in the
        # mission editor. Waypoint times will be relative to the group
        # activation time rather than in absolute local time. A flight delayed
        # until 09:10 when the overall mission start time is 09:00, with a join
        # time of 09:30 will show the join time as 00:30, not 09:30.
        group.late_activation = True

        activation_trigger = TriggerOnce(
            Event.NoEvent, f"FlightLateActivationTrigger{group.id}"
        )
        activation_trigger.add_condition(TimeAfter(seconds=int(delay.total_seconds())))

        self.prevent_spawn_at_hostile_airbase(flight, activation_trigger)
        activation_trigger.add_action(ActivateGroup(group.id))
        self.m.triggerrules.triggers.append(activation_trigger)

    def set_startup_time(
        self, flight: Flight, group: FlyingGroup[Any], delay: timedelta
    ) -> None:
        # Uncontrolled causes the AI unit to spawn, but not begin startup.
        group.uncontrolled = True

        activation_trigger = TriggerOnce(Event.NoEvent, f"FlightStartTrigger{group.id}")
        activation_trigger.add_condition(TimeAfter(seconds=int(delay.total_seconds())))

        self.prevent_spawn_at_hostile_airbase(flight, activation_trigger)
        group.add_trigger_action(StartCommand())
        activation_trigger.add_action(AITaskPush(group.id, len(group.tasks)))
        self.m.triggerrules.triggers.append(activation_trigger)

    def prevent_spawn_at_hostile_airbase(
        self, flight: Flight, trigger: TriggerRule
    ) -> None:
        # Prevent delayed flights from spawning at airbases if they were
        # captured before they've spawned.
        if flight.from_cp.cptype != ControlPointType.AIRBASE:
            return

        coalition = self.game.coalition_for(flight.departure.captured).coalition_id
        trigger.add_condition(CoalitionHasAirdrome(coalition, flight.from_cp.id))

    def generate_planned_flight(
        self, cp: ControlPoint, country: Country, flight: Flight
    ) -> FlyingGroup[Any]:
        name = namegen.next_aircraft_name(country, cp.id, flight)
        group: FlyingGroup[Any]
        try:
            if flight.start_type == "In Flight":
                group = self._generate_inflight(
                    name=name, side=country, flight=flight, origin=cp
                )
                return group
            elif isinstance(cp, NavalControlPoint):
                group_name = cp.get_carrier_group_name()
                carrier_group = self.m.find_group(group_name)
                if not isinstance(carrier_group, ShipGroup):
                    raise RuntimeError(
                        f"Carrier group {carrier_group} is a "
                        "{carrier_group.__class__.__name__}, expected a ShipGroup"
                    )
                return self._generate_at_group(
                    name=name,
                    side=country,
                    unit_type=flight.unit_type.dcs_unit_type,
                    count=flight.count,
                    start_type=flight.start_type,
                    at=carrier_group,
                )
            else:
                # If the flight is an helicopter flight, then prioritize dedicated helipads
                if flight.unit_type.helicopter:
                    return self._generate_at_cp_helipad(
                        name=name,
                        side=country,
                        unit_type=flight.unit_type.dcs_unit_type,
                        count=flight.count,
                        start_type=flight.start_type,
                        cp=cp,
                    )

                if not isinstance(cp, Airfield):
                    raise RuntimeError(
                        f"Attempted to spawn at airfield for non-airfield {cp}"
                    )
                return self._generate_at_airport(
                    name=name,
                    side=country,
                    unit_type=flight.unit_type.dcs_unit_type,
                    count=flight.count,
                    start_type=flight.start_type,
                    airport=cp.airport,
                )
        except Exception as e:
            # Generated when there is no place on Runway or on Parking Slots
            logging.error(e)
            logging.warning(
                "No room on runway or parking slots. Starting from the air."
            )
            flight.start_type = "In Flight"
            group = self._generate_inflight(
                name=name, side=country, flight=flight, origin=cp
            )
            group.points[0].alt = 1500
            return group

    @staticmethod
    def set_reduced_fuel(
        flight: Flight, group: FlyingGroup[Any], unit_type: Type[FlyingType]
    ) -> None:
        if unit_type is Su_33:
            for unit in group.units:
                if flight.flight_type is not CAP:
                    unit.fuel = Su_33.fuel_max / 2.2
                else:
                    unit.fuel = Su_33.fuel_max * 0.8
        elif unit_type in [C_101EB, C_101CC]:
            for unit in group.units:
                unit.fuel = unit_type.fuel_max * 0.5
        else:
            raise RuntimeError(f"No reduced fuel case for type {unit_type}")

    @staticmethod
    def flight_always_keeps_gun(flight: Flight) -> bool:
        # Never take bullets from players. They're smart enough to know when to use it
        # and when to RTB.
        if flight.client_count > 0:
            return True

        return flight.unit_type.always_keeps_gun

    def configure_behavior(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        react_on_threat: Optional[OptReactOnThreat.Values] = None,
        roe: Optional[int] = None,
        rtb_winchester: Optional[OptRTBOnOutOfAmmo.Values] = None,
        restrict_jettison: Optional[bool] = None,
        mission_uses_gun: bool = True,
    ) -> None:
        group.points[0].tasks.clear()
        if react_on_threat is not None:
            group.points[0].tasks.append(OptReactOnThreat(react_on_threat))
        if roe is not None:
            group.points[0].tasks.append(OptROE(roe))
        if restrict_jettison is not None:
            group.points[0].tasks.append(OptRestrictJettison(restrict_jettison))
        if rtb_winchester is not None:
            group.points[0].tasks.append(OptRTBOnOutOfAmmo(rtb_winchester))

        # Confiscate the bullets of AI missions that do not rely on the gun. There is no
        # "all but gun" RTB winchester option, so air to ground missions with mixed
        # weapon types will insist on using all of their bullets after running out of
        # missiles and bombs. Take away their bullets so they don't strafe a Tor.
        #
        # Exceptions are made for player flights and for airframes where the gun is
        # essential like the A-10 or warbirds.
        if not mission_uses_gun and not self.flight_always_keeps_gun(flight):
            for unit in group.units:
                unit.gun = 0

        group.points[0].tasks.append(OptRTBOnBingoFuel(True))
        # Do not restrict afterburner.
        # https://forums.eagle.ru/forum/english/digital-combat-simulator/dcs-world-2-5/bugs-and-problems-ai/ai-ad/7121294-ai-stuck-at-high-aoa-after-making-sharp-turn-if-afterburner-is-restricted

    @staticmethod
    def configure_eplrs(group: FlyingGroup[Any], flight: Flight) -> None:
        if flight.unit_type.eplrs_capable:
            group.points[0].tasks.append(EPLRS(group.id))

    def configure_cap(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = CAP.name
        self._setup_group(group, package, flight, dynamic_runways)

        if not flight.unit_type.gunfighter:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_sweep(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = FighterSweep.name
        self._setup_group(group, package, flight, dynamic_runways)

        if not flight.unit_type.gunfighter:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_cas(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.Unguided,
            restrict_jettison=True,
        )

    def configure_dead(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # Only CAS and SEAD are capable of the Attack Group task. SEAD is arguably more
        # appropriate but it has an extremely limited list of capable aircraft, whereas
        # CAS has a much wider selection of units.
        #
        # Note that the only effect that the DCS task type has is in determining which
        # waypoint actions the group may perform.
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.All,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_sead(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # CAS is able to perform all the same tasks as SEAD using a superset of the
        # available aircraft, and F-14s are not able to be SEAD despite having TALDs.
        # https://forums.eagle.ru/topic/272112-cannot-assign-f-14-to-sead/
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            # ASM includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.ASM,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_strike(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = GroundAttack.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_anti_ship(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = AntishipStrike.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_runway_attack(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = RunwayAttack.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_oca_strike(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
        )

    def configure_awacs(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = AWACS.name

        if not isinstance(flight.flight_plan, AwacsFlightPlan):
            logging.error(
                f"Cannot configure AEW&C tasks for {flight} because it does not have an AEW&C flight plan."
            )
            return

        self._setup_group(group, package, flight, dynamic_runways)

        # Awacs task action
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

        group.points[0].tasks.append(AWACSTaskAction())

    def configure_refueling(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = Refueling.name

        if not isinstance(flight.flight_plan, RefuelingFlightPlan):
            logging.error(
                f"Cannot configure racetrack refueling tasks for {flight} because it "
                "does not have an racetrack refueling flight plan."
            )
            return

        self._setup_group(group, package, flight, dynamic_runways)

        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_escort(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # Escort groups are actually given the CAP task so they can perform the
        # Search Then Engage task, which we have to use instead of the Escort
        # task for the reasons explained in JoinPointBuilder.
        group.task = CAP.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight, group, roe=OptROE.Values.OpenFire, restrict_jettison=True
        )

    def configure_sead_escort(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        # CAS is able to perform all the same tasks as SEAD using a superset of the
        # available aircraft, and F-14s are not able to be SEAD despite having TALDs.
        # https://forums.eagle.ru/topic/272112-cannot-assign-f-14-to-sead/
        group.task = CAS.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            roe=OptROE.Values.OpenFire,
            # ASM includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.ASM,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_transport(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        group.task = Transport.name
        self._setup_group(group, package, flight, dynamic_runways)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_unknown_task(self, group: FlyingGroup[Any], flight: Flight) -> None:
        logging.error(f"Unhandled flight type: {flight.flight_type}")
        self.configure_behavior(flight, group)

    def setup_flight_group(
        self,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        flight_type = flight.flight_type
        if flight_type in [
            FlightType.BARCAP,
            FlightType.TARCAP,
            FlightType.INTERCEPTION,
        ]:
            self.configure_cap(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.SWEEP:
            self.configure_sweep(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.AEWC:
            self.configure_awacs(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.REFUELING:
            self.configure_refueling(group, package, flight, dynamic_runways)
        elif flight_type in [FlightType.CAS, FlightType.BAI]:
            self.configure_cas(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.DEAD:
            self.configure_dead(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.SEAD:
            self.configure_sead(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.SEAD_ESCORT:
            self.configure_sead_escort(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.STRIKE:
            self.configure_strike(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.ANTISHIP:
            self.configure_anti_ship(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.ESCORT:
            self.configure_escort(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.OCA_RUNWAY:
            self.configure_runway_attack(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.OCA_AIRCRAFT:
            self.configure_oca_strike(group, package, flight, dynamic_runways)
        elif flight_type == FlightType.TRANSPORT:
            self.configure_transport(group, package, flight, dynamic_runways)
        else:
            self.configure_unknown_task(group, flight)

        self.configure_eplrs(group, flight)

    def create_waypoints(
        self, group: FlyingGroup[Any], package: Package, flight: Flight
    ) -> None:

        for waypoint in flight.points:
            waypoint.tot = None

        takeoff_point = FlightWaypoint.from_pydcs(group.points[0], flight.from_cp)
        self.set_takeoff_time(takeoff_point, package, flight, group)

        filtered_points = []  # type: List[FlightWaypoint]

        for point in flight.points:
            if point.only_for_player and not flight.client_count:
                continue
            filtered_points.append(point)
        # Only add 1 target waypoint for Viggens.  This only affects player flights,
        # the Viggen can't have more than 9 waypoints which leaves us with two target point
        # under the current flight plans.
        # TODO: Make this smarter, it currently selects a random unit in the group for target,
        # this could be updated to make it pick the "best" two targets in the group.
        if flight.unit_type.dcs_unit_type is AJS37 and flight.client_count:
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
            PydcsWaypointBuilder.for_waypoint(
                point, group, package, flight, self.m, self.air_support
            ).build()

        # Set here rather than when the FlightData is created so they waypoints
        # have their TOTs and fuel minimums set. Once we're more confident in our fuel
        # estimation ability the minimum fuel amounts will be calculated during flight
        # plan construction, but for now it's only used by the kneeboard so is generated
        # late.
        waypoints = [takeoff_point] + flight.points
        self._estimate_min_fuel_for(flight, waypoints)
        self.flights[-1].waypoints = waypoints

    @staticmethod
    def _estimate_min_fuel_for(flight: Flight, waypoints: list[FlightWaypoint]) -> None:
        if flight.unit_type.fuel_consumption is None:
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

        consumption = flight.unit_type.fuel_consumption
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

    def should_delay_flight(self, flight: Flight, start_time: timedelta) -> bool:
        if start_time.total_seconds() <= 0:
            return False

        if not flight.client_count:
            return True

        if start_time < timedelta(minutes=10):
            # Don't bother delaying client flights with short start delays. Much
            # more than ten minutes starts to eat into fuel a bit more
            # (espeicially for something fuel limited like a Harrier).
            return False

        return not self.settings.never_delay_player_flights

    def set_takeoff_time(
        self,
        waypoint: FlightWaypoint,
        package: Package,
        flight: Flight,
        group: FlyingGroup[Any],
    ) -> None:
        estimator = TotEstimator(package)
        start_time = estimator.mission_start_time(flight)

        if self.should_delay_flight(flight, start_time):
            if self.should_activate_late(flight):
                # Late activation causes the aircraft to not be spawned
                # until triggered.
                self.set_activation_time(flight, group, start_time)
            elif flight.start_type == "Cold":
                # Setting the start time causes the AI to wait until the
                # specified time to begin their startup sequence.
                self.set_startup_time(flight, group, start_time)

        # And setting *our* waypoint TOT causes the takeoff time to show up in
        # the player's kneeboard.
        waypoint.tot = flight.flight_plan.takeoff_time()
        # And finally assign it to the FlightData info so it shows correctly in
        # the briefing.
        self.flights[-1].departure_delay = start_time

    @staticmethod
    def should_activate_late(flight: Flight) -> bool:
        if flight.start_type != "Cold":
            # Avoid spawning aircraft in the air or on the runway until it's
            # time for their mission. Also avoid burning through gas spawning
            # hot aircraft hours before their takeoff time.
            return True

        if flight.from_cp.is_fleet:
            # Carrier spawns will crowd the carrier deck, especially without
            # super carrier.
            # TODO: Is there enough parking on the supercarrier?
            return True

        return False


class PydcsWaypointBuilder:
    def __init__(
        self,
        waypoint: FlightWaypoint,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        mission: Mission,
        air_support: AirSupport,
    ) -> None:
        self.waypoint = waypoint
        self.group = group
        self.package = package
        self.flight = flight
        self.mission = mission
        self.air_support = air_support

    def build(self) -> MovingPoint:
        waypoint = self.group.add_waypoint(
            Point(self.waypoint.x, self.waypoint.y),
            self.waypoint.alt.meters,
            name=self.waypoint.name,
        )

        if self.waypoint.flyover:
            waypoint.action = PointAction.FlyOverPoint
            # It seems we need to leave waypoint.type exactly as it is even
            # though it's set to "Turning Point". If I set this to "Fly Over
            # Point" and then save the mission in the ME DCS resets it.

        waypoint.alt_type = self.waypoint.alt_type
        tot = self.flight.flight_plan.tot_for_waypoint(self.waypoint)
        if tot is not None:
            self.set_waypoint_tot(waypoint, tot)
        return waypoint

    def set_waypoint_tot(self, waypoint: MovingPoint, tot: timedelta) -> None:
        self.waypoint.tot = tot
        if not self._viggen_client_tot():
            waypoint.ETA = int(tot.total_seconds())
            waypoint.ETA_locked = True
            waypoint.speed_locked = False

    @classmethod
    def for_waypoint(
        cls,
        waypoint: FlightWaypoint,
        group: FlyingGroup[Any],
        package: Package,
        flight: Flight,
        mission: Mission,
        air_support: AirSupport,
    ) -> PydcsWaypointBuilder:
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
        return builder(waypoint, group, package, flight, mission, air_support)

    def _viggen_client_tot(self) -> bool:
        """Viggen player aircraft consider any waypoint with a TOT set to be a target ("M") waypoint.
        If the flight is a player controlled Viggen flight, no TOT should be set on any waypoint except actual target waypoints.
        """
        if (
            self.flight.client_count > 0
            and self.flight.unit_type.dcs_unit_type == AJS37
        ) and (self.waypoint.waypoint_type not in TARGET_WAYPOINTS):
            return True
        else:
            return False

    def register_special_waypoints(
        self, targets: Iterable[Union[MissionTarget, Unit]]
    ) -> None:
        """Create special target waypoints for various aircraft"""
        for i, t in enumerate(targets):
            if self.group.units[0].unit_type == JF_17 and i < 4:
                self.group.add_nav_target_point(t.position, "PP" + str(i + 1))
            if self.group.units[0].unit_type == F_14B and i == 0:
                self.group.add_nav_target_point(t.position, "ST")


class DefaultWaypointBuilder(PydcsWaypointBuilder):
    pass


class HoldPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        loiter = ControlledTask(
            OrbitAction(altitude=waypoint.alt, pattern=OrbitAction.OrbitPattern.Circle)
        )
        if not isinstance(self.flight.flight_plan, LoiterFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot configure hold for for {self.flight} because "
                f"{flight_plan_type} does not define a push time. AI will push "
                "immediately and may flight unsuitable speeds."
            )
            return waypoint
        push_time = self.flight.flight_plan.push_time
        self.waypoint.departure_time = push_time
        loiter.stop_after_time(int(push_time.total_seconds()))
        waypoint.add_task(loiter)
        return waypoint


class BaiIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        # TODO: Add common "UnitGroupTarget" base type.
        group_names = []
        target = self.package.target
        if isinstance(target, TheaterGroundObject):
            for group in target.groups:
                group_names.append(group.name)
        elif isinstance(target, MultiGroupTransport):
            group_names.append(target.name)
        else:
            logging.error(
                "Unexpected target type for BAI mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        for group_name in group_names:
            group = self.mission.find_group(group_name)
            if group is None:
                logging.error("Could not find group for BAI mission %s", group_name)
                continue

            task = AttackGroup(group.id, weapon_type=WeaponType.Auto)
            task.params["attackQtyLimit"] = False
            task.params["directionEnabled"] = False
            task.params["altitudeEnabled"] = False
            task.params["groupAttack"] = True
            waypoint.tasks.append(task)
        return waypoint


class CasIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        if isinstance(self.flight.flight_plan, CasFlightPlan):
            waypoint.add_task(
                EngageTargetsInZone(
                    position=self.flight.flight_plan.target.position,
                    radius=int(self.flight.flight_plan.engagement_distance.meters),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )
        else:
            logging.error("No CAS waypoint found. Falling back to search and engage")
            waypoint.add_task(
                EngageTargets(
                    max_distance=int(nautical_miles(10).meters),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )
        return waypoint


class DeadIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        self.register_special_waypoints(self.waypoint.targets)

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for DEAD mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        for group in target.groups:
            miz_group = self.mission.find_group(group.name)
            if miz_group is None:
                logging.error(f"Could not find group for DEAD mission {group.name}")
                continue

            task = AttackGroup(miz_group.id, weapon_type=WeaponType.Auto)
            task.params["expend"] = "All"
            task.params["attackQtyLimit"] = False
            task.params["directionEnabled"] = False
            task.params["altitudeEnabled"] = False
            task.params["groupAttack"] = True
            waypoint.tasks.append(task)
        return waypoint


class OcaAircraftIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        target = self.package.target
        if not isinstance(target, Airfield):
            logging.error(
                "Unexpected target type for OCA Strike mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        task = EngageTargetsInZone(
            position=target.position,
            # Al Dhafra is 4 nm across at most. Add a little wiggle room in case
            # the airport position from DCS is not centered.
            radius=int(nautical_miles(3).meters),
            targets=[Targets.All.Air],
        )
        task.params["attackQtyLimit"] = False
        task.params["directionEnabled"] = False
        task.params["altitudeEnabled"] = False
        task.params["groupAttack"] = True
        waypoint.tasks.append(task)
        return waypoint


class OcaRunwayIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        target = self.package.target
        if not isinstance(target, Airfield):
            logging.error(
                "Unexpected target type for runway bombing mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        waypoint.tasks.append(
            BombingRunway(airport_id=target.airport.id, group_attack=True)
        )
        return waypoint


class SeadIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        self.register_special_waypoints(self.waypoint.targets)

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for SEAD mission: %s",
                target.__class__.__name__,
            )
            return waypoint

        for group in target.groups:
            miz_group = self.mission.find_group(group.name)
            if miz_group is None:
                logging.error(f"Could not find group for SEAD mission {group.name}")
                continue

            task = AttackGroup(miz_group.id, weapon_type=WeaponType.Guided)
            task.params["expend"] = "All"
            task.params["attackQtyLimit"] = False
            task.params["directionEnabled"] = False
            task.params["altitudeEnabled"] = False
            task.params["groupAttack"] = True
            waypoint.tasks.append(task)
        return waypoint


class StrikeIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        if self.group.units[0].unit_type in [B_17G, B_52H, Tu_22M3]:
            return self.build_bombing()
        else:
            return self.build_strike()

    def build_bombing(self) -> MovingPoint:
        waypoint = super().build()

        targets = self.waypoint.targets
        if not targets:
            return waypoint

        center = Point(0, 0)
        for target in targets:
            center.x += target.position.x
            center.y += target.position.y
        center.x /= len(targets)
        center.y /= len(targets)
        bombing = Bombing(center, weapon_type=WeaponType.Bombs)
        bombing.params["expend"] = "All"
        bombing.params["attackQtyLimit"] = False
        bombing.params["directionEnabled"] = False
        bombing.params["altitudeEnabled"] = False
        bombing.params["groupAttack"] = True
        waypoint.tasks.append(bombing)
        return waypoint

    def build_strike(self) -> MovingPoint:
        waypoint = super().build()
        for target in self.waypoint.targets:
            bombing = Bombing(target.position, weapon_type=WeaponType.Auto)
            # If there is only one target, drop all ordnance in one pass.
            if len(self.waypoint.targets) == 1:
                bombing.params["expend"] = "All"
            bombing.params["groupAttack"] = True
            waypoint.tasks.append(bombing)

            # Register special waypoints
            self.register_special_waypoints(self.waypoint.targets)
        return waypoint


class SweepIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, SweepFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create sweep for {self.flight} because "
                f"{flight_plan_type} is not a sweep flight plan."
            )
            return waypoint

        waypoint.tasks.append(
            EngageTargets(
                max_distance=int(nautical_miles(50).meters),
                targets=[
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )
        )

        return waypoint


class JoinPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        if self.flight.flight_type == FlightType.ESCORT:
            self.configure_escort_tasks(
                waypoint,
                [
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )
        elif self.flight.flight_type == FlightType.SEAD_ESCORT:
            self.configure_escort_tasks(
                waypoint, [Targets.All.GroundUnits.AirDefence.AAA.SAMRelated]
            )
        return waypoint

    @staticmethod
    def configure_escort_tasks(
        waypoint: MovingPoint, target_types: List[Type[TargetType]]
    ) -> None:
        # Ideally we would use the escort mission type and escort task to have
        # the AI automatically but the AI only escorts AI flights while they are
        # traveling between waypoints. When an AI flight performs an attack
        # (such as attacking the mission target), AI escorts wander aimlessly
        # until the escorted group resumes its flight plan.
        #
        # As such, we instead use the Search Then Engage task, which is an
        # enroute task that causes the AI to follow their flight plan and engage
        # enemies of the set type within a certain distance. The downside to
        # this approach is that AI escorts are no longer related to the group
        # they are escorting, aside from the fact that they fly a similar flight
        # plan at the same time. With Escort, the escorts will follow the
        # escorted group out of the area. The strike element may or may not fly
        # directly over the target, and they may or may not require multiple
        # attack runs. For the escort flight we must just assume a flight plan
        # for the escort to fly. If the strike flight doesn't need to overfly
        # the target, the escorts are needlessly going in harms way. If the
        # strike flight needs multiple passes, the escorts may leave before the
        # escorted aircraft do.
        #
        # Another possible option would be to use Search Then Engage for join ->
        # ingress and egress -> split, but use a Search Then Engage in Zone task
        # for the target area that is set to end on a flag flip that occurs when
        # the strike aircraft finish their attack task.
        #
        # https://forums.eagle.ru/topic/251798-options-for-alternate-ai-escort-behavior
        waypoint.add_task(
            ControlledTask(
                EngageTargets(
                    # TODO: From doctrine.
                    max_distance=int(nautical_miles(30).meters),
                    targets=target_types,
                )
            )
        )

        # We could set this task to end at the split point. pydcs doesn't
        # currently support that task end condition though, and we don't really
        # need it.


class LandingPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.type = "Land"
        waypoint.action = PointAction.Landing
        return waypoint


class CargoStopBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.type = "LandingReFuAr"
        waypoint.action = PointAction.LandingReFuAr
        waypoint.landing_refuel_rearm_time = 2  # Minutes.
        return waypoint


class RaceTrackBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        flight_plan = self.flight.flight_plan

        if not isinstance(flight_plan, PatrollingFlightPlan):
            flight_plan_type = flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a patrol."
            )
            return waypoint

        # NB: It's important that the engage task comes before the orbit task.
        # Though they're on the same waypoint, if the orbit task comes first it
        # is their first priority and they will not engage any targets because
        # they're fully focused on orbiting. If the STE task is first, they will
        # engage targets if available and orbit if they find nothing to shoot.
        if self.flight.flight_type is FlightType.REFUELING:
            self.configure_refueling_actions(waypoint)

        # TODO: Move the properties of this task into the flight plan?
        # CAP is the only current user of this so it's not a big deal, but might
        # be good to make this usable for things like BAI when we add that
        # later.
        cap_types = {FlightType.BARCAP, FlightType.TARCAP}
        if self.flight.flight_type in cap_types:
            engagement_distance = int(flight_plan.engagement_distance.meters)
            waypoint.tasks.append(
                EngageTargets(
                    max_distance=engagement_distance, targets=[Targets.All.Air]
                )
            )

        # TODO: Set orbit speeds for all race tracks and remove this special case.
        if isinstance(flight_plan, RefuelingFlightPlan):
            orbit = OrbitAction(
                altitude=waypoint.alt,
                pattern=OrbitAction.OrbitPattern.RaceTrack,
                speed=int(flight_plan.patrol_speed.kph),
            )
        else:
            orbit = OrbitAction(
                altitude=waypoint.alt, pattern=OrbitAction.OrbitPattern.RaceTrack
            )

        racetrack = ControlledTask(orbit)
        self.set_waypoint_tot(waypoint, flight_plan.patrol_start_time)
        racetrack.stop_after_time(int(flight_plan.patrol_end_time.total_seconds()))
        waypoint.add_task(racetrack)

        return waypoint

    def configure_refueling_actions(self, waypoint: MovingPoint) -> None:
        waypoint.add_task(Tanker())

        if self.flight.unit_type.dcs_unit_type.tacan:
            tanker_info = self.air_support.tankers[-1]
            tacan = tanker_info.tacan
            tacan_callsign = {
                "Texaco": "TEX",
                "Arco": "ARC",
                "Shell": "SHL",
            }.get(tanker_info.callsign)

            waypoint.add_task(
                ActivateBeaconCommand(
                    tacan.number,
                    tacan.band.value,
                    tacan_callsign,
                    bearing=True,
                    unit_id=self.group.units[0].id,
                    aa=True,
                )
            )


class RaceTrackEndBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a patrol."
            )
            return waypoint

        self.waypoint.departure_time = self.flight.flight_plan.patrol_end_time
        return waypoint
