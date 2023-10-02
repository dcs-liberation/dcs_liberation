import pytest

from game.datalink.sourcetracknumber import SourceTrackNumber
from game.datalink.sourcetracknumberprefix import SourceTrackNumberPrefix


def test_limits() -> None:
    SourceTrackNumber(SourceTrackNumberPrefix(0), 0)
    SourceTrackNumber(SourceTrackNumberPrefix(0o7777), 7)
    with pytest.raises(ValueError):
        SourceTrackNumber(SourceTrackNumberPrefix(0), -1)
    with pytest.raises(ValueError):
        SourceTrackNumber(SourceTrackNumberPrefix(0o7777), 0o10)


def test_str() -> None:
    assert str(SourceTrackNumber(SourceTrackNumberPrefix(0), 0)) == "00000"
    assert str(SourceTrackNumber(SourceTrackNumberPrefix(0o123), 4)) == "01234"
    assert str(SourceTrackNumber(SourceTrackNumberPrefix(0o7777), 7)) == "77777"


def test_repr() -> None:
    assert (
        repr(SourceTrackNumber(SourceTrackNumberPrefix(0), 0))
        == "SourceTrackNumber(SourceTrackNumberPrefix(0o0), 0)"
    )
    assert (
        repr(SourceTrackNumber(SourceTrackNumberPrefix(0o123), 4))
        == "SourceTrackNumber(SourceTrackNumberPrefix(0o123), 4)"
    )
    assert (
        repr(SourceTrackNumber(SourceTrackNumberPrefix(0o7777), 7))
        == "SourceTrackNumber(SourceTrackNumberPrefix(0o7777), 7)"
    )
