from PySide2.QtGui import QStandardItem, QStandardItemModel

from game import Game
from game.theater import ControlPointType, BuildingGroundObject
from game.utils import Distance
from gen.conflictgen import Conflict
from gen.flights.flight import FlightWaypoint, FlightWaypointType
from qt_ui.widgets.combos.QFilteredComboBox import QFilteredComboBox


class QPredefinedWaypointSelectionComboBox(QFilteredComboBox):
    def __init__(
        self,
        game: Game,
        parent=None,
        include_targets=True,
        include_airbases=True,
        include_frontlines=True,
        include_units=True,
        include_enemy=True,
        include_friendly=True,
    ):
        super(QPredefinedWaypointSelectionComboBox, self).__init__(parent)
        self.game = game
        self.include_targets = include_targets
        self.include_airbases = include_airbases
        self.include_frontlines = include_frontlines
        self.include_units = include_units
        self.include_enemy = include_enemy
        self.include_friendly = include_friendly
        self.find_possible_waypoints()

    def get_selected_waypoints(self, include_all_from_same_location=False):
        n = self.currentText()
        first_waypoint = None
        for w in self.wpts:
            if w.pretty_name == n:
                first_waypoint = w
                break
        if first_waypoint is None:
            return []
        waypoints = [first_waypoint]
        if include_all_from_same_location:
            for w in self.wpts:
                if (
                    w is not first_waypoint
                    and w.obj_name
                    and w.obj_name == first_waypoint.obj_name
                ):
                    waypoints.append(w)
        return waypoints

    def find_possible_waypoints(self):

        self.wpts = []
        model = QStandardItemModel()
        i = 0

        def add_model_item(i, model, name, wpt):
            item = QStandardItem(name)
            model.setItem(i, 0, item)
            self.wpts.append(wpt)
            return i + 1

        if self.include_frontlines:
            for front_line in self.game.theater.conflicts():
                pos = Conflict.frontline_position(front_line, self.game.theater)[0]
                wpt = FlightWaypoint(
                    FlightWaypointType.CUSTOM,
                    pos.x,
                    pos.y,
                    Distance.from_meters(800),
                )
                wpt.name = f"Frontline {front_line.name} [CAS]"
                wpt.alt_type = "RADIO"
                wpt.pretty_name = wpt.name
                wpt.description = "Frontline"
                i = add_model_item(i, model, wpt.pretty_name, wpt)

        if self.include_targets:
            for cp in self.game.theater.controlpoints:
                if (self.include_enemy and not cp.captured) or (
                    self.include_friendly and cp.captured
                ):
                    for ground_object in cp.ground_objects:
                        if not ground_object.is_dead and isinstance(
                            ground_object, BuildingGroundObject
                        ):
                            wpt = FlightWaypoint(
                                FlightWaypointType.CUSTOM,
                                ground_object.position.x,
                                ground_object.position.y,
                                Distance.from_meters(0),
                            )
                            wpt.alt_type = "RADIO"
                            wpt.name = ground_object.waypoint_name
                            wpt.pretty_name = wpt.name
                            wpt.obj_name = ground_object.obj_name
                            wpt.targets.append(ground_object)
                            if cp.captured:
                                wpt.description = "Friendly Building"
                            else:
                                wpt.description = "Enemy Building"
                            i = add_model_item(i, model, wpt.pretty_name, wpt)

        if self.include_units:
            for cp in self.game.theater.controlpoints:
                if (self.include_enemy and not cp.captured) or (
                    self.include_friendly and cp.captured
                ):
                    for ground_object in cp.ground_objects:
                        if not ground_object.is_dead and (
                            ground_object.dcs_identifier == "AA"
                            or ground_object.dcs_identifier == "EWR"
                        ):
                            for g in ground_object.groups:
                                for j, u in enumerate(g.units):
                                    wpt = FlightWaypoint(
                                        FlightWaypointType.CUSTOM,
                                        u.position.x,
                                        u.position.y,
                                        Distance.from_meters(0),
                                    )
                                    wpt.alt_type = "RADIO"
                                    wpt.name = wpt.name = (
                                        "["
                                        + str(ground_object.obj_name)
                                        + "] : "
                                        + u.type
                                        + " #"
                                        + str(j)
                                    )
                                    wpt.pretty_name = wpt.name
                                    wpt.targets.append(u)
                                    wpt.obj_name = ground_object.obj_name
                                    wpt.waypoint_type = FlightWaypointType.CUSTOM
                                    if cp.captured:
                                        wpt.description = "Friendly unit : " + u.type
                                    else:
                                        wpt.description = "Enemy unit : " + u.type
                                    i = add_model_item(i, model, wpt.pretty_name, wpt)

        if self.include_airbases:
            for cp in self.game.theater.controlpoints:
                if (self.include_enemy and not cp.captured) or (
                    self.include_friendly and cp.captured
                ):
                    wpt = FlightWaypoint(
                        FlightWaypointType.CUSTOM,
                        cp.position.x,
                        cp.position.y,
                        Distance.from_meters(0),
                    )
                    wpt.alt_type = "RADIO"
                    wpt.name = cp.name
                    if cp.captured:
                        wpt.description = (
                            "Position of " + cp.name + " [Friendly Airbase]"
                        )
                    else:
                        wpt.description = "Position of " + cp.name + " [Enemy Airbase]"

                    if cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
                        wpt.pretty_name = cp.name + " (Aircraft Carrier Group)"
                    elif cp.cptype == ControlPointType.LHA_GROUP:
                        wpt.pretty_name = cp.name + " (LHA Group)"
                    else:
                        wpt.pretty_name = cp.name + " (Airbase)"

                    i = add_model_item(i, model, wpt.pretty_name, wpt)

        self.setModel(model)
