from __future__ import annotations

from collections.abc import Iterator
from typing import Optional, TYPE_CHECKING

from game.ato.iflightroster import IFlightRoster

if TYPE_CHECKING:
    from game.squadrons import Squadron, Pilot


class FlightRoster(IFlightRoster):
    def __init__(self, squadron: Squadron, initial_size: int = 0) -> None:
        self.squadron = squadron
        self.pilots: list[Optional[Pilot]] = []
        self.resize(initial_size)

    def iter_pilots(self) -> Iterator[Pilot | None]:
        yield from self.pilots

    def pilot_at(self, idx: int) -> Pilot | None:
        return self.pilots[idx]

    @property
    def max_size(self) -> int:
        return len(self.pilots)

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
