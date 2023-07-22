from collections import deque


class LaserCodeRegistry:
    def __init__(self) -> None:
        self.allocated_codes: set[int] = set()
        self.available_codes = LaserCodeRegistry._all_valid_laser_codes()

    def alloc_laser_code(self) -> int:
        try:
            code = self.available_codes.popleft()
            self.allocated_codes.add(code)
            return code
        except IndexError:
            raise RuntimeError("All laser codes have been allocated")

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
