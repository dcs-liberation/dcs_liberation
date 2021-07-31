from collections import deque
from typing import Iterator


class OutOfLaserCodesError(RuntimeError):
    def __init__(self) -> None:
        super().__init__(
            f"All JTAC laser codes have been allocated.  No available codes."
        )


class LaserCodeRegistry:
    def __init__(self) -> None:
        self.allocated_codes: set[int] = set()
        self.allocator: Iterator[int] = LaserCodeRegistry.__laser_code_generator()

    def get_next_laser_code(self) -> int:
        try:
            while (code := next(self.allocator)) in self.allocated_codes:
                pass
            self.allocated_codes.add(code)
            return code
        except StopIteration:
            raise OutOfLaserCodesError

    @staticmethod
    def __laser_code_generator() -> Iterator[int]:
        # Valid laser codes are as follows
        # First digit is always 1
        # Second digit is 5-7
        # Third and fourth digits are 1 - 8
        # We iterate backward (reversed()) so that 1687 follows 1688
        q = deque(int(oct(code)[2:]) + 11 for code in reversed(range(0o1500, 0o2000)))

        # We start with the default of 1688 and wrap around when we reach the end
        q.rotate(-q.index(1688))
        return iter(q)
