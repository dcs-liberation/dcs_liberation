"""Radio frequency types and allocators."""
import itertools
from dataclasses import dataclass
from typing import Dict, Iterator, List, Set


@dataclass(frozen=True)
class RadioFrequency:
    """A radio frequency.

    Not currently concerned with tracking modulation, just the frequency.
    """

    #: The frequency in kilohertz.
    hertz: int

    def __str__(self):
        if self.hertz >= 1000000:
            return self.format("MHz", 1000000)
        return self.format("kHz", 1000)

    def format(self, units: str, divisor: int) -> str:
        converted = self.hertz / divisor
        if converted.is_integer():
            return f"{int(converted)} {units}"
        return f"{converted:0.3f} {units}"

    @property
    def mhz(self) -> float:
        """Returns the frequency in megahertz.

        Returns:
            The frequency in megahertz.
        """
        return self.hertz / 1000000


def MHz(num: int, khz: int = 0) -> RadioFrequency:
    return RadioFrequency(num * 1000000 + khz * 1000)


def kHz(num: int) -> RadioFrequency:
    return RadioFrequency(num * 1000)


@dataclass(frozen=True)
class Radio:
    """A radio.

    Defines the minimum (inclusive) and maximum (exclusive) range of the radio.
    """

    #: The name of the radio.
    name: str

    #: The minimum (inclusive) frequency tunable by this radio.
    minimum: RadioFrequency

    #: The maximum (exclusive) frequency tunable by this radio.
    maximum: RadioFrequency

    #: The spacing between adjacent frequencies.
    step: RadioFrequency

    def __str__(self) -> str:
        return self.name

    def range(self) -> Iterator[RadioFrequency]:
        """Returns an iterator over the usable frequencies of this radio."""
        return (RadioFrequency(x) for x in range(
            self.minimum.hertz, self.maximum.hertz, self.step.hertz
        ))


class OutOfChannelsError(RuntimeError):
    """Raised when all channels usable by this radio have been allocated."""

    def __init__(self, radio: Radio) -> None:
        super().__init__(f"No available channels for {radio}")


class ChannelInUseError(RuntimeError):
    """Raised when attempting to reserve an in-use frequency."""

    def __init__(self, frequency: RadioFrequency) -> None:
        super().__init__(f"{frequency} is already in use")


# TODO: Figure out appropriate steps for each radio. These are just guesses.
#: List of all known radios used by aircraft in the game.
RADIOS: List[Radio] = [
    Radio("AN/ARC-164", MHz(225), MHz(400), step=MHz(1)),
    Radio("AN/ARC-186(V) AM", MHz(116), MHz(152), step=MHz(1)),
    Radio("AN/ARC-186(V) FM", MHz(30), MHz(76), step=MHz(1)),
    # The AN/ARC-210 can also use [30, 88) and [108, 118), but the current
    # implementation can't implement the gap and the radio can't transmit on the
    # latter. There's still plenty of channels between 118 MHz and 400 MHz, so
    # not worth worrying about.
    Radio("AN/ARC-210", MHz(118), MHz(400), step=MHz(1)),
    Radio("AN/ARC-222", MHz(116), MHz(174), step=MHz(1)),
    Radio("SCR-522", MHz(100), MHz(156), step=MHz(1)),
    Radio("A.R.I. 1063", MHz(100), MHz(156), step=MHz(1)),
    Radio("BC-1206", kHz(200), kHz(400), step=kHz(10)),

    # Note: The M2000C V/UHF can operate in both ranges, but has a gap between
    # 150 MHz and 225 MHz. We can't allocate in that gap, and the current
    # system doesn't model gaps, so just pretend it ends at 150 MHz for now. We
    # can model gaps later if needed.
    Radio("TRT ERA 7000 V/UHF", MHz(118), MHz(150), step=MHz(1)),
    Radio("TRT ERA 7200 UHF", MHz(225), MHz(400), step=MHz(1)),

    # Tomcat radios
    # # https://www.heatblur.se/F-14Manual/general.html#an-arc-159-uhf-1-radio
    Radio("AN/ARC-159", MHz(225), MHz(400), step=MHz(1)),
    # AN/ARC-182 can also operate from 30 MHz to 88 MHz, as well as from 225 MHz
    # to 400 MHz range, but we can't model gaps with the current implementation.
    # https://www.heatblur.se/F-14Manual/general.html#an-arc-182-v-uhf-2-radio
    Radio("AN/ARC-182", MHz(108), MHz(174), step=MHz(1)),

    # Also capable of [103, 156) at 25 kHz intervals, but we can't do gaps.
    Radio("FR 22", MHz(225), MHz(400), step=kHz(50)),

    # P-51 / P-47 Radio
    # 4 preset channels (A/B/C/D)
    Radio("SCR522", MHz(100), MHz(156), step=kHz(25)),

    Radio("R&S M3AR VHF", MHz(120), MHz(174), step=MHz(1)),
    Radio("R&S M3AR UHF", MHz(225), MHz(400), step=MHz(1)),

    # MiG-15bis
    Radio("RSI-6K HF", MHz(3, 750), MHz(5), step=kHz(25)),

    # MiG-19P
    Radio("RSIU-4V", MHz(100), MHz(150), step=MHz(1)),

    # MiG-21bis
    Radio("RSIU-5V", MHz(118), MHz(140), step=MHz(1)),

    # Ka-50
    # Note: Also capable of 100MHz-150MHz, but we can't model gaps.
    Radio("R-800L1", MHz(220), MHz(400), step=kHz(25)),
    Radio("R-828", MHz(20), MHz(60), step=kHz(25)),

    # UH-1H
    Radio("AN/ARC-51BX", MHz(225), MHz(400), step=kHz(50)),
    Radio("AN/ARC-131", MHz(30), MHz(76), step=kHz(50)),
    Radio("AN/ARC-134", MHz(116), MHz(150), step=kHz(25)),
]


def get_radio(name: str) -> Radio:
    """Returns the radio with the given name.

    Args:
        name: Name of the radio to return.

    Returns:
        The radio matching name.

    Raises:
        KeyError: No matching radio was found.
    """
    for radio in RADIOS:
        if radio.name == name:
            return radio
    raise KeyError


class RadioRegistry:
    """Manages allocation of radio channels.

    There's some room for improvement here. We could prefer to allocate
    frequencies that are available to the fewest number of radios first, so
    radios with wide bands like the AN/ARC-210 don't exhaust all the channels
    available to narrower radios like the AN/ARC-186(V). In practice there are
    probably plenty of channels, so we can deal with that later if we need to.

    We could also allocate using a larger increment, returning to smaller
    increments each time the range is exhausted. This would help with the
    previous problem, as the AN/ARC-186(V) would still have plenty of 25 kHz
    increment channels left after the AN/ARC-210 moved on to the higher
    frequencies. This would also look a little nicer than having every flight
    allocated in the 30 MHz range.
    """

    # Not a real radio, but useful for allocating a channel usable for
    # inter-flight communications.
    BLUFOR_UHF = Radio("BLUFOR UHF", MHz(225), MHz(400), step=MHz(1))

    def __init__(self) -> None:
        self.allocated_channels: Set[RadioFrequency] = set()
        self.radio_allocators: Dict[Radio, Iterator[RadioFrequency]] = {}

        radios = itertools.chain(RADIOS, [self.BLUFOR_UHF])
        for radio in radios:
            self.radio_allocators[radio] = radio.range()

    def alloc_for_radio(self, radio: Radio) -> RadioFrequency:
        """Allocates a radio channel tunable by the given radio.

        Args:
            radio: The radio to allocate a channel for.

        Returns:
            A radio channel compatible with the given radio.

        Raises:
            OutOfChannelsError: All channels compatible with the given radio are
                already allocated.
        """
        allocator = self.radio_allocators[radio]
        try:
            while (channel := next(allocator)) in self.allocated_channels:
                pass
            self.reserve(channel)
            return channel
        except StopIteration:
            raise OutOfChannelsError(radio)

    def alloc_uhf(self) -> RadioFrequency:
        """Allocates a UHF radio channel suitable for inter-flight comms.

        Returns:
            A UHF radio channel suitable for inter-flight comms.

        Raises:
            OutOfChannelsError: All channels compatible with the given radio are
                already allocated.
        """
        return self.alloc_for_radio(self.BLUFOR_UHF)

    def reserve(self, frequency: RadioFrequency) -> None:
        """Reserves the given channel.

        Reserving a channel ensures that it will not be allocated in the future.

        Args:
            frequency: The channel to reserve.

        Raises:
            ChannelInUseError: The given frequency is already in use.
        """
        if frequency in self.allocated_channels:
            raise ChannelInUseError(frequency)
        self.allocated_channels.add(frequency)
