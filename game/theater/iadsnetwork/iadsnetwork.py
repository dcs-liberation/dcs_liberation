from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field

import logging
from typing import TYPE_CHECKING, Iterator, Optional
from uuid import UUID
import uuid

from game.theater.iadsnetwork.iadsrole import IadsRole
from game.dcs.groundunittype import GroundUnitType
from game.theater.theatergroundobject import (
    IadsBuildingGroundObject,
    IadsGroundObject,
    NavalGroundObject,
    TheaterGroundObject,
)
from game.theater.theatergroup import IadsGroundGroup

if TYPE_CHECKING:
    from game.game import Game
    from game.sim import GameUpdateEvents


class IadsNetworkException(Exception):
    pass


@dataclass
class SkynetNode:
    """Dataclass for a SkynetNode used in the LUA Data table by the luagenerator"""

    dcs_name: str
    player: bool
    iads_role: IadsRole
    properties: dict[str, str] = field(default_factory=dict)
    connections: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    @staticmethod
    def dcs_name_for_group(group: IadsGroundGroup) -> str:
        if group.iads_role in [
            IadsRole.EWR,
            IadsRole.COMMAND_CENTER,
            IadsRole.CONNECTION_NODE,
            IadsRole.POWER_SOURCE,
        ]:
            # Use UnitName for EWR, CommandCenter, Comms, Power
            for unit in group.units:
                # Check for alive units in the group
                if unit.alive:
                    return unit.unit_name
            if group.units[0].is_static:
                # Statics will be placed as dead unit
                return group.units[0].unit_name
            # If no alive unit is available and not static raise error
            raise IadsNetworkException("Group has no skynet usable units")
        else:
            # Use the GroupName for SAMs, SAMAsEWR and PDs
            return group.group_name

    @classmethod
    def from_group(cls, group: IadsGroundGroup) -> SkynetNode:
        node = cls(
            cls.dcs_name_for_group(group),
            group.ground_object.is_friendly(True),
            group.iads_role,
        )
        unit_type = group.units[0].unit_type
        if unit_type is not None and isinstance(unit_type, GroundUnitType):
            node.properties = unit_type.skynet_properties.to_dict()
        return node


class IadsNetworkNode:
    """IadsNetworkNode which particicpates to the IADS Network and has connections to Power Sources, Comms or Point Defenses. A network node can be a SAM System, EWR or Command Center"""

    def __init__(self, group: IadsGroundGroup) -> None:
        self.group = group
        self.connections: dict[UUID, IadsGroundGroup] = {}

    def __str__(self) -> str:
        return self.group.group_name

    def add_connection_for_tgo(self, tgo: TheaterGroundObject) -> None:
        """Add all possible connections for the given TGO to the node"""
        for group in tgo.groups:
            if isinstance(group, IadsGroundGroup) and group.iads_role.participate:
                self.add_connection_for_group(group)

    def add_connection_for_group(self, group: IadsGroundGroup) -> None:
        """Add connection for the given GroundGroup with unique ID"""
        self.connections[uuid.uuid4()] = group
        self._push_updated_node()

    def _push_updated_node(self) -> None:
        from game.server import EventStream

        with EventStream.event_context() as events:
            events.update_iads_node(self)


class IadsNetwork:
    """IADS Network consisting of multiple Network nodes and connections. The Network represents all possible connections of ground objects regardless if a tgo is under control of red or blue. The network can run in either advanced or basic mode. The advanced network can be created by a given configuration in the campaign yaml or computed by Range. The basic mode is a fallback mode which does not use Comms, Power or Command Centers. The network will be used to visualize all connections at the map and for creating the needed Lua data for the skynet plugin"""

    def __init__(
        self, advanced: bool, iads_data: list[str | dict[str, list[str]]]
    ) -> None:
        self.advanced_iads = advanced
        self.ground_objects: dict[str, TheaterGroundObject] = {}
        self.nodes: list[IadsNetworkNode] = []
        self.iads_config: dict[str, list[str]] = defaultdict(list)

        # Load Iads config from the campaign data
        for element in iads_data:
            if isinstance(element, str):
                self.iads_config[element] = []
            elif isinstance(element, dict):
                for iads_node, iads_connections in element.items():
                    self.iads_config[iads_node] = iads_connections
            else:
                raise RuntimeError("Invalid iads_config in campaign")

    def skynet_nodes(self, game: Game) -> list[SkynetNode]:
        """Get all skynet nodes from the IADS Network"""
        skynet_nodes: list[SkynetNode] = []
        for node in self.nodes:
            if game.iads_considerate_culling(node.group.ground_object):
                # Skip culled ground objects
                continue

            skynet_node = SkynetNode.from_group(node.group)
            for connection in node.connections.values():
                is_friendly = connection.ground_object.is_friendly(skynet_node.player)
                is_culled = game.iads_considerate_culling(connection.ground_object)
                if is_friendly and not is_culled:
                    key = connection.iads_role.value
                    name = SkynetNode.dcs_name_for_group(connection)
                    skynet_node.connections[key].append(name)
            skynet_nodes.append(skynet_node)

        return skynet_nodes

    def _update_iads_building(self, tgo: TheaterGroundObject, events: GameUpdateEvents) -> None:
        if not isinstance(tgo, IadsBuildingGroundObject):
            return

        for node in self.nodes:
            for cID, group in node.connections.items():
                if group.ground_object is tgo:
                    events.delete_iads_connection(cID)
        self._update_network(tgo, events)

    def update_tgo(self, tgo: TheaterGroundObject, events: GameUpdateEvents) -> None:
        """Update the IADS Network for the given TGO"""
        if isinstance(tgo, IadsBuildingGroundObject):
            return self._update_iads_building(tgo, events)
        # Remove existing nodes for the given tgo
        for cn in self.nodes:
            if cn.group.ground_object == tgo:
                self.nodes.remove(cn)
                for cID in cn.connections:
                    events.delete_iads_connection(cID)
        # Create a new node for the tgo
        # TODO Add the connections or calculate them..
        node = self.node_for_tgo(tgo)
        if node is None:
            # Not participating
            return
        self.nodes.append(node)
        self._connect_to_network(node, tgo, events)

    def node_for_group(self, group: IadsGroundGroup) -> IadsNetworkNode:
        """Get existing node from the iads network or create a new node"""
        for cn in self.nodes:
            if cn.group == group:
                return cn

        node = IadsNetworkNode(group)
        self.nodes.append(node)
        return node

    def node_for_tgo(self, tgo: TheaterGroundObject) -> Optional[IadsNetworkNode]:
        """Get existing node from the iads network or create a new node"""
        for cn in self.nodes:
            if cn.group.ground_object is tgo:
                return cn

        # Create new connection_node if none exists
        node: Optional[IadsNetworkNode] = None
        for group in tgo.groups:
            # TODO Cleanup
            if isinstance(group, IadsGroundGroup):
                # The first IadsGroundGroup is always the primary Group
                if not node and group.iads_role.participate:
                    # Primary Node
                    node = self.node_for_group(group)
                elif node and group.iads_role == IadsRole.POINT_DEFENSE:
                    # Point Defense Node for this TGO
                    node.add_connection_for_group(group)
        return node

    def initialize_network(self, ground_objects: Iterator[TheaterGroundObject]) -> None:
        """Initialize the IADS network in advanced or basic mode depending on the campaign"""
        for tgo in ground_objects:
            self.ground_objects[tgo.original_name] = tgo
        if self.advanced_iads:
            # Advanced mode
            if self.iads_config:
                # Load from Configuration File
                self.initialize_network_from_config()
            else:
                # Load from Range
                self.initialize_network_from_range()

        # basic mode if no advanced iads support or network init created no connections
        if not self.nodes:
            self.initialize_basic_iads()

    def initialize_basic_iads(self) -> None:
        """Initialize the IADS Network in basic mode (SAM & EWR only)"""
        for go in self.ground_objects.values():
            if isinstance(go, IadsGroundObject):
                node = self.node_for_tgo(go)
                if node is None:
                    # TGO does not participate to the IADS -> Skip
                    pass

    def initialize_network_from_config(self) -> None:
        """Initialize the IADS Network from a configuration"""
        for element_name, connections in self.iads_config.items():
            warning_msg = (
                f"IADS: No ground object found for {element_name}."
                f" This can be normal behaviour."
            )
            try:
                node = self.node_for_tgo(self.ground_objects[element_name])
            except KeyError:
                node = None
                warning_msg = (
                    f"IADS: No ground object found for connection {element_name}"
                )

            if node is None:
                # Log a warning as this can be normal. Possible case is for example
                # when the campaign request a Long Range SAM but the faction has none
                # available. Therefore the TGO will not get populated at all

                logging.warning(warning_msg)
                continue

            # Find all connected ground_objects
            for node_name in connections:
                try:
                    tgo = self.ground_objects[node_name]
                except KeyError:
                    logging.error(
                        f"IADS: No ground object found for connection {node_name}"
                    )
                    continue
                node.add_connection_for_tgo(tgo)

    def initialize_network_from_range(self) -> None:
        """Initialize the IADS Network by range"""
        for go in self.ground_objects.values():
            is_iads = go.is_iads()
            is_iads_cc = IadsRole.for_category(go.category) == IadsRole.COMMAND_CENTER
            if is_iads or is_iads_cc:
                # Set as primary node
                node = self.node_for_tgo(go)
                if node is None:
                    # TGO does not participate to iads network
                    continue
                self._connect_to_network(node, go)

    def _is_friendly(self, node: IadsNetworkNode, tgo: TheaterGroundObject) -> bool:
        node_friendly = node.group.ground_object.is_friendly(True)
        tgo_friendly = tgo.is_friendly(True)
        return node_friendly == tgo_friendly

    def _connect_to_network(
        self, node: IadsNetworkNode, go: TheaterGroundObject, events: GameUpdateEvents
    ) -> None:
        if go.is_dead:
            return
        # Find nearby Power or Connection
        for nearby_go in self.ground_objects.values():
            if nearby_go == go:
                continue
            iads_role = IadsRole.for_category(nearby_go.category)
            if iads_role.is_comms_or_power:
                dist = nearby_go.position.distance_to_point(go.position)
                in_range = dist < iads_role.connection_range.meters
                if in_range and self._is_friendly(node, nearby_go):
                    node.add_connection_for_tgo(nearby_go)
                    events.update_iads_node(node)

    def _update_network(self, tgo: TheaterGroundObject, events: GameUpdateEvents) -> None:
        if tgo.is_dead:
            return
        # Reversing the idea of _connect_to_network...
        iads_role = IadsRole.for_category(tgo.category)
        if not iads_role.is_comms_or_power:
            return
        for node in self.nodes:
            dist = node.group.ground_object.position.distance_to_point(tgo.position)
            in_range = dist < iads_role.connection_range.meters
            if in_range and self._is_friendly(node, tgo):
                node.add_connection_for_tgo(tgo)
                events.update_iads_node(node)
