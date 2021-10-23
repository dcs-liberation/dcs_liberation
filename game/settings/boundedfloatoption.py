from dataclasses import dataclass, field
from typing import Any, Optional

from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY


@dataclass(frozen=True)
class BoundedFloatOption(OptionDescription):
    min: float
    max: float
    divisor: int


def bounded_float_option(
    text: str,
    page: str,
    section: str,
    default: float,
    min: float,
    max: float,
    divisor: int,
    detail: Optional[str] = None,
    tooltip: Optional[str] = None,
    **kwargs: Any,
) -> float:
    return field(
        metadata={
            SETTING_DESCRIPTION_KEY: BoundedFloatOption(
                page,
                section,
                text,
                detail,
                tooltip,
                causes_expensive_game_update=False,
                min=min,
                max=max,
                divisor=divisor,
            )
        },
        default=default,
        **kwargs,
    )
