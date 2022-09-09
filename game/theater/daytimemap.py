from dataclasses import dataclass
from datetime import time
from typing import TypeAlias

from game.timeofday import TimeOfDay

TimeRange: TypeAlias = tuple[time, time]


@dataclass(frozen=True)
class DaytimeMap:
    dawn: TimeRange
    day: TimeRange
    dusk: TimeRange
    night: TimeRange

    def __post_init__(self) -> None:
        # Checks that we only are even given whole-hour intervals. There's no reason to
        # not support this eventually, but for now the fact that missions always start
        # on the hour is a nice gameplay property. That'll have to go as a part of the
        # mid-mission starts and removal of turns, but for now we can keep it to
        # preserve the old behavior.
        #
        # Mission start time generation (currently in Conditions.generate_start_time)
        # will need to be updated if and when this changes.
        def check_time_is_hours(descr: str, t: time) -> None:
            if t.minute:
                raise ValueError(
                    f"{descr} has non-zero minutes; only hour intervals are currently "
                    "supported"
                )
            if t.second:
                raise ValueError(
                    f"{descr} has non-zero seconds; only hour intervals are currently "
                    "supported"
                )
            if t.microsecond:
                raise ValueError(
                    f"{descr} has non-zero microseconds; only hour intervals are "
                    "currently supported"
                )

        check_time_is_hours("dawn start", self.dawn[0])
        check_time_is_hours("dawn end", self.dawn[1])
        check_time_is_hours("day start", self.day[0])
        check_time_is_hours("day end", self.day[1])
        check_time_is_hours("dusk start", self.dusk[0])
        check_time_is_hours("dusk end", self.dusk[1])
        check_time_is_hours("night start", self.night[0])
        check_time_is_hours("night end", self.night[1])

    def range_of(self, item: TimeOfDay) -> TimeRange:
        match item:
            case TimeOfDay.Dawn:
                return self.dawn
            case TimeOfDay.Day:
                return self.day
            case TimeOfDay.Dusk:
                return self.dusk
            case TimeOfDay.Night:
                return self.night
            case _:
                raise ValueError(f"Invalid value for TimeOfDay: {item}")

    def best_guess_time_of_day_at(self, at: time) -> TimeOfDay:
        """Returns an approximation of the time of day at the given time.

        This is the best guess because time ranges need not cover the whole day. For the
        Caucasus, for example, dusk ends at 20:00 but night does not begin until 24:00.
        If a time between those hours is given, we call it dusk.
        """
        if self.night[0] < self.dawn[0] and at < self.night[0]:
            # Night happens at or before midnight, so there's a time before dawn but
            # after midnight where it can still be dusk.
            return TimeOfDay.Dusk
        if at < self.dawn[0]:
            return TimeOfDay.Night
        if at < self.day[0]:
            return TimeOfDay.Dawn
        if at < self.dusk[0]:
            return TimeOfDay.Day
        if self.night[0] > self.dusk[0] and at >= self.night[0]:
            # Night happens before midnight, so it might still be dusk or night.
            return TimeOfDay.Night
        # If night starts at or before midnight, and it's at least dusk, it's definitely
        # dusk.
        return TimeOfDay.Dusk
