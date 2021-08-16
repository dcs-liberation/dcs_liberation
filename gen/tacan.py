"""TACAN channel handling."""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterator, Set


class TacanBand(Enum):
    X = "X"
    Y = "Y"

    def range(self) -> Iterator["TacanChannel"]:
        """Returns an iterator over the channels in this band."""
        return (TacanChannel(x, self) for x in range(1, 126))


class TacanUsage(Enum):
    TransmitReceive = "TransmitReceive"
    AirToAir = "AirToAir"


# Avoid certain TACAN channels for various reasons
# https://forums.eagle.ru/topic/276390-datalink-issue/
UNAVAILABLE_T_R = {
    TacanBand.X: set(range(2, 30)) | set(range(47, 63)),
    TacanBand.Y: set(range(2, 30)) | set(range(64, 92)),
}
UNAVAILABLE_A2A = {
    TacanBand.X: set(range(1, 36)) | set(range(64, 99)),
    TacanBand.Y: set(range(1, 36)) | set(range(64, 99)),
}


@dataclass(frozen=True)
class TacanChannel:
    number: int
    band: TacanBand

    def __str__(self) -> str:
        return f"{self.number}{self.band.value}"


class OutOfTacanChannelsError(RuntimeError):
    """Raised when all channels in this band have been allocated."""

    def __init__(self, band: TacanBand) -> None:
        super().__init__(f"No available channels in TACAN {band.value} band")


class TacanChannelInUseError(RuntimeError):
    """Raised when attempting to reserve an in-use channel."""

    def __init__(self, channel: TacanChannel) -> None:
        super().__init__(f"{channel} is already in use")


class TacanChannelForbiddenError(RuntimeError):
    """Raised when attempting to reserve a, for technical reasons, forbidden channel."""

    def __init__(self, channel: TacanChannel) -> None:
        super().__init__(f"{channel} is forbidden")


class TacanRegistry:
    """Manages allocation of TACAN channels."""

    def __init__(self) -> None:
        self.allocated_channels: Set[TacanChannel] = set()
        self.band_allocators: Dict[TacanBand, Iterator[TacanChannel]] = {}

        for band in TacanBand:
            self.band_allocators[band] = band.range()

    def alloc_for_band(self, band: TacanBand) -> TacanChannel:
        """Allocates a TACAN channel in the given band.

        Args:
            band: The TACAN band to allocate a channel for.

        Returns:
            A TACAN channel in the given band.

        Raises:
            OutOfTacanChannelsError: All channels compatible with the given radio are
                already allocated.
        """
        allocator = self.band_allocators[band]
        try:
            while (channel := next(allocator)) in self.allocated_channels:
                pass
            return channel
        except StopIteration:
            raise OutOfTacanChannelsError(band)

    def reserve(self, channel: TacanChannel, intendedUsage: TacanUsage) -> None:
        """Reserves the given channel.

        Reserving a channel ensures that it will not be allocated in the future.

        Args:
            channel: The channel to reserve.

        Raises:
            TacanChannelInUseError: The given frequency is already in use.
            TacanChannelForbiddenError: The given frequency is forbidden.
        """
        if channel in self.allocated_channels:
            raise TacanChannelInUseError(channel)
        self.allocated_channels.add(channel)
