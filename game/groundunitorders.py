from __future__ import annotations

import logging
from collections import defaultdict
from typing import Optional, TYPE_CHECKING

from game.theater import ControlPoint
from .coalition import Coalition
from .dcs.groundunittype import GroundUnitType
from .theater.transitnetwork import (
    NoPathError,
    TransitNetwork,
)
from .transfers import TransferOrder

if TYPE_CHECKING:
    from .game import Game


class GroundUnitOrders:
    def __init__(self, destination: ControlPoint) -> None:
        self.destination = destination

        # Maps unit type to order quantity.
        self.units: dict[GroundUnitType, int] = defaultdict(int)

    def __str__(self) -> str:
        return f"Pending ground unit delivery to {self.destination}"

    def order(self, units: dict[GroundUnitType, int]) -> None:
        for k, v in units.items():
            self.units[k] += v

    def sell(self, units: dict[GroundUnitType, int]) -> None:
        for k, v in units.items():
            self.units[k] -= v
            if self.units[k] == 0:
                del self.units[k]

    def refund_all(self, coalition: Coalition) -> None:
        self._refund(coalition, self.units)
        self.units = defaultdict(int)

    def _refund(self, coalition: Coalition, units: dict[GroundUnitType, int]) -> None:
        for unit_type, count in units.items():
            logging.info(f"Refunding {count} {unit_type} at {self.destination.name}")
            coalition.adjust_budget(unit_type.price * count)

    def pending_orders(self, unit_type: GroundUnitType) -> int:
        pending_units = self.units.get(unit_type)
        if pending_units is None:
            pending_units = 0
        return pending_units

    def process(self, game: Game) -> None:
        coalition = game.coalition_for(self.destination.captured)
        ground_unit_source = self.find_ground_unit_source(game)
        if ground_unit_source is None:
            game.message(
                f"{self.destination.name} lost its source for ground unit "
                "reinforcements. Refunding purchase price."
            )
            self.refund_all(coalition)

        bought_units: dict[GroundUnitType, int] = {}
        units_needing_transfer: dict[GroundUnitType, int] = {}
        for unit_type, count in self.units.items():
            allegiance = "Ally" if self.destination.captured else "Enemy"
            d: dict[GroundUnitType, int]
            if self.destination != ground_unit_source:
                source = ground_unit_source
                d = units_needing_transfer
            else:
                source = self.destination
                d = bought_units

            if count < 0:
                logging.error(
                    f"Attempted sale of {unit_type} at {self.destination} but ground "
                    "units cannot be sold"
                )
            elif count > 0:
                d[unit_type] = count
                game.message(
                    f"{allegiance} reinforcements: {unit_type} x {count} at {source}"
                )

        self.units = defaultdict(int)
        self.destination.base.commission_units(bought_units)

        if units_needing_transfer:
            if ground_unit_source is None:
                raise RuntimeError(
                    f"Ground unit source could not be found for {self.destination} but "
                    "still tried to transfer units to there"
                )
            ground_unit_source.base.commission_units(units_needing_transfer)
            self.create_transfer(coalition, ground_unit_source, units_needing_transfer)

    def create_transfer(
        self,
        coalition: Coalition,
        source: ControlPoint,
        units: dict[GroundUnitType, int],
    ) -> None:
        coalition.transfers.new_transfer(TransferOrder(source, self.destination, units))

    def find_ground_unit_source(self, game: Game) -> Optional[ControlPoint]:
        # This is running *after* the turn counter has been incremented, so this is the
        # reaction to turn 0. On turn zero we allow units to be recruited anywhere for
        # delivery on turn 1 so that turn 1 always starts with units on the front line.
        if game.turn == 1:
            return self.destination

        # Fast path if the destination is a valid source.
        if self.destination.can_recruit_ground_units(game):
            return self.destination

        try:
            return self.find_ground_unit_source_in_network(
                game.transit_network_for(self.destination.captured), game
            )
        except NoPathError:
            return None

    def find_ground_unit_source_in_network(
        self, network: TransitNetwork, game: Game
    ) -> Optional[ControlPoint]:
        sources = []
        for control_point in game.theater.control_points_for(self.destination.captured):
            if control_point.can_recruit_ground_units(
                game
            ) and network.has_path_between(self.destination, control_point):
                sources.append(control_point)

        if not sources:
            return None

        # Fast path to skip the distance calculation if we have only one option.
        if len(sources) == 1:
            return sources[0]

        closest = sources[0]
        _, cost = network.shortest_path_with_cost(self.destination, closest)
        for source in sources:
            _, new_cost = network.shortest_path_with_cost(self.destination, source)
            if new_cost < cost:
                closest = source
                cost = new_cost
        return closest
