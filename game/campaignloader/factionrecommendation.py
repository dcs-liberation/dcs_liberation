from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from game.factions import Faction

if TYPE_CHECKING:
    from game.factions.factions import Factions


class FactionRecommendation(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def register_campaign_specific_faction(self, factions: Factions) -> None: ...

    @abstractmethod
    def get_faction(self, factions: Factions) -> Faction: ...

    @staticmethod
    def from_field(
        data: str | dict[str, Any] | None, player: bool
    ) -> FactionRecommendation:
        if data is None:
            name = "USA 2005" if player else "Russia 1990"
            return BuiltinFactionRecommendation(name)
        if isinstance(data, str):
            return BuiltinFactionRecommendation(data)
        return CampaignDefinedFactionRecommendation(Faction.from_dict(data))


class BuiltinFactionRecommendation(FactionRecommendation):
    def register_campaign_specific_faction(self, factions: Factions) -> None:
        pass

    def get_faction(self, factions: Factions) -> Faction:
        return factions.get_by_name(self.name)


class CampaignDefinedFactionRecommendation(FactionRecommendation):
    def __init__(self, faction: Faction) -> None:
        super().__init__(faction.name)
        self.faction = faction

    def register_campaign_specific_faction(self, factions: Factions) -> None:
        factions.add_campaign_defined(self.faction)

    def get_faction(self, factions: Factions) -> Faction:
        return self.faction
