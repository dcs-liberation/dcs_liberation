from game.sidc import (
    LandInstallationEntity,
    StandardIdentity,
    Status,
    SymbolIdentificationCode,
    SymbolSet,
)


def test_sidc() -> None:
    sidc = SymbolIdentificationCode(
        standard_identity=StandardIdentity.FRIEND,
        symbol_set=SymbolSet.LAND_INSTALLATIONS,
        status=Status.PRESENT_DAMAGED,
        entity=LandInstallationEntity.AIPORT_AIR_BASE,
    )
    assert str(sidc) == "10032030001213010000"
