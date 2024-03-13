from typing import Any, Optional

from .choicesoption import choices_option


def skill_option(
    text: str,
    page: str,
    section: str,
    default: str,
    detail: Optional[str] = None,
    tooltip: Optional[str] = None,
    **kwargs: Any,
) -> str:
    return choices_option(
        text,
        page,
        section,
        default,
        ["Average", "Good", "High", "Excellent"],
        detail=detail,
        tooltip=tooltip,
        **kwargs,
    )
