from dataclasses import dataclass, field
from typing import Any, Optional

from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY


@dataclass(frozen=True)
class BoundedIntOption(OptionDescription):
    min: int
    max: int


def bounded_int_option(
    text: str,
    page: str,
    section: str,
    default: int,
    min: int,
    max: int,
    detail: Optional[str] = None,
    **kwargs: Any,
) -> int:
    return field(
        metadata={
            SETTING_DESCRIPTION_KEY: BoundedIntOption(
                page, section, text, detail, min, max
            )
        },
        default=default,
        **kwargs,
    )
