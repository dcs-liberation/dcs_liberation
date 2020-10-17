"""Combo box for selecting a flight's task type."""
import logging
from typing import Iterator

from PySide2.QtWidgets import QComboBox

from gen.flights.flight import FlightType
from theater import (
    ConflictTheater,
    ControlPoint,
    FrontLine,
    MissionTarget,
    TheaterGroundObject,
)


class QFlightTypeComboBox(QComboBox):
    """Combo box for selecting a flight task type."""

    COMMON_ENEMY_MISSIONS = [
        FlightType.ESCORT,
        FlightType.SEAD,
        FlightType.DEAD,
        # TODO: FlightType.ELINT,
        # TODO: FlightType.EWAR,
        # TODO: FlightType.RECON,
    ]

    COMMON_FRIENDLY_MISSIONS = [
        FlightType.BARCAP,
    ]

    FRIENDLY_AIRBASE_MISSIONS = [
        # TODO: FlightType.INTERCEPTION
        # TODO: FlightType.LOGISTICS
    ] + COMMON_FRIENDLY_MISSIONS

    FRIENDLY_CARRIER_MISSIONS = [
        # TODO: FlightType.INTERCEPTION
        # TODO: Buddy tanking for the A-4?
        # TODO: Rescue chopper?
        # TODO: Inter-ship logistics?
    ] + COMMON_FRIENDLY_MISSIONS

    ENEMY_CARRIER_MISSIONS = [
        FlightType.ESCORT,
        FlightType.BARCAP,
        # TODO: FlightType.ANTISHIP
    ]

    ENEMY_AIRBASE_MISSIONS = [
        FlightType.BARCAP,
        # TODO: FlightType.STRIKE
    ] + COMMON_ENEMY_MISSIONS

    FRIENDLY_GROUND_OBJECT_MISSIONS = [
        # TODO: FlightType.LOGISTICS
        # TODO: FlightType.TROOP_TRANSPORT
    ] + COMMON_FRIENDLY_MISSIONS

    ENEMY_GROUND_OBJECT_MISSIONS = [
        FlightType.BARCAP,
        FlightType.STRIKE,
    ] + COMMON_ENEMY_MISSIONS

    FRONT_LINE_MISSIONS = [
        FlightType.CAS,
        FlightType.TARCAP,
        # TODO: FlightType.TROOP_TRANSPORT
        # TODO: FlightType.EVAC
    ] + COMMON_ENEMY_MISSIONS

    # TODO: Add BAI missions after we have useful BAI targets.

    def __init__(self, theater: ConflictTheater, target: MissionTarget) -> None:
        super().__init__()
        self.theater = theater
        self.target = target
        for mission_type in self.mission_types_for_target():
            self.addItem(mission_type.name, userData=mission_type)

    def mission_types_for_target(self) -> Iterator[FlightType]:
        if isinstance(self.target, ControlPoint):
            friendly = self.target.captured
            fleet = self.target.is_fleet
            if friendly:
                if fleet:
                    yield from self.FRIENDLY_CARRIER_MISSIONS
                else:
                    yield from self.FRIENDLY_AIRBASE_MISSIONS
            else:
                if fleet:
                    yield from self.ENEMY_CARRIER_MISSIONS
                else:
                    yield from self.ENEMY_AIRBASE_MISSIONS
        elif isinstance(self.target, TheaterGroundObject):
            # TODO: Filter more based on the category.
            friendly = self.target.parent_control_point(self.theater).captured
            if friendly:
                yield from self.FRIENDLY_GROUND_OBJECT_MISSIONS
            else:
                yield from self.ENEMY_GROUND_OBJECT_MISSIONS
        elif isinstance(self.target, FrontLine):
            yield from self.FRONT_LINE_MISSIONS
        else:
            logging.error(
                f"Unhandled target type: {self.target.__class__.__name__}"
            )
