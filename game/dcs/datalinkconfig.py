from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DatalinkConfig:
    max_team_members: int
    max_donors: int

    @staticmethod
    def from_data(data: dict[str, Any]) -> DatalinkConfig | None:
        try:
            data = data["datalink"]
        except KeyError:
            return None
        return DatalinkConfig(int(data["max_team_members"]), int(data["max_donors"]))
