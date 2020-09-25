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
        FlightType.TARCAP,
        FlightType.SEAD,
        FlightType.DEAD,
        # TODO: FlightType.ELINT,
        # TODO: FlightType.ESCORT,
        # TODO: FlightType.EWAR,
        # TODO: FlightType.RECON,
    ]

    FRIENDLY_AIRBASE_MISSIONS = [
        FlightType.CAP,
        # TODO: FlightType.INTERCEPTION
        # TODO: FlightType.LOGISTICS
    ]

    FRIENDLY_CARRIER_MISSIONS = [
        FlightType.BARCAP,
        # TODO: FlightType.INTERCEPTION
        # TODO: Buddy tanking for the A-4?
        # TODO: Rescue chopper?
        # TODO: Inter-ship logistics?
    ]

    ENEMY_CARRIER_MISSIONS = [
        FlightType.TARCAP,
        # TODO: FlightType.ANTISHIP
        # TODO: FlightType.ESCORT,
    ]

    ENEMY_AIRBASE_MISSIONS = [
        # TODO: FlightType.STRIKE
    ] + COMMON_ENEMY_MISSIONS

    FRIENDLY_GROUND_OBJECT_MISSIONS = [
        FlightType.CAP,
        # TODO: FlightType.LOGISTICS
        # TODO: FlightType.TROOP_TRANSPORT
    ]

    ENEMY_GROUND_OBJECT_MISSIONS = [
        FlightType.STRIKE,
    ] + COMMON_ENEMY_MISSIONS

    FRONT_LINE_MISSIONS = [
        FlightType.CAS,
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
