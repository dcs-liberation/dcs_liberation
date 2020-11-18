"""Qt data models for game objects."""
import datetime
from typing import Any, Callable, Dict, Iterator, Optional, TypeVar

from PySide2.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Qt,
    Signal,
)
from PySide2.QtGui import QIcon

from game import db
from game.game import Game
from gen.ato import AirTaskingOrder, Package
from gen.flights.flight import Flight
from gen.flights.traveltime import TotEstimator
from qt_ui.uiconstants import AIRCRAFT_ICONS
from game.theater.missiontarget import MissionTarget


class DeletableChildModelManager:
    """Manages lifetimes for child models.

    Qt's data models don't have a good way of modeling related data aside from
    lists, tables, or trees of similar objects. We could build one monolithic
    GameModel that tracks all of the data in the game and use the parent/child
    relationships of that model to index down into the ATO, packages, flights,
    etc, but doing so is error prone because it requires us to manually manage
    that relationship tree and keep our own mappings from row/column into
    specific members.

    However, creating child models outside of the tree means that removing an
    item from the parent will not signal the child's deletion to any views, so
    we must track this explicitly.

    Any model which has child data types should use this class to track the
    deletion of child models. All child model types must define a signal named
    `deleted`. This signal will be emitted when the child model is being
    deleted. Any views displaying such data should subscribe to those events and
    update their display accordingly.
    """

    #: The type of data owned by models created by this class.
    DataType = TypeVar("DataType")

    #: The type of model managed by this class.
    ModelType = TypeVar("ModelType")

    ModelDict = Dict[DataType, ModelType]

    def __init__(self, create_model: Callable[[DataType], ModelType]) -> None:
        self.create_model = create_model
        self.models: DeletableChildModelManager.ModelDict = {}

    def acquire(self, data: DataType) -> ModelType:
        """Returns a model for the given child data.

        If a model has already been created for the given data, it will be
        returned. The data type must be hashable.
        """
        if data in self.models:
            return self.models[data]
        model = self.create_model(data)
        self.models[data] = model
        return model

    def release(self, data: DataType) -> None:
        """Releases the model matching the given data, if one exists.

        If the given data has had a model created for it, that model will be
        deleted and its `deleted` signal will be emitted.
        """
        if data in self.models:
            model = self.models[data]
            del self.models[data]
            model.deleted.emit()

    def clear(self) -> None:
        """Deletes all managed models."""
        for data in list(self.models.keys()):
            self.release(data)


class NullListModel(QAbstractListModel):
    """Generic empty list model."""

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        return None


class PackageModel(QAbstractListModel):
    """The model for an ATO package."""

    FlightRole = Qt.UserRole

    #: Emitted when this package is being deleted from the ATO.
    deleted = Signal()

    def __init__(self, package: Package) -> None:
        super().__init__()
        self.package = package

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.package.flights)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        flight = self.flight_at_index(index)
        if role == Qt.DisplayRole:
            return self.text_for_flight(flight)
        if role == Qt.DecorationRole:
            return self.icon_for_flight(flight)
        elif role == PackageModel.FlightRole:
            return flight
        return None

    def text_for_flight(self, flight: Flight) -> str:
        """Returns the text that should be displayed for the flight."""
        task = flight.flight_type.name
        count = flight.count
        name = db.unit_type_name(flight.unit_type)
        estimator = TotEstimator(self.package)
        delay = datetime.timedelta(
            seconds=int(estimator.mission_start_time(flight).total_seconds()))
        origin = flight.from_cp.name
        return f"[{task}] {count} x {name} from {origin} in {delay}"

    @staticmethod
    def icon_for_flight(flight: Flight) -> Optional[QIcon]:
        """Returns the icon that should be displayed for the flight."""
        name = db.unit_type_name(flight.unit_type)
        if name in AIRCRAFT_ICONS:
            return QIcon(AIRCRAFT_ICONS[name])
        return None

    def add_flight(self, flight: Flight) -> None:
        """Adds the given flight to the package."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.package.add_flight(flight)
        self.endInsertRows()

    def delete_flight_at_index(self, index: QModelIndex) -> None:
        """Removes the flight at the given index from the package."""
        self.delete_flight(self.flight_at_index(index))

    def delete_flight(self, flight: Flight) -> None:
        """Removes the given flight from the package.

        If the flight is using claimed inventory, the caller is responsible for
        returning that inventory.
        """
        index = self.package.flights.index(flight)
        self.beginRemoveRows(QModelIndex(), index, index)
        self.package.remove_flight(flight)
        self.endRemoveRows()

    def flight_at_index(self, index: QModelIndex) -> Flight:
        """Returns the flight located at the given index."""
        return self.package.flights[index.row()]

    def update_tot(self, tot: datetime.timedelta) -> None:
        self.package.time_over_target = tot
        self.layoutChanged.emit()

    @property
    def mission_target(self) -> MissionTarget:
        """Returns the mission target of the package."""
        package = self.package
        target = package.target
        return target

    @property
    def description(self) -> str:
        """Returns the description of the package."""
        return self.package.package_description

    @property
    def flights(self) -> Iterator[Flight]:
        """Iterates over the flights in the package."""
        for flight in self.package.flights:
            yield flight


class AtoModel(QAbstractListModel):
    """The model for an AirTaskingOrder."""

    PackageRole = Qt.UserRole

    client_slots_changed = Signal()

    def __init__(self, game: Optional[Game], ato: AirTaskingOrder) -> None:
        super().__init__()
        self.game = game
        self.ato = ato
        self.package_models = DeletableChildModelManager(PackageModel)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.ato.packages)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        package = self.ato.packages[index.row()]
        if role == Qt.DisplayRole:
            return f"{package.package_description} {package.target.name}"
        elif role == AtoModel.PackageRole:
            return package
        return None

    def add_package(self, package: Package) -> None:
        """Adds a package to the ATO."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.ato.add_package(package)
        self.endInsertRows()
        # noinspection PyUnresolvedReferences
        self.client_slots_changed.emit()

    def delete_package_at_index(self, index: QModelIndex) -> None:
        """Removes the package at the given index from the ATO."""
        self.delete_package(self.package_at_index(index))

    def delete_package(self, package: Package) -> None:
        """Removes the given package from the ATO."""
        self.package_models.release(package)
        index = self.ato.packages.index(package)
        self.beginRemoveRows(QModelIndex(), index, index)
        self.ato.remove_package(package)
        for flight in package.flights:
            self.game.aircraft_inventory.return_from_flight(flight)
        self.endRemoveRows()
        # noinspection PyUnresolvedReferences
        self.client_slots_changed.emit()

    def package_at_index(self, index: QModelIndex) -> Package:
        """Returns the package at the given index."""
        return self.ato.packages[index.row()]

    def replace_from_game(self, game: Optional[Game], player: bool) -> None:
        """Updates the ATO object to match the updated game object.

        If the game is None (as is the case when no game has been loaded), an
        empty ATO will be used.
        """
        self.beginResetModel()
        self.game = game
        self.package_models.clear()
        if self.game is not None:
            if player:
                self.ato = game.blue_ato
            else:
                self.ato = game.red_ato
        else:
            self.ato = AirTaskingOrder()
        self.endResetModel()
        # noinspection PyUnresolvedReferences
        self.client_slots_changed.emit()

    def get_package_model(self, index: QModelIndex) -> PackageModel:
        """Returns a model for the package at the given index."""
        return self.package_models.acquire(self.package_at_index(index))

    @property
    def packages(self) -> Iterator[PackageModel]:
        """Iterates over all the packages in the ATO."""
        for package in self.ato.packages:
            yield self.package_models.acquire(package)


class GameModel:
    """A model for the Game object.

    This isn't a real Qt data model, but simplifies management of the game and
    its ATO objects.
    """
    def __init__(self, game: Optional[Game]) -> None:
        self.game: Optional[Game] = game
        if self.game is None:
            self.ato_model = AtoModel(self.game, AirTaskingOrder())
            self.red_ato_model = AtoModel(self.game, AirTaskingOrder())
        else:
            self.ato_model = AtoModel(self.game, self.game.blue_ato)
            self.red_ato_model = AtoModel(self.game, self.game.red_ato)

    def set(self, game: Optional[Game]) -> None:
        """Updates the managed Game object.

        The argument will be None when no game has been loaded. In this state,
        much of the UI is still visible and needs to handle that behavior. To
        simplify that case, the AtoModel will model an empty ATO when no game is
        loaded.
        """
        self.game = game
        self.ato_model.replace_from_game(self.game, player=True)
        self.red_ato_model.replace_from_game(self.game, player=False)
