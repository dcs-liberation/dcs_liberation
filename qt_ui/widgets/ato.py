"""Widgets for displaying air tasking orders."""
import datetime
import logging
from contextlib import contextmanager
from typing import ContextManager, Optional

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
)
from PySide2.QtGui import (
    QContextMenuEvent,
    QFont,
    QFontMetrics,
    QIcon,
    QPainter,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QGroupBox,
    QHBoxLayout,
    QListView,
    QMenu,
    QPushButton,
    QSplitter,
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QVBoxLayout,
)

from game import db
from gen.ato import Package
from gen.flights.flight import Flight
from gen.flights.traveltime import TotEstimator
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from ..models import AtoModel, GameModel, NullListModel, PackageModel


class FlightDelegate(QStyledItemDelegate):
    FONT_SIZE = 10
    HMARGIN = 4
    VMARGIN = 4

    def __init__(self, package: Package) -> None:
        super().__init__()
        self.package = package

    def get_font(self, option: QStyleOptionViewItem) -> QFont:
        font = QFont(option.font)
        font.setPointSize(self.FONT_SIZE)
        return font

    @staticmethod
    def flight(index: QModelIndex) -> Flight:
        return index.data(PackageModel.FlightRole)

    def first_row_text(self, index: QModelIndex) -> str:
        flight = self.flight(index)
        task = flight.flight_type.name
        count = flight.count
        name = db.unit_type_name(flight.unit_type)
        estimator = TotEstimator(self.package)
        delay = datetime.timedelta(
            seconds=int(estimator.mission_start_time(flight).total_seconds()))
        return f"[{task}] {count} x {name} in {delay}"

    def second_row_text(self, index: QModelIndex) -> str:
        flight = self.flight(index)
        origin = flight.from_cp.name
        return f"From {origin}"

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex) -> None:
        # Draw the list item with all the default selection styling, but with an
        # invalid index so text formatting is left to us.
        super().paint(painter, option, QModelIndex())

        rect = option.rect.adjusted(self.HMARGIN, self.VMARGIN, -self.HMARGIN,
                                    -self.VMARGIN)

        with painter_context(painter):
            painter.setFont(self.get_font(option))

            icon: Optional[QIcon] = index.data(Qt.DecorationRole)
            if icon is not None:
                icon.paint(painter, rect, Qt.AlignLeft | Qt.AlignVCenter,
                           self.icon_mode(option),
                           self.icon_state(option))

            rect = rect.adjusted(self.icon_size(option).width() + self.HMARGIN,
                                 0, 0, 0)
            painter.drawText(rect, Qt.AlignLeft, self.first_row_text(index))
            line2 = rect.adjusted(0, rect.height() / 2, 0, rect.height() / 2)
            painter.drawText(line2, Qt.AlignLeft, self.second_row_text(index))

            clients = self.num_clients(index)
            if clients:
                painter.drawText(rect, Qt.AlignRight,
                                 f"Player Slots: {clients}")

    def num_clients(self, index: QModelIndex) -> int:
        flight = self.flight(index)
        return flight.client_count

    @staticmethod
    def icon_mode(option: QStyleOptionViewItem) -> QIcon.Mode:
        if not (option.state & QStyle.State_Enabled):
            return QIcon.Disabled
        elif option.state & QStyle.State_Selected:
            return QIcon.Selected
        elif option.state & QStyle.State_Active:
            return QIcon.Active
        return QIcon.Normal

    @staticmethod
    def icon_state(option: QStyleOptionViewItem) -> QIcon.State:
        return QIcon.On if option.state & QStyle.State_Open else QIcon.Off

    @staticmethod
    def icon_size(option: QStyleOptionViewItem) -> QSize:
        icon_size: Optional[QSize] = option.decorationSize
        if icon_size is None:
            return QSize(0, 0)
        else:
            return icon_size

    def sizeHint(self, option: QStyleOptionViewItem,
                 index: QModelIndex) -> QSize:
        left = self.icon_size(option).width() + self.HMARGIN
        metrics = QFontMetrics(self.get_font(option))
        first = metrics.size(0, self.first_row_text(index))
        second = metrics.size(0, self.second_row_text(index))
        text_width = max(first.width(), second.width())
        return QSize(left + text_width + 2 * self.HMARGIN,
                     first.height() + second.height() + 2 * self.VMARGIN)


class QFlightList(QListView):
    """List view for displaying the flights of a package."""

    def __init__(self, game_model: GameModel,
                 package_model: Optional[PackageModel]) -> None:
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

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.edit_flight(index)

    def edit_flight(self, index: QModelIndex) -> None:
        from qt_ui.dialogs import Dialog
        Dialog.open_edit_flight_dialog(
            self.package_model, self.package_model.flight_at_index(index)
        )

    def delete_flight(self, index: QModelIndex) -> None:
        self.game_model.game.aircraft_inventory.return_from_flight(
            self.selected_item)
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

    def __init__(self, game_model: GameModel,
                 package_model: Optional[PackageModel] = None) -> None:
        super().__init__("Flights")
        self.game_model = game_model
        self.package_model = package_model

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

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


@contextmanager
def painter_context(painter: QPainter) -> ContextManager[None]:
    try:
        painter.save()
        yield
    finally:
        painter.restore()


class PackageDelegate(QStyledItemDelegate):
    FONT_SIZE = 12
    HMARGIN = 4
    VMARGIN = 4

    def get_font(self, option: QStyleOptionViewItem) -> QFont:
        font = QFont(option.font)
        font.setPointSize(self.FONT_SIZE)
        return font

    @staticmethod
    def package(index: QModelIndex) -> Package:
        return index.data(AtoModel.PackageRole)

    def left_text(self, index: QModelIndex) -> str:
        package = self.package(index)
        return f"{package.package_description} {package.target.name}"

    def right_text(self, index: QModelIndex) -> str:
        package = self.package(index)
        delay = datetime.timedelta(
            seconds=int(package.time_over_target.total_seconds()))
        return f"TOT T+{delay}"

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex) -> None:
        # Draw the list item with all the default selection styling, but with an
        # invalid index so text formatting is left to us.
        super().paint(painter, option, QModelIndex())

        rect = option.rect.adjusted(self.HMARGIN, self.VMARGIN, -self.HMARGIN,
                                    -self.VMARGIN)

        with painter_context(painter):
            painter.setFont(self.get_font(option))

            painter.drawText(rect, Qt.AlignLeft, self.left_text(index))
            line2 = rect.adjusted(0, rect.height() / 2, 0, rect.height() / 2)
            painter.drawText(line2, Qt.AlignLeft, self.right_text(index))

            clients = self.num_clients(index)
            if clients:
                painter.drawText(rect, Qt.AlignRight,
                                 f"Player Slots: {clients}")

    def num_clients(self, index: QModelIndex) -> int:
        package = self.package(index)
        return sum(f.client_count for f in package.flights)

    def sizeHint(self, option: QStyleOptionViewItem,
                 index: QModelIndex) -> QSize:
        metrics = QFontMetrics(self.get_font(option))
        left = metrics.size(0, self.left_text(index))
        right = metrics.size(0, self.right_text(index))
        return QSize(max(left.width(), right.width()) + 2 * self.HMARGIN,
                     left.height() + right.height() + 2 * self.VMARGIN)


class QPackageList(QListView):
    """List view for displaying the packages of an ATO."""

    def __init__(self, model: AtoModel) -> None:
        super().__init__()
        self.ato_model = model
        self.setModel(model)
        self.setItemDelegate(PackageDelegate())
        self.setIconSize(QSize(91, 24))
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

    def on_new_packages(self, _parent: QModelIndex, first: int,
                        _last: int) -> None:
        # Select the newly created pacakges. This should only ever happen due to
        # the player saving a new package, so selecting it helps them view/edit
        # it faster.
        self.selectionModel().setCurrentIndex(self.model().index(first, 0),
                                              QItemSelectionModel.Select)

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
        enabled = index.isValid()
        self.edit_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)
        self.change_map_package_selection(index)

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
            self.flight_panel.set_package(
                self.ato_model.get_package_model(index)
            )
        else:
            self.flight_panel.set_package(None)
