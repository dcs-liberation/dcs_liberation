from __future__ import annotations

import logging
from datetime import timedelta
from typing import List, Optional, Tuple, Union

from PySide2.QtCore import Property, QObject, Signal, Slot
from dcs import Point
from dcs.unit import Unit
from dcs.vehicles import vehicle_map
from shapely.geometry import LineString, Point as ShapelyPoint, Polygon, MultiPolygon

from game import Game, db
from game.factions.faction import Faction
from game.profiling import logged_duration
from game.theater import (
    ConflictTheater,
    ControlPoint,
    TheaterGroundObject,
    FrontLine,
    LatLon,
)
from game.threatzones import ThreatZones
from game.transfers import MultiGroupTransport, TransportMap
from game.utils import meters, nautical_miles
from gen.ato import AirTaskingOrder
from gen.flights.flight import Flight, FlightWaypoint, FlightWaypointType
from gen.flights.flightplan import FlightPlan, PatrollingFlightPlan
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel, AtoModel
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


def shapely_poly_to_leaflet_points(
    poly: Polygon, theater: ConflictTheater
) -> Optional[List[LeafletLatLon]]:
    if poly.is_empty:
        return None
    return [theater.point_to_ll(Point(x, y)).as_list() for x, y in poly.exterior.coords]


class ControlPointJs(QObject):
    nameChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()
    mobileChanged = Signal()
    destinationChanged = Signal(list)
    categoryChanged = Signal()

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

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.control_point.category

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.control_point.position)
        return [ll.latitude, ll.longitude]

    @Property(bool, notify=mobileChanged)
    def mobile(self) -> bool:
        return self.control_point.moveable and self.control_point.captured

    @Property(list, notify=destinationChanged)
    def destination(self) -> LeafletLatLon:
        if self.control_point.target_position is None:
            # Qt seems to convert None to [] for list Properties :(
            return []
        return self.theater.point_to_ll(self.control_point.target_position).as_list()

    def destination_in_range(self, destination: Point) -> bool:
        from qt_ui.widgets.map.QLiberationMap import MAX_SHIP_DISTANCE

        move_distance = meters(
            destination.distance_to_point(self.control_point.position)
        )
        return move_distance <= MAX_SHIP_DISTANCE

    @Slot(list, result=bool)
    def destinationInRange(self, destination: LeafletLatLon) -> bool:
        return self.destination_in_range(self.theater.ll_to_point(LatLon(*destination)))

    @Slot(list, result=str)
    def setDestination(self, destination: LeafletLatLon) -> str:
        from qt_ui.widgets.map.QLiberationMap import MAX_SHIP_DISTANCE

        if not self.control_point.moveable:
            return f"{self.control_point} is not mobile"
        if not self.control_point.captured:
            return f"{self.control_point} is not owned by player"

        point = self.theater.ll_to_point(LatLon(*destination))
        if not self.destination_in_range(point):
            return (
                f"Cannot move {self.control_point} more than "
                f"{MAX_SHIP_DISTANCE.nautical_miles}nm."
            )
        self.control_point.target_position = point
        self.destinationChanged.emit(destination)
        return ""

    @Slot()
    def cancelTravel(self) -> None:
        self.control_point.target_position = None
        self.destinationChanged.emit([])

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
    categoryChanged = Signal()
    deadChanged = Signal()

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

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.tgo.category

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
        # TGOs with a non-empty group set are non-building TGOs. Building TGOs have no
        # groups set, but instead are one TGO per building "group" (DCS doesn't support
        # groups of statics) all with the same name.
        if self.tgo.groups:
            for unit in self.tgo.units:
                units.append(self.make_unit_name(unit, dead=False))
            for unit in self.tgo.dead_units:
                units.append(self.make_unit_name(unit, dead=True))
        else:
            for building in self.buildings:
                dead = " [DEAD]" if building.is_dead else ""
                units.append(f"{building.dcs_identifier}{dead}")
        return units

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.tgo.control_point.captured

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.tgo.position)
        return [ll.latitude, ll.longitude]

    @Property(bool, notify=deadChanged)
    def dead(self) -> bool:
        if not self.tgo.groups:
            return all(b.is_dead for b in self.buildings)
        return not any(g.units for g in self.tgo.groups)

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
            return self.find_in_transport_map(self.game.transfers.cargo_ships)
        return self.find_in_transport_map(self.game.transfers.convoys)

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
    isTakeoffChanged = Signal()
    isDivertChanged = Signal()
    isBullseyeChanged = Signal()

    def __init__(
        self,
        waypoint: FlightWaypoint,
        number: int,
        flight_model: FlightJs,
        theater: ConflictTheater,
        ato_model: AtoModel,
    ) -> None:
        super().__init__()
        self.waypoint = waypoint
        self._number = number
        self.flight_model = flight_model
        self.theater = theater
        self.ato_model = ato_model

    @property
    def flight(self) -> Flight:
        return self.flight_model.flight

    @property
    def flight_plan(self) -> FlightPlan:
        return self.flight.flight_plan

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

    @Property(bool, notify=isTakeoffChanged)
    def isTakeoff(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.TAKEOFF

    @Property(bool, notify=isDivertChanged)
    def isDivert(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.DIVERT

    @Property(bool, notify=isBullseyeChanged)
    def isBullseye(self) -> bool:
        return self.waypoint.waypoint_type is FlightWaypointType.BULLSEYE

    @Slot(list, result=str)
    def setPosition(self, position: LeafletLatLon) -> str:
        point = self.theater.ll_to_point(LatLon(*position))
        self.waypoint.x = point.x
        self.waypoint.y = point.y
        package = self.ato_model.find_matching_package_model(self.flight.package)
        if package is None:
            return "Could not find package model containing modified flight"
        package.update_tot()
        self.positionChanged.emit()
        self.flight_model.commitBoundaryChanged.emit()
        return ""


class FlightJs(QObject):
    flightPlanChanged = Signal()
    blueChanged = Signal()
    selectedChanged = Signal()
    commitBoundaryChanged = Signal()

    def __init__(
        self,
        flight: Flight,
        selected: bool,
        theater: ConflictTheater,
        faction: Faction,
        ato_model: AtoModel,
    ) -> None:
        super().__init__()
        self.flight = flight
        self._selected = selected
        self.theater = theater
        self.faction = faction
        self.ato_model = ato_model
        self._waypoints = self.make_waypoints()

    def update_waypoints(self) -> None:
        for waypoint in self._waypoints:
            waypoint.timingChanged.emit()

    def make_waypoints(self) -> List[WaypointJs]:
        departure = FlightWaypoint(
            FlightWaypointType.TAKEOFF,
            self.flight.departure.position.x,
            self.flight.departure.position.y,
            meters(0),
        )
        departure.alt_type = "RADIO"
        waypoints = []
        for idx, point in enumerate([departure] + self.flight.points):
            waypoint = WaypointJs(point, idx, self, self.theater, self.ato_model)
            waypoint.positionChanged.connect(self.update_waypoints)
            waypoints.append(waypoint)
        return waypoints

    @Property(list, notify=flightPlanChanged)
    def flightPlan(self) -> List[WaypointJs]:
        return self._waypoints

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.flight.departure.captured

    @Property(bool, notify=selectedChanged)
    def selected(self) -> bool:
        return self._selected

    @Property(list, notify=commitBoundaryChanged)
    def commitBoundary(self) -> List[LeafletLatLon]:
        if not isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            return []
        start = self.flight.flight_plan.patrol_start
        end = self.flight.flight_plan.patrol_end
        line = LineString(
            [
                ShapelyPoint(start.x, start.y),
                ShapelyPoint(end.x, end.y),
            ]
        )
        doctrine = self.faction.doctrine
        bubble = line.buffer(doctrine.cap_engagement_range.meters)
        return shapely_poly_to_leaflet_points(bubble, self.theater)


class ThreatZonesJs(QObject):
    fullChanged = Signal()
    aircraftChanged = Signal()
    airDefensesChanged = Signal()
    radarSamsChanged = Signal()

    def __init__(
        self,
        full: List[List[LeafletLatLon]],
        aircraft: List[List[LeafletLatLon]],
        air_defenses: List[List[LeafletLatLon]],
        radar_sams: List[List[LeafletLatLon]],
    ) -> None:
        super().__init__()
        self._full = full
        self._aircraft = aircraft
        self._air_defenses = air_defenses
        self._radar_sams = radar_sams

    @Property(list, notify=fullChanged)
    def full(self) -> List[List[LeafletLatLon]]:
        return self._full

    @Property(list, notify=aircraftChanged)
    def aircraft(self) -> List[List[LeafletLatLon]]:
        return self._aircraft

    @Property(list, notify=airDefensesChanged)
    def airDefenses(self) -> List[List[LeafletLatLon]]:
        return self._air_defenses

    @Property(list, notify=radarSamsChanged)
    def radarSams(self) -> List[List[LeafletLatLon]]:
        return self._radar_sams

    @staticmethod
    def polys_to_leaflet(
        poly: Union[Polygon, MultiPolygon], theater: ConflictTheater
    ) -> List[List[LeafletLatLon]]:
        if isinstance(poly, MultiPolygon):
            polys = poly.geoms
        else:
            polys = [poly]
        return [shapely_poly_to_leaflet_points(poly, theater) for poly in polys]

    @classmethod
    def from_zones(cls, zones: ThreatZones, theater: ConflictTheater) -> ThreatZonesJs:
        return ThreatZonesJs(
            cls.polys_to_leaflet(zones.all, theater),
            cls.polys_to_leaflet(zones.airbases, theater),
            cls.polys_to_leaflet(zones.air_defenses, theater),
            cls.polys_to_leaflet(zones.radar_sam_threats, theater),
        )

    @classmethod
    def empty(cls) -> ThreatZonesJs:
        return ThreatZonesJs([], [], [], [])


class ThreatZoneContainerJs(QObject):
    blueChanged = Signal()
    redChanged = Signal()

    def __init__(self, blue: ThreatZonesJs, red: ThreatZonesJs) -> None:
        super().__init__()
        self._blue = blue
        self._red = red

    @Property(ThreatZonesJs, notify=blueChanged)
    def blue(self) -> ThreatZonesJs:
        return self._blue

    @Property(ThreatZonesJs, notify=redChanged)
    def red(self) -> ThreatZonesJs:
        return self._red


class MapModel(QObject):
    cleared = Signal()

    mapCenterChanged = Signal(list)
    controlPointsChanged = Signal()
    groundObjectsChanged = Signal()
    supplyRoutesChanged = Signal()
    flightsChanged = Signal()
    frontLinesChanged = Signal()
    threatZonesChanged = Signal()

    def __init__(self, game_model: GameModel) -> None:
        super().__init__()
        self.game_model = game_model
        self._map_center = [0, 0]
        self._control_points = []
        self._ground_objects = []
        self._supply_routes = []
        self._flights = []
        self._front_lines = []
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.empty(), ThreatZonesJs.empty()
        )
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
        self._threat_zones = ThreatZoneContainerJs(
            ThreatZonesJs.empty(), ThreatZonesJs.empty()
        )
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
            self.reset_threat_zones()

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
                        faction=self.game.faction_for(blue),
                        ato_model=self.game_model.ato_model_for(blue),
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

    @property
    def game(self) -> Game:
        if self.game_model.game is None:
            raise RuntimeError("No game loaded")
        return self.game_model.game
