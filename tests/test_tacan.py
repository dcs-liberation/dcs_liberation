from gen.tacan import TacanBand, TacanChannel, TacanChannelForbiddenError, TacanChannelInUseError, TacanRegistry, TacanUsage
import unittest

class TestTacanRegistry(unittest.TestCase):
    def setUp(self):
        pass

    def test_allocate_first_few_channels(self):
        registry = TacanRegistry()
        chan1 = registry.alloc_for_band(TacanBand.X)
        chan2 = registry.alloc_for_band(TacanBand.X)
        chan3 = registry.alloc_for_band(TacanBand.X)
        self.assertEqual(chan1, TacanChannel(1, TacanBand.X))
        self.assertEqual(chan2, TacanChannel(31, TacanBand.X))
        self.assertEqual(chan3, TacanChannel(32, TacanBand.X))

    def test_reserve_invalid_tr_channels(self):
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
            try:
                registry.reserve(chan, TacanUsage.TransmitReceive)
                self.fail(f"Should have raised error for {chan}")
            except TacanChannelForbiddenError:
                pass

    def test_reserve_invalid_a2a_channels(self):
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
            try:
                registry.reserve(chan, TacanUsage.AirToAir)
                self.fail(f"Should have raised error for {chan}")
            except TacanChannelForbiddenError:
                pass

    def test_reserve_again(self):
        registry = TacanRegistry()
        try:
            registry.reserve(TacanChannel(1, TacanBand.X))
            registry.reserve(TacanChannel(1, TacanBand.X))
            self.fail(f"Should have raised error")
        except TacanChannelInUseError:
            pass

