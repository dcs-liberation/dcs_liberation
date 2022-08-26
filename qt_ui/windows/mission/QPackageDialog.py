"""Dialogs for creating and editing ATO packages."""
import logging
from datetime import timedelta
from typing import Optional

from PySide2.QtCore import QItemSelection, QTime, Qt, Signal
from PySide2.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
)

from game.ato.flight import Flight
from game.ato.flightplans.planningerror import PlanningError
from game.ato.package import Package
from game.game import Game
from game.server import EventStream
from game.sim import GameUpdateEvents
from game.theater.missiontarget import MissionTarget
from qt_ui.models import AtoModel, GameModel, PackageModel
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.ato import QFlightList
from qt_ui.windows.mission.flight.QFlightCreator import QFlightCreator


class QPackageDialog(QDialog):
    """Base package management dialog.

    The dialogs for creating a new package and editing an existing dialog are
    very similar, and this implements the shared behavior.
    """

    #: Emitted when a change is made to the package.
    package_changed = Signal()

    def __init__(self, game_model: GameModel, model: PackageModel, parent=None) -> None:
        super().__init__(parent)
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
        self.package_changed.connect(
            lambda: self.package_type_text.setText(self.package_model.description)
        )
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
        self.tot_spinner.setToolTip("Package TOT relative to mission TOT")
        self.tot_spinner.setEnabled(not self.package_model.package.auto_asap)
        self.tot_column.addWidget(self.tot_spinner)

        self.auto_asap = QCheckBox("ASAP")
        self.auto_asap.setToolTip(
            "Sets the package TOT to the earliest time that all flights can "
            "arrive at the target."
        )
        self.auto_asap.setChecked(self.package_model.package.auto_asap)
        self.auto_asap.toggled.connect(self.set_asap)
        self.tot_column.addWidget(self.auto_asap)

        self.tot_help_label = QLabel(
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Mission-planning"><span style="color:#FFFFFF;">Help</span></a>'
        )
        self.tot_help_label.setAlignment(Qt.AlignCenter)
        self.tot_help_label.setOpenExternalLinks(True)
        self.tot_column.addWidget(self.tot_help_label)

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

        self.package_model.tot_changed.connect(self.update_tot)

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

    def on_close(self, _result) -> None:
        EventStream.put_nowait(
            GameUpdateEvents().update_flights_in_package(self.package_model.package)
        )

    def on_save(self) -> None:
        self.save_tot()

    def save_tot(self) -> None:
        time = self.tot_spinner.time()
        seconds = time.hour() * 3600 + time.minute() * 60 + time.second()
        self.package_model.set_tot(timedelta(seconds=seconds))

    def set_asap(self, checked: bool) -> None:
        self.package_model.set_asap(checked)
        self.tot_spinner.setEnabled(not self.package_model.package.auto_asap)
        self.update_tot()

    def update_tot(self) -> None:
        self.tot_spinner.setTime(self.tot_qtime())

    def on_selection_changed(
        self, selected: QItemSelection, _deselected: QItemSelection
    ) -> None:
        """Updates the state of the delete button."""
        self.delete_flight_button.setEnabled(not selected.empty())

    def on_add_flight(self) -> None:
        """Opens the new flight dialog."""
        self.add_flight_dialog = QFlightCreator(
            self.game, self.package_model.package, parent=self.window()
        )
        self.add_flight_dialog.created.connect(self.add_flight)
        self.add_flight_dialog.show()

    def add_flight(self, flight: Flight) -> None:
        """Adds the new flight to the package."""
        self.package_model.add_flight(flight)
        try:
            flight.recreate_flight_plan()
            self.package_model.update_tot()
            EventStream.put_nowait(GameUpdateEvents().new_flight(flight))
        except PlanningError as ex:
            self.package_model.delete_flight(flight)
            logging.exception("Could not create flight")
            QMessageBox.critical(
                self, "Could not create flight", str(ex), QMessageBox.Ok
            )
        # noinspection PyUnresolvedReferences
        self.package_changed.emit()

    def on_delete_flight(self) -> None:
        """Removes the selected flight from the package."""
        flight = self.package_view.selected_item
        if flight is None:
            logging.error(f"Cannot delete flight when no flight is selected.")
            return
        self.package_model.cancel_or_abort_flight(flight)
        # noinspection PyUnresolvedReferences
        self.package_changed.emit()


class QNewPackageDialog(QPackageDialog):
    """Dialog window for creating a new package.

    New packages do not affect the ATO model until they are saved.
    """

    def __init__(
        self, game_model: GameModel, model: AtoModel, target: MissionTarget, parent=None
    ) -> None:
        super().__init__(
            game_model,
            PackageModel(
                Package(target, game_model.game.db.flights, auto_asap=True), game_model
            ),
            parent=parent,
        )
        self.ato_model = model

        # In the *new* package dialog, a package has been created and may have aircraft
        # assigned to it, but it is not a part of the ATO until the user saves it.
        #
        # Other actions (modifying settings, closing some other dialogs like the base
        # menu) can cause a Game update which will forcibly close this window without
        # either accepting or rejecting it, so we neither save the package nor release
        # any allocated units.
        #
        # While it would be preferable to be able to update this dialog as needed in the
        # event of game updates, the quick fix is to just not allow interaction with
        # other UI elements until the new package has either been finalized or canceled.
        self.setModal(True)

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
            self.package_model.cancel_or_abort_flight(flight)


class QEditPackageDialog(QPackageDialog):
    """Dialog window for editing an existing package.

    Changes to existing packages occur immediately.
    """

    def __init__(
        self, game_model: GameModel, model: AtoModel, package: PackageModel
    ) -> None:
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
        self.ato_model.cancel_or_abort_package(self.package_model.package)
        self.close()
