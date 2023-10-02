from dataclasses import dataclass


@dataclass(frozen=True)
class SourceTrackNumberPrefix:
    """The prefix of a source track number (STN) for a flight.

    STNs are 5 octal digits. To make it easier for players to guess the codes for their
    flight members, these are segmented so that the least significant digit is always
    the flight member index. This wastes of the address space, but even at the lowest
    density (single-member flights, ~88% waste), there are still enough prefixes for
    4096 aircraft.

    There is no per-package segmenting, however. DCS imposes a flight-size limitation on
    us (usually four, sometimes fewer), but we do not restrict the number of flights
    that can be in a package. If we were to carve out a digit for the package, we'd be
    limiting the package to a max of eight flights. It's larger than a typical package,
    but it's not unreasonable for a large OCA strike. If we carved out two digits, the
    limit would be more than enough (64), but it would also limit the game to 64
    packages. That's also quite high, but it's low enough that it could be hit. There's
    some wiggle room here, since for now the only aircraft that need STNs are the F-16C,
    F/A-18C, and A-10C II, but we shouldn't break in the unlikely case where the game is
    composed entirely of those airframes.

    Carving up the address space in different ways (such as two bits for the flight and
    six for the package) would defeat the purpose of doing so, since they wouldn't be
    recognizable prefixes for players, since these are expressed as octal in the jet.
    """

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("STN prefixes cannot be negative")
        if self.value >= 0o10000:
            raise ValueError("STN prefixes must be < 0o10000")

    def __str__(self) -> str:
        return f"{oct(self.value)[2:]:0>4}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({oct(self.value)})"
