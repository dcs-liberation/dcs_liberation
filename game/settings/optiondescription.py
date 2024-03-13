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

    # If True, the player's selection for this value will be saved to settings.yaml in
    # the Liberation user directory when a new game is created, and those values will be
    # used by default for new games. This is conditional because many settings are not
    # appropriate for cross-game persistence (economy settings are, for example, usually
    # hinted by the campaign itself).
    remember_player_choice: bool
