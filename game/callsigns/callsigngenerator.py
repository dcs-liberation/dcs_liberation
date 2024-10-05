from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from enum import StrEnum

from collections import deque
from typing import Any, List, Optional

from dcs.country import Country
from dcs.countries import countries_by_name

from game.ato.flight import Flight
from game.ato.flighttype import FlightType


MAX_GROUP_ID = 99


class CallsignCategory(StrEnum):
    AIR = "Air"
    TANKERS = "Tankers"
    AWACS = "AWACS"
    GROUND_UNITS = "GroundUnits"
    HELIPADS = "Helipad"
    GRASS_AIRFIELDS = "GrassAirfield"


@dataclass(frozen=True)
class Callsign:
    name: Optional[
        str
    ]  # Callsign name e.g. "Enfield" for western callsigns. None for eastern callsigns.
    group_id: int  # ID of the group e.g. 2 in Enfield-2-3 for western callsigns. First two digits of eastern callsigns.
    unit_id: int  # ID of the unit e.g. 3 in Enfield-2-3 for western callsigns. Last digit of eastern callsigns.

    def __post_init__(self) -> None:
        if self.group_id < 1 or self.group_id > MAX_GROUP_ID:
            raise ValueError(
                f"Invalid group ID {self.group_id}. Group IDs have to be between 1 and {MAX_GROUP_ID}."
            )
        if self.unit_id < 1 or self.unit_id > 9:
            raise ValueError(
                f"Invalid unit ID {self.unit_id}. Unit IDs have to be between 1 and 9."
            )

    def __str__(self) -> str:
        if self.name is not None:
            return f"{self.name}{self.group_id}{self.unit_id}"
        else:
            return str(self.group_id * 10 + self.unit_id)

    def lead_callsign(self) -> Callsign:
        return Callsign(self.name, self.group_id, 1)

    def unit_callsign(self, unit_id: int) -> Callsign:
        return Callsign(self.name, self.group_id, unit_id)

    def group_name(self) -> str:
        if self.name is not None:
            return f"{self.name}-{self.group_id}"
        else:
            return str(self.lead_callsign())

    def pydcs_dict(self, country: str) -> dict[Any, Any]:
        country_obj = countries_by_name[country]()
        for category in CallsignCategory:
            if category in country_obj.callsign:
                for index, name in enumerate(country_obj.callsign[category]):
                    if name == self.name:
                        return {
                            "name": str(self),
                            1: index + 1,
                            2: self.group_id,
                            3: self.unit_id,
                        }
        raise ValueError(f"Could not find callsign {name} in {country}.")


class WesternGroupIdRegistry:

    def __init__(self, country: Country, max_group_id: int = MAX_GROUP_ID):
        self._names: dict[str, deque[int]] = {}
        for category in CallsignCategory:
            if category in country.callsign:
                for name in country.callsign[category]:
                    self._names[name] = deque()
        self._max_group_id = max_group_id
        self.reset()

    def reset(self) -> None:
        for name in self._names:
            self._names[name] = deque()
            for i in range(
                self._max_group_id, 0, -1
            ):  # Put group IDs on FIFO queue so 1 gets popped first
                self._names[name].appendleft(i)

    def alloc_group_id(self, name: str) -> int:
        return self._names[name].popleft()

    def release_group_id(self, callsign: Callsign) -> None:
        if callsign.name is None:
            raise ValueError("Releasing eastern callsign")
        self._names[callsign.name].appendleft(callsign.group_id)


class EasternGroupIdRegistry:

    def __init__(self, max_group_id: int = MAX_GROUP_ID):
        self._max_group_id = max_group_id
        self._queue: deque[int] = deque()
        self.reset()

    def reset(self) -> None:
        self._queue = deque()
        for i in range(
            self._max_group_id, 0, -1
        ):  # Put group IDs on FIFO queue so 1 gets popped first
            self._queue.appendleft(i)

    def alloc_group_id(self) -> int:
        return self._queue.popleft()

    def release_group_id(self, callsign: Callsign) -> None:
        self._queue.appendleft(callsign.group_id)


class RoundRobinNameAllocator:

    def __init__(self, names: List[str]):
        self.names = names
        self._index = 0

    def allocate(self) -> str:
        this_index = self._index
        if this_index == len(self.names) - 1:
            self._index = 0
        else:
            self._index += 1
        return self.names[this_index]


class FlightTypeNameAllocator:
    def __init__(self, names: List[str]):
        self.names = names

    def allocate(self, flight: Flight) -> str:
        index = self.FLIGHT_TYPE_LOOKUP.get(flight.flight_type, 0)
        return self.names[index]

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


class WesternFlightCallsignGenerator:
    """Generate western callsign for lead unit in a group"""

    def __init__(self, country: str) -> None:
        self._country = countries_by_name[country]()
        self._group_id_registry = WesternGroupIdRegistry(self._country)
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
            name = self._awacs_name_allocator.allocate()
        elif flight.flight_type == FlightType.REFUELING:
            if self._tankers_name_allocator is None:
                raise ValueError(f"{self._country.name} does not have tanker callsigns")
            name = self._tankers_name_allocator.allocate()
        else:
            name = self._air_name_allocator.allocate(flight)
        group_id = self._group_id_registry.alloc_group_id(name)
        return Callsign(name, group_id, 1)

    def release_callsign(self, callsign: Callsign) -> None:
        self._group_id_registry.release_group_id(callsign)


class EasternFlightCallsignGenerator:
    """Generate eastern callsign for lead unit in a group"""

    def __init__(self) -> None:
        self._group_id_registry = EasternGroupIdRegistry()

    def reset(self) -> None:
        self._group_id_registry.reset()

    def alloc_callsign(self, flight: Flight) -> Callsign:
        group_id = self._group_id_registry.alloc_group_id()
        return Callsign(None, group_id, 1)

    def release_callsign(self, callsign: Callsign) -> None:
        self._group_id_registry.release_group_id(callsign)


class FlightCallsignGenerator:

    def __init__(self, country: str):
        self._generators: dict[
            bool, WesternFlightCallsignGenerator | EasternFlightCallsignGenerator
        ] = {
            True: WesternFlightCallsignGenerator(country),
            False: EasternFlightCallsignGenerator(),
        }
        self._use_western_callsigns = countries_by_name[country]().use_western_callsigns

    def reset(self) -> None:
        self._generators[self._use_western_callsigns].reset()

    def alloc_callsign(self, flight: Flight) -> Callsign:
        return self._generators[self._use_western_callsigns].alloc_callsign(flight)

    def release_callsign(self, callsign: Callsign) -> None:
        self._generators[self._use_western_callsigns].release_callsign(callsign)
