from __future__ import annotations

from dataclasses import dataclass
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
    auto_assignable_mission_types: set[FlightType]
    operating_bases: OperatingBases
    female_pilot_percentage: int
    pilot_pool: list[Pilot]
    claimed: bool = False

    def __str__(self) -> str:
        if self.nickname is None:
            return self.name
        return f'{self.name} "{self.nickname}"'

    def capable_of(self, task: FlightType) -> bool:
        """Returns True if the squadron is capable of performing the given task.

        A squadron may be capable of performing a task even if it will not be
        automatically assigned to it.
        """
        return self.aircraft.capable_of(task)

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

        return SquadronDef(
            name=data["name"],
            nickname=data.get("nickname"),
            country=data["country"],
            role=data["role"],
            aircraft=unit_type,
            livery=data.get("livery"),
            auto_assignable_mission_types=set(unit_type.iter_task_capabilities()),
            operating_bases=OperatingBases.from_yaml(unit_type, data.get("bases", {})),
            female_pilot_percentage=female_pilot_percentage,
            pilot_pool=pilots,
        )
