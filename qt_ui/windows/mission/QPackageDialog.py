"""Dialogs for creating and editing ATO packages."""
import logging
from typing import Optional

from PySide2.QtCore import QItemSelection, QTime, Signal
from PySide2.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
)

from game.game import Game
from gen.ato import Package
from gen.flights.flight import Flight
from gen.flights.flightplan import FlightPlanBuilder
from qt_ui.models import AtoModel, PackageModel
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.ato import QFlightList
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.mission.flight.QFlightCreator import QFlightCreator
from theater.missiontarget import MissionTarget


class QPackageDialog(QDialog):
    """Base package management dialog.

    The dialogs for creating a new package and editing an existing dialog are
    very similar, and this implements the shared behavior.
    """

    #: Emitted when a change is made to the package.
    package_changed = Signal()

    #: Emitted when a flight is added to the package.
    flight_added = Signal(Flight)

    #: Emitted when a flight is removed from the package.
    flight_removed = Signal(Flight)

    def __init__(self, game: Game, model: PackageModel) -> None:
        super().__init__()
        self.game = game
        self.package_model = model
        self.add_flight_dialog: Optional[QFlightCreator] = None

        self.setMinimumSize(1000, 440)
        self.setWindowTitle(
            f"Mission Package: {self.package_model.mission_target.name}"
        )
        self.setWindowIcon(EVENT_ICONS["strike"])

        self.layout = QVBoxLayout()

        self.summary_row = QHBoxLayout()
        self.layout.addLayout(self.summary_row)

        self.package_type_column = QHBoxLayout()
        self.summary_row.addLayout(self.package_type_column)

        self.package_type_label = QLabel("Package Type:")
        self.package_type_text = QLabel(self.package_model.description)
        # noinspection PyUnresolvedReferences
        self.package_changed.connect(lambda: self.package_type_text.setText(
            self.package_model.description
        ))
        self.package_type_column.addWidget(self.package_type_label)
        self.package_type_column.addWidget(self.package_type_text)

        self.summary_row.addStretch(1)

        self.tot_column = QHBoxLayout()
        self.summary_row.addLayout(self.tot_column)

        self.tot_label = QLabel("Time Over Target:")
        self.tot_column.addWidget(self.tot_label)

        if self.package_model.package.time_over_target is None:
            time = None
        else:
            delay = self.package_model.package.time_over_target
            hours = delay // 3600
            minutes = delay // 60 % 60
            seconds = delay % 60
            time = QTime(hours, minutes, seconds)

        self.tot_spinner = QTimeEdit(time)
        self.tot_spinner.setMinimumTime(QTime(0, 0))
        self.tot_spinner.setDisplayFormat("T+hh:mm:ss")
        self.tot_column.addWidget(self.tot_spinner)

        self.package_view = QFlightList(self.package_model)
        self.package_view.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        self.layout.addWidget(self.package_view)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.add_flight_button = QPushButton("Add Flight")
        self.add_flight_button.clicked.connect(self.on_add_flight)
        self.button_layout.addWidget(self.add_flight_button)

        self.delete_flight_button = QPushButton("Delete Selected")
        self.delete_flight_button.setProperty("style", "btn-danger")
        self.delete_flight_button.clicked.connect(self.on_delete_flight)
        self.delete_flight_button.setEnabled(False)
        self.button_layout.addWidget(self.delete_flight_button)

        self.button_layout.addStretch()

        self.setLayout(self.layout)

        self.finished.connect(self.on_close)

    def on_close(self, _result) -> None:
        time = self.tot_spinner.time()
        seconds = time.hour() * 3600 + time.minute() * 60 + time.second()
        self.package_model.update_tot(seconds)
        GameUpdateSignal.get_instance().redraw_flight_paths()

    def on_selection_changed(self, selected: QItemSelection,
                             _deselected: QItemSelection) -> None:
        """Updates the state of the delete button."""
        self.delete_flight_button.setEnabled(not selected.empty())

    def on_add_flight(self) -> None:
        """Opens the new flight dialog."""
        self.add_flight_dialog = QFlightCreator(self.game,
                                                self.package_model.package)
        self.add_flight_dialog.created.connect(self.add_flight)
        self.add_flight_dialog.show()

    def add_flight(self, flight: Flight) -> None:
        """Adds the new flight to the package."""
        self.package_model.add_flight(flight)
        planner = FlightPlanBuilder(self.game, self.package_model.package,
                                    is_player=True)
        planner.populate_flight_plan(flight)
        # noinspection PyUnresolvedReferences
        self.package_changed.emit()
        # noinspection PyUnresolvedReferences
        self.flight_added.emit(flight)

    def on_delete_flight(self) -> None:
        """Removes the selected flight from the package."""
        flight = self.package_view.selected_item
        if flight is None:
            logging.error(f"Cannot delete flight when no flight is selected.")
            return
        self.package_model.delete_flight(flight)
        # noinspection PyUnresolvedReferences
        self.package_changed.emit()
        # noinspection PyUnresolvedReferences
        self.flight_removed.emit(flight)


class QNewPackageDialog(QPackageDialog):
    """Dialog window for creating a new package.

    New packages do not affect the ATO model until they are saved.
    """

    def __init__(self, game: Game, model: AtoModel,
                 target: MissionTarget) -> None:
        super().__init__(game, PackageModel(Package(target)))
        self.ato_model = model

        self.save_button = QPushButton("Save")
        self.save_button.setProperty("style", "start-button")
        self.save_button.clicked.connect(self.on_save)
        self.button_layout.addWidget(self.save_button)

        self.delete_flight_button.clicked.connect(self.on_delete_flight)

    def on_save(self) -> None:
        """Saves the created package.

        Empty packages may be created. They can be modified later, and will have
        no effect if empty when the mission is generated.
        """
        self.ato_model.add_package(self.package_model.package)
        for flight in self.package_model.package.flights:
            self.game.aircraft_inventory.claim_for_flight(flight)
        self.close()


class QEditPackageDialog(QPackageDialog):
    """Dialog window for editing an existing package.

    Changes to existing packages occur immediately.
    """

    def __init__(self, game: Game, model: AtoModel,
                 package: PackageModel) -> None:
        super().__init__(game, package)
        self.ato_model = model

        self.delete_button = QPushButton("Delete package")
        self.delete_button.setProperty("style", "btn-danger")
        self.delete_button.clicked.connect(self.on_delete)
        self.button_layout.addWidget(self.delete_button)

        self.done_button = QPushButton("Done")
        self.done_button.setProperty("style", "start-button")
        self.done_button.clicked.connect(self.on_done)
        self.button_layout.addWidget(self.done_button)

        # noinspection PyUnresolvedReferences
        self.flight_added.connect(self.on_flight_added)
        # noinspection PyUnresolvedReferences
        self.flight_removed.connect(self.on_flight_removed)

    # TODO: Make the new package dialog do this too, return on cancel.
    # Not claiming the aircraft when they are added to the planner means that
    # inventory counts are not updated until after the new package is updated,
    # so you can add an infinite number of aircraft to a new package in the UI,
    # which will crash when the flight package is saved.
    def on_flight_added(self, flight: Flight) -> None:
        self.game.aircraft_inventory.claim_for_flight(flight)

    def on_flight_removed(self, flight: Flight) -> None:
        self.game.aircraft_inventory.return_from_flight(flight)

    def on_done(self) -> None:
        """Closes the window."""
        self.close()

    def on_delete(self) -> None:
        """Removes the viewed package from the ATO."""
        # The ATO model returns inventory for us when deleting a package.
        self.ato_model.delete_package(self.package_model.package)
        self.close()
