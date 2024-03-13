from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from game.squadrons import Pilot


class IFlightRoster(ABC):
    @abstractmethod
    def iter_pilots(self) -> Iterator[Pilot | None]:
        ...

    @abstractmethod
    def pilot_at(self, idx: int) -> Pilot | None:
        ...

    @property
    @abstractmethod
    def max_size(self) -> int:
        ...

    @abstractmethod
    def resize(self, new_size: int) -> None:
        ...

    @abstractmethod
    def set_pilot(self, index: int, pilot: Optional[Pilot]) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...
