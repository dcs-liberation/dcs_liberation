from game.lasercodes.lasercoderegistry import LaserCodeRegistry


def test_initial_laser_codes() -> None:
    reg = LaserCodeRegistry()
    assert list(reg.available_codes)[:5] == [1688, 1687, 1686, 1685, 1684]
    assert list(reg.available_codes)[-5:] == [1715, 1714, 1713, 1712, 1711]
    assert len(reg.available_codes) == 192


def test_alloc_laser_code() -> None:
    reg = LaserCodeRegistry()
    assert reg.alloc_laser_code().code == 1688
    assert 1688 not in reg.available_codes
    assert len(reg.available_codes) == 191


def test_release_code() -> None:
    reg = LaserCodeRegistry()
    code = reg.alloc_laser_code()
    code.release()
    assert code.code in reg.available_codes
    assert len(reg.available_codes) == 192
    code.release()
    assert len(reg.available_codes) == 192
