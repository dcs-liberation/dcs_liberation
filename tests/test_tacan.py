from gen.tacan import (
    TacanBand,
    TacanChannel,
    TacanChannelForbiddenError,
    TacanChannelInUseError,
    TacanRegistry,
    TacanUsage,
)
import pytest


def test_allocate_first_few_channels() -> None:
    registry = TacanRegistry()
    chan1 = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    chan2 = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    chan3 = registry.alloc_for_band(TacanBand.X, TacanUsage.TransmitReceive)
    assert chan1 == TacanChannel(1, TacanBand.X)
    assert chan2 == TacanChannel(31, TacanBand.X)
    assert chan3 == TacanChannel(32, TacanBand.X)


@pytest.mark.skip(reason="TODO")
def test_reserve_all_valid_transmit_receive() -> None:
    pass


@pytest.mark.skip(reason="TODO")
def test_reserve_all_valid_a2a() -> None:
    pass


@pytest.mark.skip(reason="TODO")
def test_allocate_all() -> None:
    pass


def test_reserve_invalid_tr_channels() -> None:
    registry = TacanRegistry()
    some_invalid_channels = [
        TacanChannel(2, TacanBand.X),
        TacanChannel(30, TacanBand.X),
        TacanChannel(47, TacanBand.X),
        TacanChannel(63, TacanBand.X),
        TacanChannel(2, TacanBand.Y),
        TacanChannel(30, TacanBand.Y),
        TacanChannel(64, TacanBand.Y),
        TacanChannel(92, TacanBand.Y),
    ]
    for chan in some_invalid_channels:
        with pytest.raises(TacanChannelForbiddenError):
            registry.reserve(chan, TacanUsage.TransmitReceive)


def test_reserve_invalid_a2a_channels() -> None:
    registry = TacanRegistry()
    some_invalid_channels = [
        TacanChannel(1, TacanBand.X),
        TacanChannel(36, TacanBand.X),
        TacanChannel(64, TacanBand.X),
        TacanChannel(99, TacanBand.X),
        TacanChannel(1, TacanBand.Y),
        TacanChannel(36, TacanBand.Y),
        TacanChannel(64, TacanBand.Y),
        TacanChannel(99, TacanBand.Y),
    ]
    for chan in some_invalid_channels:
        with pytest.raises(TacanChannelForbiddenError):
            registry.reserve(chan, TacanUsage.AirToAir)


def test_reserve_again() -> None:
    registry = TacanRegistry()
    with pytest.raises(TacanChannelInUseError):
        registry.reserve(TacanChannel(1, TacanBand.X), TacanUsage.TransmitReceive)
        registry.reserve(TacanChannel(1, TacanBand.X), TacanUsage.TransmitReceive)
