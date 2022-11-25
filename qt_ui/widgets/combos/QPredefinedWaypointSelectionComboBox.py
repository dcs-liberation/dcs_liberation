from PySide2.QtGui import QStandardItem, QStandardItemModel

from game import Game
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.frontlineconflictdescription import (
    FrontLineConflictDescription,
)
from game.theater.controlpoint import ControlPointType
from game.utils import Distance
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
                pos = FrontLineConflictDescription.frontline_position(
                    front_line, self.game.theater
                )[0]
                wptname = f"Frontline {front_line.name} [CAS]"
                wpt = FlightWaypoint(
                    wptname, FlightWaypointType.CUSTOM, pos, Distance.from_meters(800)
                )

                wpt.alt_type = "RADIO"
                wpt.pretty_name = wpt.name
                wpt.description = "Frontline"
                i = add_model_item(i, model, wpt.pretty_name, wpt)

        for tgo in self.game.theater.ground_objects:
            for target_idx, target in enumerate(tgo.strike_targets):
                wptname = f"[{tgo.obj_name}] : {target.name} #{target_idx}"
                wpt = FlightWaypoint(
                    wptname,
                    FlightWaypointType.CUSTOM,
                    target.position,
                    Distance.from_meters(0),
                )
                wpt.alt_type = "RADIO"
                wpt.pretty_name = wptname
                wpt.targets.append(target)
                wpt.obj_name = tgo.obj_name
                wpt.waypoint_type = FlightWaypointType.CUSTOM
                if tgo.is_friendly(to_player=True):
                    wpt.description = f"Friendly unit: {target.name}"
                else:
                    wpt.description = f"Enemy unit: {target.name}"
                i = add_model_item(i, model, wpt.pretty_name, wpt)

        if self.include_airbases:
            for cp in self.game.theater.controlpoints:
                if (self.include_enemy and not cp.captured) or (
                    self.include_friendly and cp.captured
                ):
                    wpt = FlightWaypoint(
                        cp.name,
                        FlightWaypointType.CUSTOM,
                        cp.position,
                        Distance.from_meters(0),
                    )
                    wpt.alt_type = "RADIO"
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
