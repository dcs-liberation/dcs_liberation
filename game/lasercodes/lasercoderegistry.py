import logging
from collections import deque

from .ilasercoderegistry import ILaserCodeRegistry
from .lasercode import LaserCode


class LaserCodeRegistry(ILaserCodeRegistry):
    def __init__(self) -> None:
        self.allocated_codes: set[int] = set()
        self.available_codes = LaserCodeRegistry._all_valid_laser_codes()
        self.fc3_code = LaserCode(1113, self)

    def alloc_laser_code(self) -> LaserCode:
        try:
            code = self.available_codes.popleft()
            self.allocated_codes.add(code)
            return LaserCode(code, self)
        except IndexError:
            raise RuntimeError("All laser codes have been allocated")

    def release_code(self, code: LaserCode) -> None:
        if code.code in self.allocated_codes:
            self.allocated_codes.remove(code.code)
            self.available_codes.appendleft(code.code)
        else:
            logging.error(
                "attempted to release laser code %d which was not allocated", code.code
            )

    @staticmethod
    def _all_valid_laser_codes() -> deque[int]:
        # Valid laser codes are as follows
        # First digit is always 1
        # Second digit is 5-7
        # Third and fourth digits are 1 - 8
        # We iterate backward (reversed()) so that 1687 follows 1688
        q = deque(int(oct(code)[2:]) + 11 for code in reversed(range(0o1500, 0o2000)))

        # We start with the default of 1688 and wrap around when we reach the end
        q.rotate(-q.index(1688))
        return q
