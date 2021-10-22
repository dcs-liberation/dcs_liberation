from game.radio.tacan import (
    OutOfTacanChannelsError,
    TacanBand,
    TacanChannel,
    TacanChannelInUseError,
    TacanRegistry,
    TacanUsage,
)
import pytest


ALL_VALID_X_TR = [1, *range(31, 46 + 1), *range(64, 126 + 1)]
ALL_VALID_X_A2A = [*range(37, 63 + 1), *range(100, 126 + 1)]


def test_allocate_first_few_channels() -> None:
    registry = TacanRegistry()
    chan1 = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    chan2 = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    chan3 = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    assert chan1 == TacanChannel(1, TacanBand.X)
    assert chan2 == TacanChannel(31, TacanBand.X)
    assert chan3 == TacanChannel(32, TacanBand.X)


def test_allocate_different_usages() -> None:
    """Make sure unallocated channels for one use don't make channels unavailable for other usage"""
    registry = TacanRegistry()

    chanA2AX = registry.alloc_for_band(TacanBand.X, TacanUsage.AirToAir)
    chanA2AY = registry.alloc_for_band(TacanBand.Y, TacanUsage.AirToAir)
    assert chanA2AX == TacanChannel(37, TacanBand.X)
    assert chanA2AY == TacanChannel(37, TacanBand.Y)

    chanTRX = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    chanTRY = registry.alloc_for_band(TacanBand.Y, TacanUsage.TransmitReceive)
    assert chanTRX == TacanChannel(1, TacanBand.X)
    assert chanTRY == TacanChannel(1, TacanBand.Y)


def test_reserve_all_valid_transmit_receive() -> None:
    registry = TacanRegistry()
    print("All valid x", ALL_VALID_X_TR)

    for num in ALL_VALID_X_TR:
        registry.mark_unavailable(TacanChannel(num, TacanBand.X))

    with pytest.raises(OutOfTacanChannelsError):
        registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)

    # Check that we still can allocate an a2a channel even
    # though the T/R channels are used up
    chanA2A = registry.alloc_for_band(TacanBand.X, TacanUsage.AirToAir)
    assert chanA2A == TacanChannel(47, TacanBand.X)


def test_reserve_all_valid_a2a() -> None:
    registry = TacanRegistry()
    print("All valid x", ALL_VALID_X_A2A)

    for num in ALL_VALID_X_A2A:
        registry.mark_unavailable(TacanChannel(num, TacanBand.X))

    with pytest.raises(OutOfTacanChannelsError):
        registry.alloc_for_band(TacanBand.X, TacanUsage.AirToAir)

    # Check that we still can allocate an a2a channel even
    # though the T/R channels are used up
    chanTR = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    assert chanTR == TacanChannel(1, TacanBand.X)


def test_reserve_again() -> None:
    registry = TacanRegistry()
    with pytest.raises(TacanChannelInUseError):
        registry.mark_unavailable(TacanChannel(1, TacanBand.X))
        registry.mark_unavailable(TacanChannel(1, TacanBand.X))
