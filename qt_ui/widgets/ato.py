"""Widgets for displaying air tasking orders."""
import logging
from typing import Optional

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
)
from PySide2.QtGui import (
    QContextMenuEvent,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QMenu,
    QPushButton,
    QSplitter,
    QVBoxLayout,
)

from gen.ato import Package
from gen.flights.flight import Flight
from gen.flights.traveltime import TotEstimator
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from ..delegates import TwoColumnRowDelegate
from ..models import AtoModel, GameModel, NullListModel, PackageModel


class FlightDelegate(TwoColumnRowDelegate):
    def __init__(self, package: Package) -> None:
        super().__init__(rows=2, columns=2, font_size=10)
        self.package = package

    @staticmethod
    def flight(index: QModelIndex) -> Flight:
        return index.data(PackageModel.FlightRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        flight = self.flight(index)
        if (row, column) == (0, 0):
            estimator = TotEstimator(self.package)
            delay = estimator.mission_start_time(flight)
            return f"{flight} in {delay}"
        elif (row, column) == (0, 1):
            clients = self.num_clients(index)
            return f"Player Slots: {clients}" if clients else ""
        elif (row, column) == (1, 0):
            origin = flight.from_cp.name
            if flight.arrival != flight.departure:
                return f"From {origin} to {flight.arrival.name}"
            return f"From {origin}"
        elif (row, column) == (1, 1):
            missing_pilots = flight.missing_pilots
            return f"Missing pilots: {flight.missing_pilots}" if missing_pilots else ""
        return ""

    def num_clients(self, index: QModelIndex) -> int:
        flight = self.flight(index)
        return flight.client_count


class QFlightList(QListView):
    """List view for displaying the flights of a package."""

    def __init__(
        self, game_model: GameModel, package_model: Optional[PackageModel]
    ) -> None:
        super().__init__()
        self.game_model = game_model
        self.package_model = package_model
        self.set_package(package_model)
        if package_model is not None:
            self.setItemDelegate(FlightDelegate(package_model.package))
        self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.doubleClicked.connect(self.on_double_click)

    def set_package(self, model: Optional[PackageModel]) -> None:
        """Sets the package model to display."""
        if model is None:
            self.disconnect_model()
        else:
            self.package_model = model
            self.setItemDelegate(FlightDelegate(model.package))
            self.setModel(model)
            # noinspection PyUnresolvedReferences
            model.deleted.connect(self.disconnect_model)
            self.selectionModel().setCurrentIndex(
                model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
            )

    def disconnect_model(self) -> None:
        """Clears the listview of any model attachments.

        Displays an empty list until set_package is called with a valid model.
        """
        model = self.model()
        if model is not None and isinstance(model, PackageModel):
            model.deleted.disconnect(self.disconnect_model)
        self.setModel(NullListModel())

    @property
    def selected_item(self) -> Optional[Flight]:
        """Returns the selected flight, if any."""
        index = self.currentIndex()
        if not index.isValid():
            return None
        return self.package_model.flight_at_index(index)

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.edit_flight(index)

    def edit_flight(self, index: QModelIndex) -> None:
        from qt_ui.dialogs import Dialog

        Dialog.open_edit_flight_dialog(
            self.package_model,
            self.package_model.flight_at_index(index),
            parent=self.window(),
        )

    def delete_flight(self, index: QModelIndex) -> None:
        self.package_model.delete_flight_at_index(index)
        GameUpdateSignal.get_instance().redraw_flight_paths()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        index = self.indexAt(event.pos())

        menu = QMenu("Menu")

        edit_action = QAction("Edit")
        edit_action.triggered.connect(lambda: self.edit_flight(index))
        menu.addAction(edit_action)

        delete_action = QAction(f"Delete")
        delete_action.triggered.connect(lambda: self.delete_flight(index))
        menu.addAction(delete_action)

        menu.exec_(event.globalPos())


class QFlightPanel(QGroupBox):
    """The flight display portion of the ATO panel.

    Displays the flights assigned to the selected package, and includes edit and
    delete buttons for flight management.
    """

    def __init__(
        self, game_model: GameModel, package_model: Optional[PackageModel] = None
    ) -> None:
        super().__init__("Flights")
        self.game_model = game_model
        self.package_model = package_model

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.tip = QLabel(
            "To add flights to a package, edit the package by double clicking "
            "it or pressing the edit button."
        )
        self.vbox.addWidget(self.tip)

        self.flight_list = QFlightList(game_model, package_model)
        self.vbox.addWidget(self.flight_list)

        self.button_row = QHBoxLayout()
        self.vbox.addLayout(self.button_row)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.on_edit)
        self.button_row.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        # noinspection PyTypeChecker
        self.delete_button.setProperty("style", "btn-danger")
        self.delete_button.clicked.connect(self.on_delete)
        self.button_row.addWidget(self.delete_button)

        self.selection_changed.connect(self.on_selection_changed)
        self.on_selection_changed()

    def set_package(self, model: Optional[PackageModel]) -> None:
        """Sets the package model to display."""
        self.package_model = model
        self.flight_list.set_package(model)
        self.selection_changed.connect(self.on_selection_changed)
        self.on_selection_changed()

    @property
    def selection_changed(self):
        """Returns the signal emitted when the flight selection changes."""
        return self.flight_list.selectionModel().selectionChanged

    def on_selection_changed(self) -> None:
        """Updates the status of the edit and delete buttons."""
        index = self.flight_list.currentIndex()
        enabled = index.isValid()
        self.edit_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)
        self.change_map_flight_selection(index)

    @staticmethod
    def change_map_flight_selection(index: QModelIndex) -> None:
        if not index.isValid():
            GameUpdateSignal.get_instance().select_flight(None)
            return

        GameUpdateSignal.get_instance().select_flight(index.row())

    def on_edit(self) -> None:
        """Opens the flight edit dialog."""
        index = self.flight_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot edit flight when no flight is selected.")
            return
        self.flight_list.edit_flight(index)

    def on_delete(self) -> None:
        """Removes the selected flight from the package."""
        index = self.flight_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot delete flight when no flight is selected.")
            return
        self.flight_list.delete_flight(index)


class PackageDelegate(TwoColumnRowDelegate):
    def __init__(self) -> None:
        super().__init__(rows=2, columns=2)

    @staticmethod
    def package(index: QModelIndex) -> Package:
        return index.data(AtoModel.PackageRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        package = self.package(index)
        if (row, column) == (0, 0):
            return f"{package.package_description} {package.target.name}"
        elif (row, column) == (0, 1):
            clients = self.num_clients(index)
            return f"Player Slots: {clients}" if clients else ""
        elif (row, column) == (1, 0):
            return f"TOT T+{package.time_over_target}"
        elif (row, column) == (1, 1):
            unassigned_pilots = self.missing_pilots(index)
            return f"Missing pilots: {unassigned_pilots}" if unassigned_pilots else ""
        return ""

    def num_clients(self, index: QModelIndex) -> int:
        package = self.package(index)
        return sum(f.client_count for f in package.flights)

    def missing_pilots(self, index: QModelIndex) -> int:
        package = self.package(index)
        return sum(f.missing_pilots for f in package.flights)


class QPackageList(QListView):
    """List view for displaying the packages of an ATO."""

    def __init__(self, model: AtoModel) -> None:
        super().__init__()
        self.ato_model = model
        self.setModel(model)
        self.setItemDelegate(PackageDelegate())
        self.setIconSize(QSize(0, 0))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.model().rowsInserted.connect(self.on_new_packages)
        self.doubleClicked.connect(self.on_double_click)

    @property
    def selected_item(self) -> Optional[Package]:
        """Returns the selected package, if any."""
        index = self.currentIndex()
        if not index.isValid():
            return None
        return self.ato_model.package_at_index(index)

    def edit_package(self, index: QModelIndex) -> None:
        from qt_ui.dialogs import Dialog

        Dialog.open_edit_package_dialog(self.ato_model.get_package_model(index))

    def delete_package(self, index: QModelIndex) -> None:
        self.ato_model.delete_package_at_index(index)
        GameUpdateSignal.get_instance().redraw_flight_paths()

    def on_new_packages(self, _parent: QModelIndex, first: int, _last: int) -> None:
        # Select the newly created pacakges. This should only ever happen due to
        # the player saving a new package, so selecting it helps them view/edit
        # it faster.
        self.selectionModel().setCurrentIndex(
            self.model().index(first, 0), QItemSelectionModel.Select
        )

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.edit_package(index)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        index = self.indexAt(event.pos())

        menu = QMenu("Menu")

        edit_action = QAction("Edit")
        edit_action.triggered.connect(lambda: self.edit_package(index))
        menu.addAction(edit_action)

        delete_action = QAction(f"Delete")
        delete_action.triggered.connect(lambda: self.delete_package(index))
        menu.addAction(delete_action)

        menu.exec_(event.globalPos())


class QPackagePanel(QGroupBox):
    """The package display portion of the ATO panel.

    Displays the package assigned to the player's ATO, and includes edit and
    delete buttons for package management.
    """

    def __init__(self, model: AtoModel) -> None:
        super().__init__("Packages")
        self.ato_model = model
        self.ato_model.layoutChanged.connect(self.on_current_changed)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.tip = QLabel(
            "To create a new package, right click the mission target on the "
            "map. To target airbase objectives, use\n"
            "the attack button in the airbase view."
        )
        self.vbox.addWidget(self.tip)

        # Planning Row
        # Shows the current planned Flights / Available ones
        # Lets user fill with ai generated packages
        self.planning_row = QHBoxLayout()
        self.vbox.addLayout(self.planning_row)

        self.planning_status = QLabel(self.planning_status_text())
        self.planning_row.addWidget(self.planning_status)

        self.fill_button = QPushButton("Rerun the AI Planner")
        self.fill_button.clicked.connect(self.on_fill)
        self.planning_row.addWidget(self.fill_button)
        self.assigned_aircraft_count = 0
        self.available_aircraft_count = 0

        # Package List
        self.package_list = QPackageList(self.ato_model)
        self.vbox.addWidget(self.package_list)

        self.button_row = QHBoxLayout()
        self.vbox.addLayout(self.button_row)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.on_edit)
        self.button_row.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        # noinspection PyTypeChecker
        self.delete_button.setProperty("style", "btn-danger")
        self.delete_button.clicked.connect(self.on_delete)
        self.button_row.addWidget(self.delete_button)

        self.current_changed.connect(self.on_current_changed)
        self.on_current_changed()

    @property
    def current_changed(self):
        """Returns the signal emitted when the flight selection changes."""
        return self.package_list.selectionModel().currentChanged

    def on_current_changed(self) -> None:
        """Updates the status of the edit and delete buttons."""
        index = self.package_list.currentIndex()
        modify_enabled = index.isValid()
        self.edit_button.setEnabled(modify_enabled)
        self.delete_button.setEnabled(modify_enabled)
        self.change_map_package_selection(index)
        self.update_aircraft_count()

        fill_enabled = self.ato_model.game is not None and (
            self.assigned_aircraft_count
            < self.ato_model.game.settings.perf_limit_aircraft_amount
        )
        self.fill_button.setEnabled(fill_enabled)
        self.planning_status.setText(self.planning_status_text())

    def change_map_package_selection(self, index: QModelIndex) -> None:
        if not index.isValid():
            GameUpdateSignal.get_instance().select_package(None)
            return

        package = self.ato_model.get_package_model(index)
        if package.rowCount() == 0:
            GameUpdateSignal.get_instance().select_package(None)
        else:
            GameUpdateSignal.get_instance().select_package(index.row())

    def on_edit(self) -> None:
        """Opens the package edit dialog."""
        index = self.package_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot edit package when no package is selected.")
            return
        self.package_list.edit_package(index)

    def on_delete(self) -> None:
        """Removes the package from the ATO."""
        index = self.package_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot delete package when no package is selected.")
            return
        self.package_list.delete_package(index)
        self.on_current_changed()

    def on_fill(self) -> None:
        """Fills the ATO with AI generated packages."""
        self.ato_model.game.blue.plan_missions()
        GameUpdateSignal.get_instance().updateGame(self.ato_model.game)
        self.on_current_changed()
        return

    def update_aircraft_count(self):
        if self.ato_model.game:
            aircraft_count = 0
            for package in self.ato_model.packages:
                for flight in package.flights:
                    aircraft_count += flight.count
            self.assigned_aircraft_count = aircraft_count

            available = 0
            for (
                control_point,
                inventory,
            ) in self.ato_model.game.aircraft_inventory.inventories.items():
                if control_point.captured:
                    for aircraft, count in inventory.all_aircraft:
                        if control_point.can_operate(aircraft):
                            available += count
            self.available_aircraft_count = available

    def planning_status_text(self) -> str:
        status_text = ""
        if self.ato_model.game:
            status_text = f"Aircraft assigned: {self.assigned_aircraft_count}/{self.assigned_aircraft_count + self.available_aircraft_count}"
            if self.ato_model.game.settings.perf_limit_aircraft:
                status_text += f" (Limit: {self.ato_model.game.settings.perf_limit_aircraft_amount})"
        return status_text


class QAirTaskingOrderPanel(QSplitter):
    """A split panel for displaying the packages and flights of an ATO.

    Used as the left-bar of the main UI. The top half of the panel displays the
    packages of the player's ATO, and the bottom half displays the flights of
    the selected package.
    """

    def __init__(self, game_model: GameModel) -> None:
        super().__init__(Qt.Vertical)
        self.ato_model = game_model.ato_model

        self.package_panel = QPackagePanel(self.ato_model)
        self.package_panel.current_changed.connect(self.on_package_change)
        self.addWidget(self.package_panel)

        self.flight_panel = QFlightPanel(game_model)
        self.addWidget(self.flight_panel)

    def on_package_change(self) -> None:
        """Sets the newly selected flight for display in the bottom panel."""
        index = self.package_panel.package_list.currentIndex()
        if index.isValid():
            self.flight_panel.set_package(self.ato_model.get_package_model(index))
        else:
            self.flight_panel.set_package(None)
