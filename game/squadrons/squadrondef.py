from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, TYPE_CHECKING

import yaml

from game.dcs.aircrafttype import AircraftType
from game.squadrons.operatingbases import OperatingBases
from game.squadrons.pilot import Pilot

if TYPE_CHECKING:
    from game.ato.flighttype import FlightType
    from game.theater import ControlPoint


@dataclass
class SquadronDef:
    name: str
    nickname: Optional[str]
    country: str
    role: str
    aircraft: AircraftType
    livery: Optional[str]
    mission_types: tuple[FlightType, ...]
    operating_bases: OperatingBases
    female_pilot_percentage: int
    pilot_pool: list[Pilot]
    claimed: bool = False

    auto_assignable_mission_types: set[FlightType] = field(
        init=False, hash=False, compare=False
    )

    def __post_init__(self) -> None:
        self.auto_assignable_mission_types = set(self.mission_types)

    def __str__(self) -> str:
        if self.nickname is None:
            return self.name
        return f'{self.name} "{self.nickname}"'

    def set_allowed_mission_types(self, mission_types: Iterable[FlightType]) -> None:
        self.mission_types = tuple(mission_types)
        self.auto_assignable_mission_types.intersection_update(self.mission_types)

    def can_auto_assign(self, task: FlightType) -> bool:
        return task in self.auto_assignable_mission_types

    def operates_from(self, control_point: ControlPoint) -> bool:
        if not control_point.can_operate(self.aircraft):
            return False
        if control_point.is_carrier:
            return self.operating_bases.carrier
        elif control_point.is_lha:
            return self.operating_bases.lha
        else:
            return self.operating_bases.shore

    @classmethod
    def from_yaml(cls, path: Path) -> SquadronDef:
        from game.ato.ai_flight_planner_db import tasks_for_aircraft
        from game.ato import FlightType

        with path.open(encoding="utf8") as squadron_file:
            data = yaml.safe_load(squadron_file)

        name = data["aircraft"]
        try:
            unit_type = AircraftType.named(name)
        except KeyError as ex:
            raise KeyError(f"Could not find any aircraft named {name}") from ex

        pilots = [Pilot(n, player=False) for n in data.get("pilots", [])]
        pilots.extend([Pilot(n, player=True) for n in data.get("players", [])])
        female_pilot_percentage = data.get("female_pilot_percentage", 6)

        mission_types = [FlightType.from_name(n) for n in data["mission_types"]]
        tasks = tasks_for_aircraft(unit_type)
        for mission_type in list(mission_types):
            if mission_type not in tasks:
                logging.error(
                    f"Squadron has mission type {mission_type} but {unit_type} is not "
                    f"capable of that task: {path}"
                )
                mission_types.remove(mission_type)

        return SquadronDef(
            name=data["name"],
            nickname=data.get("nickname"),
            country=data["country"],
            role=data["role"],
            aircraft=unit_type,
            livery=data.get("livery"),
            mission_types=tuple(mission_types),
            operating_bases=OperatingBases.from_yaml(unit_type, data.get("bases", {})),
            female_pilot_percentage=female_pilot_percentage,
            pilot_pool=pilots,
        )
