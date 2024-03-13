from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ControlPointConfig:
    ferry_only: bool

    @staticmethod
    def from_data(data: dict[str, Any]) -> ControlPointConfig:
        return ControlPointConfig(ferry_only=data.get("ferry_only", False))

    @staticmethod
    def iter_from_data(
        data: dict[str | int, Any]
    ) -> Iterator[tuple[str | int, ControlPointConfig]]:
        for name_or_id, cp_data in data.items():
            yield name_or_id, ControlPointConfig.from_data(cp_data)
