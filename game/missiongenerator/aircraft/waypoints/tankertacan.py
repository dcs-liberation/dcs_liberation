from dcs.task import ActivateBeaconCommand

from game.radio.tacan import TacanBand, TacanChannel

# DCS uses separate beacon system IDs for airborne TACAN X and Y.
AIRBORNE_TACAN_SYSTEM = {
    TacanBand.X: 4,
    TacanBand.Y: 5,
}


def tanker_tacan_beacon(
    tacan: TacanChannel, callsign: str | None, unit_id: int
) -> ActivateBeaconCommand:
    beacon = ActivateBeaconCommand(
        tacan.number,
        tacan.band.value,
        callsign,
        bearing=True,
        unit_id=unit_id,
        aa=True,
    )
    beacon.params["action"]["params"]["system"] = AIRBORNE_TACAN_SYSTEM[tacan.band]
    return beacon
