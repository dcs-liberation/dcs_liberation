from __future__ import annotations

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint
from game.theater import ControlPoint


class ControlPointJs(BaseModel):
    id: int
    name: str
    blue: bool
    position: LeafletPoint
    mobile: bool
    destination: LeafletPoint | None
    sidc: str

    @staticmethod
    def for_control_point(control_point: ControlPoint) -> ControlPointJs:
        destination = None
        if control_point.target_position is not None:
            destination = control_point.target_position.latlng()
        return ControlPointJs(
            id=control_point.id,
            name=control_point.name,
            blue=control_point.captured,
            position=control_point.position.latlng(),
            mobile=control_point.moveable and control_point.captured,
            destination=destination,
            sidc=str(control_point.sidc()),
        )
