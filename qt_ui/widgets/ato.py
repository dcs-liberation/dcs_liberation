"""Widgets for displaying air tasking orders."""
import logging
from typing import Optional

from PySide2.QtCore import QItemSelectionModel, QModelIndex, QSize, Qt
from PySide2.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QListView,
    QPushButton,
    QSplitter,
    QVBoxLayout,
)

from gen.ato import Package
from gen.flights.flight import Flight
from ..models import AtoModel, GameModel, NullListModel, PackageModel


class QFlightList(QListView):
    """List view for displaying the flights of a package."""

    def __init__(self, model: Optional[PackageModel]) -> None:
        super().__init__()
        self.package_model = model
        self.set_package(model)
        self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)

    def set_package(self, model: Optional[PackageModel]) -> None:
        """Sets the package model to display."""
        if model is None:
            self.disconnect_model()
        else:
            self.package_model = model
            self.setModel(model)
            # noinspection PyUnresolvedReferences
            model.deleted.connect(self.disconnect_model)
            self.selectionModel().setCurrentIndex(
                model.index(0, 0, QModelIndex()),
                QItemSelectionModel.Select
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


class QFlightPanel(QGroupBox):
    """The flight display portion of the ATO panel.

    Displays the flights assigned to the selected package, and includes edit and
    delete buttons for flight management.
    """

    def __init__(self, game_model: GameModel,
                 package_model: Optional[PackageModel] = None) -> None:
        super().__init__("Flights")
        self.game_model = game_model
        self.package_model = package_model

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.flight_list = QFlightList(package_model)
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

    def on_edit(self) -> None:
        """Opens the flight edit dialog."""
        index = self.flight_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot edit flight when no flight is selected.")
            return
        from qt_ui.dialogs import Dialog
        Dialog.open_edit_flight_dialog(
            self.package_model.flight_at_index(index)
        )

    def on_delete(self) -> None:
        """Removes the selected flight from the package."""
        index = self.flight_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot delete flight when no flight is selected.")
            return
        self.game_model.game.aircraft_inventory.return_from_flight(
            self.flight_list.selected_item)
        self.package_model.delete_flight_at_index(index)


class QPackageList(QListView):
    """List view for displaying the packages of an ATO."""

    def __init__(self, model: AtoModel) -> None:
        super().__init__()
        self.ato_model = model
        self.setModel(model)
        self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)

    @property
    def selected_item(self) -> Optional[Package]:
        """Returns the selected package, if any."""
        index = self.currentIndex()
        if not index.isValid():
            return None
        return self.ato_model.package_at_index(index)


class QPackagePanel(QGroupBox):
    """The package display portion of the ATO panel.

    Displays the package assigned to the player's ATO, and includes edit and
    delete buttons for package management.
    """

    def __init__(self, model: AtoModel) -> None:
        super().__init__("Packages")
        self.ato_model = model
        self.ato_model.layoutChanged.connect(self.on_selection_changed)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

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

        self.selection_changed.connect(self.on_selection_changed)
        self.on_selection_changed()

    @property
    def selection_changed(self):
        """Returns the signal emitted when the flight selection changes."""
        return self.package_list.selectionModel().selectionChanged

    def on_selection_changed(self) -> None:
        """Updates the status of the edit and delete buttons."""
        index = self.package_list.currentIndex()
        enabled = index.isValid()
        self.edit_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)

    def on_edit(self) -> None:
        """Opens the package edit dialog."""
        index = self.package_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot edit package when no package is selected.")
            return
        from qt_ui.dialogs import Dialog
        Dialog.open_edit_package_dialog(self.ato_model.get_package_model(index))

    def on_delete(self) -> None:
        """Removes the package from the ATO."""
        index = self.package_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot delete package when no package is selected.")
            return
        self.ato_model.delete_package_at_index(index)


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
        self.package_panel.selection_changed.connect(self.on_package_change)
        self.ato_model.rowsInserted.connect(self.on_package_change)
        self.addWidget(self.package_panel)

        self.flight_panel = QFlightPanel(game_model)
        self.addWidget(self.flight_panel)

    def on_package_change(self) -> None:
        """Sets the newly selected flight for display in the bottom panel."""
        index = self.package_panel.package_list.currentIndex()
        if index.isValid():
            self.flight_panel.set_package(
                self.ato_model.get_package_model(index)
            )
        else:
            self.flight_panel.set_package(None)
