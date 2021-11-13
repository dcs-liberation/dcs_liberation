from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.squadrons import Squadron, Pilot


class FlightRoster:
    def __init__(self, squadron: Squadron, initial_size: int = 0) -> None:
        self.squadron = squadron
        self.pilots: list[Optional[Pilot]] = []
        self.resize(initial_size)

    @property
    def max_size(self) -> int:
        return len(self.pilots)

    @property
    def player_count(self) -> int:
        return len([p for p in self.pilots if p is not None and p.player])

    @property
    def missing_pilots(self) -> int:
        return len([p for p in self.pilots if p is None])

    def resize(self, new_size: int) -> None:
        if self.max_size > new_size:
            self.squadron.return_pilots(
                [p for p in self.pilots[new_size:] if p is not None]
            )
            self.pilots = self.pilots[:new_size]
            return
        self.pilots.extend(
            [
                self.squadron.claim_available_pilot()
                for _ in range(new_size - self.max_size)
            ]
        )

    def set_pilot(self, index: int, pilot: Optional[Pilot]) -> None:
        if pilot is not None:
            self.squadron.claim_pilot(pilot)
        if (current_pilot := self.pilots[index]) is not None:
            self.squadron.return_pilot(current_pilot)
        self.pilots[index] = pilot

    def clear(self) -> None:
        self.squadron.return_pilots([p for p in self.pilots if p is not None])
