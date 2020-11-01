"""Dialogs for creating and editing ATO packages."""
import logging
from datetime import timedelta
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
from gen.flights.traveltime import TotEstimator
from qt_ui.models import AtoModel, GameModel, PackageModel
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

    def __init__(self, game_model: GameModel, model: PackageModel) -> None:
        super().__init__()
        self.game_model = game_model
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

        self.tot_spinner = QTimeEdit(self.tot_qtime())
        self.tot_spinner.setMinimumTime(QTime(0, 0))
        self.tot_spinner.setDisplayFormat("T+hh:mm:ss")
        self.tot_spinner.timeChanged.connect(self.save_tot)
        self.tot_column.addWidget(self.tot_spinner)

        self.reset_tot_button = QPushButton("ASAP")
        self.reset_tot_button.setToolTip(
            "Sets the package TOT to the earliest time that all flights can "
            "arrive at the target."
        )
        self.reset_tot_button.clicked.connect(self.reset_tot)
        self.tot_column.addWidget(self.reset_tot_button)

        self.package_view = QFlightList(self.game_model, self.package_model)
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
        self.delete_flight_button.setEnabled(model.rowCount() > 0)
        self.button_layout.addWidget(self.delete_flight_button)

        self.button_layout.addStretch()

        self.setLayout(self.layout)

        self.accepted.connect(self.on_save)
        self.finished.connect(self.on_close)
        self.rejected.connect(self.on_cancel)

    @property
    def game(self) -> Game:
        return self.game_model.game

    def tot_qtime(self) -> QTime:
        delay = int(self.package_model.package.time_over_target.total_seconds())
        hours = delay // 3600
        minutes = delay // 60 % 60
        seconds = delay % 60
        return QTime(hours, minutes, seconds)

    def on_cancel(self) -> None:
        pass

    @staticmethod
    def on_close(_result) -> None:
        GameUpdateSignal.get_instance().redraw_flight_paths()

    def on_save(self) -> None:
        self.save_tot()

    def save_tot(self) -> None:
        time = self.tot_spinner.time()
        seconds = time.hour() * 3600 + time.minute() * 60 + time.second()
        self.package_model.update_tot(timedelta(seconds=seconds))

    def reset_tot(self) -> None:
        if not list(self.package_model.flights):
            self.package_model.update_tot(timedelta())
        else:
            self.package_model.update_tot(
                TotEstimator(self.package_model.package).earliest_tot())

        # Block signals while setting the auto computed TOT. The actual TOT will
        # have resolution down to the microsecond, but the QTimeEdit is not
        # capable of displaying that, so when we set the rounded value it saves
        # that back to the package with less precision. Block signals so we only
        # update the UI and not the package's value.
        self.tot_spinner.blockSignals(True)
        try:
            self.tot_spinner.setTime(self.tot_qtime())
        finally:
            self.tot_spinner.blockSignals(False)

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
        self.game.aircraft_inventory.claim_for_flight(flight)
        self.package_model.add_flight(flight)
        planner = FlightPlanBuilder(self.game, self.package_model.package,
                                    is_player=True)
        planner.populate_flight_plan(flight)
        # noinspection PyUnresolvedReferences
        self.package_changed.emit()

    def on_delete_flight(self) -> None:
        """Removes the selected flight from the package."""
        flight = self.package_view.selected_item
        if flight is None:
            logging.error(f"Cannot delete flight when no flight is selected.")
            return
        self.game.aircraft_inventory.return_from_flight(flight)
        self.package_model.delete_flight(flight)
        # noinspection PyUnresolvedReferences
        self.package_changed.emit()


class QNewPackageDialog(QPackageDialog):
    """Dialog window for creating a new package.

    New packages do not affect the ATO model until they are saved.
    """

    def __init__(self, game_model: GameModel, model: AtoModel,
                 target: MissionTarget) -> None:
        super().__init__(game_model, PackageModel(Package(target)))
        self.ato_model = model

        self.save_button = QPushButton("Save")
        self.save_button.setProperty("style", "start-button")
        self.save_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.save_button)

    def on_save(self) -> None:
        """Saves the created package.

        Empty packages may be created. They can be modified later, and will have
        no effect if empty when the mission is generated.
        """
        super().on_save()
        self.ato_model.add_package(self.package_model.package)

    def on_cancel(self) -> None:
        super().on_cancel()
        for flight in self.package_model.package.flights:
            self.game.aircraft_inventory.return_from_flight(flight)


class QEditPackageDialog(QPackageDialog):
    """Dialog window for editing an existing package.

    Changes to existing packages occur immediately.
    """

    def __init__(self, game_model: GameModel, model: AtoModel,
                 package: PackageModel) -> None:
        super().__init__(game_model, package)
        self.ato_model = model

        self.delete_button = QPushButton("Delete package")
        self.delete_button.setProperty("style", "btn-danger")
        self.delete_button.clicked.connect(self.on_delete)
        self.button_layout.addWidget(self.delete_button)

        self.done_button = QPushButton("Done")
        self.done_button.setProperty("style", "start-button")
        self.done_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.done_button)

    def on_delete(self) -> None:
        """Removes the viewed package from the ATO."""
        # The ATO model returns inventory for us when deleting a package.
        self.ato_model.delete_package(self.package_model.package)
        self.close()
