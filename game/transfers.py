import logging
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Type

from dcs.unittype import VehicleType
from game.theater import ControlPoint
from game.theater.supplyroutes import SupplyRoute


@dataclass
class TransferOrder:
    """The base type of all transfer orders.

    A transfer order can transfer multiple units of multiple types.
    """

    #: The location the units are transferring from.
    origin: ControlPoint

    #: The location the units are transferring to.
    destination: ControlPoint

    #: True if the transfer order belongs to the player.
    player: bool


@dataclass
class RoadTransferOrder(TransferOrder):
    """A transfer order that moves units by road."""

    #: The units being transferred.
    units: Dict[Type[VehicleType], int]

    #: The current position of the group being transferred. Groups move one control
    #: point a turn through the supply line.
    position: ControlPoint = field(init=False)

    def __post_init__(self) -> None:
        self.position = self.origin

    def path(self) -> List[ControlPoint]:
        supply_route = SupplyRoute.for_control_point(self.position)
        return supply_route.shortest_path_between(self.position, self.destination)


class PendingTransfers:
    def __init__(self) -> None:
        self.pending_transfers: List[RoadTransferOrder] = []

    def __iter__(self) -> Iterator[RoadTransferOrder]:
        yield from self.pending_transfers

    @property
    def pending_transfer_count(self) -> int:
        return len(self.pending_transfers)

    def transfer_at_index(self, index: int) -> RoadTransferOrder:
        return self.pending_transfers[index]

    def new_transfer(self, transfer: RoadTransferOrder) -> None:
        transfer.origin.base.commit_losses(transfer.units)
        self.pending_transfers.append(transfer)

    def cancel_transfer(self, transfer: RoadTransferOrder) -> None:
        self.pending_transfers.remove(transfer)
        transfer.origin.base.commision_units(transfer.units)

    def perform_transfers(self) -> None:
        incomplete = []
        for transfer in self.pending_transfers:
            if not self.perform_transfer(transfer):
                incomplete.append(transfer)
        self.pending_transfers = incomplete

    def perform_transfer(self, transfer: RoadTransferOrder) -> bool:
        if transfer.player != transfer.destination.captured:
            logging.info(
                f"Transfer destination {transfer.destination.name} was captured."
            )
            self.handle_route_interrupted(transfer)
            return True

        supply_route = SupplyRoute.for_control_point(transfer.destination)
        if transfer.position not in supply_route:
            logging.info(
                f"Route from {transfer.position.name} to {transfer.destination.name} "
                "was cut off."
            )
            self.handle_route_interrupted(transfer)
            return True

        path = transfer.path()
        next_hop = path[0]
        if next_hop == transfer.destination:
            logging.info(
                f"Units transferred from {transfer.origin.name} to "
                f"{transfer.destination.name}"
            )
            transfer.destination.base.commision_units(transfer.units)
            return True

        logging.info(
            f"Units transferring from {transfer.origin.name} to "
            f"{transfer.destination.name} arrived at {next_hop.name}. {len(path) - 1} "
            "turns remaining."
        )
        transfer.position = next_hop
        return False

    @staticmethod
    def handle_route_interrupted(transfer: RoadTransferOrder):
        # Halt the transfer in place if safe.
        if transfer.player == transfer.position.captured:
            logging.info(f"Transferring units are halting at {transfer.position.name}.")
            transfer.position.base.commision_units(transfer.units)
            return

        # If the current position was captured attempt to divert to a neighboring
        # friendly CP.
        for connected in transfer.position.connected_points:
            if connected.captured == transfer.player:
                logging.info(f"Transferring units are re-routing to {connected.name}.")
                connected.base.commision_units(transfer.units)
                return

        # If the units are cutoff they are destroyed.
        logging.info(
            f"Both {transfer.position.name} and {transfer.destination.name} were "
            "captured. Units were surrounded and destroyed during transfer."
        )
