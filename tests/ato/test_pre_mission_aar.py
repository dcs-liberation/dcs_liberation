from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast

from dcs import Point
from dcs.point import MovingPoint
from dcs.terrain import Caucasus

from game.ato import FlightWaypoint
from game.ato.flightplans.cas import CasFlightPlan, CasLayout
from game.ato.flightplans.flightplanbuildertypes import FlightPlanBuilderTypes
from game.ato.flightplans.packagerefueling import PackageRefuelingFlightPlan
from game.ato.flightplans.patrolling import PatrollingLayout
from game.ato.flightplans.formationattack import FormationAttackLayout
from game.ato.flightplans.sweep import SweepFlightPlan, SweepLayout
from game.ato.flightplans.tarcap import TarCapFlightPlan, TarCapLayout
from game.ato.flightplans.theaterrefueling import TheaterRefuelingFlightPlan
from game.ato.flight import Flight
from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.package import Package
from game.ato.starttype import StartType
from game.flightplan.waypointactions.hold import Hold
from game.missiongenerator.aircraft.waypoints.premissionaar import PreMissionAarBuilder
from game.missiongenerator.aircraft.waypoints.racetrack import RaceTrackBuilder
from game.missiongenerator.missiondata import TankerInfo
from game.radio.radios import MHz
from game.radio.tacan import TacanBand, TacanChannel
from game.settings.settings import Settings
from game.theater.frontline import FrontLine
from game.utils import feet, kph
from qt_ui.models import PackageModel


class FakeDcsWaypoint:
    def __init__(self) -> None:
        self.tasks: list[Any] = []

    def add_task(self, task: Any) -> None:
        self.tasks.append(task)


def waypoint(
    name: str, waypoint_type: FlightWaypointType = FlightWaypointType.NAV
) -> FlightWaypoint:
    return FlightWaypoint(name, waypoint_type, Point(0, 0, Caucasus()), feet(20000))


def fake_flight(package: Any) -> Any:
    return SimpleNamespace(
        package=package,
        coalition=SimpleNamespace(
            game=SimpleNamespace(
                settings=SimpleNamespace(
                    pre_mission_aar_hold_duration=timedelta(minutes=15)
                )
            )
        ),
        squadron=SimpleNamespace(aircraft=SimpleNamespace(cruise_speed=kph(400))),
        unit_type=SimpleNamespace(patrol_speed=kph(400)),
    )


def test_sweep_pre_mission_aar_is_before_sweep_start() -> None:
    package = SimpleNamespace(time_over_target=datetime(2026, 8, 21, 12))
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    layout = SweepLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        hold=waypoint("HOLD", FlightWaypointType.LOITER),
        nav_to=[],
        pre_refuel=pre_refuel,
        nav_from_pre_refuel=[],
        sweep_start=waypoint("SWEEP START"),
        sweep_end=waypoint("SWEEP END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )

    plan = SweepFlightPlan(cast(Any, fake_flight(package)), layout)

    assert [w.name for w in plan.waypoints] == [
        "TAKEOFF",
        "HOLD",
        "PRE-REFUEL",
        "SWEEP START",
        "SWEEP END",
        "LANDING",
        "BULLSEYE",
    ]


def test_tarcap_pre_mission_aar_is_before_patrol_start_and_return_refuel_remains() -> (
    None
):
    package = SimpleNamespace(time_over_target=datetime(2026, 8, 21, 12))
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    return_refuel = waypoint("REFUEL", FlightWaypointType.REFUEL)
    layout = TarCapLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        pre_refuel=pre_refuel,
        nav_from_pre_refuel=[],
        refuel=return_refuel,
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )

    plan = TarCapFlightPlan(cast(Any, fake_flight(package)), layout)

    assert [w.name for w in plan.waypoints] == [
        "TAKEOFF",
        "PRE-REFUEL",
        "PATROL START",
        "PATROL END",
        "REFUEL",
        "LANDING",
        "BULLSEYE",
    ]


def test_cas_pre_mission_aar_is_before_ingress() -> None:
    package = SimpleNamespace(time_over_target=datetime(2026, 8, 21, 12))
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    layout = CasLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        ingress=waypoint("INGRESS", FlightWaypointType.INGRESS_CAS),
        pre_refuel=pre_refuel,
        nav_from_pre_refuel=[],
        patrol_start=waypoint("FLOT START"),
        patrol_end=waypoint("FLOT END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )

    plan = CasFlightPlan(cast(Any, fake_flight(package)), layout)

    assert [w.name for w in plan.waypoints] == [
        "TAKEOFF",
        "PRE-REFUEL",
        "INGRESS",
        "FLOT START",
        "FLOT END",
        "LANDING",
        "BULLSEYE",
    ]


def test_refuel_task_precedes_hold_task() -> None:
    mission_start = datetime(2026, 8, 21, 12)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    pre_refuel.add_action(
        Hold(lambda: mission_start + timedelta(minutes=15), feet(20000), kph(400))
    )
    dcs_waypoint = FakeDcsWaypoint()
    builder: Any = object.__new__(PreMissionAarBuilder)
    builder.package = SimpleNamespace(has_flight_with_task=lambda task: True)
    builder.waypoint = pre_refuel
    builder.now = mission_start

    builder.add_tasks(cast(Any, dcs_waypoint))

    assert [task.id for task in dcs_waypoint.tasks] == [
        "Refueling",
        "ControlledTask",
    ]


def test_refuel_and_hold_are_serialized_on_pre_mission_aar_waypoint() -> None:
    mission_start = datetime(2026, 8, 21, 12)
    push_time = mission_start + timedelta(minutes=15)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    pre_refuel.add_action(Hold(lambda: push_time, feet(20000), kph(400)))
    dcs_waypoint = MovingPoint(pre_refuel.position)
    builder: Any = object.__new__(PreMissionAarBuilder)
    builder.package = SimpleNamespace(has_flight_with_task=lambda task: True)
    builder.waypoint = pre_refuel
    builder.now = mission_start

    builder.add_tasks(dcs_waypoint)

    tasks = dcs_waypoint.dict()["task"]["params"]["tasks"]
    assert tasks[1]["id"] == "Refueling"
    assert tasks[2]["id"] == "ControlledTask"
    assert tasks[2]["params"]["task"]["id"] == "Orbit"
    assert tasks[2]["params"]["task"]["params"]["pattern"] == "Circle"
    assert tasks[2]["params"]["stopCondition"]["time"] == 15 * 60


def test_refuel_task_is_added_for_external_tanker_package() -> None:
    dcs_waypoint = FakeDcsWaypoint()
    external_tanker_package = SimpleNamespace(
        has_flight_with_task=lambda task: task == FlightType.REFUELING
    )
    builder: Any = object.__new__(PreMissionAarBuilder)
    builder.package = SimpleNamespace(has_flight_with_task=lambda task: False)
    builder.flight = SimpleNamespace(
        coalition=SimpleNamespace(
            ato=SimpleNamespace(packages=[external_tanker_package])
        )
    )
    builder.waypoint = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    builder.now = datetime(2026, 8, 21, 12)

    builder.add_tasks(cast(Any, dcs_waypoint))

    assert [task.id for task in dcs_waypoint.tasks] == ["Refueling"]


def test_sweep_pre_mission_aar_hold_duration_is_respected() -> None:
    package = SimpleNamespace(time_over_target=datetime(2026, 8, 21, 12))
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    layout = SweepLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        hold=waypoint("HOLD", FlightWaypointType.LOITER),
        nav_to=[],
        pre_refuel=pre_refuel,
        nav_from_pre_refuel=[],
        sweep_start=waypoint("SWEEP START"),
        sweep_end=waypoint("SWEEP END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )

    plan = SweepFlightPlan(cast(Any, fake_flight(package)), layout)
    depart_time = plan.depart_time_for_waypoint(pre_refuel)
    arrival_time = plan.tot_for_waypoint(pre_refuel)

    assert depart_time is not None
    assert arrival_time is not None
    assert depart_time - arrival_time == timedelta(minutes=15)
    assert plan.depart_time_for_waypoint(layout.sweep_start) is None


def test_pre_mission_aar_waypoint_stores_departure_time_for_kneeboard() -> None:
    package = SimpleNamespace(time_over_target=datetime(2026, 8, 21, 12))
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    layout = SweepLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        hold=waypoint("HOLD", FlightWaypointType.LOITER),
        nav_to=[],
        pre_refuel=pre_refuel,
        nav_from_pre_refuel=[],
        sweep_start=waypoint("SWEEP START"),
        sweep_end=waypoint("SWEEP END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = SweepFlightPlan(cast(Any, fake_flight(package)), layout)

    pre_refuel.tot = plan.tot_for_waypoint(pre_refuel)
    pre_refuel.departure_time = plan.depart_time_for_waypoint(pre_refuel)

    assert pre_refuel.tot is not None
    assert pre_refuel.departure_time is not None
    assert pre_refuel.departure_time - pre_refuel.tot == timedelta(minutes=15)
    assert layout.sweep_start.departure_time is None


def test_package_tanker_starts_early_for_pre_mission_aar_and_keeps_recovery_window() -> (
    None
):
    native_start = datetime(2026, 8, 21, 12)
    package_tot = native_start - timedelta(minutes=10)
    recovery_duration = timedelta(minutes=20)
    pre_refuel_arrival = native_start - timedelta(minutes=30)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    outbound_flight_plan = SimpleNamespace(
        layout=SimpleNamespace(pre_refuel=pre_refuel),
        tot_for_waypoint=lambda waypoint: pre_refuel_arrival,
    )
    outbound_flight = SimpleNamespace(
        pre_mission_aar=True, flight_plan=outbound_flight_plan
    )
    tanker_flight = SimpleNamespace()
    package = SimpleNamespace(
        flights=[outbound_flight, tanker_flight],
        pre_mission_aar=True,
        time_over_target=package_tot,
    )
    tanker_flight.package = package

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return native_start

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return recovery_duration

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)
    tanker_start = pre_refuel_arrival - timedelta(minutes=5)

    assert plan.patrol_start_time == tanker_start
    assert (
        plan.patrol_start_time + plan.patrol_duration
        == native_start + recovery_duration
    )
    assert plan.tot_offset == timedelta()


def test_package_tanker_uses_native_offset_without_pre_mission_aar() -> None:
    native_start = datetime(2026, 8, 21, 12)
    recovery_duration = timedelta(minutes=20)
    tanker_flight = SimpleNamespace()
    package = SimpleNamespace(
        flights=[tanker_flight],
        pre_mission_aar=False,
        time_over_target=native_start,
    )
    tanker_flight.package = package

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return native_start

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return recovery_duration

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)

    assert plan.tot_offset == timedelta()


def test_disabling_asap_freezes_current_earliest_tot() -> None:
    now = datetime(2026, 8, 21, 12)

    class FakePackage:
        auto_asap = True
        time_over_target = now

        def set_tot_asap(self, current_time: datetime) -> None:
            self.time_over_target = current_time + timedelta(minutes=30)

        def clamp_tot_for_current_time(self, current_time: datetime) -> None:
            pass

    package = FakePackage()

    class PausedSim:
        def __enter__(self) -> None:
            return None

        def __exit__(self, *args: object) -> None:
            return None

    package_model = cast(Any, PackageModel.__new__(PackageModel))
    package_model.package = package
    package_model.game_model = SimpleNamespace(
        sim_controller=SimpleNamespace(
            current_time_in_sim=now,
            paused_sim=lambda: PausedSim(),
        )
    )
    package_model.tot_changed = SimpleNamespace(emit=lambda: None)
    package_model.layoutChanged = SimpleNamespace(emit=lambda: None)

    package_model.set_asap(False)

    assert package.auto_asap is False
    assert package.time_over_target == now + timedelta(minutes=30)


def test_theater_tanker_starts_for_external_pre_mission_aar_package() -> None:
    native_start = datetime(2026, 8, 21, 12)
    desired_duration = timedelta(minutes=60)
    pre_refuel_arrival = native_start - timedelta(minutes=30)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    outbound_flight_plan = SimpleNamespace(
        layout=SimpleNamespace(pre_refuel=pre_refuel),
        tot_for_waypoint=lambda waypoint: pre_refuel_arrival,
    )
    outbound_flight = SimpleNamespace(flight_plan=outbound_flight_plan)
    pre_refuel_package = SimpleNamespace(flights=[outbound_flight])
    tanker_flight = SimpleNamespace()
    tanker_package = SimpleNamespace(
        flights=[tanker_flight],
        pre_mission_aar=False,
        time_over_target=native_start,
    )
    coalition = SimpleNamespace(
        ato=SimpleNamespace(packages=[pre_refuel_package, tanker_package]),
        game=SimpleNamespace(
            settings=SimpleNamespace(desired_player_mission_duration=desired_duration)
        ),
    )
    tanker_flight.package = tanker_package
    tanker_flight.coalition = coalition
    tanker_flight.unit_type = SimpleNamespace(patrol_speed=kph(400))

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TheaterRefuelingFlightPlan(cast(Any, tanker_flight), layout)
    tanker_start = pre_refuel_arrival - timedelta(minutes=5)

    assert plan.patrol_start_time == tanker_start
    assert (
        plan.patrol_start_time + plan.patrol_duration
        == native_start + desired_duration + timedelta(minutes=30)
    )


def test_theater_tanker_created_before_pre_mission_aar_package_still_syncs() -> None:
    native_start = datetime(2026, 8, 21, 12)
    desired_duration = timedelta(minutes=60)
    pre_refuel_arrival = native_start - timedelta(minutes=30)
    tanker_flight = SimpleNamespace()
    tanker_package = SimpleNamespace(
        flights=[tanker_flight],
        pre_mission_aar=False,
        time_over_target=native_start,
    )
    coalition = SimpleNamespace(
        ato=SimpleNamespace(packages=[tanker_package]),
        game=SimpleNamespace(
            settings=SimpleNamespace(desired_player_mission_duration=desired_duration)
        ),
    )
    tanker_flight.package = tanker_package
    tanker_flight.coalition = coalition
    tanker_flight.unit_type = SimpleNamespace(patrol_speed=kph(400))

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TheaterRefuelingFlightPlan(cast(Any, tanker_flight), layout)
    assert plan.patrol_start_time == native_start

    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    outbound_flight_plan = SimpleNamespace(
        layout=SimpleNamespace(pre_refuel=pre_refuel),
        tot_for_waypoint=lambda waypoint: pre_refuel_arrival,
    )
    outbound_flight = SimpleNamespace(flight_plan=outbound_flight_plan)
    coalition.ato.packages.append(SimpleNamespace(flights=[outbound_flight]))

    assert plan.patrol_start_time == pre_refuel_arrival - timedelta(minutes=5)


def test_theater_tanker_pre_mission_aar_sync_does_not_recurse() -> None:
    native_start = datetime(2026, 8, 21, 12)
    desired_duration = timedelta(minutes=60)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    tanker_flight = SimpleNamespace()
    tanker_package = SimpleNamespace(
        flights=[tanker_flight],
        pre_mission_aar=False,
        time_over_target=native_start,
    )
    coalition = SimpleNamespace(
        ato=SimpleNamespace(packages=[tanker_package]),
        game=SimpleNamespace(
            settings=SimpleNamespace(desired_player_mission_duration=desired_duration)
        ),
    )
    tanker_flight.package = tanker_package
    tanker_flight.coalition = coalition
    tanker_flight.unit_type = SimpleNamespace(patrol_speed=kph(400))

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TheaterRefuelingFlightPlan(cast(Any, tanker_flight), layout)

    recursive_flight_plan = SimpleNamespace(
        layout=SimpleNamespace(pre_refuel=pre_refuel),
        tot_for_waypoint=lambda waypoint: plan.patrol_start_time,
    )
    coalition.ato.packages.append(
        SimpleNamespace(flights=[SimpleNamespace(flight_plan=recursive_flight_plan)])
    )

    assert plan.patrol_start_time == native_start


def test_package_tanker_uses_pre_refuel_waypoint_even_without_flight_flag() -> None:
    native_start = datetime(2026, 8, 21, 12)
    package_tot = native_start - timedelta(minutes=10)
    recovery_duration = timedelta(minutes=20)
    pre_refuel_arrival = native_start - timedelta(minutes=30)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    outbound_flight_plan = SimpleNamespace(
        layout=SimpleNamespace(pre_refuel=pre_refuel),
        tot_for_waypoint=lambda waypoint: pre_refuel_arrival,
    )
    outbound_flight = SimpleNamespace(flight_plan=outbound_flight_plan)
    tanker_flight = SimpleNamespace()
    package = SimpleNamespace(
        flights=[outbound_flight, tanker_flight],
        pre_mission_aar=True,
        time_over_target=package_tot,
    )
    tanker_flight.package = package

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return native_start

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return recovery_duration

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)

    assert plan.patrol_start_time == pre_refuel_arrival - timedelta(minutes=5)


def test_package_tanker_ignores_other_packages_pre_mission_aar() -> None:
    native_start = datetime(2026, 8, 21, 12)
    own_pre_refuel_arrival = native_start - timedelta(minutes=30)
    other_pre_refuel_arrival = native_start - timedelta(hours=1)
    own_pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    other_pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    own_flight = SimpleNamespace(
        flight_plan=SimpleNamespace(
            layout=SimpleNamespace(pre_refuel=own_pre_refuel),
            tot_for_waypoint=lambda waypoint: own_pre_refuel_arrival,
        )
    )
    other_flight = SimpleNamespace(
        flight_plan=SimpleNamespace(
            layout=SimpleNamespace(pre_refuel=other_pre_refuel),
            tot_for_waypoint=lambda waypoint: other_pre_refuel_arrival,
        )
    )
    tanker_flight = SimpleNamespace()
    package = SimpleNamespace(
        flights=[own_flight, tanker_flight],
        pre_mission_aar=True,
        time_over_target=native_start,
    )
    coalition = SimpleNamespace(
        ato=SimpleNamespace(
            packages=[
                SimpleNamespace(flights=[other_flight]),
                package,
            ]
        )
    )
    tanker_flight.package = package
    tanker_flight.coalition = coalition

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return native_start

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return timedelta(minutes=20)

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)

    assert plan.patrol_start_time == own_pre_refuel_arrival - timedelta(minutes=5)


def test_package_tanker_takeoff_uses_pre_mission_aar_station_time() -> None:
    package_tot = datetime(2026, 8, 21, 12)
    pre_refuel_arrival = package_tot - timedelta(minutes=30)
    station_time = pre_refuel_arrival - timedelta(minutes=5)
    travel_to_racetrack = timedelta(minutes=30)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    outbound_flight_plan = SimpleNamespace(
        layout=SimpleNamespace(pre_refuel=pre_refuel),
        tot_for_waypoint=lambda waypoint: pre_refuel_arrival,
    )
    outbound_flight = SimpleNamespace(flight_plan=outbound_flight_plan)
    tanker_flight = SimpleNamespace(
        start_type=StartType.RUNWAY,
        client_count=0,
        departure=SimpleNamespace(is_fleet=False),
    )
    package = SimpleNamespace(
        flights=[outbound_flight, tanker_flight],
        pre_mission_aar=True,
        time_over_target=package_tot,
    )
    tanker_flight.package = package

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return package_tot

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return timedelta(minutes=20)

        def travel_time_between_waypoints(
            self, a: FlightWaypoint, b: FlightWaypoint
        ) -> timedelta:
            if b == self.layout.patrol_start:
                return travel_to_racetrack
            return timedelta()

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)

    assert plan.tot == package_tot
    assert plan.patrol_start_time == station_time
    assert plan.takeoff_time() == station_time - travel_to_racetrack


def test_package_tanker_startup_uses_pre_mission_aar_station_time() -> None:
    package_tot = datetime(2026, 8, 21, 12)
    pre_refuel_arrival = package_tot - timedelta(minutes=30)
    station_time = pre_refuel_arrival - timedelta(minutes=5)
    travel_to_racetrack = timedelta(minutes=30)
    pre_refuel = waypoint("PRE-REFUEL", FlightWaypointType.PRE_MISSION_AAR)
    outbound_flight_plan = SimpleNamespace(
        layout=SimpleNamespace(pre_refuel=pre_refuel),
        tot_for_waypoint=lambda waypoint: pre_refuel_arrival,
    )
    outbound_flight = SimpleNamespace(flight_plan=outbound_flight_plan)
    tanker_flight = SimpleNamespace(
        start_type=StartType.COLD,
        client_count=0,
        departure=SimpleNamespace(is_fleet=False),
    )
    package = SimpleNamespace(
        flights=[outbound_flight, tanker_flight],
        pre_mission_aar=True,
        time_over_target=package_tot,
    )
    tanker_flight.package = package

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return package_tot

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return timedelta(minutes=20)

        def travel_time_between_waypoints(
            self, a: FlightWaypoint, b: FlightWaypoint
        ) -> timedelta:
            if b == self.layout.patrol_start:
                return travel_to_racetrack
            return timedelta()

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)

    assert plan.startup_time() == (
        station_time - travel_to_racetrack - timedelta(minutes=2) - timedelta(minutes=8)
    )


def test_tanker_racetrack_start_serializes_tanker_beacon_before_orbit() -> None:
    mission_start = datetime(2026, 8, 21, 12)
    patrol_start = waypoint("RACETRACK START", FlightWaypointType.PATROL_TRACK)
    patrol_end = waypoint("RACETRACK END", FlightWaypointType.PATROL)
    dcs_waypoint = MovingPoint(patrol_start.position)
    dcs_waypoint.alt = int(patrol_start.alt.meters)
    tanker_flight = SimpleNamespace(
        package=SimpleNamespace(
            flights=[],
            pre_mission_aar=False,
            time_over_target=mission_start,
        ),
        unit_type=SimpleNamespace(
            patrol_speed=kph(400),
            dcs_unit_type=SimpleNamespace(tacan=True),
        ),
    )

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return mission_start

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return timedelta(minutes=30)

    flight_plan = TestPlan(
        cast(Any, tanker_flight),
        PatrollingLayout(
            departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
            nav_to=[],
            patrol_start=patrol_start,
            patrol_end=patrol_end,
            nav_from=[],
            arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
            divert=None,
            bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
        ),
    )
    tanker_flight.flight_plan = flight_plan
    tanker_info = TankerInfo(
        group_name="Tanker",
        callsign="Texaco",
        variant="KC-130",
        freq=MHz(251),
        tacan=TacanChannel(37, TacanBand.Y),
        start_time=mission_start,
        end_time=mission_start + timedelta(minutes=30),
        blue=True,
    )
    builder: Any = object.__new__(RaceTrackBuilder)
    tanker_flight.flight_type = FlightType.REFUELING
    builder.flight = tanker_flight
    builder.mission_data = SimpleNamespace(tankers=[tanker_info])
    builder.group = SimpleNamespace(units=[SimpleNamespace(id=1)])
    builder.now = mission_start

    builder.add_tasks(dcs_waypoint)

    tasks = list(dcs_waypoint.dict()["task"]["params"]["tasks"].values())

    def serialized_task_id(task: dict[str, Any]) -> str:
        if task["id"] == "WrappedAction":
            return str(task["params"]["action"]["id"])
        return str(task["id"])

    task_ids = [serialized_task_id(task) for task in tasks]
    assert task_ids == ["Tanker", "ActivateBeacon", "ControlledTask"]
    assert tasks[2]["params"]["task"]["id"] == "Orbit"
    assert tasks[2]["params"]["task"]["params"]["pattern"] == "Race-Track"


def test_package_tanker_respects_manual_tot_offset() -> None:
    native_start = datetime(2026, 8, 21, 12)
    package_tot = native_start - timedelta(minutes=10)
    recovery_duration = timedelta(minutes=20)
    tanker_flight = SimpleNamespace()
    package = SimpleNamespace(
        flights=[tanker_flight],
        pre_mission_aar=False,
        time_over_target=package_tot,
    )
    tanker_flight.package = package

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return native_start

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return recovery_duration

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)
    plan.tot_offset = -timedelta(minutes=5)

    assert plan.patrol_start_time == package_tot - timedelta(minutes=5)


def test_frontline_refueling_uses_package_tanker_when_pre_mission_aar_enabled() -> None:
    target = object.__new__(FrontLine)
    package = SimpleNamespace(target=target, pre_mission_aar=True)
    flight = SimpleNamespace(
        flight_type=FlightType.REFUELING,
        package=package,
        squadron=SimpleNamespace(player=True),
    )

    assert (
        FlightPlanBuilderTypes.for_flight(cast(Any, flight))
        == PackageRefuelingFlightPlan.builder_type()
    )


def test_frontline_refueling_uses_theater_tanker_when_pre_mission_aar_disabled() -> (
    None
):
    target = object.__new__(FrontLine)
    package = SimpleNamespace(target=target, pre_mission_aar=False)
    flight = SimpleNamespace(
        flight_type=FlightType.REFUELING,
        package=package,
        squadron=SimpleNamespace(player=True),
    )

    assert (
        FlightPlanBuilderTypes.for_flight(cast(Any, flight))
        == TheaterRefuelingFlightPlan.builder_type()
    )


def test_package_tanker_uses_native_timing_without_pre_mission_aar() -> None:
    native_start = datetime(2026, 8, 21, 12)
    recovery_duration = timedelta(minutes=20)
    outbound_flight = SimpleNamespace(pre_mission_aar=False)
    tanker_flight = SimpleNamespace()
    package = SimpleNamespace(
        flights=[outbound_flight, tanker_flight],
        pre_mission_aar=False,
        time_over_target=native_start,
    )
    tanker_flight.package = package

    class TestPlan(PackageRefuelingFlightPlan):
        @property
        def native_patrol_start_time(self) -> datetime:
            return native_start

        @property
        def recovery_refuel_duration(self) -> timedelta:
            return recovery_duration

    layout = PatrollingLayout(
        departure=waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        nav_to=[],
        patrol_start=waypoint("PATROL START"),
        patrol_end=waypoint("PATROL END"),
        nav_from=[],
        arrival=waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
    )
    plan = TestPlan(cast(Any, tanker_flight), layout)

    assert plan.patrol_start_time == native_start
    assert plan.patrol_duration == recovery_duration


def test_pre_mission_aar_distance_setting_was_removed() -> None:
    assert not hasattr(Settings, "pre_mission_aar_distance")


def test_old_package_save_defaults_pre_mission_aar_flag() -> None:
    package = object.__new__(Package)
    package.__setstate__({"flights": []})

    assert package.pre_mission_aar is False


def test_old_flight_save_defaults_pre_mission_aar_flag() -> None:
    flight = object.__new__(Flight)
    flight.__setstate__({})

    assert flight.pre_mission_aar is False


def test_old_formation_attack_layout_save_defaults_pre_mission_aar_fields() -> None:
    layout = object.__new__(FormationAttackLayout)
    layout.__setstate__(
        {
            "departure": waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
            "hold": waypoint("HOLD", FlightWaypointType.LOITER),
            "nav_to": [],
            "join": waypoint("JOIN"),
            "ingress": waypoint("INGRESS"),
            "targets": [waypoint("TARGET")],
            "split": waypoint("SPLIT"),
            "refuel": waypoint("REFUEL", FlightWaypointType.REFUEL),
            "nav_from": [],
            "arrival": waypoint("LANDING", FlightWaypointType.LANDING_POINT),
            "divert": None,
            "bullseye": waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
        }
    )

    assert layout.pre_refuel is None
    assert layout.nav_from_pre_refuel == []
    assert "PRE-REFUEL" not in [waypoint.name for waypoint in layout.iter_waypoints()]


def test_old_sweep_layout_save_defaults_pre_mission_aar_fields() -> None:
    layout = object.__new__(SweepLayout)
    layout.__setstate__(
        {
            "departure": waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
            "hold": waypoint("HOLD", FlightWaypointType.LOITER),
            "nav_to": [],
            "sweep_start": waypoint("SWEEP START"),
            "sweep_end": waypoint("SWEEP END"),
            "nav_from": [],
            "arrival": waypoint("LANDING", FlightWaypointType.LANDING_POINT),
            "divert": None,
            "bullseye": waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
        }
    )

    assert layout.pre_refuel is None
    assert layout.nav_from_pre_refuel == []
    assert "PRE-REFUEL" not in [waypoint.name for waypoint in layout.iter_waypoints()]


def test_old_tarcap_layout_save_defaults_pre_mission_aar_fields() -> None:
    layout = object.__new__(TarCapLayout)
    layout.__setstate__(
        {
            "departure": waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
            "nav_to": [],
            "patrol_start": waypoint("PATROL START"),
            "patrol_end": waypoint("PATROL END"),
            "refuel": waypoint("REFUEL", FlightWaypointType.REFUEL),
            "nav_from": [],
            "arrival": waypoint("LANDING", FlightWaypointType.LANDING_POINT),
            "divert": None,
            "bullseye": waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
        }
    )

    assert layout.pre_refuel is None
    assert layout.nav_from_pre_refuel == []
    assert "PRE-REFUEL" not in [waypoint.name for waypoint in layout.iter_waypoints()]


def test_old_cas_layout_save_defaults_pre_mission_aar_fields() -> None:
    layout = object.__new__(CasLayout)
    layout.__setstate__(
        {
            "departure": waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
            "nav_to": [],
            "ingress": waypoint("INGRESS", FlightWaypointType.INGRESS_CAS),
            "patrol_start": waypoint("FLOT START"),
            "patrol_end": waypoint("FLOT END"),
            "nav_from": [],
            "arrival": waypoint("LANDING", FlightWaypointType.LANDING_POINT),
            "divert": None,
            "bullseye": waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
        }
    )

    assert layout.pre_refuel is None
    assert layout.nav_from_pre_refuel == []
    assert "PRE-REFUEL" not in [waypoint.name for waypoint in layout.iter_waypoints()]
