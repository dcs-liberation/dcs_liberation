from __future__ import annotations

import datetime
from enum import Enum
import random
from typing import Tuple
from zoneinfo import ZoneInfo

from astral import LocationInfo, sun
from dcs.terrain import Terrain


class TimeOfDay(Enum):
    Dawn = "dawn"
    Day = "day"
    Dusk = "dusk"
    Night = "night"


def _location_info_from_terrain(terrain: Terrain) -> LocationInfo:
    """
    Calculates astral.LocationInfo from terrain centroid.
    Args:
        terrain: pydcs terrain object
    Return:
        astral.LocationInfo from terrain centroid
    """

    latlng = terrain.bounds.center().latlng()
    return LocationInfo(latitude=latlng.lat, longitude=latlng.lng)


def to_datetime(
    time_of_day: TimeOfDay, date: datetime.date, terrain: Terrain, night_disabled: bool
) -> datetime.datetime:
    """
    Converts TimeOfDay to datetime.datetime object.
    Args:
        time_of_day: the TimeOfDay to convert.
        date: the date for the time_of_day. Used to estimate dawn/dusk/sunrise/sunset as these vary throughout the year.
        terrain: pydcs terrain object
        night_disabled: if True, never output a time that is at night.
    Return:
        datetime.datetime object within the TimeOfDay window specified. This time is always on an even hour.
    """

    location = _location_info_from_terrain(terrain)
    day_begin_utc = datetime.datetime.combine(
        date, datetime.time(0)
    ) - terrain.utc_offset.utcoffset(None)
    day_begin_utc = day_begin_utc.replace(tzinfo=ZoneInfo("UTC"))
    try:
        sun_info = sun.sun(location.observer, date=day_begin_utc.date())
    except ValueError:
        # astral throws ValueError when the location is always in day or night at the given date
        # so use hard coded hours.
        if time_of_day == TimeOfDay.Dawn:
            hour = 6
        elif time_of_day == TimeOfDay.Day:
            hour = 12
        elif time_of_day == TimeOfDay.Dusk:
            hour = 18
        else:
            hour = 23
        return datetime.datetime.combine(date, datetime.time(hour))

    if night_disabled:
        # Evenly divide hours between dusk and dawn, less 2 hours so that missions end before dusk.
        hours_per_block = (
            (sun_info["dusk"] - sun_info["dawn"] - datetime.timedelta(hours=1))
            / datetime.timedelta(hours=2)
            / 4.0
        )
        if time_of_day == TimeOfDay.Dawn:
            begin = sun_info["dawn"]
            end = sun_info["dawn"] + datetime.timedelta(hours=hours_per_block)
        elif time_of_day == TimeOfDay.Day:
            begin = sun_info["dawn"] + datetime.timedelta(hours=hours_per_block)
            end = sun_info["dawn"] + datetime.timedelta(hours=2 * hours_per_block)
        elif time_of_day == TimeOfDay.Dusk:
            begin = sun_info["dawn"] + datetime.timedelta(hours=2 * hours_per_block)
            end = sun_info["dawn"] + datetime.timedelta(hours=3 * hours_per_block)
        else:
            begin = sun_info["dawn"] + datetime.timedelta(hours=3 * hours_per_block)
            end = sun_info["dawn"] + datetime.timedelta(hours=4 * hours_per_block)
    else:
        if time_of_day == TimeOfDay.Dawn:
            begin = sun_info["dawn"]
            end = sun_info["sunrise"] + datetime.timedelta(hours=1)
        elif time_of_day == TimeOfDay.Day:
            begin = sun_info["sunrise"] + datetime.timedelta(hours=1)
            end = sun_info["sunset"] - datetime.timedelta(hours=1)
        elif time_of_day == TimeOfDay.Dusk:
            begin = sun_info["sunset"] - datetime.timedelta(hours=1)
            end = sun_info["dusk"]
        else:
            begin = sun_info["dusk"]
            end = day_begin_utc + datetime.timedelta(
                hours=23
            )  # 11pm local time is the latest possible end time to maintain hour blocks
    if begin < day_begin_utc:
        begin += datetime.timedelta(days=1)
    if end < day_begin_utc:
        end += datetime.timedelta(days=1)
    begin_hour = int(round((begin - day_begin_utc).total_seconds() / 3600))
    end_hour = int(round((end - day_begin_utc).total_seconds() / 3600))
    if begin_hour == end_hour:
        hour = begin_hour
    else:
        hour = random.randint(begin_hour, end_hour)
    return datetime.datetime.combine(date, datetime.time(hour))


def from_datetime(time: datetime.datetime, terrain: Terrain) -> TimeOfDay:
    """
    Maps datetime.datetime object to appropriate TimeOfDay enum.

    """
    location = _location_info_from_terrain(terrain)
    utc_time = (time - terrain.utc_offset.utcoffset(None)).replace(
        tzinfo=ZoneInfo("UTC")
    )
    sun_info = sun.sun(location.observer, date=utc_time.date())

    if utc_time < sun_info["dawn"] or utc_time > sun_info["dusk"]:
        return TimeOfDay.Night

    if utc_time > sun_info["dawn"] and utc_time < sun_info[
        "sunrise"
    ] + datetime.timedelta(hours=1):
        return TimeOfDay.Dawn

    if utc_time < sun_info["dusk"] and utc_time > sun_info[
        "sunset"
    ] - datetime.timedelta(hours=1):
        return TimeOfDay.Dusk

    return TimeOfDay.Day
