from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Optional, Union

from game.theater.theatergroundobject import (
    TheaterGroundObject,
    IADSRole,
    IadsGroundGroup,
)


def find_tgo_by_original_name(
    name: str, ground_objects: list[TheaterGroundObject]
) -> TheaterGroundObject:
    for go in ground_objects:
        if go.original_name == name:
            return go
    raise StopIteration


class IADSConfigConnection:
    element_name: str
    connected: dict[str, Optional[TheaterGroundObject]]
    tgo: Optional[TheaterGroundObject]

    def __init__(self, name: str) -> None:
        self.element_name = name
        self.connected = {}
        self.tgo = None

    def update_connection(self, ground_objects: list[TheaterGroundObject]) -> None:
        # Search the tgo in the current theater. Raises StopIteration if none found
        self.tgo = find_tgo_by_original_name(self.element_name, ground_objects)

        for connection_node in self.connected:
            try:
                connected_tgo = find_tgo_by_original_name(
                    connection_node, ground_objects
                )
                self.connected[connection_node] = connected_tgo
            except StopIteration:
                logging.error(
                    f"IADS: No ground object found for connection {connection_node}"
                )
                self.connected.pop(connection_node)


@dataclass
class IADSConfig:
    connections: list[IADSConfigConnection]
    advanced_iads: bool = False  # True if campaign supports advanced iads

    @classmethod
    def from_campaign_data(cls, data: list[dict[str, list[str]]]) -> IADSConfig:
        connections: list[IADSConfigConnection] = []
        for element in data:
            for iads_node, iads_connections in element.items():
                config = IADSConfigConnection(iads_node)
                for connection in iads_connections:
                    config.connected[connection] = None
                if len(config.connected) > 0:
                    connections.append(config)
                else:
                    logging.warning(f"IADS Node {iads_node} has invalid connections")
        return IADSConfig(connections=connections, advanced_iads=True)


class IADSConnectionNode:
    connected_nodes: list[IADSConnectionNode]
    group: IadsGroundGroup

    def __str__(self) -> str:
        return self.group.group_name

    def __init__(self, group: IadsGroundGroup) -> None:
        self.group = group
        self.connected_nodes = []


class IADSNetwork:
    # Primary Connection Nodes can be SAM, EWR or CommandCenters
    # Each Connection Node is connected to a List of CN and PS
    # The final parsing, so that Skynet can handle it will happen in the luagenerator
    # This is because in the IADSNetwork we only work with the TGO instead of the Groups
    connections: list[IADSConnectionNode]
    iads_config: IADSConfig

    def __init__(self, iads_config: IADSConfig) -> None:
        self.iads_config = iads_config
        self.connections = []

    def node_for_group(self, group: IadsGroundGroup) -> IADSConnectionNode:
        for cn in self.connections:
            if cn.group == group:
                return cn

        connection_node = IADSConnectionNode(group)
        self.connections.append(connection_node)
        return connection_node

    def node_for_tgo(self, tgo: TheaterGroundObject) -> IADSConnectionNode:
        # Look for existing nodes for this tgo:
        for cn in self.connections:
            if cn.group.ground_object == tgo:
                return cn

        # Create new connection_node if none exists
        primary_node: Optional[IADSConnectionNode] = None
        for group in tgo.groups:
            if isinstance(group, IadsGroundGroup):
                # The first IadsGroundGroup is always the primary Group
                if not primary_node and group.iads_role.participate:
                    # Primary Node
                    primary_node = self.node_for_group(group)
                elif primary_node and group.iads_role == IADSRole.PointDefense:
                    # Point Defense Node for this TGO
                    primary_node.connected_nodes.append(IADSConnectionNode(group))

        if not primary_node:
            raise StopIteration
        return primary_node

    def initialize_network(self, ground_objects: list[TheaterGroundObject]) -> None:
        if self.iads_config.advanced_iads:
            if self.iads_config.connections:
                # Load from Configuration File
                self.initialize_network_from_config(ground_objects)
            else:
                # Load from Range
                self.initialize_network_from_range(ground_objects)

        # basic mode if no advanced iads support or network init created no connections
        if not self.connections:
            self.initialize_basic_iads(ground_objects)

    def initialize_basic_iads(self, ground_objects: list[TheaterGroundObject]) -> None:
        # Basic IADS Initialization with SAM & EWRs only
        for go in ground_objects:
            for group in go.groups:
                if isinstance(group, IadsGroundGroup) and group.iads_role in [
                    IADSRole.Sam,
                    IADSRole.SamAsEwr,
                    IADSRole.Ewr,
                ]:
                    self.node_for_group(group)

    def initialize_network_from_config(
        self, ground_objects: list[TheaterGroundObject]
    ) -> None:
        for connection in self.iads_config.connections:
            # Update the connection with the correct ground_objects
            try:
                connection.update_connection(ground_objects)
                assert connection.tgo is not None
                primary_node = self.node_for_tgo(connection.tgo)
            except StopIteration:
                logging.error(
                    f"IADS: No ground object found for {connection.element_name}"
                )
                continue

            # Find all connected ground_objects
            for node_name, node_tgo in connection.connected.items():
                assert node_tgo is not None
                primary_node.connected_nodes.append(self.node_for_tgo(node_tgo))

    def initialize_network_from_range(
        self, ground_objects: list[TheaterGroundObject]
    ) -> None:
        for go in ground_objects:
            for group in go.groups:
                if isinstance(group, IadsGroundGroup) and group.iads_role in [
                    IADSRole.PowerSource,
                    IADSRole.ConnectionNode,
                ]:
                    # Find nearby SAM, EWR and CommandCenters
                    connection_node = IADSConnectionNode(group)
                    for nearby_go in ground_objects:
                        if nearby_go == go:
                            continue
                        for nearby_group in nearby_go.groups:
                            if not isinstance(nearby_group, IadsGroundGroup):
                                continue
                            if (
                                nearby_group.iads_role
                                in [
                                    IADSRole.Sam,
                                    IADSRole.SamAsEwr,
                                    IADSRole.Ewr,
                                    IADSRole.CommandCenter,
                                ]
                                and nearby_go.position.distance_to_point(go.position)
                                <= group.iads_role.connection_range.meters
                            ):
                                # Create the primary node or reuse existing to prevent duplicates
                                primary_connection_node = self.node_for_tgo(nearby_go)
                                # attach the CN/PS to the primary Node
                                primary_connection_node.connected_nodes.append(
                                    connection_node
                                )
