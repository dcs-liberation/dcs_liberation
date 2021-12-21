from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal

from game.theater import ConflictTheater
from game.threatzones import ThreatZones
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class ThreatZonesJs(QObject):
    fullChanged = Signal()
    aircraftChanged = Signal()
    airDefensesChanged = Signal()
    radarSamsChanged = Signal()

    def __init__(
        self,
        full: list[LeafletPoly],
        aircraft: list[LeafletPoly],
        air_defenses: list[LeafletPoly],
        radar_sams: list[LeafletPoly],
    ) -> None:
        super().__init__()
        self._full = full
        self._aircraft = aircraft
        self._air_defenses = air_defenses
        self._radar_sams = radar_sams

    @Property(list, notify=fullChanged)
    def full(self) -> list[LeafletPoly]:
        return self._full

    @Property(list, notify=aircraftChanged)
    def aircraft(self) -> list[LeafletPoly]:
        return self._aircraft

    @Property(list, notify=airDefensesChanged)
    def airDefenses(self) -> list[LeafletPoly]:
        return self._air_defenses

    @Property(list, notify=radarSamsChanged)
    def radarSams(self) -> list[LeafletPoly]:
        return self._radar_sams

    @classmethod
    def from_zones(cls, zones: ThreatZones, theater: ConflictTheater) -> ThreatZonesJs:
        return ThreatZonesJs(
            ShapelyUtil.polys_to_leaflet(zones.all, theater),
            ShapelyUtil.polys_to_leaflet(zones.airbases, theater),
            ShapelyUtil.polys_to_leaflet(zones.air_defenses, theater),
            ShapelyUtil.polys_to_leaflet(zones.radar_sam_threats, theater),
        )

    @classmethod
    def empty(cls) -> ThreatZonesJs:
        return ThreatZonesJs([], [], [], [])
