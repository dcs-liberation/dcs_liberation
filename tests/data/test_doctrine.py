import pytest

from game.data.doctrine import Doctrine, GroundUnitProcurementRatios
from game.data.units import UnitClass


def test_ground_unit_procurement_ratios_empty() -> None:
    r = GroundUnitProcurementRatios({})
    for unit_class in UnitClass:
        assert r.for_unit_class(unit_class) == 0.0


def test_ground_unit_procurement_ratios_single_item() -> None:
    r = GroundUnitProcurementRatios({UnitClass.TANK: 1})
    for unit_class in UnitClass:
        if unit_class == UnitClass.TANK:
            assert r.for_unit_class(unit_class) == 1.0
        else:
            assert r.for_unit_class(unit_class) == 0.0


def test_ground_unit_procurement_ratios_multiple_items() -> None:
    r = GroundUnitProcurementRatios({UnitClass.TANK: 1, UnitClass.ATGM: 1})
    for unit_class in UnitClass:
        if unit_class in [UnitClass.TANK, UnitClass.ATGM]:
            assert r.for_unit_class(unit_class) == 0.5
        else:
            assert r.for_unit_class(unit_class) == 0.0


def test_ground_unit_procurement_ratios_from_dict() -> None:
    r = GroundUnitProcurementRatios.from_dict({"Tank": 1, "ATGM": 1})
    for unit_class in UnitClass:
        if unit_class in [UnitClass.TANK, UnitClass.ATGM]:
            assert r.for_unit_class(unit_class) == 0.5
        else:
            assert r.for_unit_class(unit_class) == 0.0


def test_doctrine() -> None:
    # This test checks for the presence of a doctrine named "modern" as this doctrine is used as a default
    modern_doctrine = Doctrine.named("modern")
    assert modern_doctrine.name == "modern"
