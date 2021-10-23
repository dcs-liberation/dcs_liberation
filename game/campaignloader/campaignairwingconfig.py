from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING, Union

from game.ato.flighttype import FlightType
from game.theater.controlpoint import ControlPoint

if TYPE_CHECKING:
    from game.theater import ConflictTheater


@dataclass(frozen=True)
class SquadronConfig:
    primary: FlightType
    secondary: list[FlightType]
    aircraft: list[str]
    override_aircraft_parking_enabled: bool
    override_aircraft_parking_slots: int

    @property
    def auto_assignable(self) -> set[FlightType]:
        return set(self.secondary) | {self.primary}

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> SquadronConfig:
        print(data)

        try:
            override_aircraft_parking_slots = data.get("override_aircraft_parking")
        except KeyError:
            override_aircraft_parking_enabled = False
            override_aircraft_parking_slots = 0

        if override_aircraft_parking_slots is not None:
            override_aircraft_parking_enabled = True
        else:
            override_aircraft_parking_enabled = False

        secondary_raw = data.get("secondary")
        if secondary_raw is None:
            secondary = []
        elif isinstance(secondary_raw, str):
            secondary = cls.expand_secondary_alias(secondary_raw)
        else:
            secondary = [FlightType(s) for s in secondary_raw]

        try:
            primary = data["primary"]
        except KeyError:
            primary = None

        if primary is not None:
            squadron_config = SquadronConfig(
                FlightType(primary),
                secondary,
                data.get("aircraft", []),
                override_aircraft_parking_enabled,
                override_aircraft_parking_slots,
            )
        else:
            squadron_config = SquadronConfig(
                None,
                secondary,
                data.get("aircraft", []),
                override_aircraft_parking_enabled,
                override_aircraft_parking_slots,
            )

        return squadron_config

    @staticmethod
    def expand_secondary_alias(alias: str) -> list[FlightType]:
        if alias == "any":
            return list(FlightType)
        elif alias == "air-to-air":
            return [t for t in FlightType if t.is_air_to_air]
        elif alias == "air-to-ground":
            return [t for t in FlightType if t.is_air_to_ground]
        raise KeyError(f"Unknown secondary mission type: {alias}")


@dataclass(frozen=True)
class CampaignAirWingConfig:
    by_location: dict[ControlPoint, list[SquadronConfig]]

    @classmethod
    def from_campaign_data(
        cls, data: dict[Union[str, int], Any], theater: ConflictTheater
    ) -> CampaignAirWingConfig:
        by_location: dict[ControlPoint, list[SquadronConfig]] = defaultdict(list)
        for base_id, squadron_configs in data.items():
            if isinstance(base_id, int):
                base = theater.find_control_point_by_id(base_id)
            else:
                base = theater.control_point_named(base_id)

            for squadron_data in squadron_configs:
                squadron_config = SquadronConfig.from_data(squadron_data)
                if squadron_config.override_aircraft_parking_enabled:
                    base.override_aircraft_parking_enabled = True
                    base.override_aircraft_parking_slots = (
                        squadron_config.override_aircraft_parking_slots
                    )
                    print(
                        "Set the number of parking slots at "
                        + base.name
                        + " to "
                        + str(base.override_aircraft_parking_slots)
                    )
                by_location[base].append(squadron_config)

        return CampaignAirWingConfig(by_location)
