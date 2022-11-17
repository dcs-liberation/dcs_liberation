from __future__ import annotations
from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint
from game.theater.iadsnetwork.iadsnetwork import IadsNetworkNode, IadsNetwork
from game.theater.theatergroundobject import TheaterGroundObject


class IadsConnectionJs(BaseModel):
    id: UUID
    points: list[LeafletPoint]
    node: UUID
    connected: UUID
    active: bool
    blue: bool
    is_power: bool

    class Config:
        title = "IadsConnection"

    @staticmethod
    def connections_for_tgo(
        tgo_id: UUID, network: IadsNetwork
    ) -> list[IadsConnectionJs]:
        for node in network.nodes:
            if node.group.ground_object.id == tgo_id:
                return IadsConnectionJs.connections_for_node(node)
        return []

    @staticmethod
    def connections_for_node(network_node: IadsNetworkNode) -> list[IadsConnectionJs]:
        iads_connections = []
        tgo = network_node.group.ground_object
        for id, connection in network_node.connections.items():
            if (
                not connection.iads_role.is_secondary_node
                or connection.ground_object.is_friendly(True) != tgo.is_friendly(True)
            ):
                # Skip connections to non secondary nodes (for example PD)
                # and connections which are not from same coalition
                continue
            iads_connections.append(
                IadsConnectionJs(
                    id=id,
                    points=[
                        tgo.position.latlng(),
                        connection.ground_object.position.latlng(),
                    ],
                    node=tgo.id,
                    connected=connection.ground_object.id,
                    active=(
                        network_node.group.alive_units > 0
                        and connection.alive_units > 0
                    ),
                    blue=tgo.is_friendly(True),
                    is_power="power"
                    in [tgo.category, connection.ground_object.category],
                )
            )
        return iads_connections


class IadsNetworkJs(BaseModel):
    advanced: bool
    connections: list[IadsConnectionJs]

    class Config:
        title = "IadsNetwork"

    @staticmethod
    def from_network(network: IadsNetwork) -> IadsNetworkJs:
        iads_connections = []
        for primary_node in network.nodes:
            iads_connections.extend(IadsConnectionJs.connections_for_node(primary_node))
        return IadsNetworkJs(
            advanced=network.advanced_iads, connections=iads_connections
        )
