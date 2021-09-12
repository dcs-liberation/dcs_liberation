from typing import Any, Optional

from .choicesoption import choices_option


def skill_option(
    text: str,
    page: str,
    section: str,
    detail: Optional[str] = None,
    **kwargs: Any,
) -> str:
    return choices_option(
        text,
        page,
        section,
        ["Average", "Good", "High", "Excellent"],
        detail=detail,
        **kwargs,
    )
