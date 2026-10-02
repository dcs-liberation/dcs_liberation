from typing import Any

import pytest

from game.missiongenerator.aircraft.waypoints.tankertacan import (
    AIRBORNE_TACAN_SYSTEM,
    tanker_tacan_beacon,
)
from game.radio.tacan import TacanBand, TacanChannel


@pytest.mark.parametrize(
    ("band", "expected_system"),
    [
        (TacanBand.X, 4),
        (TacanBand.Y, 5),
    ],
)
def test_tanker_tacan_beacon_uses_airborne_system_for_band(
    band: TacanBand, expected_system: int
) -> None:
    tacan = TacanChannel(37, band)

    beacon = tanker_tacan_beacon(tacan, "TEX", unit_id=463)

    params: dict[str, Any] = beacon.params["action"]["params"]
    assert params["channel"] == 37
    assert params["modeChannel"] == band.value
    assert params["system"] == expected_system
    assert AIRBORNE_TACAN_SYSTEM[band] == expected_system
