from __future__ import annotations

from typing import List

from PySide2.QtCore import Property, QObject, Signal

from game import Game
from game.theater import ControlPoint
from game.transfers import MultiGroupTransport, TransportMap
from .leaflet import LeafletLatLon


class SupplyRouteJs(QObject):
    pointsChanged = Signal()
    frontActiveChanged = Signal()
    isSeaChanged = Signal()
    blueChanged = Signal()
    activeTransportsChanged = Signal()

    def __init__(
        self,
        a: ControlPoint,
        b: ControlPoint,
        points: List[LeafletLatLon],
        sea_route: bool,
        game: Game,
    ) -> None:
        super().__init__()
        self.control_point_a = a
        self.control_point_b = b
        self._points = points
        self.sea_route = sea_route
        self.game = game

    def find_in_transport_map(
        self, transport_map: TransportMap
    ) -> List[MultiGroupTransport]:
        transports = []
        transport = transport_map.find_transport(
            self.control_point_a, self.control_point_b
        )
        if transport is not None:
            transports.append(transport)
        transport = transport_map.find_transport(
            self.control_point_b, self.control_point_a
        )
        if transport is not None:
            transports.append(transport)
        return transports

    def find_transports(self) -> List[MultiGroupTransport]:
        if self.sea_route:
            return self.find_in_transport_map(
                self.game.blue.transfers.cargo_ships
            ) + self.find_in_transport_map(self.game.red.transfers.cargo_ships)
        return self.find_in_transport_map(
            self.game.blue.transfers.convoys
        ) + self.find_in_transport_map(self.game.red.transfers.convoys)

    @Property(list, notify=activeTransportsChanged)
    def activeTransports(self) -> List[str]:
        transports = self.find_transports()
        if not transports:
            return []

        descriptions = []
        for transport in transports:
            units = "units" if transport.size > 1 else "unit"
            descriptions.append(
                f"{transport.size} {units} transferring from {transport.origin} to "
                f"{transport.destination}"
            )
        return descriptions

    @Property(list, notify=pointsChanged)
    def points(self) -> List[LeafletLatLon]:
        return self._points

    @Property(bool, notify=frontActiveChanged)
    def frontActive(self) -> bool:
        if self.sea_route:
            return False
        return self.control_point_a.front_is_active(self.control_point_b)

    @Property(bool, notify=isSeaChanged)
    def isSea(self) -> bool:
        return self.sea_route

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.control_point_a.captured
