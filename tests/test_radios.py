from typing import Callable

import pytest

from game.radio.radios import MHz, RadioFrequency, kHz


@pytest.mark.parametrize("units,factory", [("kHz", kHz), ("MHz", MHz)])
def test_radio_parsing(units: str, factory: Callable[..., RadioFrequency]) -> None:
    assert RadioFrequency.parse(f"0 {units}") == factory(0)
    assert RadioFrequency.parse(f"0.0 {units}") == factory(0)
    assert RadioFrequency.parse(f"255 {units}") == factory(255)
    assert RadioFrequency.parse(f"255.5 {units}") == factory(255, 500)
    assert RadioFrequency.parse(f"255.500 {units}") == factory(255, 500)
    assert RadioFrequency.parse(f"255.050 {units}") == factory(255, 50)
    assert RadioFrequency.parse(f"255.005 {units}") == factory(255, 5)
    assert RadioFrequency.parse(f"255.0 {units}") == factory(255)

    with pytest.raises(ValueError):
        RadioFrequency.parse("")
    with pytest.raises(ValueError):
        RadioFrequency.parse("255")
    with pytest.raises(ValueError):
        RadioFrequency.parse(f" 255 {units}")
    with pytest.raises(ValueError):
        RadioFrequency.parse(f"255 {units} ")
    with pytest.raises(ValueError):
        RadioFrequency.parse(f"255 {units.lower()}")
    with pytest.raises(ValueError):
        RadioFrequency.parse(f"255. {units}")
    with pytest.raises(ValueError):
        RadioFrequency.parse(f".0 {units}")
    with pytest.raises(ValueError):
        RadioFrequency.parse(f"0. {units}")
    with pytest.raises(ValueError):
        RadioFrequency.parse(f"255.5555 {units}")
