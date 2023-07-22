import pytest

from game.lasercodes import ILaserCodeRegistry
from game.lasercodes.lasercode import LaserCode


class MockRegistry(ILaserCodeRegistry):
    def __init__(self) -> None:
        self.release_count = 0

    def alloc_laser_code(self) -> LaserCode:
        raise NotImplementedError

    def release_code(self, code: LaserCode) -> None:
        self.release_count += 1


@pytest.fixture(name="registry")
def mock_registry() -> MockRegistry:
    return MockRegistry()


def test_lasercode_code(registry: ILaserCodeRegistry) -> None:

    assert LaserCode(1688, registry).code == 1688

    # 1113 doesn't comply to the rules, but is the only code valid for FC3 aircraft like
    # the A-10A.
    assert LaserCode(1113, registry).code == 1113

    # The first digit must be 1
    with pytest.raises(ValueError):
        # And be exactly 4 digits
        LaserCode(2688, registry)

    # The code must be exactly 4 digits
    with pytest.raises(ValueError):
        LaserCode(888, registry)
    with pytest.raises(ValueError):
        LaserCode(18888, registry)

    # 0 and 9 are invalid digits
    with pytest.raises(ValueError):
        LaserCode(1088, registry)
    with pytest.raises(ValueError):
        LaserCode(1608, registry)
    with pytest.raises(ValueError):
        LaserCode(1680, registry)
    with pytest.raises(ValueError):
        LaserCode(1988, registry)
    with pytest.raises(ValueError):
        LaserCode(1698, registry)
    with pytest.raises(ValueError):
        LaserCode(1689, registry)

    # The second digit is further constrained to be 5, 6, or 7.
    with pytest.raises(ValueError):
        LaserCode(1188, registry)
    with pytest.raises(ValueError):
        LaserCode(1288, registry)
    with pytest.raises(ValueError):
        LaserCode(1388, registry)
    with pytest.raises(ValueError):
        LaserCode(1488, registry)
    with pytest.raises(ValueError):
        LaserCode(1888, registry)


def test_lasercode_release(registry: MockRegistry) -> None:
    code = LaserCode(1688, registry)
    assert registry.release_count == 0
    code.release()
    assert registry.release_count == 1
    code.release()
    assert registry.release_count == 2
