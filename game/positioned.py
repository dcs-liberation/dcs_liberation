from typing import Protocol

from dcs import Point


class Positioned(Protocol):
    @property
    def position(self) -> Point:
        raise NotImplementedError
