from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any


class LaserCodeConfig(ABC):
    @staticmethod
    def from_yaml(data: dict[str, Any]) -> LaserCodeConfig:
        if (property_def := data.get("property")) is not None:
            return SinglePropertyLaserCodeConfig(
                property_def["id"], int(property_def["digits"])
            )
        return MultiplePropertyLaserCodeConfig(
            [(d["id"], d["digit"]) for d in data["properties"]]
        )

    @abstractmethod
    def iter_prop_ids(self) -> Iterator[str]: ...

    @abstractmethod
    def property_dict_for_code(self, code: int) -> dict[str, int]: ...


class SinglePropertyLaserCodeConfig(LaserCodeConfig):
    def __init__(self, property_id: str, digits: int) -> None:
        self.property_id = property_id
        self.digits = digits

    def iter_prop_ids(self) -> Iterator[str]:
        yield self.property_id

    def property_dict_for_code(self, code: int) -> dict[str, int]:
        return {self.property_id: code % 10**self.digits}


class MultiplePropertyLaserCodeConfig(LaserCodeConfig):
    def __init__(self, property_digit_mappings: list[tuple[str, int]]) -> None:
        self.property_digit_mappings = property_digit_mappings

    def iter_prop_ids(self) -> Iterator[str]:
        yield from (i for i, p in self.property_digit_mappings)

    def property_dict_for_code(self, code: int) -> dict[str, int]:
        d = {}
        for prop_id, idx in self.property_digit_mappings:
            d[prop_id] = code // 10**idx % 10
        return d
