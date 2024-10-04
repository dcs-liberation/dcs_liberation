from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lasercode import LaserCode


class ILaserCodeRegistry(ABC):
    @abstractmethod
    def alloc_laser_code(self) -> LaserCode: ...

    @abstractmethod
    def release_code(self, code: LaserCode) -> None: ...
