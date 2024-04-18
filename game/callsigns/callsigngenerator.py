from dataclasses import dataclass
from enum import StrEnum
from collections import deque
from typing import Any, List, Optional

from dcs.country import Country
from dcs.countries import countries_by_name

from game.ato.flight import Flight
from game.ato.flighttype import FlightType


MAX_GROUP_ID = 999


@dataclass(frozen=True)
class Callsign:
    name: str
    index: int
    group_id: int
    unit_id: int

    def __post_init__(self) -> None:
        if self.group_id < 1 or self.group_id > MAX_GROUP_ID:
            raise ValueError(
                f"Invalid group ID {self.group_id}. Group IDs have to be between 1 and 999."
            )
        if self.unit_id < 1 or self.unit_id > 9:
            raise ValueError(
                f"Invalid unit ID {self.unit_id}. Unit IDs have to be between 1 and 9."
            )

    def __str__(self) -> str:
        return f"{self.name}{self.group_id}{self.unit_id}"
        
    def group_callsign(self) -> str:
        return f"{self.name}-{self.group_id}"
        
    def pydcs_dict(self) -> dict[Any, Any]:
        return { "name": str(self),
                 1: self.index,
                 2: self.group_id,
                 3: self.unit_id }


class CallsignCategory(StrEnum):
    AIR = "Air"
    TANKERS = "Tankers"
    AWACS = "AWACS"
    GROUND_UNITS = "GroundUnits"
    HELIPADS = "Helipad"
    GRASS_AIRFIELDS = "GrassAirfield"


class GroupIdRegistry:

    def __init__(self, country: Country):
        self._names: dict[str, deque[int]] = {}
        for category in [
            CallsignCategory.AIR,
            CallsignCategory.TANKERS,
            CallsignCategory.AWACS,
            CallsignCategory.GROUND_UNITS,
            CallsignCategory.HELIPADS,
            CallsignCategory.GRASS_AIRFIELDS,
        ]:
            if category in country.callsign:
                for name in country.callsign[category]:
                    self._names[name] = deque()
        self.reset()

    def reset(self) -> None:
        for name in self._names:
            self._names[name] = deque()
            for i in range(
                MAX_GROUP_ID, 0, -1
            ):  # Put group IDs on FIFO queue so 1 gets popped first
                self._names[name].appendleft(i)

    def alloc_group_id(self, name: str) -> int:
        return self._names[name].popleft()

    def release_group_id(self, callsign: Callsign) -> None:
        self._names[callsign.name].appendleft(callsign.group_id)


class RoundRobinNameAllocator:

    def __init__(self, names: List[str]):
        self.names = names
        self._index = 0

    def allocate(self) -> tuple[str, int]:
        this_index = self._index
        if this_index == len(self.names) - 1:
            self._index = 0
        else:
            self._index += 1
        return self.names[this_index], this_index + 1


class FlightTypeNameAllocator:
    def __init__(self, names: List[str]):
        self.names = names

    def allocate(self, flight: Flight) -> tuple[str, int]:
        index = self.FLIGHT_TYPE_LOOKUP.get(flight.flight_type, 0)
        return self.names[index], index + 1

    FLIGHT_TYPE_LOOKUP: dict[FlightType, int] = {
        FlightType.TARCAP: 1,
        FlightType.BARCAP: 1,
        FlightType.INTERCEPTION: 1,
        FlightType.SWEEP: 1,
        FlightType.CAS: 2,
        FlightType.ANTISHIP: 2,
        FlightType.BAI: 2,
        FlightType.STRIKE: 3,
        FlightType.OCA_RUNWAY: 3,
        FlightType.OCA_AIRCRAFT: 3,
        FlightType.SEAD: 4,
        FlightType.DEAD: 4,
        FlightType.ESCORT: 5,
        FlightType.AIR_ASSAULT: 6,
        FlightType.TRANSPORT: 7,
        FlightType.FERRY: 7,
    }


class FlightCallsignGenerator:
    """Generate callsign for lead unit in a group"""

    def __init__(self, country: str):
        self._country = countries_by_name[country]()
    
        self._group_id_registry = GroupIdRegistry(self._country)
        self._awacs_name_allocator = None
        self._tankers_name_allocator = None
        
        if CallsignCategory.AWACS in self._country.callsign:
            self._awacs_name_allocator = RoundRobinNameAllocator(
                self._country.callsign[CallsignCategory.AWACS]
            )
        if CallsignCategory.TANKERS in self._country.callsign:
            self._tankers_name_allocator = RoundRobinNameAllocator(
                self._country.callsign[CallsignCategory.TANKERS]
            )
        self._air_name_allocator = FlightTypeNameAllocator(
            self._country.callsign[CallsignCategory.AIR]
        )

    def reset(self) -> None:
        self._group_id_registry.reset()

    def alloc_callsign(self, flight: Flight) -> Callsign:
        if flight.flight_type == FlightType.AEWC:
            if self._awacs_name_allocator is None:
                raise ValueError(f"{self._country.name} does not have AWACs callsigns")
            name, index = self._awacs_name_allocator.allocate()
        elif flight.flight_type == FlightType.REFUELING:
            if self._tankers_name_allocator is None:
                raise ValueError(f"{self._country.name} does not have tanker callsigns")
            name, index = self._tankers_name_allocator.allocate()
        else:
            name, index = self._air_name_allocator.allocate(flight)
        group_id = self._group_id_registry.alloc_group_id(name)
        return Callsign(name, index, group_id, 1)

    def release_callsign(self, callsign: Callsign) -> None:
        self._group_id_registry.release_group_id(callsign)
