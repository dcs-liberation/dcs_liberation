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
class AirBaseConfig:
    increased_aircraft_autoplanner_variety: bool

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> AirBaseConfig:

        return AirBaseConfig(bool(data["increased_aircraft_autoplanner_variety"]))


@dataclass(frozen=True)
class CampaignAirBaseConfig:
    by_location: dict[ControlPoint, list[AirBaseConfig]]

    @classmethod
    def from_campaign_data(
        cls, data: dict[Union[str, int], Any], theater: ConflictTheater
    ) -> CampaignAirBaseConfig:
        by_location: dict[ControlPoint, list[AirBaseConfig]] = defaultdict(list)
        for base_id, airbase_config_data in data.items():
            if isinstance(base_id, int):
                base = theater.find_control_point_by_id(base_id)
            else:
                base = theater.control_point_named(base_id)

            airbase_config = AirBaseConfig.from_data(airbase_config_data)
            base.increased_aircraft_autoplanner_variety = (
                airbase_config.increased_aircraft_autoplanner_variety
            )

        return CampaignAirBaseConfig(by_location)
