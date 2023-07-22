from __future__ import annotations

from collections.abc import Iterator
from typing import Optional, TYPE_CHECKING

from .flightmember import FlightMember
from .flightroster import FlightRoster
from .iflightroster import IFlightRoster
from .loadouts import Loadout

if TYPE_CHECKING:
    from game.squadrons import Pilot
    from .flight import Flight


class FlightMembers(IFlightRoster):
    def __init__(self, flight: Flight, initial_size: int = 0) -> None:
        self.flight = flight
        self.members: list[FlightMember] = []
        self.resize(initial_size)

    @staticmethod
    def from_roster(flight: Flight, roster: FlightRoster) -> FlightMembers:
        members = FlightMembers(flight)
        loadout = Loadout.default_for(flight)
        members.members = [FlightMember(p, loadout) for p in roster.pilots]
        return members

    def iter_pilots(self) -> Iterator[Pilot | None]:
        yield from (m.pilot for m in self.members)

    def pilot_at(self, idx: int) -> Pilot | None:
        return self.members[idx].pilot

    @property
    def max_size(self) -> int:
        return len(self.members)

    @property
    def player_count(self) -> int:
        return len([m for m in self.members if m.is_player])

    @property
    def missing_pilots(self) -> int:
        return len([m for m in self.members if m.pilot is None])

    def resize(self, new_size: int) -> None:
        if self.max_size > new_size:
            for member in self.members[new_size:]:
                if (pilot := member.pilot) is not None:
                    self.flight.squadron.return_pilot(pilot)
                if (code := member.tgp_laser_code) is not None:
                    code.release()
            self.members = self.members[:new_size]
            return
        if self.max_size:
            loadout = self.members[0].loadout.clone()
        else:
            loadout = Loadout.default_for(self.flight)
        for _ in range(new_size - self.max_size):
            member = FlightMember(self.flight.squadron.claim_available_pilot(), loadout)
            member.use_custom_loadout = loadout.is_custom
            self.members.append(member)

    def set_pilot(self, index: int, pilot: Optional[Pilot]) -> None:
        if pilot is not None:
            self.flight.squadron.claim_pilot(pilot)
        if (current_pilot := self.pilot_at(index)) is not None:
            self.flight.squadron.return_pilot(current_pilot)
        self.members[index].pilot = pilot

    def clear(self) -> None:
        self.flight.squadron.return_pilots(
            [p for p in self.iter_pilots() if p is not None]
        )
        for member in self.members:
            if (code := member.tgp_laser_code) is not None:
                code.release()

    def use_same_loadout_for_all_members(self) -> None:
        if not self.members:
            return
        loadout = self.members[0].loadout
        for member in self.members[1:]:
            member.loadout = loadout.clone()
