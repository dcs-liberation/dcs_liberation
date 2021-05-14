import logging
from datetime import timedelta
from typing import List, Optional, Tuple

from PySide2.QtCore import Property, QObject, Signal, Slot
from dcs import Point
from dcs.unit import Unit
from dcs.vehicles import vehicle_map

from game import Game, db
from game.profiling import logged_duration
from game.theater import (
    ConflictTheater,
    ControlPoint,
    TheaterGroundObject,
    FrontLine,
)
from game.utils import meters, nautical_miles
from gen.ato import AirTaskingOrder
from gen.flights.flight import Flight, FlightWaypoint, FlightWaypointType
from gen.flights.flightplan import FlightPlan
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu

LeafletLatLon = List[float]

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


class ControlPointJs(QObject):
    nameChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()

    def __init__(
        self,
        control_point: ControlPoint,
        game_model: GameModel,
        theater: ConflictTheater,
    ) -> None:
        super().__init__()
        self.control_point = control_point
        self.game_model = game_model
        self.theater = theater
        self.dialog: Optional[QBaseMenu2] = None

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.control_point.name

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.control_point.captured

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.control_point.position)
        return [ll.latitude, ll.longitude]

    @Slot()
    def showInfoDialog(self) -> None:
        if self.dialog is None:
            self.dialog = QBaseMenu2(None, self.control_point, self.game_model)
        self.dialog.show()

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.control_point)


class GroundObjectJs(QObject):
    nameChanged = Signal()
    unitsChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()
    samThreatRangesChanged = Signal()
    samDetectionRangesChanged = Signal()

    def __init__(self, tgo: TheaterGroundObject, game: Game) -> None:
        super().__init__()
        self.tgo = tgo
        self.game = game
        self.theater = game.theater
        self.buildings = self.theater.find_ground_objects_by_obj_name(self.tgo.obj_name)

        if self.tgo.is_friendly(to_player=True):
            self.country = game.player_country
        else:
            self.country = game.enemy_country

        self.dialog: Optional[QGroundObjectMenu] = None

    @Slot()
    def showInfoDialog(self) -> None:
        if self.dialog is None:
            self.dialog = QGroundObjectMenu(
                None,
                self.tgo,
                self.buildings,
                self.tgo.control_point,
                self.game,
            )
        self.dialog.show()

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.tgo)

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.tgo.name

    def make_unit_name(self, unit: Unit, dead: bool) -> str:
        dead_label = " [DEAD]" if dead else ""
        unit_display_name = unit.type
        unit_type = vehicle_map.get(unit.type)
        if unit_type is not None:
            unit_display_name = db.unit_get_expanded_info(
                self.country, unit_type, "name"
            )
        return f"Unit #{unit.id} - {unit_display_name}{dead_label}"

    @Property(list, notify=unitsChanged)
    def units(self) -> List[str]:
        units = []
        if self.buildings:
            for building in self.buildings:
                dead = " [DEAD]" if building.is_dead else ""
                units.append(f"{building.dcs_identifier}{dead}")
        else:
            for unit in self.tgo.units:
                units.append(self.make_unit_name(unit, dead=False))
            for unit in self.tgo.dead_units:
                units.append(self.make_unit_name(unit, dead=True))
        return units

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.tgo.control_point.captured

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.tgo.position)
        return [ll.latitude, ll.longitude]

    @Property(list, notify=samThreatRangesChanged)
    def samThreatRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            threat_range = self.tgo.threat_range(group)
            if threat_range:
                ranges.append(threat_range.meters)
        return ranges

    @Property(list, notify=samDetectionRangesChanged)
    def samDetectionRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            detection_range = self.tgo.detection_range(group)
            if detection_range:
                ranges.append(detection_range.meters)
        return ranges


class SupplyRouteJs(QObject):
    pointsChanged = Signal()
    frontActiveChanged = Signal()
    isSeaChanged = Signal()
    blueChanged = Signal()

    def __init__(
        self,
        a: ControlPoint,
        b: ControlPoint,
        points: List[LeafletLatLon],
        sea_route: bool,
    ) -> None:
        super().__init__()
        self.control_point_a = a
        self.control_point_b = b
        self._points = points
        self.sea_route = sea_route

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


class FrontLineJs(QObject):
    extentsChanged = Signal()

    def __init__(self, front_line: FrontLine, theater: ConflictTheater) -> None:
        super().__init__()
        self.front_line = front_line
        self.theater = theater

    @Property(list, notify=extentsChanged)
    def extents(self) -> List[LeafletLatLon]:
        a = self.theater.point_to_ll(
            self.front_line.position.point_from_heading(
                self.front_line.attack_heading + 90, nautical_miles(2).meters
            )
        )
        b = self.theater.point_to_ll(
            self.front_line.position.point_from_heading(
                self.front_line.attack_heading + 270, nautical_miles(2).meters
            )
        )
        return [[a.latitude, a.longitude], [b.latitude, b.longitude]]

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.front_line)


class WaypointJs(QObject):
    numberChanged = Signal()
    positionChanged = Signal()
    altitudeFtChanged = Signal()
    altitudeReferenceChanged = Signal()
    nameChanged = Signal()
    timingChanged = Signal()
    isDivertChanged = Signal()

    def __init__(
        self,
        waypoint: FlightWaypoint,
        number: int,
        flight_plan: FlightPlan,
        theater: ConflictTheater,
    ) -> None:
        super().__init__()
        self.waypoint = waypoint
        self._number = number
        self.flight_plan = flight_plan
        self.theater = theater

    @Property(int, notify=numberChanged)
    def number(self) -> int:
        return self._number

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.waypoint.position)
        return [ll.latitude, ll.longitude]

    @Property(int, notify=altitudeFtChanged)
    def altitudeFt(self) -> int:
        return int(self.waypoint.alt.feet)

    @Property(str, notify=altitudeReferenceChanged)
    def altitudeReference(self) -> str:
        return "AGL" if self.waypoint.alt_type == "RADIO" else "MSL"

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.waypoint.name

    @Property(str, notify=timingChanged)
    def timing(self) -> str:
        prefix = "TOT"
        time = self.flight_plan.tot_for_waypoint(self.waypoint)
        if time is None:
            prefix = "Depart"
            time = self.flight_plan.depart_time_for_waypoint(self.waypoint)
        if time is None:
            return ""
        return f"{prefix} T+{timedelta(seconds=int(time.total_seconds()))}"

    @Property(bool, notify=isDivertChanged)
    def isDivert(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.DIVERT


class FlightJs(QObject):
    flightPlanChanged = Signal()
    blueChanged = Signal()
    selectedChanged = Signal()

    def __init__(
        self, flight: Flight, selected: bool, theater: ConflictTheater
    ) -> None:
        super().__init__()
        self.flight = flight
        self._selected = selected
        self.theater = theater
        self._waypoints = []
        self.reset_waypoints()

    def reset_waypoints(self) -> None:
        departure = FlightWaypoint(
            FlightWaypointType.TAKEOFF,
            self.flight.departure.position.x,
            self.flight.departure.position.y,
            meters(0),
        )
        departure.alt_type = "RADIO"
        self._waypoints = [
            WaypointJs(p, i, self.flight.flight_plan, self.theater)
            for i, p in enumerate([departure] + self.flight.points)
        ]
        self.flightPlanChanged.emit()

    @Property(list, notify=flightPlanChanged)
    def flightPlan(self) -> List[WaypointJs]:
        return self._waypoints

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.flight.departure.captured

    @Property(bool, notify=selectedChanged)
    def selected(self) -> bool:
        return self._selected


class MapModel(QObject):
    cleared = Signal()

    mapCenterChanged = Signal(list)
    controlPointsChanged = Signal()
    groundObjectsChanged = Signal()
    supplyRoutesChanged = Signal()
    flightsChanged = Signal()
    frontLinesChanged = Signal()

    def __init__(self, game_model: GameModel) -> None:
        super().__init__()
        self.game_model = game_model
        self._map_center = [0, 0]
        self._control_points = []
        self._ground_objects = []
        self._supply_routes = []
        self._flights = []
        self._front_lines = []
        self._selected_flight_index: Optional[Tuple[int, int]] = None
        GameUpdateSignal.get_instance().game_loaded.connect(self.on_game_load)
        GameUpdateSignal.get_instance().flight_paths_changed.connect(self.reset_atos)
        GameUpdateSignal.get_instance().package_selection_changed.connect(
            self.set_package_selection
        )
        GameUpdateSignal.get_instance().flight_selection_changed.connect(
            self.set_flight_selection
        )
        self.reset()

    def clear(self) -> None:
        self._control_points = []
        self._supply_routes = []
        self._ground_objects = []
        self._flights = []
        self._front_lines = []
        self.cleared.emit()

    def set_package_selection(self, index: int) -> None:
        # Optional[int] isn't a valid type for a Qt signal. None will be converted to
        # zero automatically. We use -1 to indicate no selection.
        if index == -1:
            self._selected_flight_index = None
        else:
            self._selected_flight_index = index, 0
        self.reset_atos()

    def set_flight_selection(self, index: int) -> None:
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
        self.reset_atos()

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

    def _flights_in_ato(self, ato: AirTaskingOrder, blue: bool) -> List[FlightJs]:
        flights = []
        for p_idx, package in enumerate(ato.packages):
            for f_idx, flight in enumerate(package.flights):
                flights.append(
                    FlightJs(
                        flight,
                        selected=blue and (p_idx, f_idx) == self._selected_flight_index,
                        theater=self.game.theater,
                    )
                )
        return flights

    def reset_atos(self) -> None:
        self._flights = self._flights_in_ato(
            self.game.blue_ato, blue=True
        ) + self._flights_in_ato(self.game.red_ato, blue=False)
        self.flightsChanged.emit()

    @Property(list, notify=flightsChanged)
    def flights(self) -> List[FlightJs]:
        return self._flights

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

    @property
    def game(self) -> Game:
        if self.game_model.game is None:
            raise RuntimeError("No game loaded")
        return self.game_model.game
