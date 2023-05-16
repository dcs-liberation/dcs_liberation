import pytest
from typing import Any

from dcs.terrain.terrain import Airport
from game.ato.flighttype import FlightType
from game.theater.controlpoint import Airfield, Carrier, Lha, OffMapSpawn, Fob


def test_mission_types_friendly(mocker: Any) -> None:
    """
    Test the mission types that can be planned against friendly control points
    """
    # Airfield
    mocker.patch("game.theater.controlpoint.Airfield.is_friendly", return_value=True)
    airport = Airport(None, None)  # type: ignore
    airport.name = "test"  # required for Airfield.__init__
    airfield = Airfield(airport, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(airfield.mission_types(for_player=True))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # Carrier
    mocker.patch("game.theater.controlpoint.Carrier.is_friendly", return_value=True)
    carrier = Carrier(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(carrier.mission_types(for_player=True))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # LHA
    mocker.patch("game.theater.controlpoint.Lha.is_friendly", return_value=True)
    lha = Lha(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(lha.mission_types(for_player=True))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # Fob
    mocker.patch("game.theater.controlpoint.Fob.is_friendly", return_value=True)
    fob = Fob(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(fob.mission_types(for_player=True))
    assert len(mission_types) == 2
    assert FlightType.AEWC in mission_types
    assert FlightType.BARCAP in mission_types

    # Off map spawn
    mocker.patch("game.theater.controlpoint.OffMapSpawn.is_friendly", return_value=True)
    off_map_spawn = OffMapSpawn(name="test", position=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(off_map_spawn.mission_types(for_player=True))
    assert len(mission_types) == 0


def test_mission_types_enemy(mocker: Any) -> None:
    """
    Test the mission types that can be planned against enemy control points
    """
    # Airfield
    mocker.patch("game.theater.controlpoint.Airfield.is_friendly", return_value=False)
    airport = Airport(None, None)  # type: ignore
    airport.name = "test"  # required for Airfield.__init__
    airfield = Airfield(airport, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(airfield.mission_types(for_player=True))
    assert len(mission_types) == 8
    assert FlightType.OCA_AIRCRAFT in mission_types
    assert FlightType.OCA_RUNWAY in mission_types
    assert FlightType.AIR_ASSAULT in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types
    assert FlightType.REFUELING in mission_types

    # Carrier
    mocker.patch("game.theater.controlpoint.Carrier.is_friendly", return_value=False)
    carrier = Carrier(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(carrier.mission_types(for_player=True))
    assert len(mission_types) == 5
    assert FlightType.ANTISHIP in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    # LHA
    mocker.patch("game.theater.controlpoint.Lha.is_friendly", return_value=False)
    lha = Lha(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(lha.mission_types(for_player=True))
    assert len(mission_types) == 5
    assert FlightType.ANTISHIP in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    # Fob
    mocker.patch("game.theater.controlpoint.Fob.is_friendly", return_value=False)
    fob = Fob(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(fob.mission_types(for_player=True))
    assert len(mission_types) == 6
    assert FlightType.AIR_ASSAULT in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types
    assert FlightType.STRIKE in mission_types

    # Off map spawn
    mocker.patch(
        "game.theater.controlpoint.OffMapSpawn.is_friendly", return_value=False
    )
    off_map_spawn = OffMapSpawn(name="test", position=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(off_map_spawn.mission_types(for_player=True))
    assert len(mission_types) == 0
