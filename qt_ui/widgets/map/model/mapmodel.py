from __future__ import annotations

from typing import List, Optional

from PySide2.QtCore import Property, QObject, Signal
from dcs.mapping import LatLng

from game import Game
from game.profiling import logged_duration
from game.theater import (
    ConflictTheater,
)
from qt_ui.models import GameModel
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from .controlpointjs import ControlPointJs
from .leaflet import LeafletLatLon
from .supplyroutejs import SupplyRouteJs


# **EVERY PROPERTY NEEDS A NOTIFY SIGNAL**
#
# https://bugreports.qt.io/browse/PYSIDE-1426
#
# PySide2 5.15.2 released 6 days before the fix for this was merged, but presumably we
# can clean up after 5.15.3 (or a future version) is released.
#
# Until then, all properties must use a notify signal. For some reason the error doesn't
# show up when running from source, and member properties also are not sufficient.
# Failing to do this will cause every sync of the property to emit an expensive log
# message. This can prevent the UI from being responsive.
#
# A local signal (i.e. `@Property(t, notify=Signal())`) is not sufficient. The class
# needs a named signal for every property, even if it is constant.


class MapModel(QObject):
    cleared = Signal()

    apiKeyChanged = Signal(str)
    mapCenterChanged = Signal(list)
    controlPointsChanged = Signal()
    supplyRoutesChanged = Signal()
    mapReset = Signal()

    def __init__(self, game_model: GameModel) -> None:
        super().__init__()
        self.game_model = game_model
        self._map_center = LatLng(0, 0)
        self._control_points = []
        self._supply_routes = []

        GameUpdateSignal.get_instance().game_loaded.connect(self.on_game_load)
        self.reset()

    def clear(self) -> None:
        self._control_points = []
        self._supply_routes = []
        self.cleared.emit()

    def reset(self) -> None:
        if self.game_model.game is None:
            self.clear()
            return
        with logged_duration("Map reset"):
            self.reset_control_points()
            self.reset_routes()
            self.mapReset.emit()

    def on_game_load(self, game: Optional[Game]) -> None:
        if game is not None:
            self.reset_map_center(game.theater)

    def reset_map_center(self, theater: ConflictTheater) -> None:
        self._map_center = theater.terrain.map_view_default.position.latlng()
        self.mapCenterChanged.emit(self._map_center.as_list())

    @Property(list, notify=mapCenterChanged)
    def mapCenter(self) -> LeafletLatLon:
        return self._map_center.as_list()

    def reset_control_points(self) -> None:
        self._control_points = [
            ControlPointJs(c, self.game_model, self.game.theater)
            for c in self.game.theater.controlpoints
        ]
        self.controlPointsChanged.emit()

    @Property(list, notify=controlPointsChanged)
    def controlPoints(self) -> List[ControlPointJs]:
        return self._control_points

    def reset_routes(self) -> None:
        seen = set()
        self._supply_routes = []
        for control_point in self.game.theater.controlpoints:
            seen.add(control_point)
            for destination, convoy_route in control_point.convoy_routes.items():
                if destination in seen:
                    continue
                self._supply_routes.append(
                    SupplyRouteJs(
                        control_point,
                        destination,
                        [p.latlng().as_list() for p in convoy_route],
                        sea_route=False,
                        game=self.game,
                    )
                )
            for destination, shipping_lane in control_point.shipping_lanes.items():
                if destination in seen:
                    continue
                if control_point.is_friendly(destination.captured):
                    self._supply_routes.append(
                        SupplyRouteJs(
                            control_point,
                            destination,
                            [p.latlng().as_list() for p in shipping_lane],
                            sea_route=True,
                            game=self.game,
                        )
                    )
        self.supplyRoutesChanged.emit()

    @Property(list, notify=supplyRoutesChanged)
    def supplyRoutes(self) -> List[SupplyRouteJs]:
        return self._supply_routes

    @property
    def game(self) -> Game:
        if self.game_model.game is None:
            raise RuntimeError("No game loaded")
        return self.game_model.game
