from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ilasercoderegistry import ILaserCodeRegistry


class LaserCode:
    def __init__(self, code: int, registry: ILaserCodeRegistry) -> None:
        self.verify_laser_code(code)
        self.code = code
        self.registry = registry

    def release(self) -> None:
        self.registry.release_code(self)

    @staticmethod
    def verify_laser_code(code: int) -> None:
        # https://forum.dcs.world/topic/211574-valid-laser-codes/
        # Valid laser codes are as follows
        # First digit is always 1
        # Second digit is 5-7
        # Third and fourth digits are 1 - 8
        # We iterate backward (reversed()) so that 1687 follows 1688

        # Special case used by FC3 aircraft like the A-10A that is not valid for other
        # aircraft.
        if code == 1113:
            return

        # Must be 4 digits with no leading 0
        if code < 1000 or code >= 2000:
            raise ValueError

        # The first digit was already verified above. Isolate the remaining three
        # digits. The resulting list is ordered by significance, not printed position.
        digits = [code // 10**i % 10 for i in range(3)]

        if digits[0] < 1 or digits[0] > 8:
            raise ValueError
        if digits[1] < 1 or digits[1] > 8:
            raise ValueError
        if digits[2] < 5 or digits[2] > 7:
            raise ValueError

    def __str__(self) -> str:
        return f"{self.code}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LaserCode):
            return False
        return self.code == other.code

    def __hash__(self) -> int:
        return hash(self.code)
