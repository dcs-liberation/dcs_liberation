from __future__ import annotations

from datetime import timezone

from dcs.terrain import Terrain

from .conflicttheater import ConflictTheater
from .daytimemap import DaytimeMap
from .landmap import Landmap
from .seasonalconditions import SeasonalConditions


class YamlTheater(ConflictTheater):
    def __init__(
        self,
        terrain: Terrain,
        landmap: Landmap | None,
        time_zone: timezone,
        seasonal_conditions: SeasonalConditions,
        daytime_map: DaytimeMap,
    ) -> None:
        super().__init__()
        self.terrain = terrain
        self.landmap = landmap
        self._timezone = time_zone
        self._seasonal_conditions = seasonal_conditions
        self.daytime_map = daytime_map

    @property
    def timezone(self) -> timezone:
        return self._timezone

    @property
    def seasonal_conditions(self) -> SeasonalConditions:
        return self._seasonal_conditions
