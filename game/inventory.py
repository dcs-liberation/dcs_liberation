"""Inventory management APIs."""
from __future__ import annotations

from collections import defaultdict, Iterator, Iterable
from typing import TYPE_CHECKING

from game.dcs.aircrafttype import AircraftType

if TYPE_CHECKING:
    from game.theater import ControlPoint
    from gen.flights.flight import Flight


class ControlPointAircraftInventory:
    """Aircraft inventory for a single control point."""

    def __init__(self, control_point: ControlPoint) -> None:
        self.control_point = control_point
        self.inventory: dict[AircraftType, int] = defaultdict(int)

    def clone(self) -> ControlPointAircraftInventory:
        new = ControlPointAircraftInventory(self.control_point)
        new.inventory = self.inventory.copy()
        return new

    def add_aircraft(self, aircraft: AircraftType, count: int) -> None:
        """Adds aircraft to the inventory.

        Args:
            aircraft: The type of aircraft to add.
            count: The number of aircraft to add.
        """
        self.inventory[aircraft] += count

    def remove_aircraft(self, aircraft: AircraftType, count: int) -> None:
        """Removes aircraft from the inventory.

        Args:
            aircraft: The type of aircraft to remove.
            count: The number of aircraft to remove.

        Raises:
            ValueError: The control point cannot fulfill the requested number of
            aircraft.
        """
        available = self.inventory[aircraft]
        if available < count:
            raise ValueError(
                f"Cannot remove {count} {aircraft} from "
                f"{self.control_point.name}. Only have {available}."
            )
        self.inventory[aircraft] -= count

    def available(self, aircraft: AircraftType) -> int:
        """Returns the number of available aircraft of the given type.

        Args:
            aircraft: The type of aircraft to query.
        """
        try:
            return self.inventory[aircraft]
        except KeyError:
            return 0

    @property
    def types_available(self) -> Iterator[AircraftType]:
        """Iterates over all available aircraft types."""
        for aircraft, count in self.inventory.items():
            if count > 0:
                yield aircraft

    @property
    def all_aircraft(self) -> Iterator[tuple[AircraftType, int]]:
        """Iterates over all available aircraft types, including amounts."""
        for aircraft, count in self.inventory.items():
            if count > 0:
                yield aircraft, count

    def clear(self) -> None:
        """Clears all aircraft from the inventory."""
        self.inventory.clear()


class GlobalAircraftInventory:
    """Game-wide aircraft inventory."""

    def __init__(self, control_points: Iterable[ControlPoint]) -> None:
        self.inventories: dict[ControlPoint, ControlPointAircraftInventory] = {
            cp: ControlPointAircraftInventory(cp) for cp in control_points
        }

    def clone(self) -> GlobalAircraftInventory:
        new = GlobalAircraftInventory([])
        new.inventories = {
            cp: inventory.clone() for cp, inventory in self.inventories.items()
        }
        return new

    def reset(self, for_player: bool) -> None:
        """Clears the inventory of every control point owned by the given coalition."""
        for inventory in self.inventories.values():
            if inventory.control_point.captured == for_player:
                inventory.clear()

    def set_from_control_point(self, control_point: ControlPoint) -> None:
        """Set the control point's aircraft inventory.

        If the inventory for the given control point has already been set for
        the turn, it will be overwritten.
        """
        inventory = self.inventories[control_point]
        for aircraft, count in control_point.base.aircraft.items():
            inventory.add_aircraft(aircraft, count)

    def for_control_point(
        self, control_point: ControlPoint
    ) -> ControlPointAircraftInventory:
        """Returns the inventory specific to the given control point."""
        return self.inventories[control_point]

    @property
    def available_types_for_player(self) -> Iterator[AircraftType]:
        """Iterates over all aircraft types available to the player."""
        seen: set[AircraftType] = set()
        for control_point, inventory in self.inventories.items():
            if control_point.captured:
                for aircraft in inventory.types_available:
                    if not control_point.can_operate(aircraft):
                        continue
                    if aircraft not in seen:
                        seen.add(aircraft)
                        yield aircraft

    def claim_for_flight(self, flight: Flight) -> None:
        """Removes aircraft from the inventory for the given flight."""
        inventory = self.for_control_point(flight.from_cp)
        inventory.remove_aircraft(flight.unit_type, flight.count)

    def return_from_flight(self, flight: Flight) -> None:
        """Returns a flight's aircraft to the inventory."""
        inventory = self.for_control_point(flight.from_cp)
        inventory.add_aircraft(flight.unit_type, flight.count)
