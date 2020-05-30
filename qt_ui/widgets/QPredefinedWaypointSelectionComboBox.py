from PySide2.QtCore import QSortFilterProxyModel, Qt, QModelIndex
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QComboBox, QCompleter
from game import Game
from gen import Conflict
from gen.flights.flight import FlightWaypoint
from theater import ControlPointType


class QPredefinedWaypointSelectionComboBox(QComboBox):

    def __init__(self, game: Game, parent=None):
        super(QPredefinedWaypointSelectionComboBox, self).__init__(parent)

        self.game = game
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.completer = QCompleter(self)

        # always show all completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.completer.setPopup(self.view())

        self.setCompleter(self.completer)

        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

        self.find_possible_waypoints()

    def setModel(self, model):
        super(QPredefinedWaypointSelectionComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(QPredefinedWaypointSelectionComboBox, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

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
                if w is not first_waypoint and w.obj_name and w.obj_name == first_waypoint.obj_name:
                    waypoints.append(w)

        return waypoints

    def find_possible_waypoints(self):

        self.wpts = []
        model = QStandardItemModel()
        i = 0

        def add_model_item(i, model, name, wpt):
            print(name)
            item = QStandardItem(name)
            model.setItem(i, 0, item)
            self.wpts.append(wpt)
            return i + 1

        for cp in self.game.theater.controlpoints:
            print(cp)
            if cp.captured:
                enemy_cp = [ecp for ecp in cp.connected_points if ecp.captured != cp.captured]
                for ecp in enemy_cp:
                    pos = Conflict.frontline_position(self.game.theater, cp, ecp)[0]
                    wpt = FlightWaypoint(pos.x, pos.y, 800)
                    wpt.name = "Frontline " + cp.name + "/" + ecp.name + " [CAS]"
                    wpt.pretty_name = wpt.name
                    wpt.description = "Frontline"
                    i = add_model_item(i, model, wpt.pretty_name, wpt)


        for cp in self.game.theater.controlpoints:
            for ground_object in cp.ground_objects:
                if not ground_object.is_dead and not ground_object.dcs_identifier == "AA":
                    wpt = FlightWaypoint(ground_object.position.x,ground_object.position.y, 0)
                    wpt.name = wpt.name = "[" + str(ground_object.obj_name) + "] : " + ground_object.category + " #" + str(ground_object.object_id)
                    wpt.pretty_name = wpt.name
                    wpt.obj_name = ground_object.obj_name
                    if cp.captured:
                        wpt.description = "Friendly Building"
                    else:
                        wpt.description = "Enemy Building"
                    i = add_model_item(i, model, wpt.pretty_name, wpt)

        for cp in self.game.theater.controlpoints:

            for ground_object in cp.ground_objects:
                if not ground_object.is_dead and ground_object.dcs_identifier == "AA":
                    for g in ground_object.groups:
                        for j, u in enumerate(g.units):
                            wpt = FlightWaypoint(u.position.x, u.position.y, 0)
                            wpt.name = wpt.name = "[" + str(ground_object.obj_name) + "] : " + u.type + " #" + str(j)
                            wpt.pretty_name = wpt.name
                            wpt.obj_name = ground_object.obj_name
                            if cp.captured:
                                wpt.description = "Friendly unit : " + u.type
                            else:
                                wpt.description = "Enemy unit : " + u.type
                            i = add_model_item(i, model, wpt.pretty_name, wpt)

        for cp in self.game.theater.controlpoints:

            wpt = FlightWaypoint(cp.position.x, cp.position.y, 0)
            wpt.name = cp.name
            if cp.captured:
                wpt.description = "Position of " + cp.name + " [Friendly Airbase]"
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
