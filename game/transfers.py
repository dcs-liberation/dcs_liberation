import logging
from dataclasses import dataclass
from typing import Dict, List, Type

from dcs.unittype import VehicleType
from game.theater import ControlPoint


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


class PendingTransfers:
    def __init__(self) -> None:
        self.pending_transfers: List[RoadTransferOrder] = []

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

    def complete_transfers(self) -> None:
        for transfer in self.pending_transfers:
            self.complete_transfer(transfer)
        self.pending_transfers.clear()

    @staticmethod
    def complete_transfer(transfer: RoadTransferOrder) -> None:
        if transfer.player == transfer.destination.captured:
            logging.info(
                f"Units transferred from {transfer.origin.name} to "
                f"{transfer.destination.name}"
            )
            transfer.destination.base.commision_units(transfer.units)
        elif transfer.player == transfer.origin.captured:
            logging.info(
                f"{transfer.destination.name} was captured. Transferring units are "
                f"returning to {transfer.origin.name}"
            )
            transfer.origin.base.commision_units(transfer.units)
        else:
            logging.info(
                f"Both {transfer.origin.name} and {transfer.destination.name} were "
                "captured. Units were surrounded and captured during transfer."
            )
