from dataclasses import dataclass, field
from typing import Any, Optional

from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY


@dataclass(frozen=True)
class BooleanOption(OptionDescription):
    invert: bool


def boolean_option(
    text: str,
    page: str,
    section: str,
    default: bool,
    invert: bool = False,
    detail: Optional[str] = None,
    tooltip: Optional[str] = None,
    causes_expensive_game_update: bool = False,
    **kwargs: Any,
) -> bool:
    return field(
        metadata={
            SETTING_DESCRIPTION_KEY: BooleanOption(
                page,
                section,
                text,
                detail,
                tooltip,
                causes_expensive_game_update,
                invert,
            )
        },
        default=default,
        **kwargs,
    )
