"""Maps generated units back to their Liberation types."""
from typing import Dict, Optional

from dcs.unitgroup import FlyingGroup

from game.theater import Airfield
from gen.flights.flight import Flight


class UnitMap:
    def __init__(self) -> None:
        self.aircraft: Dict[str, Flight] = {}
        self.airfields: Dict[str, Airfield] = {}

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

    def add_airfield(self, airfield: Airfield) -> None:
        if airfield.name in self.airfields:
            raise RuntimeError(f"Duplicate airfield: {airfield.name}")
        self.airfields[airfield.name] = airfield

    def airfield(self, name: str) -> Optional[Airfield]:
        return self.airfields.get(name, None)
