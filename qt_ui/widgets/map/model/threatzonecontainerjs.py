from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal

from .threatzonesjs import ThreatZonesJs


class ThreatZoneContainerJs(QObject):
    blueChanged = Signal()
    redChanged = Signal()

    def __init__(self, blue: ThreatZonesJs, red: ThreatZonesJs) -> None:
        super().__init__()
        self._blue = blue
        self._red = red

    @Property(ThreatZonesJs, notify=blueChanged)
    def blue(self) -> ThreatZonesJs:
        return self._blue

    @Property(ThreatZonesJs, notify=redChanged)
    def red(self) -> ThreatZonesJs:
        return self._red
