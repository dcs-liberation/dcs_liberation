from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union

from game.theater.theatergroundobject import (
    IadsGroundObject,
    IadsBuildingGroundObject,
    SamGroundObject,
    EwrGroundObject,
    TheaterGroundObject,
    IADSRole,
)


def find_tgo_by_original_name(
    name: str, ground_objects: List[TheaterGroundObject[Any]]
) -> List[TheaterGroundObject[Any]]:
    return [
        go
        for go in ground_objects
        if (
            isinstance(go, IadsGroundObject) or isinstance(go, IadsBuildingGroundObject)
        )
        and go.original_name == name
    ]


class IADSConfigConnection:
    element_name: str
    connected: Dict[str, Optional[TheaterGroundObject[Any]]]
    iads_role: IADSRole
    tgo: Optional[TheaterGroundObject[Any]]

    def __init__(self, name: str, iads_role: str) -> None:
        self.element_name = name
        self.connected = {}
        self.iads_role = IADSRole(iads_role)
        self.tgo = None

    def update_connection(self, ground_objects: List[TheaterGroundObject[Any]]) -> None:
        # Search the tgo in the current theater
        found_tgo = find_tgo_by_original_name(self.element_name, ground_objects)
        if found_tgo:
            # Link the TheaterGroundObject
            self.tgo = found_tgo[0]
        else:
            logging.error(
                f"IADS: No ground object found for {self.element_name} which was defined in campaign yaml"
            )
            return

        for connection_node in self.connected:
            found_node_tgo = find_tgo_by_original_name(connection_node, ground_objects)
            if found_node_tgo:
                self.connected[connection_node] = found_node_tgo[0]
            else:
                logging.error(
                    f"IADS: No ground object found for connection_node {connection_node} of {self.element_name}"
                )


@dataclass
class IADSConfig:
    connections: List[IADSConfigConnection]
    advanced_iads: bool = False  # True if campaign supports advanced iads

    @classmethod
    def from_campaign_data(cls, data: dict[Union[str, int], Any]) -> IADSConfig:
        connections: List[IADSConfigConnection] = []
        for iads_role, iads_nodes in data.items():
            for iads_node in iads_nodes:
                try:
                    connection = IADSConfigConnection(
                        iads_node.get("name"), str(iads_role)
                    )
                    connections.append(connection)
                except (ValueError, KeyError, TypeError):
                    logging.error(
                        f"IADS Node {iads_node} could not be loaded from campaign yaml"
                    )
                    continue
                try:
                    for connected_asset in iads_node.get("connected"):
                        connection.connected[connected_asset] = None
                except (ValueError, KeyError, TypeError):
                    logging.warning(
                        f"IADS Node {iads_node} has invalid or no connections"
                    )
                    continue
        return IADSConfig(connections=connections, advanced_iads=True)

    def update_connections(
        self, ground_objects: List[TheaterGroundObject[Any]]
    ) -> None:
        for connection in self.connections:
            connection.update_connection(ground_objects)


class IADSConnectionNode:
    connected_nodes: List[IADSConnectionNode]
    ground_object: TheaterGroundObject[Any]

    def __init__(self, go: TheaterGroundObject[Any]) -> None:
        self.ground_object = go
        self.connected_nodes = []

    @property
    def participate(self) -> bool:
        # exclude current non skynet_capable ground_units
        # they could later participate when the player for example upgrades them
        if self.iads_role in [
            IADSRole.Ewr,
            IADSRole.Sam,
            IADSRole.SamAsEwr,
            IADSRole.ConnectionNode,
            IADSRole.CommandCenter,
            IADSRole.PowerSource,
        ]:
            return True
        return False

    @property
    def iads_role(self) -> IADSRole:
        if isinstance(self.ground_object, IadsGroundObject) or isinstance(
            self.ground_object, IadsBuildingGroundObject
        ):
            return self.ground_object.iads_role
        return IADSRole.NoBehavior


class IADSNetwork:
    # Primary Connection Nodes can be SAM, EWR or CommandCenters
    # Each Connection Node is connected to a List of CN and PS
    # The final parsing, so that Skynet can handle it will happen in the luagenerator
    # This is because in the IADSNetwork we only work with the TGO instead of the Groups
    connections: List[IADSConnectionNode]
    iads_config: IADSConfig

    def __init__(self, iads_config: IADSConfig) -> None:
        self.iads_config = iads_config
        self.connections = []

    def connection_node_for(self, tgo: TheaterGroundObject[Any]) -> IADSConnectionNode:
        for cn in self.connections:
            if cn.ground_object == tgo:
                # use existing node
                return cn

        # Create new connection_node if none exists
        connection_node = IADSConnectionNode(tgo)
        self.connections.append(connection_node)
        return connection_node

    def initialize_network(
        self, ground_objects: List[TheaterGroundObject[Any]]
    ) -> None:
        if self.iads_config.advanced_iads:
            if self.iads_config.connections:
                self.iads_config.update_connections(ground_objects)
                self.initialize_network_from_config(ground_objects)
            else:
                self.initialize_network_from_range(ground_objects)

        # basic mode if no advanced iads support or network init created no connections
        if not self.connections:
            self.initialize_basic_iads(ground_objects)

    def initialize_basic_iads(
        self, ground_objects: List[TheaterGroundObject[Any]]
    ) -> None:
        # Basic IADS Initialization with SAM & EWRs only
        for go in ground_objects:
            if isinstance(go, IadsGroundObject) and go.iads_role in [
                IADSRole.Sam,
                IADSRole.SamAsEwr,
                IADSRole.Ewr,
            ]:
                self.connections.append(IADSConnectionNode(go))
        return

    def initialize_network_from_config(
        self, ground_objects: List[TheaterGroundObject[Any]]
    ) -> None:
        for connection in self.iads_config.connections:
            if not connection.tgo:
                # Skip all invalid IADS Elements
                continue
            primary_connection_node = IADSConnectionNode(connection.tgo)
            for node_name, node_tgo in connection.connected.items():
                if not node_tgo:
                    # Skip all invalid connections
                    continue
                primary_connection_node.connected_nodes.append(
                    IADSConnectionNode(node_tgo)
                )
            self.connections.append(primary_connection_node)

    def initialize_network_from_range(
        self, ground_objects: List[TheaterGroundObject[Any]]
    ) -> None:
        for go in ground_objects:
            if (
                # Only parse Connection_Nodes and Power_Sources
                isinstance(go, IadsBuildingGroundObject)
                and (
                    go.iads_role == IADSRole.PowerSource
                    or go.iads_role == IADSRole.ConnectionNode
                )
            ):
                # Find nearby SAM, EWR and CommandCenters
                connection_node = IADSConnectionNode(go)
                nearby_ground_objects = [
                    nearby_go
                    for nearby_go in ground_objects
                    if nearby_go != go
                    and (
                        # Filter for SAM, EWR and CommandCenters
                        (
                            isinstance(nearby_go, SamGroundObject)
                            or isinstance(nearby_go, EwrGroundObject)
                        )
                        or (
                            isinstance(nearby_go, IadsBuildingGroundObject)
                            and nearby_go.iads_role == IADSRole.CommandCenter
                        )
                    )
                    and nearby_go.position.distance_to_point(go.position)
                    <= go.connection_range.meters
                ]

                for nearby_go in nearby_ground_objects:
                    # Create the primary node or reuse existing to prevent duplicates
                    primary_connection_node = self.connection_node_for(nearby_go)
                    # attach the CN/PS to the primary Node
                    primary_connection_node.connected_nodes.append(connection_node)
