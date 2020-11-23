"""Maps generated units back to their Liberation types."""
from typing import Dict, Optional

from dcs.unitgroup import FlyingGroup

from gen.flights.flight import Flight


class UnitMap:
    def __init__(self) -> None:
        self.aircraft: Dict[str, Flight] = {}

    def add_aircraft(self, group: FlyingGroup, flight: Flight) -> None:
        for unit in group.units:
            # The actual name is a String (the pydcs translatable string), which
            # doesn't define __eq__.
            name = str(unit.name)
            if name in self.aircraft:
                raise RuntimeError(f"Duplicate unit name: {name}")
            self.aircraft[name] = flight

    def flight(self, unit_name: str) -> Optional[Flight]:
        return self.aircraft.get(unit_name, None)
