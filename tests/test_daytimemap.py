from datetime import time

import pytest

from game.theater.daytimemap import DaytimeMap
from game.timeofday import TimeOfDay


def test_range_of() -> None:
    m = DaytimeMap(
        dawn=(time(hour=6), time(hour=9)),
        day=(time(hour=9), time(hour=18)),
        dusk=(time(hour=18), time(hour=20)),
        night=(time(hour=0), time(hour=5)),
    )

    assert m.range_of(TimeOfDay.Dawn) == (time(hour=6), time(hour=9))
    assert m.range_of(TimeOfDay.Day) == (time(hour=9), time(hour=18))
    assert m.range_of(TimeOfDay.Dusk) == (time(hour=18), time(hour=20))
    assert m.range_of(TimeOfDay.Night) == (time(hour=0), time(hour=5))


def test_best_guess_time_of_day_at() -> None:
    night_at_midnight = DaytimeMap(
        dawn=(time(hour=6), time(hour=9)),
        day=(time(hour=9), time(hour=18)),
        dusk=(time(hour=18), time(hour=20)),
        night=(time(hour=0), time(hour=5)),
    )

    assert night_at_midnight.best_guess_time_of_day_at(time(hour=0)) == TimeOfDay.Night
    assert night_at_midnight.best_guess_time_of_day_at(time(hour=5)) == TimeOfDay.Night
    assert night_at_midnight.best_guess_time_of_day_at(time(hour=6)) == TimeOfDay.Dawn
    assert night_at_midnight.best_guess_time_of_day_at(time(hour=7)) == TimeOfDay.Dawn
    assert night_at_midnight.best_guess_time_of_day_at(time(hour=9)) == TimeOfDay.Day
    assert night_at_midnight.best_guess_time_of_day_at(time(hour=10)) == TimeOfDay.Day
    assert night_at_midnight.best_guess_time_of_day_at(time(hour=18)) == TimeOfDay.Dusk
    assert night_at_midnight.best_guess_time_of_day_at(time(hour=19)) == TimeOfDay.Dusk

    night_before_midnight = DaytimeMap(
        dawn=(time(hour=6), time(hour=9)),
        day=(time(hour=9), time(hour=18)),
        dusk=(time(hour=18), time(hour=20)),
        night=(time(hour=22), time(hour=5)),
    )

    assert (
        night_before_midnight.best_guess_time_of_day_at(time(hour=0)) == TimeOfDay.Night
    )
    assert (
        night_before_midnight.best_guess_time_of_day_at(time(hour=1)) == TimeOfDay.Night
    )
    assert (
        night_before_midnight.best_guess_time_of_day_at(time(hour=22))
        == TimeOfDay.Night
    )
    assert (
        night_before_midnight.best_guess_time_of_day_at(time(hour=23))
        == TimeOfDay.Night
    )
    assert (
        night_before_midnight.best_guess_time_of_day_at(time(hour=6)) == TimeOfDay.Dawn
    )

    night_after_midnight = DaytimeMap(
        dawn=(time(hour=6), time(hour=9)),
        day=(time(hour=9), time(hour=18)),
        dusk=(time(hour=18), time(hour=20)),
        night=(time(hour=2), time(hour=5)),
    )

    assert (
        night_after_midnight.best_guess_time_of_day_at(time(hour=0)) == TimeOfDay.Dusk
    )
    assert (
        night_after_midnight.best_guess_time_of_day_at(time(hour=23)) == TimeOfDay.Dusk
    )
    assert (
        night_after_midnight.best_guess_time_of_day_at(time(hour=2)) == TimeOfDay.Night
    )
    assert (
        night_after_midnight.best_guess_time_of_day_at(time(hour=6)) == TimeOfDay.Dawn
    )


def test_whole_hours_only() -> None:
    with pytest.raises(ValueError):
        DaytimeMap(
            dawn=(time(minute=6), time(hour=9)),
            day=(time(hour=9), time(hour=18)),
            dusk=(time(hour=18), time(hour=20)),
            night=(time(hour=2), time(hour=5)),
        )
    with pytest.raises(ValueError):
        DaytimeMap(
            dawn=(time(hour=6), time(hour=9)),
            day=(time(second=9), time(hour=18)),
            dusk=(time(hour=18), time(hour=20)),
            night=(time(hour=2), time(hour=5)),
        )
    with pytest.raises(ValueError):
        DaytimeMap(
            dawn=(time(hour=6), time(hour=9)),
            day=(time(hour=9), time(hour=18)),
            dusk=(time(hour=18), time(microsecond=20)),
            night=(time(hour=2), time(hour=5)),
        )
