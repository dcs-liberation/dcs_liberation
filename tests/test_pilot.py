import pytest
from faker import Faker

from game.squadrons.pilot import Pilot, PilotStatus


@pytest.fixture(scope="function")
def pilot() -> Pilot:
    return Pilot("John Doe")


def test_pilot_creation() -> None:
    new_pilot = Pilot("John Doe")
    assert new_pilot.name == "John Doe"
    assert new_pilot.status == PilotStatus.Active


def test_pilot_active(pilot: Pilot) -> None:
    assert pilot.status == PilotStatus.Active


def test_pilot_alive(pilot: Pilot) -> None:
    assert pilot.alive == True


def test_pilot_on_leave(pilot: Pilot) -> None:
    pilot.send_on_leave()
    assert pilot.status == PilotStatus.OnLeave
    assert pilot.on_leave == True
    pilot.return_from_leave()
    assert pilot.status == PilotStatus.Active
    # mypy thinks this line is unreachable. It isn't.
    assert pilot.on_leave == False  # type: ignore


def test_pilot_on_leave_twice(pilot: Pilot) -> None:
    pilot.send_on_leave()
    assert pilot.status == PilotStatus.OnLeave
    with pytest.raises(RuntimeError):
        pilot.send_on_leave()


def test_pilot_not_on_leave(pilot: Pilot) -> None:
    with pytest.raises(RuntimeError):
        pilot.return_from_leave()


def test_pilot_dead(pilot: Pilot) -> None:
    pilot.kill()
    assert pilot.status == PilotStatus.Dead


def test_pilot_record(pilot: Pilot) -> None:
    pilot.record.missions_flown == 0


def test_missions_flown(pilot: Pilot) -> None:
    pilot.record.missions_flown = 1
    assert pilot.record.missions_flown == 1


def test_random_pilot_name() -> None:
    faker = Faker()
    random_pilot = Pilot.random(faker)
    assert random_pilot.name
