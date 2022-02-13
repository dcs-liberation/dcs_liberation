from __future__ import annotations

import json
import logging
from typing import List, Optional, Tuple

from PySide2.QtCore import Property, QObject, Signal
from dcs import Point

from game import Game
from game.ato.airtaaskingorder import AirTaskingOrder
from game.profiling import logged_duration
from game.sim.combat import FrozenCombat
from game.sim.combat.aircombat import AirCombat
from game.sim.combat.atip import AtIp
from game.sim.combat.defendingsam import DefendingSam
from game.sim.gameupdateevents import GameUpdateEvents
from game.theater import (
    ConflictTheater,
)
from qt_ui.models import GameModel
from qt_ui.simcontroller import SimController
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from .aircombatjs import AirCombatJs
from .controlpointjs import ControlPointJs
from .flightjs import FlightJs
from .frontlinejs import FrontLineJs
from .groundobjectjs import GroundObjectJs
from .holdzonesjs import HoldZonesJs
from .ipcombatjs import IpCombatJs
from .ipzonesjs import IpZonesJs
from .joinzonesjs import JoinZonesJs
from .leaflet import LeafletLatLon
from .mapzonesjs import MapZonesJs
from .navmeshjs import NavMeshJs
from .samcombatjs import SamCombatJs
from .supplyroutejs import SupplyRouteJs
from .threatzonecontainerjs import ThreatZoneContainerJs
from .threatzonesjs import ThreatZonesJs
from .unculledzonejs import UnculledZone


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

    mapCenterChanged = Signal(list)
    controlPointsChanged = Signal()
    groundObjectsChanged = Signal()
    supplyRoutesChanged = Signal()
    flightsChanged = Signal()
    frontLinesChanged = Signal()
    threatZonesChanged = Signal()
    navmeshesChanged = Signal()
    mapZonesChanged = Signal()
    unculledZonesChanged = Signal()
    ipZonesChanged = Signal()
    joinZonesChanged = Signal()
    holdZonesChanged = Signal()
    airCombatsChanged = Signal()
    samCombatsChanged = Signal()
    ipCombatsChanged = Signal()

    def __init__(self, game_model: GameModel, sim_controller: SimController) -> None:
        super().__init__()
        self.game_model = game_model
        self._map_center = [0, 0]
        self._control_points = []
        self._ground_objects = []
        self._supply_routes = []
        self._flights: dict[tuple[bool, int, int], FlightJs] = {}
        self._front_lines = []
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.empty(), ThreatZonesJs.empty()
        )
        self._navmeshes = NavMeshJs([], [])
        self._map_zones = MapZonesJs([], [], [])
        self._unculled_zones = []
        self._ip_zones = IpZonesJs.empty()
        self._join_zones = JoinZonesJs.empty()
        self._hold_zones = HoldZonesJs.empty()
        self._selected_flight_index: Optional[Tuple[int, int]] = None
        self._air_combats = []
        self._sam_combats = []
        self._ip_combats = []

        GameUpdateSignal.get_instance().game_loaded.connect(self.on_game_load)
        GameUpdateSignal.get_instance().flight_paths_changed.connect(self.reset_atos)
        GameUpdateSignal.get_instance().package_selection_changed.connect(
            self.set_package_selection
        )
        GameUpdateSignal.get_instance().flight_selection_changed.connect(
            self.set_flight_selection
        )
        self.game_model.ato_model_for(True).packages_changed.connect(
            self.on_package_change
        ),
        self.game_model.ato_model_for(False).packages_changed.connect(
            self.on_package_change
        ),
        sim_controller.sim_update.connect(self.on_sim_update)
        self.reset()

    def clear(self) -> None:
        self._control_points = []
        self._supply_routes = []
        self._ground_objects = []
        self._flights = {}
        self._front_lines = []
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.empty(), ThreatZonesJs.empty()
        )
        self._navmeshes = NavMeshJs([], [])
        self._map_zones = MapZonesJs([], [], [])
        self._unculled_zones = []
        self._ip_zones = IpZonesJs.empty()
        self._air_combats = []
        self._sam_combats = []
        self._ip_combats = []
        self.cleared.emit()

    def on_sim_update(self, events: GameUpdateEvents) -> None:
        # TODO: Only update flights with changes.
        # We have the signal of which flights have updates, but no fast lookup for
        # Flight -> FlightJs since Flight isn't hashable. Faster to update every flight
        # than do do the O(n^2) filtered update.
        for flight in self._flights.values():
            flight.positionChanged.emit()
        for combat in events.new_combats:
            self.on_add_combat(combat)
        for combat in events.updated_combats:
            self.on_combat_changed(combat)

    def set_package_selection(self, index: int) -> None:
        self.deselect_current_flight()
        # Optional[int] isn't a valid type for a Qt signal. None will be converted to
        # zero automatically. We use -1 to indicate no selection.
        if index == -1:
            self._selected_flight_index = None
        else:
            self._selected_flight_index = index, 0
        self.select_current_flight()
        self.reset_debug_zones()

    def set_flight_selection(self, index: int) -> None:
        self.deselect_current_flight()
        if self._selected_flight_index is None:
            if index != -1:
                # We don't know what order update_package_selection and
                # update_flight_selection will be called in when the last
                # package is removed. If no flight is selected, it's not a
                # problem to also have no package selected.
                logging.error("Flight was selected with no package selected")
            return

        # Optional[int] isn't a valid type for a Qt signal. None will be converted to
        # zero automatically. We use -1 to indicate no selection.
        if index == -1:
            self._selected_flight_index = self._selected_flight_index[0], None
        self._selected_flight_index = self._selected_flight_index[0], index
        self.select_current_flight()
        self.reset_debug_zones()

    @property
    def _selected_flight(self) -> Optional[FlightJs]:
        if self._selected_flight_index is None:
            return None
        package_index, flight_index = self._selected_flight_index
        blue = True
        return self._flights.get((blue, package_index, flight_index))

    def deselect_current_flight(self) -> None:
        flight = self._selected_flight
        if flight is None:
            return None
        flight.set_selected(False)

    def select_current_flight(self):
        flight = self._selected_flight
        if flight is None:
            return None
        flight.set_selected(True)

    @staticmethod
    def leaflet_coord_for(point: Point, theater: ConflictTheater) -> LeafletLatLon:
        ll = theater.point_to_ll(point)
        return [ll.latitude, ll.longitude]

    def reset(self) -> None:
        if self.game_model.game is None:
            self.clear()
            return
        with logged_duration("Map reset"):
            self.reset_control_points()
            self.reset_ground_objects()
            self.reset_routes()
            self.reset_atos()
            self.reset_front_lines()
            self.reset_threat_zones()
            self.reset_navmeshes()
            self.reset_map_zones()
            self.reset_unculled_zones()
            self.reset_combats()

    def on_game_load(self, game: Optional[Game]) -> None:
        if game is not None:
            self.reset_map_center(game.theater)

    def reset_map_center(self, theater: ConflictTheater) -> None:
        ll = theater.point_to_ll(theater.terrain.map_view_default.position)
        self._map_center = [ll.latitude, ll.longitude]
        self.mapCenterChanged.emit(self._map_center)

    @Property(list, notify=mapCenterChanged)
    def mapCenter(self) -> LeafletLatLon:
        return self._map_center

    def _flights_in_ato(
        self, ato: AirTaskingOrder, blue: bool
    ) -> dict[tuple[bool, int, int], FlightJs]:
        flights = {}
        for p_idx, package in enumerate(ato.packages):
            for f_idx, flight in enumerate(package.flights):
                flights[blue, p_idx, f_idx] = FlightJs(
                    flight,
                    selected=blue and (p_idx, f_idx) == self._selected_flight_index,
                    theater=self.game.theater,
                    ato_model=self.game_model.ato_model_for(blue),
                )
        return flights

    def reset_atos(self) -> None:
        self._flights = self._flights_in_ato(
            self.game.blue.ato, blue=True
        ) | self._flights_in_ato(self.game.red.ato, blue=False)
        self.flightsChanged.emit()
        self.reset_debug_zones()

    def reset_debug_zones(self) -> None:
        selected_flight = None
        if self._selected_flight is not None:
            selected_flight = self._selected_flight.flight
        if selected_flight is None:
            self._ip_zones = IpZonesJs.empty()
            self._join_zones = JoinZonesJs.empty()
            self._hold_zones = HoldZonesJs.empty()
        else:
            self._ip_zones = IpZonesJs.for_flight(selected_flight, self.game)
            self._join_zones = JoinZonesJs.for_flight(selected_flight, self.game)
            self._hold_zones = HoldZonesJs.for_flight(selected_flight, self.game)
        self.ipZonesChanged.emit()
        self.joinZonesChanged.emit()
        self.holdZonesChanged.emit()

    @Property(list, notify=flightsChanged)
    def flights(self) -> list[FlightJs]:
        return list(self._flights.values())

    def reset_control_points(self) -> None:
        self._control_points = [
            ControlPointJs(c, self.game_model, self.game.theater)
            for c in self.game.theater.controlpoints
        ]
        self.controlPointsChanged.emit()

    @Property(list, notify=controlPointsChanged)
    def controlPoints(self) -> List[ControlPointJs]:
        return self._control_points

    def reset_ground_objects(self) -> None:
        seen = set()
        self._ground_objects = []
        for cp in self.game.theater.controlpoints:
            for tgo in cp.ground_objects:
                if tgo.name in seen:
                    continue
                seen.add(tgo.name)

                if tgo.is_control_point:
                    # TGOs that are the CP (CV groups) are an implementation quirk that
                    # we don't need to expose to the UI.
                    continue

                self._ground_objects.append(GroundObjectJs(tgo, self.game))
        self.groundObjectsChanged.emit()

    @Property(list, notify=groundObjectsChanged)
    def groundObjects(self) -> List[GroundObjectJs]:
        return self._ground_objects

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
                        [
                            self.leaflet_coord_for(p, self.game.theater)
                            for p in convoy_route
                        ],
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
                            [
                                self.leaflet_coord_for(p, self.game.theater)
                                for p in shipping_lane
                            ],
                            sea_route=True,
                            game=self.game,
                        )
                    )
        self.supplyRoutesChanged.emit()

    @Property(list, notify=supplyRoutesChanged)
    def supplyRoutes(self) -> List[SupplyRouteJs]:
        return self._supply_routes

    def reset_front_lines(self) -> None:
        self._front_lines = [
            FrontLineJs(f, self.game.theater) for f in self.game.theater.conflicts()
        ]
        self.frontLinesChanged.emit()

    @Property(list, notify=frontLinesChanged)
    def frontLines(self) -> List[FrontLineJs]:
        return self._front_lines

    def reset_threat_zones(self) -> None:
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.from_zones(
                self.game.threat_zone_for(player=True), self.game.theater
            ),
            ThreatZonesJs.from_zones(
                self.game.threat_zone_for(player=False), self.game.theater
            ),
        )
        self.threatZonesChanged.emit()

    @Property(ThreatZoneContainerJs, notify=threatZonesChanged)
    def threatZones(self) -> ThreatZoneContainerJs:
        return self._threat_zones

    def reset_navmeshes(self) -> None:
        self._navmeshes = NavMeshJs.from_game(self.game)
        self.navmeshesChanged.emit()

    @Property(NavMeshJs, notify=navmeshesChanged)
    def navmeshes(self) -> NavMeshJs:
        return self._navmeshes

    def reset_map_zones(self) -> None:
        self._map_zones = MapZonesJs.from_game(self.game)
        self.mapZonesChanged.emit()

    @Property(MapZonesJs, notify=mapZonesChanged)
    def mapZones(self) -> NavMeshJs:
        return self._map_zones

    def on_package_change(self) -> None:
        self.reset_unculled_zones()

    def reset_unculled_zones(self) -> None:
        self._unculled_zones = list(UnculledZone.each_from_game(self.game))
        self.unculledZonesChanged.emit()

    @Property(list, notify=unculledZonesChanged)
    def unculledZones(self) -> list[UnculledZone]:
        return self._unculled_zones

    @Property(str, notify=ipZonesChanged)
    def ipZones(self) -> str:
        return json.dumps(self._ip_zones.dict(by_alias=True))

    @Property(str, notify=joinZonesChanged)
    def joinZones(self) -> str:
        # Must be dumped as a string and deserialized in js because QWebChannel can't
        # handle a dict. Can be cleaned up by switching from QWebChannel to FastAPI.
        return json.dumps(self._join_zones.dict(by_alias=True))

    @Property(str, notify=holdZonesChanged)
    def holdZones(self) -> str:
        return json.dumps(self._hold_zones.dict(by_alias=True))

    def reset_combats(self) -> None:
        self._air_combats = []
        self._sam_combats = []
        self._ip_combats = []
        self.airCombatsChanged.emit()
        self.samCombatsChanged.emit()
        self.ipCombatsChanged.emit()

    def on_add_combat(self, combat: FrozenCombat) -> None:
        if isinstance(combat, AirCombat):
            self.add_air_combat(combat)
        elif isinstance(combat, DefendingSam):
            self.add_sam_combat(combat)
        elif isinstance(combat, AtIp):
            self.add_ip_combat(combat)
        else:
            logging.error(f"Unhandled FrozenCombat type: {combat.__class__}")

    def add_air_combat(self, combat: AirCombat) -> None:
        self._air_combats.append(AirCombatJs(combat, self.game.theater))
        self.airCombatsChanged.emit()

    def add_sam_combat(self, combat: DefendingSam) -> None:
        self._sam_combats.append(SamCombatJs(combat, self.game_model))
        self.samCombatsChanged.emit()

    def add_ip_combat(self, combat: AtIp) -> None:
        self._ip_combats.append(IpCombatJs(combat, self.game_model))
        self.ipCombatsChanged.emit()

    def on_combat_changed(self, combat: FrozenCombat) -> None:
        if isinstance(combat, AirCombat):
            self.refresh_air_combat(combat)
        elif isinstance(combat, DefendingSam):
            self.refresh_sam_combat(combat)
        elif isinstance(combat, AtIp):
            self.refresh_ip_combat(combat)
        else:
            logging.error(f"Unhandled FrozenCombat type: {combat.__class__}")

    def refresh_air_combat(self, combat: AirCombat) -> None:
        for js in self._air_combats:
            if js.combat == combat:
                js.refresh()
                return
        logging.error(f"Could not find existing combat model to update for {combat}")

    def refresh_sam_combat(self, combat: DefendingSam) -> None:
        for js in self._sam_combats:
            if js.combat == combat:
                js.refresh()
                return
        logging.error(f"Could not find existing combat model to update for {combat}")

    def refresh_ip_combat(self, combat: AtIp) -> None:
        for js in self._ip_combats:
            if js.combat == combat:
                js.refresh()
                return
        logging.error(f"Could not find existing combat model to update for {combat}")

    @Property(list, notify=airCombatsChanged)
    def airCombats(self) -> list[AirCombatJs]:
        return self._air_combats

    @Property(list, notify=samCombatsChanged)
    def samCombats(self) -> list[SamCombatJs]:
        return self._sam_combats

    @Property(list, notify=ipCombatsChanged)
    def ipCombats(self) -> list[IpCombatJs]:
        return self._ip_combats

    @property
    def game(self) -> Game:
        if self.game_model.game is None:
            raise RuntimeError("No game loaded")
        return self.game_model.game
