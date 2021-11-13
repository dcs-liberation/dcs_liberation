from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from dcs import Point
from shapely.geometry import Point as ShapelyPoint
from shapely.ops import unary_union

from game.ato.flightstate import InFlight

if TYPE_CHECKING:
    from game.ato import Flight
    from game.ato.airtaaskingorder import AirTaskingOrder
    from game.threatzones import ThreatPoly


class AircraftEngagementZones:
    def __init__(self, threat_zones: ThreatPoly) -> None:
        self.threat_zones = threat_zones

    def covers(self, position: Point) -> bool:
        return self.threat_zones.intersects(ShapelyPoint(position.x, position.y))

    @classmethod
    def from_ato(cls, ato: AirTaskingOrder) -> AircraftEngagementZones:
        commit_regions = []
        for package in ato.packages:
            for flight in package.flights:
                if (region := cls.commit_region(flight)) is not None:
                    commit_regions.append(region)
        return AircraftEngagementZones(unary_union(commit_regions))

    @classmethod
    def commit_region(cls, flight: Flight) -> Optional[ThreatPoly]:
        if isinstance(flight.state, InFlight):
            return flight.state.a2a_commit_region()
        return None
