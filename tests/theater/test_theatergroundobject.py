import pytest
from typing import Any

from dcs.mapping import Point
from dcs.terrain import Terrain
from game.ato.flighttype import FlightType
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    CarrierGroundObject,
    LhaGroundObject,
    MissileSiteGroundObject,
    CoastalSiteGroundObject,
    SamGroundObject,
    VehicleGroupGroundObject,
    EwrGroundObject,
    ShipGroundObject,
    IadsBuildingGroundObject,
)
from game.theater.controlpoint import OffMapSpawn
from game.utils import Heading


def test_mission_types_friendly(mocker: Any) -> None:
    """
    Test the mission types that can be planned against friendly Theater Ground Objects
    """
    # Set up dummy inputs
    dummy_location = PresetLocation(
        name="dummy_location", position=Point(0, 0, None), heading=Heading(0)  # type: ignore
    )
    dummy_control_point = OffMapSpawn(
        name="dummy_control_point",
        position=Point(0, 0, None),  # type: ignore
        theater=None,  # type: ignore
        starts_blue=True,
    )

    # Patch is_friendly as it's difficult to set up a proper ControlPoint
    mocker.patch("game.theater.controlpoint.OffMapSpawn.is_friendly", return_value=True)

    for ground_object_type in [
        CarrierGroundObject,
        LhaGroundObject,
        MissileSiteGroundObject,
        CoastalSiteGroundObject,
        SamGroundObject,
        VehicleGroupGroundObject,
        EwrGroundObject,
        ShipGroundObject,
    ]:
        ground_object = ground_object_type(  # type: ignore
            name="test",
            location=dummy_location,
            control_point=dummy_control_point,
        )
        mission_types = list(ground_object.mission_types(for_player=True))
        assert mission_types == [FlightType.BARCAP]

    for ground_object_type in [BuildingGroundObject, IadsBuildingGroundObject]:  # type: ignore
        ground_object = ground_object_type(  # type: ignore
            name="test",
            category="ammo",
            location=dummy_location,
            control_point=dummy_control_point,
        )
        mission_types = list(ground_object.mission_types(for_player=True))
        assert mission_types == [FlightType.BARCAP]


def test_mission_types_enemy(mocker: Any) -> None:
    """
    Test the mission types that can be planned against enemy Theater Ground Objects
    """
    # Set up dummy inputs
    dummy_location = PresetLocation(
        name="dummy_location", position=Point(0, 0, None), heading=Heading(0)  # type: ignore
    )
    dummy_control_point = OffMapSpawn(
        name="dummy_control_point",
        position=Point(0, 0, None),  # type: ignore
        theater=None,  # type: ignore
        starts_blue=True,
    )

    # Patch is_friendly as it's difficult to set up a proper ControlPoint
    mocker.patch(
        "game.theater.controlpoint.OffMapSpawn.is_friendly", return_value=False
    )

    building = BuildingGroundObject(
        name="test",
        category="ammo",
        location=dummy_location,
        control_point=dummy_control_point,
    )
    mission_types = list(building.mission_types(for_player=False))
    assert len(mission_types) == 6
    assert FlightType.STRIKE in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    iads_building = IadsBuildingGroundObject(
        name="test",
        category="ammo",
        location=dummy_location,
        control_point=dummy_control_point,
    )
    mission_types = list(iads_building.mission_types(for_player=False))
    assert len(mission_types) == 7
    assert FlightType.STRIKE in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types
    assert FlightType.DEAD in mission_types

    for ground_object_type in [
        CarrierGroundObject,
        LhaGroundObject,
        ShipGroundObject,
    ]:
        ground_object = ground_object_type(  # type: ignore
            name="test",
            location=dummy_location,
            control_point=dummy_control_point,
        )
        mission_types = list(ground_object.mission_types(for_player=False))
        assert len(mission_types) == 7
        assert FlightType.ANTISHIP in mission_types
        assert FlightType.STRIKE in mission_types
        assert FlightType.REFUELING in mission_types
        assert FlightType.ESCORT in mission_types
        assert FlightType.TARCAP in mission_types
        assert FlightType.SEAD_ESCORT in mission_types
        assert FlightType.SWEEP in mission_types

    sam = SamGroundObject(
        name="test",
        location=dummy_location,
        control_point=dummy_control_point,
    )
    mission_types = list(sam.mission_types(for_player=False))
    assert len(mission_types) == 8
    assert FlightType.DEAD in mission_types
    assert FlightType.SEAD in mission_types
    assert FlightType.STRIKE in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    ewr = EwrGroundObject(
        name="test",
        location=dummy_location,
        control_point=dummy_control_point,
    )
    mission_types = list(ewr.mission_types(for_player=False))
    assert len(mission_types) == 7
    assert FlightType.DEAD in mission_types
    assert FlightType.STRIKE in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    for ground_object_type in [  # type: ignore
        CoastalSiteGroundObject,
        MissileSiteGroundObject,
    ]:
        ground_object = ground_object_type(  # type: ignore
            name="test",
            location=dummy_location,
            control_point=dummy_control_point,
        )
        mission_types = list(ground_object.mission_types(for_player=False))
        assert len(mission_types) == 6
        assert FlightType.STRIKE in mission_types
        assert FlightType.REFUELING in mission_types
        assert FlightType.ESCORT in mission_types
        assert FlightType.TARCAP in mission_types
        assert FlightType.SEAD_ESCORT in mission_types
        assert FlightType.SWEEP in mission_types

    vehicles = VehicleGroupGroundObject(
        name="test",
        location=dummy_location,
        control_point=dummy_control_point,
    )
    mission_types = list(vehicles.mission_types(for_player=False))
    assert len(mission_types) == 7
    assert FlightType.BAI in mission_types
    assert FlightType.STRIKE in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types
