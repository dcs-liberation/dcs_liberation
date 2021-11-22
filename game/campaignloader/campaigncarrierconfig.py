from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING, Union, Type

from dcs.unittype import ShipType

from game.db import ship_type_from_name
from game.theater.controlpoint import ControlPoint

if TYPE_CHECKING:
    from game.theater import ConflictTheater


@dataclass(frozen=True)
class CarrierConfig:
    preferred_name: str
    preferred_type: Type[ShipType]

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> CarrierConfig:
        return CarrierConfig(
            str(data["preferred_name"]), ship_type_from_name(data["preferred_type"])
        )


@dataclass(frozen=True)
class CampaignCarrierConfig:
    by_location: dict[ControlPoint, CarrierConfig]

    @classmethod
    def from_campaign_data(
        cls, data: dict[Union[str, int], Any], theater: ConflictTheater
    ) -> CampaignCarrierConfig:
        by_location: dict[ControlPoint, CarrierConfig] = defaultdict()
        print(data)
        for base_id, carrier_configs in data.items():
            if isinstance(base_id, int):
                base = theater.find_control_point_by_id(base_id)
            else:
                base = theater.control_point_named(base_id)

            carrier_config = CarrierConfig.from_data(carrier_configs)
            base.preferred_name = carrier_config.preferred_name
            base.preferred_type = carrier_config.preferred_type
            by_location[base] = carrier_config
            # for carrier_data in carrier_configs:
            #    CarrierConfig.from_data(squadron_data)
            #    by_location[base].preferred_name = carrier_configs

        return CampaignCarrierConfig(by_location)
