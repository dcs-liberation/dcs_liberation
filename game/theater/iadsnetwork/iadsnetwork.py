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
            is_dead = group.alive_units == 0
            for unit in group.units:
                if unit.alive or (is_dead and unit.is_static):
                    # Return first alive unit within the group or otherwise return the
                    # first static object as these will still be added to the mission
                    return unit.unit_name
            # Raise error if there is no skynet capable unit in this group
            raise IadsNetworkException(f"Group {group.name} has no skynet usable units")
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

    def add_secondary_node(self, tgo: TheaterGroundObject) -> None:
        """Add all possible connections for the given secondary node to this node"""
        for group in tgo.groups:
            if isinstance(group, IadsGroundGroup) and group.iads_role.is_secondary_node:
                self.add_connection_for_group(group)

    def add_connection_for_group(self, group: IadsGroundGroup) -> None:
        """Add connection for the given GroundGroup with unique ID"""
        self.connections[uuid.uuid4()] = group


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

    @property
    def participating(self) -> Iterator[TheaterGroundObject]:
        """All unique participating TGOs. First primary then secondary"""
        secondary_nodes = []
        for node in self.nodes:
            yield node.group.ground_object
            for connection in node.connections.values():
                # Check for duplicate secondary node as a secondary node can be
                # connected to 1..N primary nodes but we do not want to yiel them
                # multiple times so we prevent dups
                if connection.ground_object not in secondary_nodes:
                    secondary_nodes.append(connection.ground_object)
        yield from secondary_nodes

    def skynet_nodes(self, game: Game) -> list[SkynetNode]:
        """Get all skynet nodes from the IADS Network"""
        skynet_nodes: list[SkynetNode] = []
        for node in self.nodes:
            if game.iads_considerate_culling(node.group.ground_object):
                # Skip culled ground objects
                continue

            if node.group.alive_units == 0 and not node.group.has_statics:
                # Skip non-static nodes with no alive units left
                # Dead static nodes can be added to skynet as these are added to the
                # mission as dead unit. Non static will not be added to the mission and
                # are therefore not accessible by skynet
                continue

            # SkynetNode.from_group(node.group) may raise an exception
            #  (originating from SkynetNode.dcs_name_for_group)
            # but if it does, we want to know because it's supposed to be impossible afaict
            skynet_node = SkynetNode.from_group(node.group)
            for connection in node.connections.values():
                if connection.alive_units == 0 and not connection.has_statics:
                    # Skip non static and dead connection nodes. See comment above
                    continue
                if connection.ground_object.is_friendly(
                    skynet_node.player
                ) and not game.iads_considerate_culling(connection.ground_object):
                    skynet_node.connections[connection.iads_role.value].append(
                        SkynetNode.dcs_name_for_group(connection)
                    )
            skynet_nodes.append(skynet_node)
        return skynet_nodes

    def update_tgo(self, tgo: TheaterGroundObject, events: GameUpdateEvents) -> None:
        """Update the IADS Network for the given TGO"""
        # Remove existing nodes for the given tgo if there are any
        for cn in self.nodes:
            if cn.group.ground_object == tgo:
                self.nodes.remove(cn)
                # Also delete all connections for the given node
                for cID in cn.connections:
                    events.delete_iads_connection(cID)

        # Try to create a new primary node for the TGO
        node = self._new_node_for_tgo(tgo)
        if node is None:
            # the ground object is not participating to the IADS Network
            return

        if self.advanced_iads:
            # Create the connections to the secondary nodes
            if self.iads_config:
                # If iads_config was defined and campaign designer added a config for
                # the given primary node generate the connections from the config. If
                # the primary node was not defined in the iads_config it will be added
                # without any connections
                self._add_connections_from_config(node)
            else:
                # Otherwise calculate the connections by range
                self._calculate_connections_by_range(node)

        events.update_iads_node(node)

    def update_network(self, events: GameUpdateEvents) -> None:
        """Update all primary nodes of the IADS and recalculate connections"""
        primary_nodes = [node.group.ground_object for node in self.nodes]
        for primary_node in primary_nodes:
            self.update_tgo(primary_node, events)

    def node_for_tgo(self, tgo: TheaterGroundObject) -> Optional[IadsNetworkNode]:
        """Create Primary node for the TGO or return existing one"""
        for cn in self.nodes:
            if cn.group.ground_object == tgo:
                return cn
        return self._new_node_for_tgo(tgo)

    def _new_node_for_tgo(self, tgo: TheaterGroundObject) -> Optional[IadsNetworkNode]:
        """Create a new primary node for the given TGO.

        Will return None if the given TGO is not capable of being a primary node.
        This will also add any PointDefense of this TGO to the primary node"""
        node: Optional[IadsNetworkNode] = None
        for group in tgo.groups:
            if isinstance(group, IadsGroundGroup):
                # The first IadsGroundGroup is always the primary Group
                if node is None and group.iads_role.is_primary_node:
                    # Create Primary Node
                    node = IadsNetworkNode(group)
                    self.nodes.append(node)
                elif node is not None and group.iads_role == IadsRole.POINT_DEFENSE:
                    # Point Defense Node for this TGO
                    node.add_connection_for_group(group)

        if node is None:
            logging.debug(f"TGO {tgo.name} not participating to IADS")
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
                self.node_for_tgo(go)

    def initialize_network_from_config(self) -> None:
        """Initialize the IADS Network from a configuration"""
        for primary_node in self.iads_config.keys():
            warning_msg = (
                f"IADS: No ground object found for {primary_node}."
                f" This can be normal behaviour."
            )
            if primary_node in self.ground_objects:
                node = self.node_for_tgo(self.ground_objects[primary_node])
            else:
                node = None
                warning_msg = (
                    f"IADS: No ground object found for connection {primary_node}"
                )

            if node is None:
                # Log a warning as this can be normal. Possible case is for example
                # when the campaign request a Long Range SAM but the faction has none
                # available. Therefore the TGO will not get populated at all
                logging.warning(warning_msg)
                continue
            self._add_connections_from_config(node)

    def _add_connections_from_config(self, node: IadsNetworkNode) -> None:
        """Add all connections for the given primary node based on the iads_config"""
        primary_node = node.group.ground_object.original_name
        # iads_config uses defaultdict, therefore when the connections of a primary
        # node where not defined in the iads_config they will just be empty
        connections = self.iads_config[primary_node]
        for secondary_node in connections:
            try:
                nearby_go = self.ground_objects[secondary_node]
                if IadsRole.for_category(nearby_go.category).is_secondary_node:
                    node.add_secondary_node(nearby_go)
                else:
                    logging.error(
                        f"IADS: {secondary_node} is not a valid secondary node"
                    )
            except KeyError:
                logging.exception(
                    f"IADS: No ground object found for connection {secondary_node}"
                )
                continue

    def _calculate_connections_by_range(self, node: IadsNetworkNode) -> None:
        """Add all connections for the primary node by calculating them by range"""
        primary_tgo = node.group.ground_object
        for nearby_go in self.ground_objects.values():
            # Find nearby Power or Connection
            if nearby_go == primary_tgo:
                continue
            nearby_iads_role = IadsRole.for_category(nearby_go.category)
            if (
                nearby_iads_role.is_secondary_node
                and nearby_go.position.distance_to_point(primary_tgo.position)
                <= nearby_iads_role.connection_range.meters
            ):
                node.add_secondary_node(nearby_go)

    def initialize_network_from_range(self) -> None:
        """Initialize the IADS Network by range"""
        for go in self.ground_objects.values():
            if (
                isinstance(go, IadsGroundObject)
                or isinstance(go, NavalGroundObject)
                or (
                    isinstance(go, IadsBuildingGroundObject)
                    and IadsRole.for_category(go.category) == IadsRole.COMMAND_CENTER
                )
            ):
                # Set as primary node
                node = self.node_for_tgo(go)
                if node is None:
                    # TGO does not participate to iads network
                    continue
                self._calculate_connections_by_range(node)
