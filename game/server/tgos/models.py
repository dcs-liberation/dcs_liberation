from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint
from game.theater import TheaterGroundObject


class TgoJs(BaseModel):
    id: UUID
    name: str
    control_point_name: str
    category: str
    blue: bool
    position: LeafletPoint
    units: list[str]  # TODO: Event stream
    threat_ranges: list[float]  # TODO: Event stream
    detection_ranges: list[float]  # TODO: Event stream
    dead: bool  # TODO: Event stream
    sidc: str  # TODO: Event stream

    @staticmethod
    def for_tgo(tgo: TheaterGroundObject) -> TgoJs:
        if not tgo.might_have_aa:
            threat_ranges = []
            detection_ranges = []
        else:
            threat_ranges = [tgo.threat_range(group).meters for group in tgo.groups]
            detection_ranges = [
                tgo.detection_range(group).meters for group in tgo.groups
            ]
        return TgoJs(
            id=tgo.id,
            name=tgo.name,
            control_point_name=tgo.control_point.name,
            category=tgo.category,
            blue=tgo.control_point.captured,
            position=tgo.position.latlng(),
            units=[unit.display_name for unit in tgo.units],
            threat_ranges=threat_ranges,
            detection_ranges=detection_ranges,
            dead=tgo.is_dead,
            sidc=str(tgo.sidc()),
        )
