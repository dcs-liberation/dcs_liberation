import pytest

from dcs.countries import countries_by_name

from game.callsigns.callsigngenerator import (
    Callsign,
    EasternGroupIdRegistry,
    WesternGroupIdRegistry,
    RoundRobinNameAllocator,
)


def test_callsign() -> None:

    valid_callsign = Callsign("Enfield", 2, 3)
    assert str(valid_callsign) == "Enfield23"
    assert valid_callsign.group_name() == "Enfield-2"
    assert valid_callsign.pydcs_dict("USA") == {"name": "Enfield23", 1: 1, 2: 2, 3: 3}

    # Invalid callsign, group ID too large.
    with pytest.raises(ValueError):
        Callsign("Enfield", 1000, 3)

    # Invalid callsign, group ID zero.
    with pytest.raises(ValueError):
        Callsign("Enfield", 0, 3)

    # Invalid callsign, unit ID zero.
    with pytest.raises(ValueError):
        Callsign("Enfield", 1, 0)

    # Invalid callsign, unit ID too large.
    with pytest.raises(ValueError):
        Callsign("Enfield", 1, 11)


def test_western_group_id_registry() -> None:
    registry = WesternGroupIdRegistry(countries_by_name["USA"]())

    # Check registry increments group IDs.
    assert registry.alloc_group_id("Enfield") == 1
    assert registry.alloc_group_id("Enfield") == 2

    # Check allocation on a new name Springfield.
    assert registry.alloc_group_id("Springfield") == 1

    # Check release of Enfield-1.
    registry.release_group_id(Callsign("Enfield", 1, 1))
    assert registry.alloc_group_id("Enfield") == 1

    # Reset and check allocation og Enfield-1 and Springfield-1.
    registry.reset()
    assert registry.alloc_group_id("Enfield") == 1
    assert registry.alloc_group_id("Springfield") == 1


def test_eastern_group_id_registry() -> None:
    registry = EasternGroupIdRegistry()

    # Check registry increments group IDs.
    assert registry.alloc_group_id() == 1
    assert registry.alloc_group_id() == 2

    # Check release.
    registry.release_group_id(Callsign(None, 1, 1))
    assert registry.alloc_group_id() == 1

    # Reset and check allocation.
    registry.reset()
    assert registry.alloc_group_id() == 1


def test_round_robin_allocator() -> None:
    allocator = RoundRobinNameAllocator(["A", "B", "C"])

    assert allocator.allocate() == "A"
    assert allocator.allocate() == "B"
    assert allocator.allocate() == "C"
    assert allocator.allocate() == "A"
