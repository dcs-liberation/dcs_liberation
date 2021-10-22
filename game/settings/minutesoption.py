from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Optional

from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY


@dataclass(frozen=True)
class MinutesOption(OptionDescription):
    min: int
    max: int


def minutes_option(
    text: str,
    page: str,
    section: str,
    default: timedelta,
    min: int,
    max: int,
    detail: Optional[str] = None,
    tooltip: Optional[str] = None,
    **kwargs: Any,
) -> timedelta:
    return field(
        metadata={
            SETTING_DESCRIPTION_KEY: MinutesOption(
                page,
                section,
                text,
                detail,
                tooltip,
                causes_expensive_game_update=False,
                min=min,
                max=max,
            )
        },
        default=default,
        **kwargs,
    )
