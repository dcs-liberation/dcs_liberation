from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

ValueT = TypeVar("ValueT", bool, int)


@dataclass(frozen=True)
class PropertyValue(Generic[ValueT]):
    id: str
    value: ValueT
