from dataclasses import dataclass
from typing import Optional


SETTING_DESCRIPTION_KEY = "DCS_LIBERATION_SETTING_DESCRIPTION_KEY"


@dataclass(frozen=True)
class OptionDescription:
    page: str
    section: str
    text: str
    detail: Optional[str]
    tooltip: Optional[str]
    causes_expensive_game_update: bool
