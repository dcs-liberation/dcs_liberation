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
                # Can't preserve timedelta until we create some custom serialization for
                # it. The default serialization is as a python object, which isn't
                # allowed in yaml.safe_load because a malicious modification of the
                # settings file would be able to execute arbitrary code.
                remember_player_choice=False,
                min=min,
                max=max,
            )
        },
        default=default,
        **kwargs,
    )
