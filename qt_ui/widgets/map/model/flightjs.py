from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal, Slot

from game.ato import Flight
from game.ato.flightstate import InFlight
from game.server.leaflet import LeafletLatLon
from game.theater import ConflictTheater
from qt_ui.models import AtoModel


class FlightJs(QObject):
    idChanged = Signal()
    positionChanged = Signal()
    blueChanged = Signal()
    selectedChanged = Signal()

    def __init__(
        self,
        flight: Flight,
        selected: bool,
        theater: ConflictTheater,
        ato_model: AtoModel,
    ) -> None:
        super().__init__()
        self.flight = flight
        self._selected = selected
        self.theater = theater
        self.ato_model = ato_model

    @Property(str, notify=idChanged)
    def id(self) -> str:
        return str(self.flight.id)

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        if isinstance(self.flight.state, InFlight):
            ll = self.theater.point_to_ll(self.flight.state.estimate_position())
            return [ll.lat, ll.lng]
        return []

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.flight.departure.captured

    @Property(bool, notify=selectedChanged)
    def selected(self) -> bool:
        return self._selected

    @Slot(result=bool)
    def flightIsInAto(self) -> bool:
        if self.flight.package not in self.flight.squadron.coalition.ato.packages:
            return False
        if self.flight not in self.flight.package.flights:
            return False
        return True

    def set_selected(self, value: bool) -> None:
        self._selected = value
        self.selectedChanged.emit()
