import pytest

from game.datalink.sourcetracknumberprefix import SourceTrackNumberPrefix


def test_limits() -> None:
    SourceTrackNumberPrefix(0)
    SourceTrackNumberPrefix(0o7777)
    with pytest.raises(ValueError):
        SourceTrackNumberPrefix(0o10000)
    with pytest.raises(ValueError):
        SourceTrackNumberPrefix(-1)


def test_str() -> None:
    assert str(SourceTrackNumberPrefix(0)) == "0000"
    assert str(SourceTrackNumberPrefix(0o123)) == "0123"
    assert str(SourceTrackNumberPrefix(0o7777)) == "7777"


def test_repr() -> None:
    assert repr(SourceTrackNumberPrefix(0)) == "SourceTrackNumberPrefix(0o0)"
    assert repr(SourceTrackNumberPrefix(0o123)) == "SourceTrackNumberPrefix(0o123)"
    assert repr(SourceTrackNumberPrefix(0o7777)) == "SourceTrackNumberPrefix(0o7777)"
